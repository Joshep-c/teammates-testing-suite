import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 },  // Inicio suave
    { duration: '15s', target: 25 },  // Carga moderada
    { duration: '15s', target: 40 },  // Carga alta
    { duration: '15s', target: 60 },  // Carga extrema (estrés)
  ],
  thresholds: {
    http_req_duration: ['avg<4000', 'p(95)<8000'],  // Tolerancia mayor
    http_req_failed: ['rate<0.10'],                 // Hasta 10% de errores
    http_reqs: ['rate>1'],                          // Degradación aceptable
  },
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, '');
  const courseId = `CS-STRESS-${__VU}-${timestamp}`; // ID único

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - Estrés',
    courseInstitute: 'Universidad Nacional de San Agustin',
    timeZone: 'America/Lima',
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'EB3036A47A1204970E0A24ECB962CCB16D4874B6C08564A94AFB180BF14EBF88',
    'Cookie': 'JSESSIONID=node0gf9jwis94yq21l9x2avfg45ew0.node0; AUTH-TOKEN=',
  };

  //CREACIÓN – esta operación sí se mide
  const res = http.post(
    `${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`,
    payload,
    { headers }
  );

  const ok = check(res, {
    'Curso creado - status 200': (r) => r.status === 200,
    'Body is not empty': (r) => r.body && r.body.length > 0,
  });

  if (!ok) {
    console.error(`Error en creación: status=${res.status}, body=${res.body}`);
  } else {
    console.log(`Curso creado correctamente: ${courseId}`);
  }

  sleep(1); // deja respirar 1s antes de nueva iteración

  //ELIMINACIÓN – no medida
  try {
    const del = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
    if (del.status === 200) {
      console.log(`🗑 Curso eliminado: ${courseId}`);
    } else {
      console.warn(`Error al eliminar: ${courseId} | status: ${del.status}`);
    }
  } catch (e) {
    console.warn(`Fallo al eliminar curso: ${courseId}`);
  }
}

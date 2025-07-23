import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 5 },   // Subida inicial
    { duration: '10s', target: 10 }, // Concurrencia sostenida
    { duration: '10s', target: 15 }, // Pico de estrés
    { duration: '5s', target: 0 },   // Descenso gradual
  ],
  thresholds: {
    http_req_duration: ['avg<2000', 'p(95)<4000'],  // Tolerancia para concurrencia
    http_req_failed: ['rate<0.05'],                 // Hasta 5% permitido
    http_reqs: ['rate>2'],                          // Esperamos al menos 2 req/s
  },
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, '');
  const courseId = `CS-CONC-${__VU}-${timestamp}`;

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - Concurrencia',
    courseInstitute: 'Universidad Nacional de San Agustin',
    timeZone: 'America/Lima',
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'EB3036A47A1204970E0A24ECB962CCB16D4874B6C08564A94AFB180BF14EBF88',
    'Cookie': 'JSESSIONID=node0gf9jwis94yq21l9x2avfg45ew0.node0; AUTH-TOKEN=',
  };

  //CREACIÓN DEL CURSO (medido)
  const res = http.post(
    `${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`,
    payload,
    { headers }
  );

  const success = check(res, {
    'Curso creado - status 200': (r) => r.status === 200,
    'Body is not empty': (r) => r.body && r.body.length > 0,
  });

  if (!success) {
    console.error(`Error en creación: status=${res.status}, body=${res.body}`);
  } else {
    console.log(`Curso creado correctamente: ${courseId}`);
  }

  sleep(1); // Delay para mitigar carga continua

  //ELIMINACIÓN (no medida)
  try {
    const del = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
    if (del.status === 200) {
      console.log(`🗑 Curso eliminado: ${courseId}`);
    } else {
      console.warn(`Error al eliminar: ${courseId} | status: ${del.status}`);
    }
  } catch (err) {
    console.warn(`Fallo al eliminar curso: ${courseId}`);
  }
}

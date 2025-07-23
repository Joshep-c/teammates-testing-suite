import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2s', target: 1 },   // Inicio suave (baseline)
    { duration: '3s', target: 30 },  // Pico súbito
    { duration: '5s', target: 30 },  // Carga mantenida
    { duration: '3s', target: 1 },   // Descenso abrupto
  ],
  thresholds: {
    http_req_duration: ['avg<1500', 'p(95)<3000'],
    http_req_failed: ['rate<0.05'],
    http_reqs: ['rate>6'],
  },
  gracefulStop: '20s',
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, '');
  const courseId = `CS-SPIKE-${__VU}-${timestamp}`;

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - Spike',
    courseInstitute: 'Universidad Nacional de San Agustin',
    timeZone: 'America/Lima',
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'EB3036A47A1204970E0A24ECB962CCB16D4874B6C08564A94AFB180BF14EBF88',
    'Cookie': 'JSESSIONID=node0gf9jwis94yq21l9x2avfg45ew0.node0; AUTH-TOKEN=2CBD1277E7C50AE6403AEC2DE1E5A08724A6F0D5BDDA1EAA570FAD095E2FE57B146235971B063DBCD422B4C78EFD2997DBCB086CD3E47F3452FA594000577B252A79F24456FE8FB4851AA76029859F80110128648D81BFA125F157B3A1170BA81D8C55309982B8DE01CD89564F97A8631D9F1CFC3D7B70818A70723FAC7F94DE',
  };

  //CREACIÓN (medida)
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

  sleep(1); // Evitar sobrecarga artificial

  //ELIMINACIÓN (no medida)
  try {
    const deleteRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
    if (deleteRes.status === 200) {
      console.log(`🗑 Curso eliminado: ${courseId}`);
    } else {
      console.warn(`Error al eliminar: ${courseId} | status: ${deleteRes.status}`);
    }
  } catch (e) {
    console.warn(`Fallo al eliminar curso: ${courseId}`);
  }
}

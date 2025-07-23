import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,                // 10 usuarios concurrentes
  duration: '20s',       // durante 20 segundos
  thresholds: {
    http_req_duration: ['avg<1000', 'p(95)<2000'],
    http_req_failed: ['rate<0.01'],
    http_reqs: ['rate>3'],
  },
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const timestamp = Date.now();
  const courseId = `CS-${__VU}-${__ITER}-${timestamp}`;

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - Carga',
    courseInstitute: 'Universidad Nacional de San Agustin',
    timeZone: 'America/Lima',
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'FA8F9A4E6766557ABA60207E00F6805E7FB0246FDB8CB1871B2FDA63B594463A',
    'Cookie': 'JSESSIONID=node01jhtpvm9su3gx694wb9b67lrm0.node0; AUTH-TOKEN=',
  };

  //Crear curso (esto se mide)
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
    console.log(`Curso creado correctamente: status ${res.status}`);
  }

  sleep(1);

  //Eliminar curso (no medido)
  try {
    http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
  } catch (err) {
    console.warn(`No se pudo eliminar el curso ${courseId}:`, err.message);
  }
}

import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  vus: 1,
  duration: '10s',
  thresholds: {
    http_req_duration: ['avg<1500', 'p(95)<3000'],
    http_req_failed: ['rate<0.05'],
    http_reqs: ['rate>1'],
  },
};

const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
const headers = {
  'Content-Type': 'application/json',
  'x-csrf-token': '95F4B1F1C1A8A3044F92096FD115D70C54E280A407A4547EEABDF69B1BF6D046',
  'Cookie': 'JSESSIONID=node02bl204cp74yf6ohrkfw0w1mk0.node0; AUTH-TOKEN=', 
};

const payloadTemplate = {
  courseInstitute: 'Universidad Nacional de San Agustin',
  timeZone: 'America/Lima',
};

// Función para generar strings largos
function generateString(length) {
  return 'X'.repeat(length);
}

export default function () {
  //Grupo 1: courseId límite válido (64)
  group('courseId 64 chars (válido)', () => {
    const courseId = generateString(64);
    const courseName = 'Curso válido';
    const payload = JSON.stringify({ ...payloadTemplate, courseId, courseName });

    const res = http.post(`${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`, payload, { headers });

    check(res, {
      'Status 200 esperado': (r) => r.status === 200,
    });
    if (res.status === 200) {
  const delRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
  if (delRes.status === 200) {
    console.log(`🗑 Curso eliminado correctamente: ${courseId}`);
  } else {
    console.warn(`No se pudo eliminar: ${courseId} | status=${delRes.status}`);
  }
}

    sleep(1);
  });

  //Grupo 2: courseId 65 chars (inválido)
  group('courseId 65 chars (inválido)', () => {
    const courseId = generateString(65);
    const courseName = 'Curso válido';
    const payload = JSON.stringify({ ...payloadTemplate, courseId, courseName });

    const res = http.post(`${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`, payload, { headers });

    check(res, {
      'Status 400/422 esperado (NO 500)': (r) => r.status >= 400 && r.status < 500,
    });
    if (res.status === 200) {
  const delRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
  if (delRes.status === 200) {
    console.log(`🗑 Curso eliminado correctamente: ${courseId}`);
  } else {
    console.warn(`No se pudo eliminar: ${courseId} | status=${delRes.status}`);
  }
}

    sleep(1);
  });

  //Grupo 3: courseName 80 chars (válido)
  group('courseName 80 chars (válido)', () => {
    const courseId = `ID-${Date.now()}`;
    const courseName = generateString(80);
    const payload = JSON.stringify({ ...payloadTemplate, courseId, courseName });

    const res = http.post(`${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`, payload, { headers });

    check(res, {
      'Status 200 esperado': (r) => r.status === 200,
    });
    if (res.status === 200) {
  const delRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
  if (delRes.status === 200) {
    console.log(`🗑 Curso eliminado correctamente: ${courseId}`);
  } else {
    console.warn(`No se pudo eliminar: ${courseId} | status=${delRes.status}`);
  }
}

    sleep(1);
  });

  //Grupo 4: courseName 81 chars (inválido)
  group('courseName 81 chars (inválido)', () => {
    const courseId = `ID-${Date.now()}`;
    const courseName = generateString(81);
    const payload = JSON.stringify({ ...payloadTemplate, courseId, courseName });

    const res = http.post(`${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`, payload, { headers });

    check(res, {
      'Status 400/422 esperado (NO 500)': (r) => r.status >= 400 && r.status < 500,
    });
    if (res.status === 200) {
  const delRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
  if (delRes.status === 200) {
    console.log(`🗑 Curso eliminado correctamente: ${courseId}`);
  } else {
    console.warn(`No se pudo eliminar: ${courseId} | status=${delRes.status}`);
  }
}

    sleep(1);
  });
}

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 5, // Usuarios virtuales simulados
  duration: '30m', // Duración ajustada a 30 minutos
  thresholds: {
    http_req_duration: ['avg<1200', 'p(95)<2000'], // Tiempos sostenidos aceptables
    http_req_failed: ['rate<0.01'], // Error rate bajo
    http_reqs: ['rate>0.5'], // Throughput constante por VU
  },
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const timestamp = new Date().toISOString().replace(/[-:.TZ]/g, '');
  const courseId = `CS-SOAK-${__VU}-${timestamp}`;

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - Soak Test',
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

  sleep(10); // 💤 Espera para simular uso prolongado sin saturación inmediata

  //ELIMINACIÓN (no medida)
  try {
    const delRes = http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
    if (delRes.status === 200) {
      console.log(`🗑 Curso eliminado: ${courseId}`);
    } else {
      console.warn(`Error al eliminar: ${courseId} | status: ${delRes.status}`);
    }
  } catch (err) {
    console.warn(`Fallo al eliminar curso: ${courseId}`);
  }
}

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  duration: '10s',
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com';
  const courseId = `CS${Math.floor(Math.random() * 10000)}`;

  const payload = JSON.stringify({
    courseId: courseId,
    courseName: 'Ingeniería de Software - K6',
    courseInstitute: 'Universidad Nacional de San Agustin',
    timeZone: 'America/Lima',
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'CF9D74D1EDD123AC6360FD941E0FC49B054201E349C2FB710ADF294A113F219DC89A7046D807814E294A39DF1D149867',
    'Cookie': 'JSESSIONID=node01jowmj1f1jmy06np5zi3ot7pi15.node0; AUTH-TOKEN=2CBD1277E7C50AE6403AEC2DE1E5A08724A6F0D5BDDA1EAA570FAD095E2FE57B146235971B063DBCD422B4C78EFD2997DBCB086CD3E47F3452FA594000577B252A79F24456FE8FB4851AA76029859F80110128648D81BFA125F157B3A1170BA81D8C55309982B8DE01CD89564F97A8631D9F1CFC3D7B70818A70723FAC7F94DE',
  };

  //Solo medimos la creación (POST)
  const createRes = http.post(`${baseUrl}/webapi/course?instructorinstitution=Universidad%20Nacional%20de%20San%20Agustin`, payload, { headers });

  check(createRes, {
    'Curso creado - status 200': (r) => r.status === 200,
    'Body is not empty': (r) => r.body && r.body.length > 0,
  });

  console.log('CREATE status:', createRes.status);
  console.log('CREATE body:', createRes.body);

  sleep(1);

  //Elimina luego SIN medir (excluido de métricas principales)
  http.put(`${baseUrl}/webapi/bin/course?courseid=${courseId}`, null, { headers });
}

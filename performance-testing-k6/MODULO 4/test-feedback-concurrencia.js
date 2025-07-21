import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 20,
  iterations: 20
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com/webapi';
  const questionId = 'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgITsr5UKDA';
  const url = `${baseUrl}/responses?questionid=${questionId}&intent=STUDENT_SUBMISSION`;

  const payload = JSON.stringify({
    responses: [
      {
        recipient: 'desmond@example.com',
        responseDetails: {
          answer: '<p>Respuesta simultánea en VU concurrente</p>',
          questionType: 'TEXT'
        }
      }
    ]
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035',
    'Cookie': 'AUTH-TOKEN=A68F5ACA81F57026D45F075AA7C42BDB08FA7B0ED3245CA1EA4402D5BEE58EEF0C9BD2DF77E5AC16504E5436419F55C52D2B5C728D6CE3CE92B524FCE19E6AE9221201B673A13B97B7413F8D9F601B6D9193B77B365F8D08C2AB056DBF87B95F97E67DFBA722893120DB142BFBB1944FA208408E38047AA239C39D7CA6547CD0; CSRF-TOKEN=A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035; JSESSIONID=node0hep8osmxknpwfmowvf63p4v51.node0'
  };

  const res = http.put(url, payload, { headers });

  check(res, {
    'Status is 200': (r) => r.status === 200,
    'Body not empty': (r) => r.body && r.body.length > 0
  });

  console.log('VU response status:', res.status);
}
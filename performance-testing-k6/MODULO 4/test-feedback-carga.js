import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,
  duration: '15s',
};

export default function () {
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com/webapi';
  const questionIds = [
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgITsr5UKDA', // pregunta 1
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgOj3rYcKDA', // pregunta 2
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgLizyJYKDA', // pregunta 3
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgLjx8ZQKDA', // pregunta 4
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgOj3u5YKDA', // pregunta 5
    'ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgOj3u5YJDA'  // pregunta 6
  ];

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035',
    'Cookie': 'AUTH-TOKEN=A68F5ACA81F57026D45F075AA7C42BDB08FA7B0ED3245CA1EA4402D5BEE58EEF0C9BD2DF77E5AC16504E5436419F55C52D2B5C728D6CE3CE92B524FCE19E6AE9221201B673A13B97B7413F8D9F601B6D9193B77B365F8D08C2AB056DBF87B95F97E67DFBA722893120DB142BFBB1944FA208408E38047AA239C39D7CA6547CD0; JSESSIONID=node0hep8osmxknpwfmowvf63p4v51.node0; CSRF-TOKEN=A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035',
  };

  for (let i = 0; i < questionIds.length; i++) {
    const url = `${baseUrl}/responses?questionid=${questionIds[i]}&intent=STUDENT_SUBMISSION`;

    const payload = JSON.stringify({
      responses: [
        {
          recipient: 'desmond@example.com',
          responseDetails: {
            answer: `<p>Respuesta automatizada a pregunta ${i + 1}</p>`,
            questionType: 'TEXT'
          }
        }
      ]
    });

    const res = http.put(url, payload, { headers });

    check(res, {
      [`Pregunta ${i + 1}: status 200`]: (r) => r.status === 200,
      [`Pregunta ${i + 1}: body válido`]: (r) => r.body && r.body.length > 0,
    });

    console.log(`Pregunta ${i + 1} - Status: ${res.status}`);
    console.log(`Pregunta ${i + 1} - Body:`, res.body);
  }
}
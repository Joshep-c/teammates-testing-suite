import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 },   // carga inicial
    { duration: '30s', target: 50 },   // carga moderada
    { duration: '45s', target: 100 },  // carga alta
    { duration: '60s', target: 200 },  // carga muy alta
    { duration: '90s', target: 300 },  // estrés extremo
  ],
};

export default function () {
  const courseId = '1234';
  const baseUrl = 'https://modern-vortex-463217-h9.uc.r.appspot.com/webapi';

  const now = new Date();
  const nextHour = new Date(now);
  nextHour.setHours(now.getHours() + 1, 0, 0, 0);

  const feedbackSessionName = `session_${Math.floor(Math.random() * 100000)}`;

  const payload = JSON.stringify({
    feedbackSessionName,
    timeZone: 'America/Lima',
    instructions: '<p>Responde las preguntas por favor.</p>',
    sessionVisibleFromTimestamp: nextHour.getTime(),
    submissionStartTimestamp: nextHour.getTime(),
    submissionEndTimestamp: nextHour.getTime() + 60 * 60 * 1000,
    submissionEndWithExtensionTimestamp: nextHour.getTime() + 60 * 60 * 1000,
    gracePeriod: 20,
    sessionVisibleSetting: 'AT_OPEN',
    responseVisibleSetting: 'LATER',
    isClosingSoonEmailEnabled: true,
    isPublishedEmailEnabled: true
  });

  const headers = {
    'Content-Type': 'application/json',
    'x-csrf-token': 'A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035',
    'Cookie': 'AUTH-TOKEN=A68F5ACA81F57026D45F075AA7C42BDB08FA7B0ED3245CA1EA4402D5BEE58EEF0C9BD2DF77E5AC16504E5436419F55C52D2B5C728D6CE3CE92B524FCE19E6AE9221201B673A13B97B7413F8D9F601B6D9193B77B365F8D08C2AB056DBF87B95F97E67DFBA722893120DB142BFBB1944FA208408E38047AA239C39D7CA6547CD0; JSESSIONID=node0hep8osmxknpwfmowvf63p4v51.node0; CSRF-TOKEN=A6EC4FED4A7FC6165E5FFCB7AD63044F7C4A42871E67DE2AEED6DCAC9D187035',
  };

  const createUrl = `${baseUrl}/session?courseid=${courseId}`;
  const res = http.post(createUrl, payload, { headers });

  check(res, {
    'Status is 200': (r) => r.status === 200,
    'Body is not empty': (r) => r.body && r.body.length > 0,
  });

  const deleteUrl = `${baseUrl}/bin/session?courseid=${courseId}&fsname=${encodeURIComponent(feedbackSessionName)}`;
  const delRes = http.put(deleteUrl, null, { headers });

  check(delRes, {
    'Delete status is 200': (r) => r.status === 200,
  });
}
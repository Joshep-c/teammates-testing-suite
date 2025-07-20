import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '30s', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 150 },
    { duration: '30s', target: 200 },
  ],
};

export default function () {
  const res = http.get('https://modern-vortex-463217-h9.uc.r.appspot.com/webapi/auth', {
    headers: {
      'accept': 'application/json, text/plain, */*',
      'ngsw-bypass': 'true',
      'x-web-version': '8.8.0',
    },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

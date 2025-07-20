import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '1m', target: 20 },
    { duration: '1m', target: 30 },
    { duration: '1m', target: 40 },
    { duration: '1m', target: 50 },
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

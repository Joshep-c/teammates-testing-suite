import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '5m',
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

  sleep(1);
}

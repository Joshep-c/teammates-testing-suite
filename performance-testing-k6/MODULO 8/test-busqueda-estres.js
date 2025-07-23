import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 20 },
    { duration: '1m', target: 40 },
    { duration: '1m', target: 60 },
    { duration: '1m', target: 80 },
    { duration: '1m', target: 100 },
  ],
};

export default function () {
  const url = 'https://modern-vortex-463217-h9.uc.r.appspot.com/webapi/search/students?searchkey=Alice&entitytype=instructor';

  const headers = {
    'Accept': 'application/json, text/plain, */*',
    'X-WEB-VERSION': '8.8.0',
    'ngsw-bypass': 'true',
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search',
    'Cookie': 'AUTH-TOKEN=9F6A13FBBDA0E9B377F705B88E852ECB8690890592A17BC1F5B02A61B243B26C5E5F4279126EA5CEED82ACBE857279E5CB5F035E339EB8AFADDDCBB9D10A0D889A4F160717E2858A7A5C66E2B3B0D6588B082752BBF4C852E90B2F898EB8D88BB0798DE4336BCE3C1E1AA5E31D09CD0F780A3CD75786C7274F51FEE78F6DA999; CSRF-TOKEN=E5797A8B2F31C4C8CD2B1479E8A32819B603073E19F6DBA99DA6CCAE39A39533; JSESSIONID=node0948tyv8homb7cgbeejkz8ix610.node0'
  };

  const res = http.get(url, { headers });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body contiene resultados': (r) => r.body && r.body.includes('Alice'),
  });
}

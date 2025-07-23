import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,                // Usuario virtual único
  duration: '30s',       // Prueba durante 30 segundos
};

export default function () {
  const url = 'https://modern-vortex-463217-h9.uc.r.appspot.com/webapi/search/students?searchkey=Alice&entitytype=instructor';

  const headers = {
    'Accept': 'application/json, text/plain, */*',
    'X-WEB-VERSION': '8.8.0',
    'ngsw-bypass': 'true',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Referer': 'https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/search',
    'Cookie': 'AUTH-TOKEN=9F6A13FBBDA0E9B377F705B88E852ECB8690890592A17BC1F5B02A61B243B26C5E5F4279126EA5CEED82ACBE857279E5CB5F035E339EB8AFADDDCBB9D10A0D889A4F160717E2858A7A5C66E2B3B0D6588B082752BBF4C852E90B2F898EB8D88BB0798DE4336BCE3C1E1AA5E31D09CD0F780A3CD75786C7274F51FEE78F6DA999; JSESSIONID=node013flde4hxbyn69lf1er1c0c7h33.node0; CSRF-TOKEN=DEF97D6D2511737D2A2C999BFA6A68F87C17FCF3D94CBE0AC12B0DEB70B14C6CC89A7046D807814E294A39DF1D149867'
  };

  const res = http.get(url, { headers });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body contiene resultados': (r) => r.body && r.body.includes('Alice'),
  });

  console.log(`Estado: ${res.status}`);
  console.log(`Respuesta: ${res.body.substring(0, 200)}...`); // Muestra los primeros 200 caracteres
}

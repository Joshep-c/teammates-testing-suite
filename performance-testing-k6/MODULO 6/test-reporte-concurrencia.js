import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 30,               // 🔁 Usuarios virtuales constantes
  duration: "2m",        // ⏱️ Tiempo total de la prueba
};

export default function () {
  const url =
    "https://modern-vortex-463217-h9.uc.r.appspot.com/webapi/result?courseid=alex2004huisa.gma-demo&fsname=First%20team%20feedback%20session%20(percentage-based)&intent=FULL_DETAIL&questionid=ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgNi4o-sLDA";

  const headers = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/sessions",
    "x-web-version": "8.8.0",
    "ngsw-bypass": "true",
    "cookie":
      "AUTH-TOKEN=9F6A13FBBDA0E9B377F705B88E852ECB8690890592A17BC1F5B02A61B243B26C5E5F4279126EA5CEED82ACBE857279E5CB5F035E339EB8AFADDDCBB9D10A0D889A4F160717E2858A7A5C66E2B3B0D6588B082752BBF4C852E90B2F898EB8D88BB0798DE4336BCE3C1E1AA5E31D09CD0F780A3CD75786C7274F51FEE78F6DA999; JSESSIONID=node0tkmzwcvb9v5j1qa9ur3wdn5tk0.node0; CSRF-TOKEN=B9F8B41CE30009ABA4700DB96890661A430C4B9E47EF3001B91475B922661BFB",
  };

  const res = http.get(url, { headers });

  check(res, {
    "status es 200": (r) => r.status === 200,
    "respuesta contiene datos": (r) => r.body && r.body.length > 100,
  });

  sleep(1); // Evita saturar demasiado la instancia
}

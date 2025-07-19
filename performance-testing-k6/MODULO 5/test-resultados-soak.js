
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10,
  duration: '5m',
};

export default function () {
  const url = `https://modern-vortex-463217-h9.uc.r.appspot.com/webapi/result?courseid=mhuamanivar.uns-demo&fsname=Feedback%202&intent=FULL_DETAIL&questionid=ahlzfm1vZGVybi12b3J0ZXgtNDYzMjE3LWg5ch0LEhBGZWVkYmFja1F1ZXN0aW9uGICAgLiK-J0KDA&frgroupbysection=Tutorial%20Group%201&sectionByGiverReceiver=both`;

  const headers = {
  'Accept': 'application/json, text/plain, */*',
  'ngsw-bypass': 'true',
  'X-WEB-VERSION': '8.8.0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
  'Referer': 'https://modern-vortex-463217-h9.uc.r.appspot.com/web/instructor/sessions/report?courseid=mhuamanivar.uns-demo&fsname=Feedback%202',
  'Cookie': 'AUTH-TOKEN=A9F0B5E54DCBC16247F44B050138BFB5F852FBD99054041FABFCED9E438A39C5146235971B063DBCD422B4C78EFD299795CE4D16D4A446F2C43776ADB410D7EC067D0B7048152AC26B8AF91E1BA6AB520DDC62E7AE1F0390F533ACBECED672861D8C55309982B8DE01CD89564F97A863C701FBAE62798275EA70D7AABD7F159F; JSESSIONID=node0cb7md280rgy01t69uos1lvhu87.node0; CSRF-TOKEN=46F023643BA3EDEB5A52A38777016E35C446B29F4FA465708A69BF380FE78EE1'
};

  const res = http.get(url, { headers });

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response body contiene datos': (r) => r.body && r.body.includes('giver') || r.body.includes('responses'),
    'response time < 2000ms': (r) => r.timings.duration < 2000,
  });
}

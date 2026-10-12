/* 문제 목록 CSV 내보내기 (시트 '화분 키우기 문제 목록'이 이 파일들을 자동으로 불러가요)
   실행: node tools/export_csv.js   (로컬 서버 http://localhost:8767 에서 index.html을 열어 최종 문제 목록을 읽어요) */
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', 'data');
(async()=>{
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8767/index.html');
  const data = await pg.evaluate(()=>({
    cats: CATS.map(c=>({k:c.k, n:c.n})),
    rows: BANK.filter(x=>x.id && !/^P/.test(x.id)).map(x=>({id:x.id, k:x.k, l:x.l, t:x.t||"", q:x.q, o:x.o, a:x.a, img:x.img||""}))
  }));
  await b.close();
  const esc = v => { const s = String(v==null?"":v).replace(/\n/g," / "); return /[",\n]/.test(s) ? '"'+s.replace(/"/g,'""')+'"' : s; };
  const SITE = "https://memejalal.memejalal2026.workers.dev/";
  const summary = [["종류","키","문제 수"]];
  for(const c of data.cats){
    const rows = data.rows.filter(r=>r.k===c.k);
    const lines = [["번호","난이도","문제","정답","오답1","오답2","오답3","그림","세부 분류"]];
    rows.forEach(r=>{ const ans=r.o[r.a], wrong=r.o.filter((_,i)=>i!==r.a);
      lines.push([r.id, r.l, r.q, ans, wrong[0]||"", wrong[1]||"", wrong[2]||"", r.img ? SITE + r.img : "", r.t]); });
    fs.writeFileSync(path.join(OUT, `q-${c.k}.csv`), "﻿" + lines.map(l=>l.map(esc).join(",")).join("\n") + "\n");
    summary.push([c.n, c.k, rows.length]);
  }
  fs.writeFileSync(path.join(OUT, "q-summary.csv"), "﻿" + summary.map(l=>l.map(esc).join(",")).join("\n") + "\n");
  console.log(summary.map(s=>s.join(":")).join("  "), " 합계", data.rows.length);
})();

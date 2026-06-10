/**
 * 每日自动记录荐股前三名
 * GitHub Actions 定时运行：9:30 记录推荐，15:00 更新收盘
 */
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(__dirname, 'records.json');
const POOL = ['000001','000002','000858','002049','002230','002241','002415','002456',
  '002475','002594','002736','002916','002920','300014','300059','300274','300308',
  '300346','300394','300474','300498','300502','300661','300750','300782','600000',
  '600009','600016','600030','600036','600104','600276','600418','600519','600585',
  '600690','600703','600809','600887','600900','601012','601166','601318','601398',
  '601688','601857','601939','603501','603986','688005','688012','688036','688111',
  '688126','688256','688396','688561','688981'];

function httpGet(url) {
  const mod = url.startsWith('https') ? https : http;
  return new Promise((resolve, reject) => {
    const req = mod.get(url, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(data));
    });
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('timeout')); });
    req.on('error', reject);
  });
}

async function fetchStocks() {
  const emUrl = 'http://push2.eastmoney.com/api/qt/clist/get?' +
    'fid=f184&po=1&pz=500&pn=1&np=1&fltt=2&invt=2' +
    '&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23' +
    '&fields=f2,f3,f12,f14,f62,f66,f69,f184,f20';

  const emData = JSON.parse(await httpGet(emUrl));
  const emMap = {};
  for (const item of (emData.data || {}).diff || []) {
    emMap[item.f12] = {
      price: item.f2, chgPct: item.f3, name: item.f14,
      winRate: item.f69 || 0, dragonTiger: item.f184 || 0,
      mainForce: item.f62 || 0, superBig: item.f66 || 0,
    };
  }

  const qtUrl = 'http://qt.gtimg.cn/q=' + POOL.map(c =>
    (c[0] === '6' || c[0] === '5' || c[0] === '9' ? 'sh' : 'sz') + c
  ).join(',');

  const qtText = await httpGet(qtUrl);
  const stocks = [];
  for (const line of qtText.split(';')) {
    if (!line.includes('="')) continue;
    const m = line.match(/="(.+)"/);
    if (!m) continue;
    const f = m[1].split('~');
    if (f.length < 70) continue;
    const em = emMap[f[2]] || {};
    stocks.push({
      code: f[2], name: em.name || f[1],
      price: +f[3] || 0, chgPct: +f[32] || 0,
      volRatio: +f[49] || 0, turnover: +f[38] || 0,
      pe: +f[39] || 0, mcap: +f[44] || 0,
      inside: +f[7] || 0, outside: +f[8] || 0,
      chg5: +f[62] || 0, yrLow: +f[68] || 0,
      winRate: em.winRate, dragonTiger: em.dragonTiger,
      mainForce: em.mainForce,
    });
  }
  return stocks;
}

function analyze(s) {
  let score = 0;
  const netBuy = s.inside > 0 ? (s.outside / s.inside * 100 - 100) : 0;

  if (s.chg5 > 5) score += 18;
  else if (s.chg5 > 0) score += 14;
  else if (s.chg5 > -3) score += 10;
  else score += 4;

  if (netBuy > 20 && s.volRatio > 1.2) score += 18;
  else if (netBuy > 10) score += 12;
  else if (netBuy > 0) score += 8;
  else score += 3;

  if (s.winRate > 55) score += 12;
  else if (s.winRate > 40) score += 8;
  else if (s.winRate > 0) score += 4;

  if (s.dragonTiger > 50) score += 8;
  else if (s.dragonTiger > 30) score += 4;

  return { score: Math.round(score), netBuy, winRate: s.winRate, dragonTiger: s.dragonTiger };
}

async function main() {
  console.log('=== 股票记录器启动 ===', new Date().toISOString());
  const stocks = await fetchStocks();
  const analyzed = stocks.map(s => ({ ...s, ...analyze(s) }));
  analyzed.sort((a, b) => b.score - a.score);
  const top5 = analyzed.slice(0, 3).map(s => ({
    code: s.code, name: s.name, price: s.price,
    chgPct: +s.chgPct.toFixed(2), score: s.score,
    winRate: +(s.winRate || 0).toFixed(0),
    dragonTiger: +(s.dragonTiger || 0).toFixed(0),
  }));

  const now = new Date();
  const date = now.toISOString().slice(0, 10);
  const time = now.toTimeString().slice(0, 5);

  let records = [];
  try { records = JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8')); } catch (e) {}

  let today = records.find(r => r.date === date);
  if (!today) {
    today = { date, picks: top5, pickTime: time };
    records.push(today);
  }

  const hour = now.getHours();
  if (hour >= 15) {
    today.closeTime = time;
    today.closeData = top5.map(p => ({ ...p, closePrice: p.price, closeChg: p.chgPct }));
  }

  console.log('前三:', top5.map(p => `${p.name}(${p.score}分)`).join(', '));
  fs.writeFileSync(DATA_FILE, JSON.stringify(records, null, 2));
}

main().catch(e => { console.error(e); process.exit(1); });

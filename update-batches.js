const fs=require('fs');const http=require('http');
let batches=[];try{batches=JSON.parse(fs.readFileSync('batches.json','utf-8'))}catch(e){}
if(!batches.length){console.log('No batches');process.exit(0)}
const allCodes=[...new Set(batches.flatMap(b=>b.codes||[]))];
console.log('Tracking',allCodes.length,'codes across',batches.length,'batches');
const qt=allCodes.map(c=>(c[0]==='6'||c[0]==='5'||c[0]==='9'?'sh':'sz')+c).join(',');
const pm={};
await new Promise(r=>{http.get('http://qt.gtimg.cn/q='+qt,res=>{let d='';res.on('data',c=>d+=c);res.on('end',()=>{const{decode}=require('iconv-lite')||{decode:b=>b.toString()};try{const t=decode(Buffer.from(d,'binary'),'gbk');for(const l of t.split(';')){if(!l.includes('="'))continue;const m=l.match(/="(.+)"/);if(!m)continue;const f=m[1].split('~');if(f.length<50)continue;pm[f[2]]={open:+f[5]||0,close:+f[3]||0,prev:+f[4]||0}}}catch(e){}r()})})});
const today=new Date().toISOString().slice(0,10);let ch=false;
for(const b of batches){for(const s of b.stocks){const p=pm[s.code];if(!p)continue;s.name=s.name||'';const last=s.records[s.records.length-1];if(!last||last.date!==today){s.records.push({date:today,open:p.open,close:p.close,chg:((p.close-p.prev)/p.prev*100).toFixed(1)});if(s.records.length>30)s.records=s.records.slice(-30);ch=true}}}
if(ch){fs.writeFileSync('batches.json',JSON.stringify(batches));console.log('Updated prices for today')}else{console.log('Already up to date')}

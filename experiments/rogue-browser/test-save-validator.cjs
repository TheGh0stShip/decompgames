// Independently authored negative cases for the native format reader. MIT, 2026 DecompGames contributors.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const root=path.resolve(process.env.ROGUE_BUILD||'D:/n64work/rogue-intake-2026-10-14/guarded-v4');
const spec=JSON.parse(fs.readFileSync(path.join(root,'save-spec.json'))),sample=new Uint8Array(fs.readFileSync(path.join(root,'native-sample.save')));
const context={module:{exports:{}},Uint8Array,DataView,globalThis:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'validate-save.js'),'utf8'),context);
const validate=context.module.exports.validateNativeSave,good=validate(sample,spec);
const report={date:new Date().toISOString(),scope:'Bounded standalone native-save format and reference validation; no native loader invoked for malformed cases',validBytes:good.bytes,parsedFields:good.fields.length,sampleSha256:crypto.createHash('sha256').update(sample).digest('hex'),validatorSha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'validate-save.js'))).digest('hex'),cases:[]};
function cipher(plain){const out=new Uint8Array(plain.length);let feedback=0;for(let j=0;j<plain.length;j++){const a=spec.enc[j%spec.enc.length],b=spec.stat[j%spec.stat.length];out[j]=plain[j]^a^b^feedback;feedback=(feedback+(a<128?a:a-256)*(b<128?b:b-256))&255;}return out;}
function mutation(field,value){const bytes=sample.slice(),plain=new Uint8Array(field.size);if(field.size===4)new DataView(plain.buffer).setInt32(0,value,true);else if(field.size===2)new DataView(plain.buffer).setInt16(0,value,true);else plain.fill(value);bytes.set(cipher(plain),field.offset);return bytes;}
function reject(label,bytes){let reason;try{validate(bytes,spec);}catch(e){reason=e.message;}assert(reason,'Unexpected acceptance: '+label);report.cases.push({label,reason});}
reject('empty',new Uint8Array());reject('oversized',new Uint8Array(180001));reject('truncated-tail',sample.slice(0,-1));reject('extra-tail',new Uint8Array([...sample,0]));
for(const f of good.fields){
 if(f.label.endsWith('-count')||f.label.endsWith('-array')||f.label.endsWith('-length')){reject(f.label+' negative',mutation(f,-1));reject(f.label+' oversized',mutation(f,2147483647));}
 if((f.label.startsWith('global-')&&!['global-2','global-27'].includes(f.label))||(f.label.startsWith('pack-used-')&&f.size===1)||f.label.includes('-known-'))reject(f.label+' not boolean',mutation(f,2));
}
const selected=[['player-pos-x',80],['player-pos-y',24],['player-stats-hp',0],['player-stats-maxhp',0],['depth',0],['inventory-mode',3],['hunger',4],['equipped-0',255],['player-destination-list',4],['player-room',21],['potion-color-0',spec.colors],['ring-stone-0',spec.stones],['stick-type-0',2],['stick-material-0',1000],['window-height',25],['window-width',81],['window-cell-0',512],['player-pack-2-which',10],['map-monster-0',0],['map-flags-0',143],['map-char-0',0],['daemon-function-0',10]];
for(const [label,value]of selected){const f=good.fields.find(f=>f.label===label);assert(f,'Missing test field '+label);reject(label+' invalid value',mutation(f,value));}
if(spec.maxDepth)for(const label of ['depth','max-depth'])reject(label+' beyond authored campaign',mutation(good.fields.find(f=>f.label===label),spec.maxDepth+1));
if(spec.printableWindow)for(const value of [0,31,127,255])reject('window glyph '+value,mutation(good.fields.find(f=>f.label==='window-cell-0'),value));
const markers=new Map();for(const f of good.fields)if(f.label.startsWith('marker-')&&!markers.has(f.label))markers.set(f.label,f);
for(const [label,f]of markers)reject(label+' wrong signature',mutation(f,0));
report.status='passed';fs.writeFileSync(path.join(root,'save-validator-result.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,validBytes:report.validBytes,parsedFields:report.parsedFields,rejectedCases:report.cases.length}));

// Private campaign verification through ordinary keyboard inputs. MIT, 2026.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert');
const {chromium}=require(path.resolve('node_modules/@playwright/test'));
const root=path.resolve(process.env.ROGUE_BUILD||'D:/n64work/rogue-intake-2026-10-14/survey-maps-v1');
const report={date:new Date().toISOString(),muted:true,scope:'Final authored three-floor campaign via ordinary keys; full browser save/restart and Continue saved; read-only native observers. No retail campaign or audible claim.',errors:[],runs:[]};
let server,context,page;
const dirs=[[1,0,'ArrowRight'],[-1,0,'ArrowLeft'],[0,1,'ArrowDown'],[0,-1,'ArrowUp']];
async function view(){return page.evaluate(()=>({state:JSON.parse(Module.UTF8ToString(Module._dg_state())),map:Module.UTF8ToString(Module._dg_map()).split('\n'),screen:document.querySelector('#terminal-text').textContent,result:Module.surveyResult,exited:!!Module.exited,failed:Module.failed,frames:Module.frames}));}
async function key(k,run){run.keys.push(k);await page.keyboard.press(k);await page.waitForTimeout(65);if(await page.evaluate(()=>Module.failed))throw Error(await page.evaluate(()=>Module.failed));}
async function clearMore(run){for(let i=0;i<8;i++){if(!(await view()).screen.includes('--More--'))return;await key('Space',run);}throw Error('Too many More prompts');}
function route(v,gx,gy){const s=v.state,start=s.y*80+s.x,goal=gy*80+gx,queue=[[start,[]]],seen=new Set([start]);while(queue.length){const[pos,keys]=queue.shift();if(pos===goal)return keys;const x=pos%80,y=Math.floor(pos/80);for(const[dx,dy,k]of dirs){let nx=x+dx,ny=y+dy,next=ny*80+nx;if(nx<0||nx>=80||ny<1||ny>22||seen.has(next)||!'.#+%^*?:!)/[]=,'.includes(v.map[ny][nx]))continue;seen.add(next);queue.push([next,[...keys,k]]);}}throw Error('No route to objective');}
async function heal(run){let v=await view();const vial=v.state.pack.find(o=>o[0]===33&&o[1]===5);if(v.state.hp<8&&vial){await clearMore(run);await key('q',run);await key(String.fromCharCode(vial[3]),run);await clearMore(run);run.healed=true;}}
async function walk(x,y,run){for(let i=0;i<240;i++){await clearMore(run);let v=await view();if(v.state.hp<=0||v.result==='lost')throw Error('Native death on route');if(v.state.x===x&&v.state.y===y)return;await heal(run);v=await view();await key(route(v,x,y)[0],run);if(i%15===0)run.observations.push((await view()).state);}throw Error('Route exceeded turn budget');}
async function openContext(){context=await chromium.launchPersistentContext(path.join(root,'survey-profile'),{channel:'msedge',headless:true,args:['--mute-audio'],viewport:{width:1100,height:810}});page=context.pages()[0];await page.addInitScript(()=>{window.audioCalls=0;for(const name of ['AudioContext','webkitAudioContext'])if(window[name])window[name]=class{constructor(){window.audioCalls++;throw Error('Forbidden audio');}};});page.on('pageerror',e=>report.errors.push(e.message));}
(async()=>{try{
server=http.createServer((req,res)=>{const u=new URL(req.url,'http://localhost');if(u.pathname==='/favicon.ico'){res.writeHead(204);return res.end();}const f=path.resolve(root,'.'+(u.pathname==='/'?'/index.html':u.pathname));if(!f.startsWith(root+path.sep)||!fs.existsSync(f)){res.writeHead(404);return res.end();}res.setHeader('Content-Type',f.endsWith('.wasm')?'application/wasm':f.endsWith('.js')?'text/javascript':'text/html');res.end(fs.readFileSync(f));});await new Promise(r=>server.listen(0,'127.0.0.1',r));
await openContext();
let completed=false;
for(let attempt=0;attempt<8&&!completed;attempt++){
const run={attempt,keys:[],observations:[],milestones:[]};report.runs.push(run);
await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.evaluate(()=>localStorage.removeItem(RogueProbe.saveKey));await page.reload();await page.waitForFunction(()=>window.Module?.ready||window.Module?.failed);assert(!await page.evaluate(()=>Module.failed));await page.locator('#terminal').click();
try{
await clearMore(run);let first=await view();assert.equal(first.state.depth,1);assert.equal(first.state.x,3);assert.equal(first.state.y,5);await key('ArrowLeft',run);let blocked=await view();assert.equal(blocked.state.x,first.state.x);assert.equal(blocked.state.y,first.state.y);run.collision=true;
for(let floor=1;floor<=3;floor++){
await walk(5,5,run);assert((await view()).state.pack.some(o=>o[0]===33&&o[1]===5),'Authored vial not collected');
if(floor===3){await walk(28,6,run);assert((await view()).state.pack.some(o=>o[0]===44),'Native lens pickup missing');run.lens=true;}
await walk(29,14,run);run.milestones.push((await view()).state);
if(floor===1){await key('<',run);await clearMore(run);assert.equal((await view()).state.depth,1);run.lockedAscent=true;}
if(floor===2&&!report.restored){await clearMore(run);const before=(await view()).state;await page.locator('#save').click();await page.waitForTimeout(100);await key('y',run);await page.waitForFunction(()=>Module.exited);assert(await page.evaluate(()=>Module.savedBytes>0),'Native checkpoint rejected');const envelope=JSON.parse(await page.evaluate(()=>localStorage.getItem(RogueProbe.saveKey)));fs.writeFileSync(path.join(root,'native-sample.save'),Buffer.from(envelope.bytes));report.saveBytes=envelope.bytes.length;await context.close();context=null;await openContext();await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>window.Module?.ready||window.Module?.failed);assert(!await page.evaluate(()=>Module.failed));assert.deepStrictEqual((await view()).state,before);assert(await page.evaluate(()=>Module.checkpointConsumed));report.restored=true;report.fullBrowserRestart=true;await page.locator('#terminal').click();await page.locator('#save').click();await page.waitForTimeout(100);await key('y',run);await page.waitForFunction(()=>Module.exited);assert(await page.locator('#continue').isEnabled());await page.locator('#continue').click();await page.waitForFunction(()=>window.Module?.ready);assert.deepStrictEqual((await view()).state,before);report.continueSavedButton=true;await page.locator('#terminal').click();}
if(floor<3){await key('>',run);await clearMore(run);assert.equal((await view()).state.depth,floor+1);}
else {await key('>',run);await clearMore(run);assert.equal((await view()).state.depth,3);run.floorCap=true;}
}
for(let floor=3;floor>=1;floor--){await walk(29,14,run);await key('<',run);await clearMore(run);if(floor>1){assert.equal((await view()).state.depth,floor-1);assert.equal((await view()).state.monsters.length,0);}}
await page.waitForFunction(()=>Module.surveyResult==='won');assert((await view()).screen.includes('SURVEY COMPLETE'));await page.screenshot({path:path.join(root,'survey-victory.png')});run.won=true;completed=true;
await key('Space',run);await key('Enter',run);await page.waitForFunction(()=>Module.exited);run.nativeExit=true;assert(!await page.evaluate(()=>Module.savedBytes));
}catch(e){run.failure=e.stack;await page.screenshot({path:path.join(root,`survey-attempt-${attempt}.png`)});}
await page.evaluate(()=>RogueProbe.stop());
}
assert(completed,'No completed native campaign');assert(report.restored,'No floor-two native save/restore');
// A fresh session must remain mortal and retry must create a new native player.
await Promise.all([page.waitForEvent('load'),page.locator('#restart').click()]);await page.waitForFunction(()=>window.Module?.ready);await page.locator('#terminal').click();const death={keys:[],observations:[]};report.death=death;
for(let i=0;i<600;i++){await clearMore(death);let v=await view();if(v.result==='lost'||v.state.hp<=0)break;await key('.',death);if(i%20===0)death.observations.push((await view()).state);}
assert.equal((await view()).result,'lost');await page.screenshot({path:path.join(root,'survey-death.png')});await Promise.all([page.waitForEvent('load'),page.locator('#restart').click()]);await page.waitForFunction(()=>window.Module?.ready);let fresh=await view();assert.equal(fresh.state.hp,fresh.state.maxHp);assert.equal(fresh.state.experience,0);assert.equal(fresh.state.depth,1);report.freshRetry=true;
await page.locator('#board').screenshot({path:path.join(root,'poster.png')});
await page.evaluate(()=>RogueProbe.stop());const frames=await page.evaluate(()=>Module.frames);await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>Module.frames),frames);assert(await page.evaluate(()=>Module.stopped&&Module.exited));report.nativeStop=true;report.audioCalls=await page.evaluate(()=>audioCalls);assert.equal(report.audioCalls,0);assert.deepStrictEqual(report.errors,[]);report.status='passed';
}catch(e){report.status='failed';report.failure=e.stack;if(page){try{report.last=await view();await page.screenshot({path:path.join(root,'survey-failure.png')});}catch{}}}
finally{if(context)await context.close();if(server)await new Promise(r=>server.close(r));report.playersClosed=true;const n=fs.readdirSync(root).filter(n=>/^survey-result-\d+\.json$/.test(n)).length+1;fs.writeFileSync(path.join(root,`survey-result-${n}.json`),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,failure:report.failure,runs:report.runs.map(r=>({attempt:r.attempt,won:r.won,failure:r.failure,keys:r.keys.length})),restored:report.restored,freshRetry:report.freshRetry}));if(report.status!=='passed')process.exitCode=1;}
})();

// Copyright 2026 DecompGames contributors. SPDX-License-Identifier: MIT.
const fs=require('fs'),path=require('path'),http=require('http'),assert=require('assert'),crypto=require('crypto');
const {chromium}=require('@playwright/test');
const repo=path.resolve(__dirname,'..'),cache=path.join(repo,'.cache');fs.mkdirSync(cache,{recursive:true});
const source=process.env.BEACON_SOURCE_DIR;assert(source,'Set BEACON_SOURCE_DIR to the extracted, hash-verified corresponding source archive.');
const manifest=JSON.parse(fs.readFileSync(path.join(repo,'public/manifests/beacon-yard.json')));
const production=process.env.BEACON_BASE_URL;const profile=path.join(cache,'beacon-profile-'+Date.now());
const report={date:new Date().toISOString(),production:!!production,muted:true,errors:[],missing:[],external:[],logs:[],blockedAnalyticsDiagnostics:[],audioContextsCreated:0,audibleAudioVerified:false};
let server,context,base;
async function open(){
 context=await chromium.launchPersistentContext(profile,{channel:'msedge',headless:true,viewport:{width:1200,height:1000},args:['--mute-audio','--enable-unsafe-swiftshader']});
 await context.addInitScript(()=>{
  window.audioContextConstructions=0;
  for(const name of ['AudioContext','webkitAudioContext']){const Original=window[name];if(Original)window[name]=new Proxy(Original,{construct(target,args,newTarget){window.audioContextConstructions++;return Reflect.construct(target,args,newTarget);}});}
  window.glLifetime={};
  for(const kind of ['Buffer','Texture','Framebuffer','Renderbuffer','Shader','Program','VertexArray']){
   const live=new Set();window.glLifetime[kind]={created:0,deleted:0,live:0};
   const p=WebGL2RenderingContext.prototype,c=p['create'+kind],d=p['delete'+kind];if(!c||!d)continue;
   p['create'+kind]=function(...args){const v=c.apply(this,args);if(v){live.add(v);window.glLifetime[kind].created++;window.glLifetime[kind].live=live.size;}return v;};
   p['delete'+kind]=function(v){if(live.delete(v)){window.glLifetime[kind].deleted++;window.glLifetime[kind].live=live.size;}return d.call(this,v);};
  }
 });
 await context.route('**/*',route=>{if(new URL(route.request().url()).origin!==base){report.external.push(route.request().url());return route.fulfill({status:200,contentType:'application/javascript',body:''});}return route.continue();});
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(String(e.stack||e)));page.on('console',m=>{const text=m.text();report.logs.push(text);if(m.type()==='error'){
  // An empty analytics stub intentionally fails Cloudflare's script integrity check.
  // Keep that diagnostic; every other console error still fails acceptance.
  if(text.startsWith("Failed to find a valid digest in the 'integrity' attribute for resource 'https://static.cloudflareinsights.com/beacon.min.js/")&&report.external.some(url=>text.includes(url)))report.blockedAnalyticsDiagnostics.push(text);
  else report.errors.push(text);
 }});page.on('response',r=>{if(r.status()>=400)report.missing.push(r.url());});
 await page.goto(base+'/games/beacon-yard/');assert((await page.locator('#stage-note').textContent()).includes('Silent edition'));
 await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#stage iframe')?.contentWindow?.BeaconYard?.state.ready,null,{timeout:60000});
 const frame=page.frames().find(f=>f.url().includes(manifest.base));assert(frame);await frame.locator('#canvas').click();
 // Observe cleanup only after the real Stop returns; no gameplay state writes.
 await frame.evaluate(()=>{const stop=BeaconYard.stop;BeaconYard.stop=async()=>{await stop();parent.beaconStoppedObservation={nativeShutdown:!!window.nativeShutdownComplete,currentContext:GL.currentContext==null,registeredContexts:GL.contexts.filter(Boolean).length,dbConnections:Object.keys(IDBFS.dbs).length,objects:window.glLifetime,audioContexts:window.audioContextConstructions};};});
 const adapter={evaluate:frame.evaluate.bind(frame),waitForFunction:frame.waitForFunction.bind(frame),locator:frame.locator.bind(frame),waitForTimeout:page.waitForTimeout.bind(page),keyboard:page.keyboard,mouse:{click:()=>frame.locator('#canvas').click()}};
 return {page,frame,adapter};
}
async function stopHost(p){await p.locator('#stop').click();await p.waitForFunction(()=>!document.querySelector('#stage iframe'));const s=await p.evaluate(()=>window.beaconStoppedObservation);assert(s.nativeShutdown);assert(s.currentContext);assert.equal(s.registeredContexts,0);assert.equal(s.dbConnections,0);assert(Object.values(s.objects).every(x=>x.live===0));assert.equal(s.audioContexts,0);assert.equal(await p.locator('#stop').isDisabled(),true);assert.equal(await p.locator('#play').isDisabled(),false);report.audioContextsCreated+=s.audioContexts;return s;}
(async()=>{try{
 if(production){base=new URL(production).origin;}else{
  server=http.createServer((req,res)=>{try{const url=new URL(req.url,'http://localhost'),binary=/^\/(runtime|data|sources)\//.test(url.pathname),root=path.join(repo,binary?'public':'dist');let p=path.resolve(root,'.'+decodeURIComponent(url.pathname));assert(p===root||p.startsWith(root+path.sep));if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');const type={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.wasm':'application/wasm','.svg':'image/svg+xml','.png':'image/png'};res.setHeader('Content-Type',type[path.extname(p)]||'application/octet-stream');res.end(fs.readFileSync(p));}catch{res.writeHead(404);res.end('Not found');}});await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;
 }
 report.distributionFiles=[];
 for(const f of [...manifest.files.map(f=>({...f,url:manifest.base+f.path})),{path:'corresponding source',url:manifest.sourceArchive,bytes:manifest.sourceArchiveBytes,sha256:manifest.sourceArchiveSha256}]){
  const response=await fetch(base+f.url,{cache:'no-store'}),bytes=Buffer.from(await response.arrayBuffer());assert(response.ok,f.url);assert.equal(bytes.length,f.bytes,f.url);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),f.sha256,f.url);report.distributionFiles.push(f.path);
 }
 let {page,frame,adapter}=await open();await require(path.join(source,'controls-acceptance.cjs')).initial(adapter,report);
 report.afterPartial=async(a,s)=>require(path.join(source,'controls-acceptance.cjs')).partial(a,report,s);
 report.afterComplete=async(a,s)=>{
  report.completed=s;await require(path.join(source,'controls-acceptance.cjs')).click(a,'save');assert.equal(await frame.locator('#storage-status').textContent(),'Saved on this device.');
  await page.screenshot({path:path.join(cache,'beacon-'+(production?'production':'local')+'-completed.png')});
  report.hostStop=await stopHost(page);await context.close();context=null;
  const next=await open();page=next.page;frame=next.frame;adapter=next.adapter;
  await frame.waitForFunction(()=>JSON.parse(Module.UTF8ToString(Module._dg_snapshot())).landed);report.restored=await frame.evaluate(()=>JSON.parse(Module.UTF8ToString(Module._dg_snapshot())));
  assert.equal(report.restored.mask,7);assert.equal(report.restored.actorActivatedMask,15);assert.equal(report.restored.complete,true);assert.equal(report.restored.gateDenied,1);assert.equal(report.restored.health,5);assert.equal(report.restored.glError,0);assert.equal(await frame.locator('#storage-status').textContent(),'Saved progress restored.');
  report.fullBrowserRestartNativePersistenceVerified=true;
  await page.screenshot({path:path.join(cache,'beacon-'+(production?'production':'local')+'-restored.png')});
  report.secondHostStop=await stopHost(page);
  // Reload a new module through the site Play button, then exercise stage-close.
  await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#stage iframe')?.contentWindow?.BeaconYard?.state.ready,null,{timeout:30000});
  const again=page.frames().find(f=>f.url().includes(manifest.base));assert(again);report.reopened=await again.evaluate(()=>JSON.parse(Module.UTF8ToString(Module._dg_snapshot())));assert.equal(report.reopened.mask,7);assert.equal(report.reopened.complete,true);
  await again.locator('#stop').click();await again.waitForFunction(()=>BeaconYard.state.stopped);await page.locator('#stop').click();await page.waitForFunction(()=>!document.querySelector('#stage iframe'));report.productStopThenHostUnloadVerified=true;report.hostPlayAfterStopVerified=true;
 };
 await require(path.join(source,'objective-journey.cjs'))(adapter,report);
 assert.equal(report.errors.length,0);assert.equal(report.missing.length,0);assert.equal(report.audioContextsCreated,0);assert(!report.logs.some(s=>s.includes('Assertion failed:')));report.assertionsPassed=true;
}catch(e){report.failure=String(e.stack||e);process.exitCode=1;if(context)try{await context.pages().at(-1).screenshot({path:path.join(cache,'beacon-site-failure.png')});}catch{}}
finally{if(context)await context.close();report.browserClosed=true;report.serverStarted=!!server;if(server){server.closeAllConnections();await new Promise(r=>server.close(r));}report.serverClosed=server?true:null;delete report.afterPartial;delete report.afterComplete;fs.writeFileSync(path.join(cache,'beacon-'+(production?'production':'local')+'-site.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({passed:!!report.assertionsPassed,failure:report.failure,distributionFiles:report.distributionFiles?.length,interactions:report.journey?.length,browserClosed:true,serverClosed:report.serverClosed}));}
})();

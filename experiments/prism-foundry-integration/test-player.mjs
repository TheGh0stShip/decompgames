// SPDX-License-Identifier: MIT
// Development smoke test. Uses only normal keyboard input and read-only exports.
import {chromium} from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]);
const route=process.argv.includes('--route');
const report={scope:'Startup and ordinary control smoke test, not campaign completion',muted:true,checkpoints:[],errors:[],consoleErrors:[],console:[],requests:[]};
const server=http.createServer((req,res)=>{
  if(req.url==='/favicon.ico'){res.writeHead(204).end();return;}
  const target=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname==='/'?'/index.html':new URL(req.url,'http://localhost').pathname));
  if(!target.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{res.setHeader('Content-Type',target.endsWith('.wasm')?'application/wasm':target.endsWith('.js')?'text/javascript':'text/html');res.end(fs.readFileSync(target));}catch{res.writeHead(404).end();}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser;
try{
  browser=await chromium.launch({channel:'msedge',headless:true,args:['--mute-audio']});
  report.browserVersion=browser.version();report.dateUtc=new Date().toISOString();
  const page=await browser.newPage({viewport:{width:1000,height:1000}});
  page.on('pageerror',e=>report.errors.push(e.stack));
  page.on('console',m=>{report.console.push(m.text());if(m.type()==='error')report.consoleErrors.push(m.text());});
  page.on('request',r=>report.requests.push(r.url().replace(/127\.0\.0\.1:\d+/,'127.0.0.1:PORT')));
  if(process.argv.includes('--loading-stop')){
    let delayed=false;
    await page.route('**/foundry.wasm',async r=>{if(!delayed){delayed=true;await new Promise(resolve=>setTimeout(resolve,1000));}try{await r.continue();}catch{}});
  }
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  if(process.argv.includes('--loading-stop')){
    await page.locator('#start').click();
    const loading=await (await page.locator('iframe').elementHandle()).contentFrame();
    await loading.waitForFunction(()=>typeof Module!=='undefined'&&typeof Module._FoundryStatus==='function'&&!foundryReady);
    assert.equal(await loading.evaluate(()=>foundrySnapshot()),null);
    await page.locator('#stop').click();
    await page.waitForFunction(()=>document.querySelector('#state').textContent==='Stopped — player context removed');
    assert.equal(await page.locator('iframe').count(),0);
    report.stoppedDuringLoadingWithoutNativeExportCall=true;
  }
  await page.locator('#start').click();
  let frame=await page.locator('iframe').elementHandle();
  let game=await frame.contentFrame();
  await game.waitForFunction(()=>window.foundrySnapshot?.()?.ticks>20,null,{timeout:30000});
  const snapshot=()=>game.evaluate(()=>foundrySnapshot());
  const tap=async key=>{await page.keyboard.down(key);await page.waitForTimeout(90);await page.keyboard.up(key);};
  report.checkpoints.push({name:'startup',state:await snapshot()});
  await game.locator('canvas').focus();
  await page.keyboard.down('ArrowRight');await page.waitForTimeout(400);await page.keyboard.up('ArrowRight');
  const moved=await snapshot();report.checkpoints.push({name:'right movement',state:moved});
  assert(moved.x>report.checkpoints[0].state.x);
  await page.keyboard.down('Space');await page.waitForTimeout(100);await page.keyboard.up('Space');
  const jumped=await snapshot();report.checkpoints.push({name:'jump',state:jumped});assert(jumped.y<moved.y);
  await tap('p');await page.waitForTimeout(80);const paused=await snapshot();
  await page.waitForTimeout(300);const still=await snapshot();
  assert.equal(still.paused,1);assert.equal(still.ticks,paused.ticks);assert.equal(still.x,paused.x);assert.equal(still.y,paused.y);
  report.checkpoints.push({name:'pause remains stationary',state:still});
  await tap('p');await page.waitForTimeout(100);assert.equal((await snapshot()).paused,0);
  await tap('n');await page.waitForTimeout(150);const noSkip=await snapshot();assert.equal(noSkip.course,0);assert.equal(noSkip.prisms,0);assert.equal(noSkip.editor,0);
  report.checkpoints.push({name:'editor skip disabled',state:noSkip});
  await tap('r');await page.waitForTimeout(500);const retry=await snapshot();assert.equal(retry.course,0);assert.equal(retry.prisms,0);assert(retry.x<150);
  report.checkpoints.push({name:'ordinary retry',state:retry});
  if(route){
    const record=async name=>{const state=await snapshot();report.checkpoints.push({name,state});console.log(JSON.stringify({name,state}));};
    const move=async target=>{
      const s=await snapshot();const key=s.x<target?'ArrowRight':'ArrowLeft';
      await page.keyboard.down(key);
      try{await game.waitForFunction(({target,right})=>{const s=foundrySnapshot();return right?s.x>=target:s.x<=target;},{target,right:s.x<target},{timeout:5000});}
      finally{await page.keyboard.up(key);}
      await page.waitForTimeout(120);
    };
    const jumpTo=async target=>{await page.keyboard.down('Space');await move(target);await page.keyboard.up('Space');await page.waitForTimeout(700);};
    await move(250);await jumpTo(428);await record('first ledge');
    await move(410);
    await page.waitForTimeout(1200);await record('first pickup settled');
    assert.equal((await snapshot()).prisms,1);
    await move(515);await jumpTo(760);await record('second ledge');
    await page.waitForTimeout(1200);await record('second pickup settled');assert.equal((await snapshot()).prisms,2);
    // Walk into the floor gap to exercise a real fall, without state mutation.
    await move(930);await page.waitForTimeout(1800);await record('gap fall and respawn');
    assert((await snapshot()).respawns>0);
    assert.equal((await snapshot()).prisms,2);
  }
  await page.screenshot({path:path.join(root,'startup-controls.png')});
  await page.locator('#stop').click();await page.waitForFunction(()=>document.querySelector('#state').textContent==='Stopped \u2014 native shutdown observed');
  assert.equal(await page.locator('iframe').count(),0);report.nativeShutdownObserved=true;
  await page.locator('#start').click();frame=await page.locator('iframe').elementHandle();game=await frame.contentFrame();
  await game.waitForFunction(()=>window.foundrySnapshot?.()?.ticks>20,{timeout:30000});
  report.checkpoints.push({name:'fresh restart',state:await snapshot()});
  await page.locator('#stop').click();await page.waitForFunction(()=>document.querySelector('#state').textContent==='Stopped \u2014 native shutdown observed');
  report.secondNativeShutdownObserved=true;
  assert.deepEqual(report.errors,[]);assert.deepEqual(report.consoleErrors,[]);
  report.passed=true;
}catch(e){report.passed=false;report.failure=e.stack;console.error(e);process.exitCode=1;}
finally{if(browser)await browser.close();await new Promise(r=>server.close(r));fs.writeFileSync(path.join(root,route?'browser-route.json':'browser-smoke.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));}

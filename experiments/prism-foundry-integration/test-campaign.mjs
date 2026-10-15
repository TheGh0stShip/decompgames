// SPDX-License-Identifier: MIT
// Ordinary keyboard route with read-only observations; no game-state writes.
import {chromium} from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import assert from 'node:assert/strict';
const root=path.resolve(process.argv[2]);
const report={scope:'Ordinary three-course campaign attempt',dateUtc:new Date().toISOString(),muted:true,checkpoints:[],errors:[],warnings:[]};
const server=http.createServer((req,res)=>{
  if(req.url==='/favicon.ico'){res.writeHead(204).end();return;}
  const name=new URL(req.url,'http://localhost').pathname;
  const target=path.resolve(root,'.'+(name==='/'?'/index.html':name));
  if(!target.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{res.setHeader('Content-Type',target.endsWith('.wasm')?'application/wasm':target.endsWith('.js')?'text/javascript':'text/html');res.end(fs.readFileSync(target));}catch{res.writeHead(404).end();}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
let browser,page,game;
try{
  browser=await chromium.launch({channel:'msedge',headless:true,args:['--mute-audio']});report.browserVersion=browser.version();
  page=await browser.newPage({viewport:{width:1000,height:1100}});
  page.on('pageerror',e=>report.errors.push(e.message));
  page.on('console',m=>{if(m.type()==='warning'||m.type()==='error')report.warnings.push(m.text());});
  await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('#start').click();
  game=await (await page.locator('iframe').elementHandle()).contentFrame();
  await game.waitForFunction(()=>window.foundrySnapshot?.()?.ticks>20,null,{timeout:30000});
  await game.locator('canvas').focus();
  const state=()=>game.evaluate(()=>foundrySnapshot());
  const record=async name=>{const s=await state();report.checkpoints.push({name,state:s});console.log(JSON.stringify({name,state:s}));};
  const ticks=async count=>{const s=await state();await game.waitForFunction(t=>{const s=foundrySnapshot();return s.ticks>=t||s.complete===1;},s.ticks+count,{timeout:5000});};
  // Let native deceleration finish, then use bounded key bursts for positioning.
  const rest=()=>ticks(40);
  const move=async target=>{
    const initialCourse=(await state()).course;
    for(let attempt=0;attempt<24;attempt++){
      const s=await state(),delta=target-s.x;
      if(s.course!==initialCourse||s.complete)return;
      if(Math.abs(delta)<18)return;
      const key=delta>0?'ArrowRight':'ArrowLeft';
      const right=delta>0;
      const threshold=Math.abs(delta)>130?target+(right?-100:100):s.x+(right?6:-6);
      await page.keyboard.down(key);
      try{await game.waitForFunction(({threshold,right,course})=>{const s=foundrySnapshot();return s.course!==course||s.complete||(right?s.x>=threshold:s.x<=threshold);},{threshold,right,course:initialCourse},{timeout:4000});}
      finally{await page.keyboard.up(key);}
      await rest();
    }
    throw Error('Positioning failed: '+JSON.stringify({target,state:await state()}));
  };
  const jump=async target=>{
    const s=await state(),key=target>s.x?'ArrowRight':'ArrowLeft';
    await page.keyboard.down(key);await page.keyboard.down('Space');
    await ticks(6);await page.keyboard.up('Space');
    const delta=Math.abs(target-s.x),cutoff=Math.max(6,Math.round(delta/4-13));
    if(cutoff>6)await ticks(cutoff-6);
    await page.keyboard.up(key);await ticks(70);
  };
  const collect=async (x,count)=>{
    if((await state()).prisms<count){await move(x);await ticks(75);}
    if((await state()).prisms<count){await move(x-24);await move(x+8);await ticks(75);}
    assert.equal((await state()).prisms,count);
  };
  await record('startup');
  await move(250);await record('first launch');await jump(420);await record('first ledge landing');
  await move(420);await ticks(75);await record('first prism');assert.equal((await state()).prisms,1);
  await move(500);await jump(740);await record('second ledge landing');
  await ticks(75);await record('second prism');assert.equal((await state()).prisms,2);
  await jump(1080);await record('first gap crossing');
  await move(1180);await jump(1330);await record('third approach ledge');
  await move(1390);await jump(1520);await record('third high ledge');
  await move(1520);await ticks(75);await record('third prism');assert.equal((await state()).prisms,3);
  await move(1900);await record('first gate');
  await game.waitForFunction(()=>foundrySnapshot().course===1,null,{timeout:5000});
  await record('Cooling Loop reached');
  report.firstCoursePassed=true;
  if(!process.argv.includes('--first-only')){
    await move(220);await jump(360);await record('cooling first step');
    await move(430);await jump(550);await collect(544,1);await record('cooling first prism');
    await move(630);await jump(900);await record('cooling first gap');
    await move(1040);await jump(1190);await collect(1184,2);await record('cooling second prism');
    await jump(1470);await record('cooling second gap');
    await move(1500);await jump(1640);await record('cooling third approach');
    await move(1710);await jump(1830);await collect(1824,3);await record('cooling third prism');
    await move(2160);await game.waitForFunction(()=>foundrySnapshot().course===2,null,{timeout:5000});await record('Night Shift reached');report.secondCoursePassed=true;
    await move(250);await jump(430);await record('night first step');
    await move(500);await jump(620);await collect(608,1);await record('night first prism');
    await move(730);await jump(1000);await record('night first gap');
    await move(1190);await jump(1320);await collect(1312,2);await record('night second prism');
    await move(1430);await jump(1740);await record('night second gap');
    await move(1900);await jump(2020);await collect(2016,3);await record('night third prism');
    await move(2420);await game.waitForFunction(()=>foundrySnapshot().complete===1,null,{timeout:5000});await record('all three courses complete');report.campaignPassed=true;
    await page.waitForFunction(()=>document.querySelector('#state').textContent==='All three courses complete. Stop and Start to play again.');
    report.visibleVictoryMessage=true;
  }
  assert.deepEqual(report.errors,[]);report.passed=true;
}catch(e){report.passed=false;report.failure=e.message;process.exitCode=1;if(game){try{report.finalState=await game.evaluate(()=>foundrySnapshot());}catch{}}console.error(e.message);}
finally{
  if(page){try{await page.screenshot({path:path.join(root,'campaign-'+Date.now()+'.png')});await page.locator('#stop').click();await page.waitForFunction(()=>document.querySelector('#state').textContent==='Stopped — native shutdown observed',null,{timeout:5000});report.nativeShutdownObserved=true;}catch{report.nativeShutdownObserved=false;}}
  if(browser)await browser.close();await new Promise(r=>server.close(r));report.browserClosed=true;report.serverClosed=true;
  fs.writeFileSync(path.join(root,'campaign-attempt-'+Date.now()+'.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
}

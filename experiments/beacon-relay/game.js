// Independently authored browser/controller code, MIT. Graphics, animation, font,
// palette and presentation text authored in this file are dedicated under CC0-1.0.
const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d'),status=document.querySelector('#status');
const color=['#101c31','#14243a','#264057','#445c69','#70687d','#9a7a78','#abc9cc','#e5f8f3','#c3766c','#daa278','#f9d46a','#68cbb7','#419fa3','#388094','#587f9c','#c0e5da'];
// Own five-row glyph definitions: no font file or cartridge font is used.
const font={A:'010101111101101',B:'110101110101110',C:'011100100100011',D:'110101101101110',E:'111100110100111',F:'111100110100100',G:'011100101101011',H:'101101111101101',I:'111010010010111',J:'001001001101010',K:'101101110101101',L:'100100100100111',M:'101111111101101',N:'101111111111101',O:'010101101101010',P:'110101110100100',Q:'010101101111011',R:'110101110101101',S:'011100010001110',T:'111010010010010',U:'101101101101111',V:'101101101101010',W:'101101111111101',X:'101101010101101',Y:'101101010010010',Z:'111001010100111','0':'111101101101111','1':'010110010010111','2':'110001010100111','3':'110001010001110','4':'101101111001001','5':'111100110001110','6':'011100111101111','7':'111001010010010','8':'111101111101111','9':'111101111001110',':':'000010000010000','/':'001001010100100','-':'000000111000000','!':'010010010000010',' ':'000000000000000'};
function rect(x,y,w,h,c){ctx.fillStyle=color[c&15];ctx.fillRect(Math.floor(x),Math.floor(y),w,h)}
function text(t,x,y,c=7){for(const ch of t){const bits=font[ch]||font[' '];for(let i=0;i<15;i++)if(bits[i]==='1')rect(x+i%3,y+Math.floor(i/3),1,1,c);x+=4}}
function sprite(id,x,y,flip){x=Math.floor(x);y=Math.floor(y);ctx.save();ctx.translate(x+(flip?8:0),y);if(flip)ctx.scale(-1,1);
 if(id>=1&&id<=7){ // Box rover: lantern visor, metal shell and two animated treads.
  rect(1,1,6,5,6);rect(0,3,8,3,12);rect(2,2,4,2,10);rect(3,2,1,1,7);rect(0,6,3,2,3);rect(5,6,3,2,3);rect((id%2)?1:0,7,2,1,11);rect((id%2)?5:6,7,2,1,11);
 }else if(id>=118&&id<=120){rect(3,0,2,8,6);rect(1,1,6,3,11);rect(2+(id-118),1,2,2,10);rect(1,7,6,1,3);
 }else if(id===26||id===27||id===28||id===29){rect(3,0,2,1,7);rect(2,1,4,4,10);rect(1,2,6,2,10);rect(3,5,2,1,9);rect(3,1,1,3,7);
 }else if(id>=18&&id<=21){rect(0,6,8,2,12);rect(1,4,6,2,10);rect(2,2,4,2,6);
 }else{rect(2,2,4,4,11);rect(3,1,2,1,7)}ctx.restore();}
function render(state){ctx.clearRect(0,0,128,128);for(const a of state.commands){switch(a[0]){
 case 'rect':rect(a[1],a[2],Math.floor(a[3])-Math.floor(a[1])+1,Math.floor(a[4])-Math.floor(a[2])+1,a[5]);break;
 case 'circle':rect(a[1]-a[3],a[2]-a[3],Math.max(1,a[3]*2),Math.max(1,a[3]*2),11);break; // square exhaust particles
 case 'tile':rect(a[1],a[2],8,8,2);rect(a[1],a[2],8,1,11);rect(a[1]+1,a[2]+3,3,1,3);rect(a[1]+5,a[2]+6,2,1,3);break;
 case 'sprite':sprite(a[1],a[2],a[3],a[6]);break;
 case 'text':text(a[1],a[2],a[3],a[4]);break;
 // Palette calls are retained in the command stream, but this renderer uses its own fixed palette.
 }}
 if(state.completed){rect(10,42,108,42,0);text('RELAY COMPLETE',36,48,10);text('THREE BEACONS LIT',28,62,11);text('NEW RELAY TO REPLAY',28,76,7)}
 else if(state.cleared){rect(10,40,108,24,0);text('BEACON LIT',44,46,10);text('NEXT COURSE BELOW',30,56,7)}
 document.querySelector('#next').disabled=!state.cleared||state.completed;
}
const keyBits={ArrowLeft:0,ArrowRight:1,ArrowUp:2,ArrowDown:3,KeyZ:4,Space:4,KeyX:5};
let runtime,bridge,state,mask=0,pending=0,paused=false,stopped=false,raf,last=0,acc=0,checkpointNote='';const held=new Set(),key='beacon-relay-checkpoint-v1';
function readSave(){try{const s=JSON.parse(localStorage.getItem(key));return s?.version===1&&Number.isInteger(s.course)&&s.course>=1&&s.course<=3?s:null}catch{return null}}
function save(course){try{localStorage.setItem(key,JSON.stringify({version:1,course}));document.querySelector('#resume').disabled=false;return true}catch{return false}}
function clearInput(){held.clear();mask=0;pending=0}function inputs(){mask=0;for(const code of held)mask|=1<<keyBits[code]}
function setState(s){state=JSON.parse(s);render(state);status.textContent=(state.completed?'Relay complete — three beacons lit.':state.cleared?`Course ${state.course+1} cleared. Continue to save a checkpoint.`:paused?'Paused.':`Course ${state.course+1} / 3 · Lights ${state.stats.PICO_BERRIES||0} · Retries ${state.stats.PICO_DEATHS||0} · Sound off`)+checkpointNote}
function restart(course){clearInput();paused=false;acc=0;last=0;checkpointNote='';document.querySelector('#pause').textContent='Pause';setState(bridge.Init(course));canvas.focus()}
function next(){if(!state.cleared||state.completed)return;clearInput();const value=bridge.Next();checkpointNote=save(JSON.parse(value).course)?' Checkpoint saved.':' Checkpoint could not be saved.';setState(value);canvas.focus()}
function pause(){paused=!paused;clearInput();document.querySelector('#pause').textContent=paused?'Continue':'Pause';setState(JSON.stringify(state));last=0;acc=0}
function loop(now){if(stopped)return;if(!last)last=now;acc+=Math.min(100,now-last);last=now;if(!paused){while(acc>=1000/30){setState(bridge.Step(mask|pending));pending=0;acc-=1000/30}}else acc=0;raf=requestAnimationFrame(loop)}
function onDown(e){if(e.code==='KeyP'&&document.activeElement===canvas&&!e.repeat){e.preventDefault();pause();return}if(e.code in keyBits&&document.activeElement===canvas){e.preventDefault();held.add(e.code);pending|=1<<keyBits[e.code];inputs()}}
function onUp(e){if(e.code in keyBits){held.delete(e.code);inputs()}}
function blur(){clearInput();if(!stopped&&!paused)pause()}
let loadingTimer;
try{const initialize=async()=>{const {dotnet}=await import('./_framework/dotnet.js');const response=await fetch('./boot.json',{signal:AbortSignal.timeout(30000)});if(!response.ok)throw Error('Boot manifest unavailable');const config=await response.json();if(stopped)throw Error('Loading canceled');const required=Object.values(config.resources).flatMap(group=>Object.keys(group));await Promise.all(required.map(async name=>{const asset=await fetch('./_framework/'+encodeURIComponent(name),{method:'HEAD',signal:AbortSignal.timeout(30000)});if(!asset.ok)throw Error('Required asset unavailable: '+name)}));if(stopped)throw Error('Loading canceled');runtime=await dotnet.withConfig(config).create();if(stopped){runtime.exit(0);throw Error('Loading canceled')}bridge=(await runtime.getAssemblyExports('Probe.dll')).GameBridge;if(stopped){runtime.exit(0);throw Error('Loading canceled')}};await Promise.race([initialize(),new Promise((_,reject)=>{loadingTimer=setTimeout(()=>reject(Error('Loading deadline exceeded')),30000)})]);clearTimeout(loadingTimer);
 setState(bridge.Init(0));document.querySelectorAll('button').forEach(b=>b.disabled=false);document.querySelector('#next').disabled=true;document.querySelector('#resume').disabled=!readSave();
 document.querySelector('#new').onclick=()=>restart(0);document.querySelector('#resume').onclick=()=>{const s=readSave();if(s)restart(s.course)};document.querySelector('#next').onclick=next;document.querySelector('#pause').onclick=pause;
 document.querySelector('#stop').onclick=()=>{stopped=true;clearInput();cancelAnimationFrame(raf);window.removeEventListener('keydown',onDown);window.removeEventListener('keyup',onUp);window.removeEventListener('blur',blur);runtime.exit(0);document.querySelectorAll('button').forEach(b=>b.disabled=true);status.textContent='Stopped. Reload this page to play.';document.body.dataset.stopped='true'};
 window.addEventListener('keydown',onDown);window.addEventListener('keyup',onUp);window.addEventListener('blur',blur);canvas.addEventListener('blur',clearInput);canvas.addEventListener('click',()=>canvas.focus());
 // Read-only observation for verification; no bridge or state mutation interface is exposed.
 Object.defineProperty(window,'relayObservation',{get:()=>JSON.parse(JSON.stringify({...state,commands:undefined,paused,stopped}))});document.body.dataset.ready='true';raf=requestAnimationFrame(loop);
}catch(e){clearTimeout(loadingTimer);stopped=true;clearInput();if(raf)cancelAnimationFrame(raf);try{runtime?.exit(0)}catch{}document.querySelectorAll('button').forEach(b=>b.disabled=true);status.textContent='Runtime failed to load. Reload this page to retry.';document.body.dataset.failed='true';console.error(e)}

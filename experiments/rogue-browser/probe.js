// Independently authored private host. MIT, 2026 DecompGames contributors.
const saveKey=window.DGSaveKey||'rogue-private-save-v2';
let finishStop;
var Module={
 wasmBinary:window.DGValidatedWasm,
 keys:[],frames:0,arguments:[],preRun:[],focused:true,
 print:console.log,printErr:console.error,
 onSurveyResult(won){Module.surveyResult=won?'won':'lost';document.body.dataset.state=Module.surveyResult;document.querySelector('#status').textContent=won?'Survey complete':'Expedition interrupted';},
 onRuntimeInitialized(){Module.runtimeInitialized=true;if(Module.stopping)Module._dg_request_stop();},
 onTerminal(a,h,w,y,x){
  if(Module.exited||Module.stopping)return;
  Module.cells=Array.from(a);
  const lines=[];
  for(let r=0;r<h;r++)lines.push(Array.from(a.slice(r*80,r*80+w),c=>String.fromCharCode(c&255)).join(''));
  (document.querySelector('#terminal-text')||document.querySelector('#terminal')).textContent=lines.join('\n');
  if(window.drawSurveyTerminal)window.drawSurveyTerminal(a,h,w);
  Module.frames++;
  Module.history=Module.history||[];
  Module.history.push(lines.join('\n'));
  if(Module.history.length>40)Module.history.shift();
 },
 onInputWait(){
  if(Module.stopping)return;
  if(!Module.ready){
   Module.ready=true;
   if(Module.restoring){localStorage.removeItem(saveKey);Module.checkpointConsumed=true;}
   document.querySelector('#status').textContent='Running — audio unavailable';
   document.body.dataset.state='ready';
  }
 },
 onExit(status){
  Module.exited=true;Module.exitStatus=status;Module.keys=[];Module.waiting=false;
  document.querySelector('#status').textContent=Module.nativeStop?'Stopped':Module.surveyResult==='won'?'Survey complete':Module.surveyResult==='lost'?'Expedition interrupted':'Exited '+status;
  if(Module.nativeStop)document.body.dataset.state='stopped';
  if(!Module.nativeStop){
   try{
    const bytes=Module.FS.readFile('/rogue.save');
    const checked=DGSave.validateNativeSave(bytes,DGSaveSpec);
    localStorage.setItem(saveKey,JSON.stringify({schema:2,build:DGSaveSpec.build,bytes:Array.from(bytes)}));
    Module.savedBytes=checked.bytes;
    const resume=document.querySelector('#continue');if(resume)resume.disabled=false;
   }catch(e){
    if(Module.FS.analyzePath('/rogue.save').exists){Module.saveFailed=String(e);document.querySelector('#status').textContent='Checkpoint rejected: '+e.message;}
   }
  }
  if(finishStop){Module.stopped=true;finishStop();finishStop=null;}
 },
 onAbort(reason){document.querySelector('#status').textContent='Failed: '+reason;Module.failed=String(reason);document.body.dataset.state='failed';}
};
const saved=localStorage.getItem(saveKey);
if(saved){
 try{
  if(saved.length>750000)throw Error('Checkpoint exceeds size limit');
  const envelope=JSON.parse(saved),b=envelope.bytes;
  if(envelope.schema!==2||envelope.build!==DGSaveSpec.build)throw Error('Checkpoint belongs to a different build');
  if(!Array.isArray(b)||b.length>180000||b.some(c=>!Number.isInteger(c)||c<0||c>255))throw Error('Invalid checkpoint bytes');
  const bytes=new Uint8Array(b);
  DGSave.validateNativeSave(bytes,DGSaveSpec);
  Module.restoring=true;Module.arguments=['/rogue.save'];
  Module.preRun.push(()=>Module.FS.writeFile('/rogue.save',bytes));
 }catch(e){Module.badSave=true;Module.noInitialRun=true;Module.failed='Checkpoint rejected: '+e.message;document.querySelector('#status').textContent=Module.failed;document.body.dataset.state='failed';}
}
function keydown(e){
 if(Module.exited||Module.failed||Module.stopping||!Module.focused)return;
 const c={ArrowLeft:'h',ArrowRight:'l',ArrowUp:'k',ArrowDown:'j',Home:'y',PageUp:'u',End:'b',PageDown:'n',Enter:'\n',Escape:'\x1b',Backspace:'\b',Delete:'\x7f'}[e.key]||e.key;
 if(c.length===1&&c.charCodeAt(0)<128){e.preventDefault();Module.keys.push(e.ctrlKey?c.charCodeAt(0)&31:c.charCodeAt(0));}
}
document.addEventListener('keydown',keydown);
window.addEventListener('blur',()=>{Module.keys=[];Module.focused=false;});
window.addEventListener('focus',()=>{Module.focused=true;});
document.querySelector('#terminal').addEventListener('focus',()=>{Module.focused=true;});
document.querySelector('#save').onclick=()=>{if(Module.ready&&!Module.exited&&!Module.stopping)Module.keys.push(83);};
document.querySelector('#restart').onclick=()=>{localStorage.removeItem(saveKey);location.reload();};
const resumeButton=document.querySelector('#continue');if(resumeButton)resumeButton.onclick=()=>location.reload();
async function stop(){
 if(Module.stopped)return;
 if(Module.stopPromise)return Module.stopPromise;
 Module.stopping=true;Module.keys=[];document.removeEventListener('keydown',keydown);
 if(Module.exited||Module.noInitialRun){Module.stopped=true;document.body.dataset.state='stopped';document.querySelector('#status').textContent='Stopped';return;}
 Module.stopPromise=new Promise((resolve,reject)=>{
  const timeout=setTimeout(()=>reject(Error('Native Stop did not complete')),5000);
  finishStop=()=>{clearTimeout(timeout);resolve();};
 });
 if(Module.runtimeInitialized)Module._dg_request_stop();
 await Module.stopPromise;
}
window.RogueProbe={stop,get stopped(){return !!Module.stopped;},saveKey};
document.querySelector('#stop').onclick=()=>stop().catch(e=>{Module.failed=e.message;document.querySelector('#status').textContent=e.message;});

// Independently authored private host. MIT, 2026 DecompGames contributors.
var Module={keys:[],frames:0,arguments:[],preRun:[],print:console.log,printErr:console.error,
 onTerminal(a,h,w,y,x){Module.cells=Array.from(a);let lines=[];for(let r=0;r<h;r++)lines.push(Array.from(a.slice(r*80,r*80+w),c=>String.fromCharCode(c&255)).join(''));document.querySelector('#terminal').textContent=lines.join('\n');Module.frames++;Module.history=(Module.history||[]);Module.history.push(lines.join('\n'));if(Module.history.length>40)Module.history.shift();document.querySelector('#status').textContent='Running — audio unavailable';},
 onExit(status){Module.exited=true;Module.exitStatus=status;document.querySelector('#status').textContent='Exited '+status;try{const bytes=Module.FS.readFile('/rogue.save');localStorage.setItem('rogue-private-save',JSON.stringify(Array.from(bytes)));Module.savedBytes=bytes.length;}catch{}},
 onAbort(reason){document.querySelector('#status').textContent='Failed: '+reason;Module.failed=String(reason);}
};
let saved=localStorage.getItem('rogue-private-save');
if(saved){try{let b=JSON.parse(saved);if(!Array.isArray(b)||b.length>200000)throw Error('Invalid checkpoint');Module.arguments=['/rogue.save'];Module.preRun.push(()=>Module.FS.writeFile('/rogue.save',new Uint8Array(b)));}catch{Module.badSave=true;}}
document.addEventListener('keydown',e=>{if(Module.exited)return;let c={ArrowLeft:'h',ArrowRight:'l',ArrowUp:'k',ArrowDown:'j',Home:'y',PageUp:'u',End:'b',PageDown:'n',Enter:'\n',Escape:'\x1b',Backspace:'\b',Delete:'\x7f'}[e.key]||e.key;if(c.length===1){e.preventDefault();Module.keys.push(e.ctrlKey?c.charCodeAt(0)&31:c.charCodeAt(0));}});
document.querySelector('#save').onclick=()=>Module.keys.push(83);
document.querySelector('#restart').onclick=()=>{localStorage.removeItem('rogue-private-save');location.reload();};

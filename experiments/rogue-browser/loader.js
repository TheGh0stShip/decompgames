// Independently authored MIT loader. Validate the finite build before native startup.
(async()=>{
 const status=document.querySelector('#status'),controller=new AbortController();
 let cancelled=false,nativeLoaded=false;
 const timeout=setTimeout(()=>{if(!nativeLoaded)controller.abort();},20000);
 const scriptNames=['glyphs.js','font-renderer.js','save-spec.js','validate-save.js','probe.js','game.js'];
 function mark(state,message){document.body.dataset.state=state;status.textContent=message;}
 async function stopLoading(){cancelled=true;controller.abort();clearTimeout(timeout);mark('stopped','Stopped');}
 window.DGSaveKey='decompgames.signal-survey.stations-v1.checkpoint';
 window.RogueProbe={stop:stopLoading,saveKey:window.DGSaveKey,get stopped(){return cancelled;}};
 document.querySelector('#stop').onclick=stopLoading;
 document.querySelector('#restart').onclick=()=>location.reload();
 async function read(name){const response=await fetch(new URL(name,location.href),{signal:controller.signal,cache:'no-store'});if(!response.ok)throw Error('Missing '+name);return new Uint8Array(await response.arrayBuffer());}
 async function script(bytes){const url=URL.createObjectURL(new Blob([bytes],{type:'text/javascript'}));try{await new Promise((resolve,reject)=>{const element=document.createElement('script');element.src=url;element.onload=resolve;element.onerror=()=>reject(Error('Player script failed'));document.body.append(element);});}finally{URL.revokeObjectURL(url);}}
 try{
  mark('loading','Loading');
  const manifest=JSON.parse(new TextDecoder().decode(await read('load-manifest.json')));
  const required=[...scriptNames,'game.wasm'];
  if(manifest.schema!==1||manifest.files.length!==required.length||new Set(manifest.files.map(f=>f.path)).size!==required.length||manifest.files.some(f=>!required.includes(f.path)||!Number.isSafeInteger(f.bytes)||f.bytes<1||f.bytes>3000000||!/^[a-f0-9]{64}$/.test(f.sha256)))throw Error('Invalid build manifest');
  const bytes={};
  await Promise.all(manifest.files.map(async file=>{const data=await read(file.path);const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',data)),b=>b.toString(16).padStart(2,'0')).join('');if(data.length!==file.bytes||digest!==file.sha256)throw Error('Build checksum differs: '+file.path);bytes[file.path]=data;}));
  if(cancelled)return;
  window.DGValidatedWasm=bytes['game.wasm'];
  for(const name of scriptNames){if(cancelled)return;await script(bytes[name]);}
  nativeLoaded=true;clearTimeout(timeout);
 }catch(error){clearTimeout(timeout);if(cancelled)return;mark('failed',controller.signal.aborted?'Loading timed out. Try again.':'Unable to start: '+error.message);window.RogueProbe={stop:stopLoading,get stopped(){return cancelled;}};document.querySelector('#stop').onclick=stopLoading;}
})();

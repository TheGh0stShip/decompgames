var Module;
(()=>{
/* Independently authored MIT browser controls and completed-round journal.
 * Observes native health/round boundaries; never writes actor, animation, RNG or save state.
 */
const ui=id=>document.getElementById(id),canvas=ui('canvas'),journalKey='decompgames.vector-duel.foundry-v1.round-journal';
const blank=()=>({version:1,practiceWins:0,practiceLosses:0,duelWins:0,duelLosses:0,draws:0});
const fields=Object.keys(blank()).filter(k=>k!=='version');let journal=blank(),runtimeInitialized=false,active=false,failed=false,finished=false,lastRound=0,roundMode=false,credited=false,armed=false,paused=false;
try{const raw=localStorage.getItem(journalKey);if(raw){const p=JSON.parse(raw);if(p.version!==1||fields.some(k=>!Number.isSafeInteger(p[k])||p[k]<0||p[k]>1000000))throw Error('Invalid journal');journal=Object.fromEntries(Object.keys(blank()).map(k=>[k,p[k]]));}}catch{journal=blank();}
function renderJournal(){ui('journal').textContent=`Practice ${journal.practiceWins}W / ${journal.practiceLosses}L · Duel ${journal.duelWins}W / ${journal.duelLosses}L · Draws ${journal.draws}`;}
function saveJournal(){try{localStorage.setItem(journalKey,JSON.stringify(journal));}catch{ui('storage').textContent='Browser storage is unavailable. Completed-round totals last for this visit only.';}renderJournal();}
function setPause(value){if(!active||finished)return;paused=!!value;Module._vector_duel_pause(paused?1:0);ui('pause').textContent=paused?'Resume':'Pause';document.body.dataset.state=paused?'paused':'ready';}
function focusArena(){if(active&&!finished){canvas.focus();setPause(false);}}
window.probeMessages=[];
window.vectorDuelLoadFailed=message=>{if(finished||failed)return;failed=true;active=false;document.body.dataset.state='failed';ui('status').textContent=message+' Reload to retry.';for(const k of ['pause','retry','mode','stop'])ui(k).disabled=true;ui('reload').hidden=false;};
window.addEventListener('unhandledrejection',()=>{if(!active&&!finished)vectorDuelLoadFailed('An arena resource could not be loaded.');});
Module={canvas,print:t=>{const message=String(t);probeMessages.push(message);if(/^(SDL could not initialize|Window could not be created|Could not create OpenGL context|Could not make OpenGL context current|Failed to initialize game)/.test(message))vectorDuelLoadFailed('The arena could not start.');},printErr:t=>probeMessages.push('stderr: '+t),onAbort:()=>vectorDuelLoadFailed('The arena could not start.'),onExit:code=>{if(code&&!finished)vectorDuelLoadFailed('The native player exited before it was ready.');},onRuntimeInitialized:()=>{runtimeInitialized=true;}};
renderJournal();
const loadDeadline=setTimeout(()=>{if(!active&&!finished)vectorDuelLoadFailed('Loading took too long.');},30000);
const timer=setInterval(()=>{
 if(failed)return;
 try{
  if(!runtimeInitialized||typeof Module._vector_duel_state!=='function')return;
  const s=JSON.parse(Module.UTF8ToString(Module._vector_duel_state()));window.nativeState=s;
  if(!s.ready)return;
  clearTimeout(loadDeadline);
  if(s.stopped){finished=true;active=false;document.body.dataset.state='stopped';ui('status').textContent='Player stopped. Your completed rounds remain in the journal.';for(const k of ['pause','retry','mode','stop'])ui(k).disabled=true;ui('reload').hidden=false;clearInterval(timer);return;}
  if(!active){active=true;for(const k of ['pause','retry','mode','stop'])ui(k).disabled=false;document.body.dataset.state='ready';}
  const [green,gold]=s.players;ui('health').textContent=`Green ${Math.max(0,green.hp)} · Gold ${Math.max(0,gold.hp)}`;ui('mode').textContent=s.offensive?'Opponent: duel':'Opponent: practice';
  if(s.round!==lastRound){lastRound=s.round;roundMode=s.offensive;credited=false;armed=green.hp>0&&gold.hp>0;}
  if(s.offensive!==roundMode)armed=false; // Mode changes abandon this round; next native reset arms it.
  let result='';
  if(green.hp<=0||gold.hp<=0){result=green.hp<=0&&gold.hp<=0?'Draw.':green.hp<=0?'Gold wins.':'Green wins.';if(armed&&!credited){credited=true;const key=green.hp<=0&&gold.hp<=0?'draws':(roundMode?'duel':'practice')+(green.hp<=0?'Losses':'Wins');journal[key]=Math.min(1000000,journal[key]+1);saveJournal();}}
  ui('status').textContent=paused?'Paused. Resume or click the arena to continue.':result?result+' Choose New round to continue.':s.offensive?'Duel round: the gold robot attacks.':'Practice round: approach the gold robot and strike.';
 }catch(e){vectorDuelLoadFailed('The native player could not be read.');probeMessages.push(e.message);}
},100);
ui('pause').onclick=()=>{const resume=paused;setPause(!paused);if(resume)canvas.focus();};
ui('retry').onclick=()=>{if(active&&!finished){Module._vector_duel_action(0);focusArena();}};
ui('mode').onclick=()=>{if(active&&!finished){Module._vector_duel_action(1);Module._vector_duel_action(0);focusArena();}};
ui('stop').onclick=()=>{if(active&&!finished)Module._vector_duel_request_stop();};
ui('reload').onclick=()=>location.reload();canvas.addEventListener('click',focusArena);
canvas.addEventListener('blur',()=>setPause(true));window.addEventListener('blur',()=>setPause(true));document.addEventListener('visibilitychange',()=>{if(document.hidden)setPause(true);});
window.addEventListener('pagehide',()=>{if(active&&!finished){Module._vector_duel_pause(1);Module._vector_duel_request_stop();}});

})();

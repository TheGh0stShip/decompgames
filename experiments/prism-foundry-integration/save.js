// SPDX-License-Identifier: MIT
// Only authored campaign progress belongs in this storage key.
(()=>{
  const revision='c418e6a2e9adb88d06061b76e7030a5dea516eb9042bcc99578532330eacc356';
  const key='decompgames.prism-foundry.progress.v1';
  const fields=['checkpoint','complete','course','prisms','revision','v'];
  function valid(r){
    return r!==null&&typeof r==='object'&&!Array.isArray(r)&&Object.keys(r).sort().join(',')===fields.join(',')&&r.v===1&&r.revision===revision&&Number.isInteger(r.course)&&r.course>=0&&r.course<=2&&Number.isInteger(r.prisms)&&r.prisms>=0&&r.prisms<=7&&typeof r.checkpoint==='boolean'&&typeof r.complete==='boolean'&&(!r.complete||(r.course===2&&r.prisms===7&&r.checkpoint));
  }
  function parse(text){if(typeof text!=='string'||text.length>1024)return null;try{const r=JSON.parse(text);return valid(r)?r:null;}catch{return null;}}
  function fromState(s){if(!s?.loaded||s.running!==1)return null;const r={v:1,revision,course:s.course,prisms:s.prismMask,checkpoint:s.checkpointActive===1,complete:s.complete===1};return valid(r)?r:null;}
  globalThis.FoundrySave=Object.freeze({key,revision,valid,parse,fromState});
})();

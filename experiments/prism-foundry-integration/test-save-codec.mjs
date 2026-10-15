// SPDX-License-Identifier: MIT
import assert from 'node:assert/strict';
import './save.js';
const codec=globalThis.FoundrySave;
let accepted=0,rejected=0;
for(let course=0;course<3;course++)for(let prisms=0;prisms<8;prisms++)for(const checkpoint of [false,true]){
  const r={v:1,revision:codec.revision,course,prisms,checkpoint,complete:false};
  assert.deepEqual(codec.parse(JSON.stringify(r)),r);accepted++;
}
const complete={v:1,revision:codec.revision,course:2,prisms:7,checkpoint:true,complete:true};
assert.deepEqual(codec.parse(JSON.stringify(complete)),complete);accepted++;
const invalid=[null,'', 'x', 'null','[]','0','"save"',' '.repeat(1025)];
for(const patch of [{v:2},{revision:'different'},{course:-1},{course:3},{course:0.5},{course:'2'},{prisms:-1},{prisms:8},{prisms:1.5},{checkpoint:1},{complete:1},{course:1},{prisms:3},{checkpoint:false},{extra:true}])invalid.push(JSON.stringify({...complete,...patch}));
for(const text of invalid){assert.equal(codec.parse(text),null);rejected++;}
assert.equal(codec.fromState({loaded:1,running:0,course:0,prismMask:0,checkpointActive:0,complete:0}),null);
assert.equal(codec.fromState({loaded:0,running:1,course:0,prismMask:0,checkpointActive:0,complete:0}),null);
assert.equal(codec.fromState({loaded:1,running:1,course:0,prismMask:8,checkpointActive:0,complete:0}),null);
const state={loaded:1,running:1,course:0,prismMask:3,checkpointActive:1,complete:0};
assert.deepEqual(codec.fromState(state),{v:1,revision:codec.revision,course:0,prisms:3,checkpoint:true,complete:false});
console.log(JSON.stringify({acceptedRecords:accepted,rejectedRecords:rejected,invalidSnapshotCases:3,liveSnapshotRoundTrip:true}));

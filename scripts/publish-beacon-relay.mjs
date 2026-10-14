// Copyright 2026 DecompGames contributors. SPDX-License-Identifier: MIT.
// Upload only this audited, hash-verified edition; never scan original data directories.
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import path from 'node:path';
const exec=promisify(execFile),root=path.resolve('public');
const m=JSON.parse(await readFile('public/manifests/beacon-relay.json','utf8'));
if(m.id!=='beacon-relay'||m.base!=='/runtime/beacon-relay/classic-relay-v1/')throw Error('Unexpected edition');
const files=[...m.files.map(f=>({...f,url:m.base+f.path})),{url:m.sourceArchive,bytes:m.sourceArchiveBytes,sha256:m.sourceArchiveSha256}];
const types={wasm:'application/wasm',html:'text/html; charset=utf-8',js:'text/javascript; charset=utf-8',json:'application/json',txt:'text/plain; charset=utf-8',md:'text/plain; charset=utf-8',zip:'application/zip'};
for(const f of files){
 const p=path.resolve(root,'.'+f.url);if(!p.startsWith(root+path.sep))throw Error('Path escaped public root');
 const bytes=await readFile(p);if(bytes.length!==f.bytes||createHash('sha256').update(bytes).digest('hex')!==f.sha256)throw Error('Distribution mismatch: '+f.url);
}
await mkdir('.cache',{recursive:true});
const report={date:new Date().toISOString(),scope:'Beacon Relay manifest files and corresponding source only',uploaded:[],failures:[]};
let index=0;
await Promise.all(Array.from({length:3},async()=>{
 while(index<files.length){const f=files[index++];try{
  await exec(process.execPath,['node_modules/wrangler/bin/wrangler.js','r2','object','put','decompgames-assets'+f.url,'--file','public'+f.url,'--content-type',types[f.url.split('.').pop().toLowerCase()]||'application/octet-stream','--remote','--force'],{maxBuffer:1048576});
  report.uploaded.push({path:f.url,sha256:f.sha256,bytes:f.bytes});console.log('Uploaded '+f.url);
 }catch(e){report.failures.push({path:f.url,message:e.message});}}
}));
await writeFile('.cache/beacon-relay-upload.json',JSON.stringify(report,null,2)+'\n');
if(report.failures.length)throw Error(`${report.failures.length} scoped uploads failed; see .cache/beacon-relay-upload.json`);
console.log(`Uploaded all ${report.uploaded.length} audited files.`);

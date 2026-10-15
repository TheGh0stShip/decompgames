#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Relink an already verified private candidate with a linker map and input trace."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--em-config',type=Path,required=True)
a=p.parse_args();build=a.build.resolve();out=a.output.resolve()
def u32(data,offset):
    value=0;shift=0
    while True:
        byte=data[offset];offset+=1;value|=(byte&127)<<shift
        if byte<128:return value,offset
        shift+=7
def parts(data):
    assert data[:8]==b'\0asm\x01\0\0\0'
    offset=8;sections=[];moduleNames=[]
    while offset<len(data):
        section=data[offset];size,body=u32(data,offset+1);payload=data[body:body+size];offset=body+size
        if section==0:
            n,start=u32(payload,0);name=payload[start:start+n]
            if name==b'name':
                current=start+n;subsections=[]
                while current<len(payload):
                    kind=payload[current];length,begin=u32(payload,current+1);value=payload[begin:begin+length];current=begin+length
                    if kind==0:
                        count,pos=u32(value,0);moduleNames.append(value[pos:pos+count].decode('utf-8'))
                    else:subsections.append((kind,value))
                sections.append((section,name,subsections));continue
        sections.append((section,payload))
    return sections,moduleNames
if out.exists():raise SystemExit('Choose a new audit directory.')
r=json.loads((build/'result.json').read_text(encoding='utf-8'))
for f in r['outputs']:
    data=(build/f['path']).read_bytes();assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
command=r['link']['command'].copy();index=command.index('-o')+1
out.mkdir(parents=True);command[index]=str(out/'audit.js');command+=['-Wl,--trace','-Wl,-Map='+str(out/'link.map')]
result=subprocess.run(command,env=dict(os.environ,EM_CONFIG=str(a.em_config.resolve())),capture_output=True,text=True)
(out/'link-trace.log').write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
assert result.returncode==0
files=[];archives={};unhashed=[]
for line in result.stdout.splitlines():
    line=line.strip();archive,sep,member=line.partition('(')
    path=Path(archive if sep else line)
    if path.is_file():
        key=str(path.resolve())
        if key not in {r['path'] for r in files}:
            data=path.read_bytes();files.append({'path':key,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        if sep:archives.setdefault(key,[]).append(member.rstrip(')'))
    elif line:unhashed.append({'name':path.name,'reason':'Trace input no longer exists after link cleanup; no file hash recorded'})
wasm=(out/'audit.wasm').read_bytes();original=next(f for f in r['outputs'] if f['path']=='foundry.wasm')
originalParts,originalNames=parts((build/'foundry.wasm').read_bytes());auditParts,auditNames=parts(wasm)
receipt={'scope':'Link-input/archive trace and map; no game execution or complete dependency license clearance','linkExitCode':0,'command':command,'files':files,'archives':archives,'unhashedTraceInputs':unhashed,'traceRecordCount':len(result.stdout.splitlines()),'wasmBytes':len(wasm),'wasmSha256':hashlib.sha256(wasm).hexdigest(),'wasmMatchesCandidate':hashlib.sha256(wasm).hexdigest()==original['sha256'],'wasmMatchesExceptModuleNameSubsection':originalParts==auditParts,'moduleNames':{'candidate':originalNames,'audit':auditNames},'gameStarted':False}
(out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'link':0,'inputFiles':len(files),'archives':len(archives),'wasmMatchesCandidate':receipt['wasmMatchesCandidate'],'matchesExceptModuleName':receipt['wasmMatchesExceptModuleNameSubsection'],'gameStarted':False}))

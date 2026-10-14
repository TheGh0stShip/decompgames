#!/usr/bin/env python3
"""Package only the hash-verified Beacon Relay candidate and corresponding source."""
from pathlib import Path
import argparse,json,hashlib,shutil,zipfile
def sha(b):return hashlib.sha256(b).hexdigest()
args=argparse.ArgumentParser();args.add_argument('--build',type=Path,required=True);opts=args.parse_args();build=opts.build.resolve();repo=Path.cwd();edition='classic-relay-v1';base='/runtime/beacon-relay/'+edition+'/'
record=json.loads((build/'files.json').read_text());files=record['files']
if len(files)!=51:raise ValueError('Unexpected candidate file count')
for f in files:
 p=(build/'site'/f['path']).resolve()
 if (build/'site').resolve() not in p.parents or sha(p.read_bytes())!=f['sha256'] or p.stat().st_size!=f['bytes']:raise ValueError('Candidate mismatch '+f['path'])
dest=repo/'public/runtime/beacon-relay'/edition;dest.mkdir(parents=True,exist_ok=True)
for f in files:p=dest/f['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(build/'site'/f['path'],p)
source=repo/'public/sources/beacon-relay-classic-relay-v1-source.zip';source.parent.mkdir(exist_ok=True)
entries={}
for p in (repo/'experiments/beacon-relay').rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:entries['beacon-relay/'+p.relative_to(repo/'experiments/beacon-relay').as_posix()]=p.read_bytes()
entries['beacon-relay/patched-source/Classic.cs']=(build/'src/Classic.cs').read_bytes()
for n in ['beacon-relay-runtime-source-review-2026-10-14.json','beacon-relay-runtime-review-2026-10-14.md']:entries['beacon-relay/review/'+n]=(repo/'docs'/n).read_bytes()
entries['beacon-relay/distribution-files.json']=json.dumps(record,indent=2).encode()
with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,b in sorted(entries.items()):info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
m={'id':'beacon-relay','base':base,'repository':'https://github.com/NoelFB/Celeste','sourceRevision':'1b0ce45c75e05649ae91b44a8bb6b196684e4352','packageRevision':edition,'classification':'Developer-released source port with three independently authored courses; managed IL inside Mono WASM, not decompilation, ROM emulation or commercial campaign','toolchain':'.NET SDK9.0.318 / Mono browser-WASM9.0.20; independently authored Canvas2D host','sourceArchive':'/sources/'+source.name,'sourceArchiveSha256':sha(source.read_bytes()),'sourceArchiveBytes':source.stat().st_size,'requirements':['Keyboard','Modern browser WebAssembly/BigInt/SIMD','Canvas2D','No ROM or original game media'],'files':files,'nativeRuntimeRebuilt':False,'compilerStampLimit':'See runtime review for recipe fork versus fixed base revision stamp; framework binary reused from signed package','cleanRoomCertified':False}
(repo/'public/manifests/beacon-relay.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');(repo/'provenance/beacon-relay.json').write_text((repo/'experiments/beacon-relay/provenance.json').read_text(),encoding='utf-8')
print(json.dumps({'runtimeFiles':len(files),'runtimeBytes':sum(f['bytes'] for f in files),'sourceEntries':len(entries),'sourceArchiveBytes':source.stat().st_size,'sourceArchiveSha256':m['sourceArchiveSha256']}))

#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check an authored pack and run upstream content functions in a Node-only harness."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

parser=argparse.ArgumentParser(description=__doc__)
for name in ['pack','build','output','emscripten','em-config','node']:parser.add_argument('--'+name,type=Path,required=True)
args=parser.parse_args();here=Path(__file__).resolve().parent;out=args.output.resolve()
if out.exists():raise SystemExit('Choose a new output directory.')
pack=args.pack.resolve();build=args.build.resolve();source=build/'source'
manifest=json.loads((pack/'provenance.json').read_text())
assert manifest['license']=='CC0-1.0' and not manifest['runtimeIntegrated']
assert manifest['generatorSha256']==hashlib.sha256((here/'generate.py').read_bytes()).hexdigest()
listed={f['path'] for f in manifest['files']}
assert {p.name for p in pack.iterdir()}==listed|{'provenance.json'}
for f in manifest['files']:
    path=(pack/f['path']).resolve();assert path.is_relative_to(pack)
    data=path.read_bytes();assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
report=json.loads((build/'result.json').read_text())
assert len(report['units'])==88 and all(u['exitCode']==0 for u in report['units']) and report['link']['exitCode']==0
for f in report['overlays']:
    assert hashlib.sha256((source/f['target']).read_bytes()).hexdigest()==f['sha256']
assert not (source/'Classes/framewrk/ffent.h').exists()
out.mkdir(parents=True)
imageLines=[];mapLines=[];collisionLines=[]
for f in manifest['files']:
    if f['path'].endswith('.pcx'):imageLines.append(f"{f['path']} {f['width']} {f['height']} {f['pixelFnv1a32']} {manifest['paletteFnv1a32']}")
    elif f['role']=='authored 32-pixel tile map':mapLines.append(f"{f['path']} {f['width']} {f['height']} {f['fnv1a32']}")
    elif f['role']=='authored 16-pixel collision grid':collisionLines.append(f"{f['path']} {f['width']} {f['heightWithMargin']-32} {f['fnv1a32']}")
assert len(imageLines)==265 and len(mapLines)==len(collisionLines)==3
for name,lines in [('images',imageLines),('maps',mapLines),('collisions',collisionLines)]:
    (out/('expected-'+name+'.txt')).write_text('\n'.join(lines)+'\n',encoding='ascii',newline='\n')
includes=['-I'+str(p) for p in sorted({p.parent for p in source.rglob('*') if p.suffix in ['.h','.hpp']})]
env=dict(os.environ,EM_CONFIG=str(args.em_config.resolve()))
objects=[build/(u['source'].replace('/','__')+'.o') for u in report['units'] if u['source']!='Platform/App/Main.cpp']
assert len(objects)==87 and all(p.is_file() for p in objects)
command=[sys.executable,str(args.emscripten.resolve()/'em++.py'),'-O0','-std=c++11','-sUSE_SDL=2','-sENVIRONMENT=node','-sSINGLE_FILE=1','-sALLOW_MEMORY_GROWTH=1','-sEXIT_RUNTIME=1','-sASSERTIONS=2','-sERROR_ON_UNDEFINED_SYMBOLS=1',*includes,str(here/'test-native-content.cpp'),*[str(p) for p in objects],'--embed-file',str(pack)+'@/data']
for name in ['images','maps','collisions']:command+=['--embed-file',str(out/('expected-'+name+'.txt'))+'@/expected-'+name+'.txt']
command+=['-o',str(out/'test-native-content.js')]
result=subprocess.run(command,env=env,capture_output=True,text=True)
(out/'compile.log').write_text(result.stdout+result.stderr,encoding='utf-8')
receipt={'scope':'Native content parser/file/collision harness, not game startup or gameplay','packFiles':len(manifest['files']),'packProvenanceSha256':hashlib.sha256((pack/'provenance.json').read_bytes()).hexdigest(),'compileCommand':command,'compileExitCode':result.returncode,'nativeObjects':len(objects),'gameMainExcluded':True,'originalMediaInputs':False,'gameLoopStarted':False,'videoInitialized':False,'audioInitialized':False}
if result.returncode==0:
    run=subprocess.run([str(args.node.resolve()),str(out/'test-native-content.js')],capture_output=True,text=True)
    (out/'run.log').write_text(run.stdout+run.stderr,encoding='utf-8');receipt['runExitCode']=run.returncode
    receipt['runOutput']=run.stdout+run.stderr
    if run.returncode==0:
        actual={}
        for line in run.stdout.splitlines():
            if line.startswith('NATIVE_IMAGE '):
                _,name,pixelHash,paletteHash=line.split()
                assert name not in actual
                actual[name]={'pixelSha256':pixelHash,'paletteSha256':paletteHash}
        expected={f['path']:f for f in manifest['files'] if f['path'].endswith('.pcx')}
        assert set(actual)==set(expected)
        assert all(actual[name]['pixelSha256']==f['pixelSha256'] and actual[name]['paletteSha256']==manifest['paletteSha256'] for name,f in expected.items())
        receipt['nativeImageSha256Comparisons']=actual
        receipt['allNativePixelAndPaletteSha256Match']=True
    data=(out/'test-native-content.js').read_bytes();receipt['testArtifact']={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({key:receipt.get(key) for key in ['packFiles','nativeObjects','compileExitCode','runExitCode','gameLoopStarted']}))
sys.exit(0 if result.returncode==0 and receipt.get('runExitCode')==0 else 1)

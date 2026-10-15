#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Test two authored integration adapters against pinned native objects; never start a game."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

parser=argparse.ArgumentParser(description=__doc__)
for name in ['base-build','pack','output','emscripten','em-config','node']:parser.add_argument('--'+name,type=Path,required=True)
args=parser.parse_args();here=Path(__file__).resolve().parent;repo=here.parent.parent
base=args.base_build.resolve();source=base/'source';pack=args.pack.resolve();out=args.output.resolve()
if out.exists():raise SystemExit('Choose a new output directory.')
reference=json.loads((repo/'docs/prism-foundry-content-2026-10-15.json').read_text())
baseReport=json.loads((base/'result.json').read_text())
assert len(baseReport['units'])==88 and baseReport['link']['exitCode']==0
records=json.loads((repo/'experiments/moon-child-source-probe/source-inputs.json').read_text())['files']
overrides={r['target']:r for r in baseReport['overlays']}
for r in records:
    if r['path']=='Classes/framewrk/ffent.h':assert not (source/r['path']).exists();continue
    expected=overrides.get(r['path'],r)
    assert hashlib.sha256((source/r['path']).read_bytes()).hexdigest()==expected['sha256'],r['path']
assert hashlib.sha256((source/'Platform/App/NullAudio.h').read_bytes()).hexdigest()==overrides['Platform/App/NullAudio.h']['sha256']
manifest=json.loads((pack/'provenance.json').read_text())
assert hashlib.sha256((pack/'provenance.json').read_bytes()).hexdigest()==reference['pack']['manifestSha256']
for r in manifest['files']:
    path=(pack/r['path']).resolve();assert path.is_relative_to(pack)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
replaced={'Classes/moonchild/anim.cpp','Classes/moonchild/asset.cpp'}
objects=[];objectRecords=[]
for r in reference['nativeVerification']['linkedAdaptedObjects']:
    if r['source'] in replaced:continue
    path=base/(r['source'].replace('/','__')+'.o');data=path.read_bytes()
    assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],r['source']
    objects.append(path);objectRecords.append(r)
assert len(objects)==85
out.mkdir(parents=True)
generated=out/'FoundryCourseData.h'
subprocess.run([sys.executable,str(here/'make-levels.py'),'--pack',str(pack),'--output',str(generated)],check=True)
includes=['-I'+str(out)]+[argument for p in sorted({p.parent for p in source.rglob('*') if p.suffix in ['.h','.hpp']}) for argument in ['-isystem',str(p)]]
env=dict(os.environ,EM_CONFIG=str(args.em_config.resolve()))
common=['-O0','-std=c++11','-sUSE_SDL=2','-UNDEBUG',*includes]
receipt={'scope':'Native animation/descriptor adapter bounds tests; no game integration, startup or gameplay','checkedBaseInputRecords':len(records),'unchangedLinkedObjects':objectRecords,'packManifestSha256':reference['pack']['manifestSha256'],'safeHeapScope':'SAFE_HEAP enabled at final link; retained native objects reused, not independently rebuilt here','newSources':[],'gameLoopStarted':False,'videoInitialized':False,'audioInitialized':False}
data=generated.read_bytes();receipt['generatedCourseData']={'path':generated.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'sourceCampaignSha256':next(r['sha256'] for r in manifest['files'] if r['path']=='campaign.json')}
for name in ['animation.cpp','assets.cpp','FoundryLevels.cpp','test-animation-bounds.cpp']:
    path=here/name;data=path.read_bytes();obj=out/(name+'.o')
    command=[sys.executable,str(args.emscripten.resolve()/'em++.py'),*common,'-Wall','-Wextra','-Werror','-c',str(path),'-o',str(obj)]
    result=subprocess.run(command,env=env,capture_output=True,text=True)
    (out/(name+'.log')).write_text(result.stdout+result.stderr,encoding='utf-8')
    receipt['newSources'].append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'exitCode':result.returncode,'command':command})
    if result.returncode:break
    objects.append(obj)
if len(receipt['newSources'])==4 and all(r['exitCode']==0 for r in receipt['newSources']):
    command=[sys.executable,str(args.emscripten.resolve()/'em++.py'),*[str(p) for p in objects],'-O0','-sUSE_SDL=2','-sENVIRONMENT=node','-sSINGLE_FILE=1','-sALLOW_MEMORY_GROWTH=1','-sEXIT_RUNTIME=1','-sASSERTIONS=2','-sSAFE_HEAP=1','-sERROR_ON_UNDEFINED_SYMBOLS=1','--embed-file',str(pack)+'@/data','-o',str(out/'test-animation-bounds.js')]
    result=subprocess.run(command,env=env,capture_output=True,text=True)
    (out/'link.log').write_text(result.stdout+result.stderr,encoding='utf-8');receipt['linkExitCode']=result.returncode
    if result.returncode==0:
        run=subprocess.run([str(args.node.resolve()),str(out/'test-animation-bounds.js')],capture_output=True,text=True)
        (out/'run.log').write_text(run.stdout+run.stderr,encoding='utf-8')
        receipt['runExitCode']=run.returncode;receipt['runOutput']=run.stdout+run.stderr
        data=(out/'test-animation-bounds.js').read_bytes();receipt['testArtifact']={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    if receipt.get('runExitCode')==0:
        # Replay the committed native-content harness with only the two adapters changed.
        contentHarness=repo/'experiments/prism-foundry-content/test-native-content.cpp'
        record=next(r for r in reference['reproduction']['fileRecords'] if r['path']=='experiments/prism-foundry-content/test-native-content.cpp')
        assert hashlib.sha256(contentHarness.read_bytes()).hexdigest()==record['sha256']
        lists={'images':[],'maps':[],'collisions':[]}
        for item in manifest['files']:
            if item['path'].endswith('.pcx'):lists['images'].append(f"{item['path']} {item['width']} {item['height']} {item['pixelFnv1a32']} {manifest['paletteFnv1a32']}")
            elif item['role']=='authored 32-pixel tile map':lists['maps'].append(f"{item['path']} {item['width']} {item['height']} {item['fnv1a32']}")
            elif item['role']=='authored 16-pixel collision grid':lists['collisions'].append(f"{item['path']} {item['width']} {item['heightWithMargin']-32} {item['fnv1a32']}")
        command=[sys.executable,str(args.emscripten.resolve()/'em++.py'),*common,'-Wall','-Wextra','-Werror',str(contentHarness),*[str(p) for p in objects[:-1]],'-sENVIRONMENT=node','-sSINGLE_FILE=1','-sALLOW_MEMORY_GROWTH=1','-sEXIT_RUNTIME=1','-sASSERTIONS=2','-sSAFE_HEAP=1','-sERROR_ON_UNDEFINED_SYMBOLS=1','--embed-file',str(pack)+'@/data']
        for name,lines in lists.items():
            path=out/('expected-'+name+'.txt');path.write_text('\n'.join(lines)+'\n',encoding='ascii',newline='\n')
            command+=['--embed-file',str(path)+'@/expected-'+name+'.txt']
        command+=['-o',str(out/'test-native-content.js')]
        compileResult=subprocess.run(command,env=env,capture_output=True,text=True)
        (out/'content-compile.log').write_text(compileResult.stdout+compileResult.stderr,encoding='utf-8')
        receipt['contentReplay']={'harnessSha256':record['sha256'],'compileExitCode':compileResult.returncode}
        if compileResult.returncode==0:
            run=subprocess.run([str(args.node.resolve()),str(out/'test-native-content.js')],capture_output=True,text=True)
            (out/'content-run.log').write_text(run.stdout+run.stderr,encoding='utf-8')
            receipt['contentReplay']['runExitCode']=run.returncode
            if run.returncode==0:
                hashes={}
                for line in run.stdout.splitlines():
                    if line.startswith('NATIVE_IMAGE '):
                        _,name,pixelHash,paletteHash=line.split();assert name not in hashes
                        hashes[name]={'pixelSha256':pixelHash,'paletteSha256':paletteHash}
                expected={item['path']:item for item in manifest['files'] if item['path'].endswith('.pcx')}
                assert set(hashes)==set(expected)
                assert all(hashes[name]['pixelSha256']==item['pixelSha256'] and hashes[name]['paletteSha256']==manifest['paletteSha256'] for name,item in expected.items())
                receipt['contentReplay']['allNativePixelAndPaletteSha256Match']=True
                receipt['contentReplay']['nativeImagesCompared']=len(hashes)
                receipt['contentReplay']['summary']=next(line for line in run.stdout.splitlines() if line.startswith('PASS:'))
                data=(out/'test-native-content.js').read_bytes();receipt['contentReplay']['testArtifact']={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'newUnits':len(receipt['newSources']),'newCompileExitCodes':[r['exitCode'] for r in receipt['newSources']],'link':receipt.get('linkExitCode'),'run':receipt.get('runExitCode'),'contentReplay':receipt.get('contentReplay',{}).get('runExitCode'),'gameStarted':False}))
sys.exit(0 if receipt.get('runExitCode')==0 and receipt.get('contentReplay',{}).get('allNativePixelAndPaletteSha256Match') else 1)

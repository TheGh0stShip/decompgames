#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Map traced SDK members to source; preserve exact local files and primary matches.

This does not rebuild SDK archives, capture transitive headers or certify licenses.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--sdk',required=True,type=Path)
p.add_argument('--output',required=True,type=Path)
p.add_argument('--verify-primary',action='store_true')
a=p.parse_args();sdk=a.sdk.resolve();out=a.output.resolve()
repo=Path(__file__).resolve().parents[2]
reference=json.loads((repo/'docs/prism-foundry-roots-runtime-2026-10-15.json').read_text(encoding='utf-8'))
if out.exists():raise SystemExit('Choose a new output directory.')
out.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
norm=lambda b:b.replace(b'\r\n',b'\n')
paths=[Path(s) for s in subprocess.check_output(['rg','--files',str(sdk/'system/lib'),str(sdk/'cache/ports/sdl2')],text=True).splitlines()]
paths=[p for p in paths if p.suffix in ['.c','.cpp','.S','.s']]
explicit={
 'SDL_sysjoystick':'cache/ports/sdl2/SDL-release-2.32.10/src/joystick/emscripten/SDL_sysjoystick.c',
 'SDL_systimer':'cache/ports/sdl2/SDL-release-2.32.10/src/timer/unix/SDL_systimer.c',
 'SDL_sysloadso':'cache/ports/sdl2/SDL-release-2.32.10/src/loadso/dlopen/SDL_sysloadso.c',
 **{name:'cache/ports/sdl2/SDL-release-2.32.10/src/thread/generic/'+name+'.c' for name in ['SDL_sysmutex','SDL_syssem','SDL_systhread','SDL_systls']},
 **{name:'system/lib/libc/'+name+'.c' for name in ['raise','pthread_sigmask','sigaction','sbrk']}
}
records=[]
for archive in reference['linkAudit']['archives']:
    name=Path(archive['path']).name
    if name=='libSDL2.a':roots=['cache/ports/sdl2/SDL-release-2.32.10/src/']
    elif name.startswith('libc++abi'):roots=['system/lib/libcxxabi/src/']
    elif name.startswith('libc++'):roots=['system/lib/libcxx/src/']
    elif name.startswith('libclang'):roots=['system/lib/compiler-rt/']
    else:roots=['system/lib/libc/','system/lib/gl/','system/lib/html5/','system/lib/pthread/','system/lib/dlmalloc.c']
    for member in archive['members']:
        stem=member.removesuffix('.o')
        if Path(stem).suffix in ['.c','.cpp','.S','.s']:stem=Path(stem).stem
        if stem in explicit:
            source=sdk/explicit[stem];basis='Explicit backend/override in tools/ports/sdl2.py or tools/system_libs.py; single-threaded browser candidate'
        else:
            matches=[path for path in paths if path.stem==stem and any(path.relative_to(sdk).as_posix().startswith(root) for root in roots)]
            assert len(matches)==1,(name,member,matches)
            source=matches[0];basis='Unique translation-unit basename within the component source root, consistent with installed SDK build recipe'
        data=source.read_bytes();relative=source.relative_to(sdk).as_posix()
        if relative.startswith('cache/ports/sdl2/SDL-release-2.32.10/'):
            url='https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/'+relative.split('SDL-release-2.32.10/',1)[1]
        else:url='https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/'+relative
        destination=out/'source'/relative;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
        records.append({'archive':name,'member':member,'source':relative,'bytes':len(data),'sha256':sha(data),'mappingBasis':basis,'url':url})
assert len(records)==380 and len({r['source'] for r in records})==380

def verify(record):
    try:
        with urllib.request.urlopen(record['url'],timeout=45) as response:data=response.read()
        local=(sdk/record['source']).read_bytes()
        record.update({'primaryBytes':len(data),'primarySha256':sha(data),'primaryMatchesLocalAfterNewlineNormalization':norm(data)==norm(local)})
    except Exception as error:record['primaryVerificationError']=str(error)
    return record
if a.verify_primary:
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(verify,records))
recipes=[]
for relative in ['tools/system_libs.py','tools/ports/sdl2.py']:
    data=(sdk/relative).read_bytes();target=out/'source'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    recipes.append({'source':relative,'bytes':len(data),'sha256':sha(data)})
bundle=out/'selected-sdk-translation-units.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED) as z:
    for path in sorted((out/'source').rglob('*')):
        if path.is_file():z.write(path,path.relative_to(out/'source').as_posix())
data=bundle.read_bytes()
report={'scope':'Source mapping and byte capture for 380 traced SDK archive member records; not a rebuild, transitive-header capture or complete permission review','sourceRevision':'Emscripten 6.0.10; SDL2 release-2.32.10','records':records,'buildRecipes':recipes,'bundle':{'name':bundle.name,'files':len(records)+len(recipes),'bytes':len(data),'sha256':sha(data),'uploaded':False},'verifiedPrimaryMatches':sum(r.get('primaryMatchesLocalAfterNewlineNormalization') is True for r in records),'mismatches':[r['source'] for r in records if r.get('primaryMatchesLocalAfterNewlineNormalization') is False],'fetchErrors':[r['source'] for r in records if 'primaryVerificationError' in r],'gameStarted':False,'archivesRebuilt':False,'transitiveHeadersCaptured':False,'licenseClearanceComplete':False}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['records','buildRecipes']}))

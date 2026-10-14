"""Prepare a private source-only archive; no runtime or automatic upload."""
import pathlib,json,hashlib,zipfile,shutil,os
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('D:/n64work/rogue-intake-2026-10-14')
OUT=pathlib.Path(os.environ.get('ROGUE_PACKAGE',str(ROOT/'source-package-v3')));OUT.mkdir(exist_ok=True)
package=OUT/'source';assert not package.exists(),'Use a new private package version'
package.mkdir()
source=json.loads((ROOT/'snapshot.json').read_text())
for f in source['records']:
    path=ROOT/'source'/f['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256']
    dest=package/'reference/source'/f['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
shutil.copy2(ROOT/'snapshot.json',package/'reference/snapshot.json')
adapter_names=['LICENSE','REFERENCE-SOURCE-LICENSE.txt','CONTENT-CC0.txt','build-probe.py','build-survey.py','author-text.py','audit-text.py','survey-world.c','curses.h','config.h','terminal.c','platform.c','observe.c','probe.html','probe.js','survey.html','font-renderer.js','glyphs.json','font-provenance.json','survey-content.json','survey-names.json','survey-messages.json','survey-literal-contracts.json','validate-save.js','trace-emitted-js.cjs','loader.js','provenance.json']
for name in adapter_names:
    dest=package/'adapter'/name;dest.parent.mkdir(exist_ok=True);shutil.copy2(HERE/name,dest)
shutil.copy2(HERE/'build-source.py',package/'build-source.py')
for path in (HERE/'sdk-notices').iterdir():
    dest=package/'sdk-notices'/path.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest)
(package/'README.md').write_text('''# Signal Survey source-only private candidate

A Rogue developer-source port with an independently authored three-station campaign.
Reference game/save code is BSD-licensed; own adapters are MIT; authored content is
CC0. Standard-library/compiler/JS notices are in sdk-notices. No claim of matching
decompilation, clean-room isolation or whole-game MIT licensing is made.

The reference directory contains the 48 pinned licensed text files, including
historical source prose and procedural generation for audit/rebuild context. The
build replaces selected presentation tables, messages and complete level/end panels.
Original PNG/media, retail executables, ROMs and prebuilt game objects are excluded.

Supply Emscripten 6.0.10 externally, then run:

    python build-source.py --emscripten-dir PATH --em-config CONFIG --out FRESH_DIRECTORY

The input manifest is verified before compilation; expected WASM bytes must match.
Serve the generated directory over localhost HTTP. Sound is unavailable. This
private candidate has not passed site integration or production acceptance.
''')
inputs=[{'path':p.relative_to(package).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(package.rglob('*')) if p.is_file()]
build=pathlib.Path(os.environ.get('ROGUE_BUILD',str(ROOT/'survey-loader-v10')))
manifest={'schema':1,'referenceRepository':source['repository'],'referencePin':source['pin'],'expectedWasmSha256':hashlib.sha256((build/'game.wasm').read_bytes()).hexdigest(),'inputs':inputs,'sourceOnly':True,'originalMedia':False,'prebuiltGameObjects':False}
(package/'build-inputs.json').write_text(json.dumps(manifest,indent=2)+'\n')
archive=OUT/'signal-survey-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(package.rglob('*')):
        if p.is_file():
            assert p.suffix not in ['.wasm','.o','.a','.png','.wav','.mp3','.exe','.rom','.z64','.n64']
            info=zipfile.ZipInfo(p.relative_to(package).as_posix(),(2026,10,14,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
receipt={'sourceArchive':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'files':len(inputs)+1,'privateOnly':True,'uploaded':False}
(OUT/'package-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))

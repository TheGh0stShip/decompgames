"""MIT: package only the audited Foundry Deck source port; no upstream media scans."""
from pathlib import Path
import argparse,json,hashlib,shutil,zipfile
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);a=ap.parse_args();build=a.build.resolve();source=a.source;repo=Path.cwd();edition='foundry-v1';base='/runtime/vector-duel/'+edition+'/'
assert json.loads((build/'private-gameplay-journal-report.json').read_text())['status']=='passed'
assert json.loads((build/'private-loading-report.json').read_text())['status']=='passed'
with zipfile.ZipFile(source)as z:
 names=z.namelist();assert len(names)==934 and len(names)==len(set(names));assert not any(n.endswith(('.o','.a','.wasm','.data','.exe'))for n in names)
 spec=json.loads(z.read('vector-duel/build-inputs.json'))
 for f in spec['inputs']:assert hashlib.sha256(z.read('vector-duel/'+f['path'])).hexdigest()==f['sha256']
 assert len(spec['rendererSources'])==69 and len(spec['nativeSources'])==9 and not spec['originalMediaIncluded']
provenance=json.loads((build/'site/asset-provenance.json').read_text());assert provenance['releaseComplete']and len(provenance['files'])==173
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted((build/'site').iterdir())if p.is_file()];assert len(files)==10
dest=repo/'public/runtime/vector-duel'/edition;dest.mkdir(parents=True,exist_ok=True)
for f in files:shutil.copyfile(build/'site'/f['path'],dest/f['path'])
archive=repo/'public/sources/vector-duel-foundry-v1-source.zip';archive.parent.mkdir(exist_ok=True);shutil.copyfile(source,archive)
manifest={'id':'vector-duel','base':base,'repository':'https://github.com/wedaly/GLFighters-SDL','sourceRevision':spec['sourceRevision'],'rendererRevision':spec['rendererRevision'],'packageRevision':edition,'classification':'Developer-released GLFighters source port with independently authored robot arena/content; not decompilation, original campaign, emulation or clean-room certificate','toolchain':'Emscripten6.0.10 / SDL2 2.32.10 / rebuilt gl4es1.1.6; native game and renderer rebuilt from corresponding source; external SDK standard objects','SDKRevision':spec['SDKRevision'],'sourceArchive':'/sources/'+archive.name,'sourceArchiveBytes':archive.stat().st_size,'sourceArchiveSha256':sha(archive),'requirements':['Keyboard','Modern WebAssembly browser with WebGL','No ROM or original media','Silent edition'],'cleanRoomCertified':False,'nativeRendererRebuilt':True,'wholeSDKIndependentlyRebuilt':False,'files':files}
(repo/'public/manifests/vector-duel.json').write_text(json.dumps(manifest,indent=2)+'\n');(repo/'provenance/vector-duel.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'files':len(files),'runtimeBytes':sum(f['bytes']for f in files),'sourceBytes':archive.stat().st_size,'sourceSHA':sha(archive)}))

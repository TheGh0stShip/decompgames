"""MIT: package only the audited native Signal Survey edition and source."""
from pathlib import Path
import argparse,json,hashlib,zipfile,shutil
ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--replay',type=Path,required=True);a=ap.parse_args()
build=a.build.resolve();repo=Path.cwd();here=repo/'experiments/rogue-browser';edition='stations-v1';base='/runtime/signal-survey/'+edition+'/'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads(max(build.glob('survey-result-*.json'),key=lambda p:p.stat().st_mtime).read_text())
assert report['status']=='passed' and report['fullBrowserRestart'] and report['continueSavedButton'] and report['nativeStop']
for name in ['loading-result.json','invalid-checkpoint-result.json','save-validator-result.json']:assert json.loads((build/name).read_text())['status']=='passed'
replay=json.loads((a.replay/'source-replay.json').read_text());assert replay['status']=='passed' and replay['wasmByteIdentical']
provenance=json.loads((here/'provenance.json').read_text());assert provenance['textGate']['unknownReferenceLiterals']==0 and provenance['ownContentLicense']=='CC0-1.0'
with zipfile.ZipFile(a.source) as z:
    names=z.namelist();assert len(names)==len(set(names)) and not any(n.endswith(('.wasm','.o','.a','.exe','.png','.wav','.rom','.z64','.n64'))for n in names)
    spec=json.loads(z.read('build-inputs.json'))
    for f in spec['inputs']:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256']
    assert sha(build/'game.wasm')==spec['expectedWasmSha256']==replay['wasmSha256']
    for name in ['game.js','game.wasm','probe.js','font-renderer.js','loader.js','save-spec.js','validate-save.js','glyphs.js','load-manifest.json']:assert (build/name).read_bytes()==(a.replay/name).read_bytes(),name
notice='Signal Survey / stations-v1\nRogue source port with authored campaign. No decompilation, retail-campaign or clean-room certificate.\n\n'
for path in [here/'REFERENCE-SOURCE-LICENSE.txt',here/'LICENSE',here/'CONTENT-CC0.txt',*sorted((here/'sdk-notices').iterdir())]:notice+='\n===== '+path.name+' =====\n'+path.read_text(encoding='utf-8')+'\n'
dest=repo/'public/runtime/signal-survey'/edition;dest.mkdir(parents=True,exist_ok=True)
runtime_names=['index.html','loader.js','load-manifest.json','game.js','game.wasm','probe.js','font-renderer.js','glyphs.js','save-spec.js','save-spec.json','validate-save.js']
for name in runtime_names:shutil.copy2(build/name,dest/name)
for name in ['provenance.json','glyphs.json','survey-content.json','survey-names.json','survey-messages.json','survey-literal-contracts.json']:shutil.copy2(here/name,dest/name)
(dest/'NOTICE.txt').write_text(notice,encoding='utf-8')
shutil.copy2(build/'sdk-audit.json',dest/'sdk-audit.json')
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(dest.iterdir()) if p.is_file()]
archive=repo/'public/sources/signal-survey-stations-v1-source.zip';archive.parent.mkdir(exist_ok=True);shutil.copy2(a.source,archive)
shutil.copy2(build/'poster.png',repo/'public/images/signal-survey.png')
manifest={'id':'signal-survey','base':base,'repository':provenance['referenceRepository'],'sourceRevision':provenance['referencePin'],'packageRevision':edition,'classification':provenance['classification'],'toolchain':'Emscripten 6.0.10; native Rogue gameplay with own terminal/browser adapter. External SDK managed C/allocator/compiler objects.','SDKRevision':provenance['sdk']['pin'],'sourceArchive':'/sources/'+archive.name,'sourceArchiveBytes':archive.stat().st_size,'sourceArchiveSha256':sha(archive),'requirements':['Keyboard','WebAssembly browser','No ROM or original media','Silent edition'],'cleanRoomCertified':False,'wholeSDKIndependentlyRebuilt':False,'nativeGameRebuilt':True,'files':files}
(repo/'public/manifests/signal-survey.json').write_text(json.dumps(manifest,indent=2)+'\n')
(repo/'provenance/signal-survey.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':sum(f['bytes']for f in files),'sourceBytes':archive.stat().st_size,'sourceSha256':sha(archive)}))

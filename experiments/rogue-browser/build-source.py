"""Portable source-only Signal Survey recipe. MIT, DecompGames contributors.
External Emscripten 6.0.10 supplies its compiler and managed standard libraries.
"""
import argparse,pathlib,json,hashlib,subprocess,sys,os
root=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--emscripten-dir',type=pathlib.Path,required=True)
ap.add_argument('--em-config',type=pathlib.Path,required=True)
ap.add_argument('--out',type=pathlib.Path,required=True)
args=ap.parse_args();sdk=args.emscripten_dir.resolve();out=args.out.resolve()
assert not out.exists(),'Use a fresh output directory'
spec=json.loads((root/'build-inputs.json').read_text())
for f in spec['inputs']:
    path=(root/f['path']).resolve()
    assert path.is_relative_to(root) and path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'],'Changed input: '+f['path']
assert (sdk/'emscripten-version.txt').read_text().strip().strip('"')=='6.0.10','Wrong SDK version'
env=os.environ.copy();env.update({'EM_CONFIG':str(args.em_config.resolve()),'ROGUE_EMSCRIPTEN':str(sdk),'ROGUE_SOURCE_ROOT':str(root/'reference'),'ROGUE_BUILD':str(out),'ROGUE_LINK_AUDIT':'1'})
p=subprocess.run([sys.executable,str(root/'adapter/build-survey.py')],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
out.mkdir(exist_ok=True);(out/'source-replay.log').write_text(p.stdout+p.stderr)
assert p.returncode==0,'Replay failed; see source-replay.log'
wasm=hashlib.sha256((out/'game.wasm').read_bytes()).hexdigest()
assert wasm==spec['expectedWasmSha256'],'WASM differs from audited candidate'
record={'sourceReplay':True,'status':'passed','wasmByteIdentical':True,'wasmSha256':wasm,'verifiedSourceInputs':len(spec['inputs']),'prebuiltGameObjectsUsed':False,'originalMediaUsed':False,'externalSDKVersion':'6.0.10','standardLibraryObjects':'Externally supplied SDK managed objects; not bundled in source archive','textGate':json.loads((out/'text-gate.json').read_text())}
(out/'source-replay.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))

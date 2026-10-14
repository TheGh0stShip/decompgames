"""Private source-only compatibility probe; not a release/distribution recipe."""
import pathlib, subprocess, os, json, hashlib, shutil
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('D:/n64work/rogue-intake-2026-10-14')
SDK=pathlib.Path('D:/n64work/emsdk/upstream/emscripten')
OUT=ROOT/'probe-v1';OUT.mkdir(exist_ok=True)
env=os.environ.copy();env['EM_CONFIG']='D:/n64work/emsdk/.emscripten'
units=[x for x in sorted((ROOT/'source').glob('*.c')) if x.name not in ['mdport.c','xcrypt.c']]+[HERE/'terminal.c',HERE/'platform.c',HERE/'observe.c']
cmd=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe',str(SDK/'emcc.py'),*[str(x) for x in units],'-I'+str(HERE),'-I'+str(ROOT/'source'),'-DHAVE_CONFIG_H','-std=gnu17','-fwrapv','-O1','-sEMULATE_FUNCTION_POINTER_CASTS=1','-sASYNCIFY','-sALLOW_MEMORY_GROWTH','-sEXIT_RUNTIME=1','-sFORCE_FILESYSTEM=1','-sEXPORTED_RUNTIME_METHODS=FS,UTF8ToString','-Werror=implicit-function-declaration','-o',str(OUT/'game.js')]
run_id=len(list(OUT.glob('build-log-*.txt')))+1
p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(OUT/'build.log').write_text(p.stdout,encoding='utf-8')
(OUT/f'build-log-{run_id}.txt').write_text(p.stdout,encoding='utf-8')
(OUT/'build-result.json').write_text(json.dumps({'exitCode':p.returncode,'command':cmd,'sources':[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in units]},indent=2))
for name in ['probe.html','probe.js']:shutil.copy2(HERE/name,OUT/('index.html' if name=='probe.html' else name))
print(p.stdout[-800:] if p.returncode==0 else p.stdout[-16000:]);raise SystemExit(p.returncode)

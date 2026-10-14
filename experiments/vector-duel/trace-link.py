from pathlib import Path
import subprocess,os,json,hashlib
r=Path('C:/Users/andre/AppData/Local/decomp-builds/glfighters-overgrowth-source-only-2026-10-14');o=r/'vector-duel-candidate-v4';c=o/'closure';c.mkdir(exist_ok=True)
env=os.environ.copy();env['EM_CONFIG']='D:/n64work/emsdk/.emscripten';env['VECTOR_DUEL_TRACE_DIR']=str(c);env['NODE_OPTIONS']='--require="'+Path('experiments/vector-duel/trace-emitted-js.cjs').resolve().as_posix()+'"'
cmd=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe','D:/n64work/emsdk/upstream/emscripten/em++.py','-O2',*[str(p)for p in sorted((o/'objects').glob('*.o'))],str(r/'gl4es-apache-platform-v3/libGL.a'),'-sUSE_SDL=2','-sFULL_ES2=1','-sALLOW_MEMORY_GROWTH=1','-sASSERTIONS=1','-sEXPORTED_RUNTIME_METHODS=["UTF8ToString"]','--preload-file',str(r/'vector-duel-authored-pack-v3/data')+'@/data','-o',str(c/'game.js')]
p=subprocess.run(cmd,env=env,capture_output=True,text=True);(c/'link.log').write_text(p.stdout+p.stderr);print(p.returncode);print(p.stderr[-2000:]);assert p.returncode==0
for n in ['game.wasm','game.data']:assert (o/'site'/n).read_bytes()==(c/n).read_bytes()
print('WASM and data byte-identical')

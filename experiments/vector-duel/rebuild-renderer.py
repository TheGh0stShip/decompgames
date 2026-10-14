"""MIT build adapter: use current SDK Apache2 GLES platform declarations in a real gl4es rebuild."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re,subprocess,os,json,hashlib,shutil
r=Path('C:/Users/andre/AppData/Local/decomp-builds/glfighters-overgrowth-source-only-2026-10-14');sdk=Path('D:/n64work/emsdk/upstream/emscripten');out=r/'gl4es-apache-platform-v3';out.mkdir(exist_ok=True);gl=r/'ptitSeb__gl4es';overlay=out/'include/GLES';overlay.mkdir(parents=True,exist_ok=True)
source=sdk/'cache/sysroot/include/GLES/glplatform.h';shutil.copyfile(source,overlay/'glplatform.h')
text=(r/'gl4es-wasm-build-v2/build.ninja').read_text();names=re.findall(r'^build (src/CMakeFiles/GL.dir/[^:]+\.c\.o): C_COMPILER[^ ]+ (C\$:/[^ ]+\.c) ',text,re.M);assert len(names)==69,len(names)
assert len(set(source for _,source in names))==69
assert all(Path(source.replace('C$:','C:')).name+'.o'==Path(obj).name for obj,source in names)
env=os.environ.copy();env['EM_CONFIG']='D:/n64work/emsdk/.emscripten';compiler=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe',str(sdk/'emcc.py')]
flags=['-sFULL_ES2=1','-O3','-DNDEBUG','-std=gnu11','-funwind-tables','-fvisibility=hidden','-Wno-pointer-sign','-Wno-dangling-else']+['-D'+s for s in ['DEFAULT_ES=2','EGL_NO_X11','GLX_STUBS','NOEGL','NOX11','NO_GBM','NO_INIT_CONSTRUCTOR','NO_LOADER','STATICLIB']]+['-I'+str(out/'include'),'-I'+str(gl/'include'),'-I'+str(gl/'src/util'),'-I'+str(gl/'src/glx')]
def compile(item):
 name,original=item;p=Path(original.replace('C$:', 'C:'));obj=out/Path(name).name;cmd=compiler+flags+['-MD','-MF',str(obj)+'.d','-c',str(p),'-o',str(obj)];d=subprocess.run(cmd,env=env,capture_output=True,text=True);(out/(obj.name+'.log')).write_text(d.stdout+d.stderr);assert d.returncode==0,(p,d.stderr[-1500:]);return {'source':p.relative_to(gl).as_posix(),'object':obj.name,'sha256':hashlib.sha256(obj.read_bytes()).hexdigest()}
with ThreadPoolExecutor(max_workers=4)as pool:records=list(pool.map(compile,names))
archive=out/'libGL.a';cmd=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe',str(sdk/'emar.py'),'rcs',str(archive),*[str(out/x['object'])for x in records]];d=subprocess.run(cmd,env=env,capture_output=True,text=True);assert d.returncode==0,d.stderr
report={'rendererSourcePin':'c9895df34cd466c23bc60c2bd3db3d87e98fcbe7','objects':records,'overlay':{'path':'GLES/glplatform.h','origin':'Current Emscripten6.0.10 sysroot Khronos2017 header','license':'Apache-2.0','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'purpose':'Use supported SDK platform declarations rather than separately licensed historical SGI platform header; real GL backend retained'},'archive':{'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},'originalArchiveUntouched':True,'gameplayClaim':False}
(out/'rebuild-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'objects':len(records),'archive':report['archive'],'overlay':report['overlay']}))

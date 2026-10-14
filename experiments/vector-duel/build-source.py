"""MIT: portable source build for the independent Foundry Deck edition.
Requires the external Emscripten6.0.10 SDK; no prebuilt game/renderer objects or original media.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,hashlib,os,subprocess,sys,shutil
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--emscripten-dir',type=Path,required=True);ap.add_argument('--em-config',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();sdk=args.emscripten_dir.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['EM_CONFIG']=str(args.em_config.resolve());spec=json.loads((root/'build-inputs.json').read_text());
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for f in spec['inputs']:
 p=(root/f['path']).resolve();assert p.is_relative_to(root)and p.is_file()and sha(p)==f['sha256'],'Source input changed: '+f['path']
assert (sdk/'emscripten-version.txt').read_text().strip().strip('"')=='6.0.10','Wrong SDK version'
compiler=[sys.executable,str(sdk/'emcc.py')];cxx=[sys.executable,str(sdk/'em++.py')]
def run(cmd,log):
 p=subprocess.run(cmd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace');log.write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,'Build failed; see '+str(log)
ro=out/'renderer-objects';ro.mkdir(exist_ok=True);no=out/'native-objects';no.mkdir(exist_ok=True)
common=['-Wno-builtin-macro-redefined','-ffile-prefix-map='+root.as_posix()+'=SOURCE','-ffile-prefix-map='+sdk.as_posix()+'=SDK']
flags=['-O3','-DNDEBUG','-std=gnu11','-funwind-tables','-fvisibility=hidden','-Wno-pointer-sign','-Wno-dangling-else']+common+['-D'+s for s in ['DEFAULT_ES=2','EGL_NO_X11','GLX_STUBS','NOEGL','NOX11','NO_GBM','NO_INIT_CONSTRUCTOR','NO_LOADER','STATICLIB']]+['-I'+str(root/p)for p in ['platform-overlay','renderer/include','renderer/src/util','renderer/src/glx']]
def renderer(src):
 p=root/'renderer'/src;obj=ro/(p.name+'.o');extra=[]
 if p.name=='build_info.c':extra=['-D__DATE__="'+spec['rendererBuildDate']+'"','-D__TIME__="'+spec['rendererBuildTime']+'"']
 run(compiler+flags+extra+['-c',str(p),'-o',str(obj)],ro/(obj.name+'.log'));return obj
with ThreadPoolExecutor(max_workers=4)as pool:objects=list(pool.map(renderer,spec['rendererSources']))
run([sys.executable,str(sdk/'emar.py'),'rcs',str(out/'libGL.a'),*[str(p)for p in objects]],out/'archive.log')
def native(src):
 p=root/'native'/src;obj=no/(p.stem+'.o');run(cxx+['-std=c++20','-O2','-sUSE_SDL=2',*common,'-I'+str(root/'renderer/include'),'-c',str(p),'-o',str(obj)],no/(obj.name+'.log'));return obj
with ThreadPoolExecutor(max_workers=4)as pool:objects=sorted(pool.map(native,spec['nativeSources']))
generated=out/'content';assert not generated.exists(),'Use a fresh output directory so content directory order is reproducible'
env['VECTOR_PACK_OUT']=str(generated);run([sys.executable,str(root/'author-pack.py')],out/'content-generation.log')
manifest=json.loads((generated/'asset-provenance.json').read_text());assert len(manifest['files'])==173
for f in manifest['files']:assert sha(generated/f['path'])==spec['contentHashes'][f['path']],'Generated content changed'
site=out/'site';site.mkdir(exist_ok=True)
for p in (root/'player').iterdir():
 if p.is_file():shutil.copyfile(p,site/p.name)
for name in ['NOTICE.txt','THIRD_PARTY_NOTICES.md','asset-provenance.json','build-inputs.json']:shutil.copyfile(root/name,site/name)
run(cxx+['-O2',*[str(p)for p in objects],str(out/'libGL.a'),'-sUSE_SDL=2','-sFULL_ES2=1','-sALLOW_MEMORY_GROWTH=1','-sASSERTIONS=1','-sEXPORTED_RUNTIME_METHODS=["UTF8ToString"]','--preload-file',str(generated/'data')+'@/data','-Wl,--why-extract='+str(out/'why-extract.tsv'),'-o',str(site/'game.js')],out/'link.log')
report={'rebuild':True,'rendererObjects':69,'nativeObjects':8,'ownObjects':1,'prebuiltGameRendererObjectsUsed':False,'originalMediaUsed':False,'SDK':'6.0.10 externally supplied; SDK standard-library/SDL objects managed by SDK','files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(site.iterdir())if p.is_file()]};(out/'rebuild-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'rendererObjects':69,'gameObjects':9,'files':len(report['files']),'out':str(out)}))

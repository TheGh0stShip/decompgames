"""Independently authored MIT evidence collector. Mapping is not a blanket license certificate."""
from pathlib import Path
import os,sys,json,csv,re,subprocess,hashlib,collections,struct,math,wave
r=Path('C:/Users/andre/AppData/Local/decomp-builds/glfighters-overgrowth-source-only-2026-10-14');o=r/'vector-duel-candidate-v4';c=o/'closure';sdk=Path('D:/n64work/emsdk/upstream/emscripten');gl=r/'ptitSeb__gl4es';sdl=sdk/'cache/ports/sdl2/SDL-release-2.32.10'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,v):(c/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
pack=r/'vector-duel-authored-pack-v3';m=json.loads((pack/'asset-provenance.json').read_text());counts=collections.Counter()
for f in m['files']:
 p=pack/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(p)==f['sha256'];counts[f['kind']]+=1
 if f['kind']=='animation':n=struct.unpack('>i',b[:4])[0];assert 1<=n<=20 and len(b)==4+n*3*18*4
 elif f['kind']=='mesh':n=struct.unpack('>I',b[:4])[0];assert 0<n<=1000 and len(b)==4+n*8*4 and all(math.isfinite(x)for x in struct.unpack('>'+str(n*8)+'f',b[4:]));assert n%3==0
 elif f['kind'] in ['texture','glyph atlas']:assert b[:2]==b'BM' and struct.unpack('<I',b[2:6])[0]==len(b) and struct.unpack('<HH',b[26:30])==(1,24)
 elif f['kind']=='map':assert len(b)==(100*100*2+32)*4;values=struct.unpack('>20032i',b);assert all(0<=x<100 for x in values[-32:]);assert len(set(zip(values[-32::2],values[-31::2])))==16
 elif f['kind']=='audio':
  with wave.open(str(p),'rb')as w:assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getframerate()==22050 and w.getnframes()==2205
assert len(m['files'])==173
dump('content-validation.json',{'status':'passed','files':173,'counts':dict(counts),'bytes':sum(f['bytes']for f in m['files']),'originalMediaRead':False,'formatOnlyNotGameplay':True})
rows=list(csv.DictReader((o/'why-extract.tsv').read_text().splitlines(),delimiter='\t'));extracted=sorted(set(x['extracted']for x in rows))
os.environ['EM_CONFIG']='D:/n64work/emsdk/.emscripten';sys.path.insert(0,str(sdk));from tools.system_libs import Library
available={x.get_filename():x for x in Library.get_all_variations().values()};runtime=[]
for entry in extracted:
 archive,member=entry.rsplit('(',1);archive=Path(archive);member=member[:-1];name=archive.name
 if name=='libGL.a':pool=gl.rglob('*.c');category='gl4es'
 elif name=='libSDL2.a':
  recipe=(sdk/'tools/ports/sdl2.py').read_text();names=re.search(r"srcs = '''(.*?)'''.split",recipe,re.S).group(1).split();names += ['thread/generic/'+n for n in ['SDL_syscond.c','SDL_sysmutex.c','SDL_syssem.c','SDL_systhread.c','SDL_systls.c']];pool=[sdl/'src'/n for n in names];category='SDL2'
 else:assert name in available,name;pool=[Path(x)for x in available[name].get_files()];category='Emscripten-system'
 candidates=[p for p in pool if p.name+'.o'==member or p.stem==Path(member).stem];assert len(candidates)==1,(name,member,candidates)
 p=candidates[0];runtime.append({'archive':name,'archiveSha256':sha(archive),'member':member,'category':category,'source':p.relative_to(gl if category=='gl4es' else sdk).as_posix(),'sourceSHA256':sha(p),'sourceUnique':True})
dump('runtime-source-map.json',runtime)
overlay=r/'gl4es-apache-platform-v3/include';blocks={}
for depfile in (r/'gl4es-apache-platform-v3').glob('*.o.d'):
 blocks[depfile.name[:-2]]=[]
 for line in depfile.read_text().splitlines()[1:]:
  p=Path(line.strip().removesuffix(' \\'));assert p.exists(),p;blocks[depfile.name[:-2]].append(p)
dump('gl4es-compiler-dependencies.json',{key:[str(p)for p in deps]for key,deps in blocks.items()})
glmembers={x['member']for x in runtime if x['category']=='gl4es'};selected=set()
for key,deps in blocks.items():
 if Path(key).name in glmembers:selected.update(deps)
for p in (o/'objects').glob('*.d'):
 for line in p.read_text().splitlines()[1:]:
  dep=Path(line.strip().removesuffix(' \\'));assert dep.exists(),dep;selected.add(dep)
inventory=[]
for p in sorted(selected):
 category='gl4es' if p.is_relative_to(gl) else 'game-and-adapter' if p.is_relative_to(o/'src') else 'renderer-platform-overlay' if p.is_relative_to(overlay) else 'toolchain-system'
 text=p.read_bytes().decode('utf-8',errors='replace');inventory.append({'path':p.relative_to(gl if category=='gl4es' else o/'src' if category=='game-and-adapter' else overlay if category=='renderer-platform-overlay' else Path('D:/n64work/emsdk/upstream')).as_posix(),'category':category,'sha256':sha(p),'noticePrefix':text[:text.find('*/')+2]if text.lstrip().startswith('/*')else None})
dump('compile-inputs.json',{'selectedRendererMembers':len(glmembers),'rendererBuildObjects':len(blocks),'files':inventory,'method':'Renderer rebuild -MD dependency graph filtered to linker-extracted renderer objects, plus native game -MD inputs'})
data=json.loads(max(c.glob('emitted-js-*.json'),key=lambda p:p.stat().st_mtime).read_text());symbols=[]
for symbol in data['metadata']['librarySymbols']:
 keys=[key for key in set([symbol[1:] if symbol.startswith('_')else '$'+symbol,'$'+symbol])if key in data['origins']];assert len(keys)==1,(symbol,keys);raw=keys[0];p=Path(data['origins'][raw]);symbols.append({'symbol':symbol,'rawKey':raw,'source':p.relative_to(sdk).as_posix(),'sha256':sha(p)})
def norm(p):
 s=p.read_text();s=re.sub(r'(?m)^([ \t]*)// (?:end )?include: .*$',r'\1// TOOLCHAIN_INCLUDE_PATH',s)
 for parent in [o/'site',c]:s=s.replace((parent/'game.data').as_posix(),'PACKAGE.data').replace(str(parent/'game.data'),'PACKAGE.data')
 return s
same=norm(o/'site/game.js')==norm(c/'game.js');assert same,'Normalized emitted JavaScript differs'
dump('emitted-js-inventory.json',{'definitions':symbols,'sourceLibraries':sorted(set(x['source']for x in symbols)),'normalizedJSByteEqual':same,'WASMByteEqual':(o/'site/game.wasm').read_bytes()==(c/'game.wasm').read_bytes(),'dataByteEqual':(o/'site/game.data').read_bytes()==(c/'game.data').read_bytes(),'compilerReadPoolBroaderThanSelected':True,'remainingTemplateAndPreloaderNoticeReview':True})
print(json.dumps({'contentFiles':173,'runtimeMembers':len(runtime),'runtimeArchives':len(set(x['archive']for x in runtime)),'categories':dict(collections.Counter(x['category']for x in runtime)),'compileInputs':len(inventory),'emittedJSSymbols':len(symbols),'emittedJSLibraries':len(set(x['source']for x in symbols)),'normalizedJSByteEqual':same,'selectedRendererSGIHeaders':[x['path']for x in inventory if x['category']=='gl4es' and 'Free Software B' in (gl/x['path']).read_text(errors='replace')]}))

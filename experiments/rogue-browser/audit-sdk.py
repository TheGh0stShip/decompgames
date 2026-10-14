"""Record the actual selected SDK archives, members, headers and emitted JS.
Audits external Emscripten 6.0.10, not a compiler provenance certificate.
"""
import pathlib,re,json,hashlib,subprocess,os,collections,sys
HERE=pathlib.Path(__file__).resolve().parent
SDK=pathlib.Path(os.environ.get('ROGUE_EMSCRIPTEN','D:/n64work/emsdk/upstream/emscripten'))
OUT=pathlib.Path(os.environ.get('ROGUE_BUILD','D:/n64work/rogue-intake-2026-10-14/survey-closure-v6'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def normalized(value):return value.replace('\\\\','\\').replace('\\','/')
pin=subprocess.check_output(['git','-C',str(SDK),'rev-parse','HEAD'],text=True).strip()
assert pin=='e566f7bdcc7735f44037911c24b87a58a3c93145'
assert not subprocess.check_output(['git','-C',str(SDK),'status','--porcelain=v1','--untracked-files=no'],text=True).strip()
log=(OUT/'build.log').read_text()
archives=collections.defaultdict(set)
for path,member in re.findall(r'([^\r\n]+?\.a)\(([^)]+)\)',log):
    if 'cache' in path:archives[pathlib.Path(normalized(path))].add(member)
expected={'libc.a','libstubs.a','libdlmalloc.a','libclang_rt.builtins.a'}
assert {p.name for p in archives}==expected
archive_records=[]
os.environ.setdefault('EM_CONFIG','D:/n64work/emsdk/.emscripten');sys.path.insert(0,str(SDK))
from tools.system_libs import Library
available={x.get_filename():x for x in Library.get_all_variations().values()}
for path,members in sorted(archives.items()):
    hashes=[]
    for member in sorted(members):
        data=subprocess.check_output([str(SDK.parent/'bin/llvm-ar.exe'),'p',str(path),member])
        candidates=[pathlib.Path(p) for p in available[path.name].get_files() if pathlib.Path(p).name+'.o'==member or pathlib.Path(p).stem==pathlib.Path(member).stem]
        assert len(candidates)==1,(path.name,member,candidates)
        source=candidates[0]
        hashes.append({'member':member,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'source':source.relative_to(SDK).as_posix(),'sourceSha256':sha(source),'sourceUnique':True})
    archive_records.append({'path':path.relative_to(SDK).as_posix(),'sha256':sha(path),'selectedMembers':hashes})
headers=[]
for value in sorted(set(re.findall(r'^\.+ (.+\.h)\s*$',log,re.M))):
    path=pathlib.Path(normalized(value.strip()))
    assert path.is_file(),path
    if path.is_relative_to(SDK):kind='sdk';label=path.relative_to(SDK).as_posix()
    elif path.is_relative_to(SDK.parent):kind='clang-resource';label=path.relative_to(SDK.parent).as_posix()
    else:kind='game-or-authored';label=path.name
    headers.append({'kind':kind,'path':label,'sha256':sha(path)})
javascript=(OUT/'game.js').read_text()
includes=[]
for name in dict.fromkeys(re.findall(r'// include: ([^\r\n]+)',javascript)):
    path=SDK/'src'/name;assert path.is_file(),name
    includes.append({'path':path.relative_to(SDK).as_posix(),'sha256':sha(path)})
# Build-only proxy records which evaluated SDK library dictionary defined each
# compiler-selected JS symbol. The SDK files and runtime are not modified.
trace=json.loads(max(OUT.glob('emitted-js-*.json'),key=lambda p:p.stat().st_mtime).read_text())
libraries=set();matched=[]
for symbol in trace['metadata']['librarySymbols']:
    keys=[key for key in set([symbol[1:] if symbol.startswith('_')else '$'+symbol,'$'+symbol])if key in trace['origins']]
    assert len(keys)==1,(symbol,keys)
    source=pathlib.Path(normalized(trace['origins'][keys[0]]));assert source.is_file()
    libraries.add(source);matched.append({'symbol':symbol,'rawKey':keys[0],'source':source.relative_to(SDK).as_posix(),'sourceSha256':sha(source)})
library_records=[]
for path in sorted(libraries):
    text=path.read_text();assert 'SPDX-License-Identifier: MIT' in text[:1000],path
    library_records.append({'path':path.relative_to(SDK).as_posix(),'sha256':sha(path),'notice':text[:text.index('*/')+2]})
notices=HERE/'sdk-notices';notices.mkdir(exist_ok=True)
notice_inputs={'EMSCRIPTEN-LICENSE.txt':'LICENSE','EMSCRIPTEN-AUTHORS.txt':'AUTHORS','MUSL-COPYRIGHT.txt':'system/lib/libc/musl/COPYRIGHT','LLVM-LICENSE.txt':'system/lib/compiler-rt/LICENSE.TXT'}
notice_records=[]
for target,source in notice_inputs.items():
    path=SDK/source;(notices/target).write_bytes(path.read_bytes());notice_records.append({'path':target,'sdkPath':source,'sha256':sha(path)})
dlmalloc=(SDK/'system/lib/dlmalloc.c').read_text();start=dlmalloc.index(' This is a version (aka dlmalloc)');end=dlmalloc.index(' * Quickstart',start)
(notices/'DLMALLOC-NOTICE.txt').write_text(dlmalloc[start:end]+'\nEmscripten adaptations are covered by the Emscripten MIT/NCSA notice.\n')
(notices/'EMITTED-LIBRARY-NOTICES.txt').write_text('\n\n'.join(r['path']+'\n'+r['notice'] for r in library_records)+'\n')
prefixes=[]
for name in sorted({m['source'] for a in archive_records for m in a['selectedMembers']}):
    text=(SDK/name).read_text(errors='replace');prefix=text.split('#include',1)[0]
    if any(word in prefix.lower() for word in ['copyright','license','permission','public domain']):prefixes.append(name+'\n'+prefix[:12000])
(notices/'SELECTED-SOURCE-NOTICES.txt').write_text('\n\n'.join(prefixes)+'\n')
wasi=(SDK/'cache/sysroot/include/wasi/api.h').read_text();(notices/'WASI-HEADER-NOTICE.txt').write_text(wasi[:wasi.index('*/',wasi.index('/*\n * File origin:'))+2]+'\n')
record={'schema':1,'sdkVersion':'6.0.10','sdkPin':pin,'trackedSDKClean':True,'archives':archive_records,'headers':headers,'emittedJSIncludes':includes,'emittedLibrarySymbolSources':matched,'emittedLibrarySources':library_records,'noticeInputs':notice_records,'gameJsSha256':sha(OUT/'game.js'),'gameWasmSha256':sha(OUT/'game.wasm'),'scope':'130 selected archive members measured and uniquely mapped to SDK source recipes. JS templates explicit; compiler-selected library symbols mapped by build-only dictionary-definition observer. Compiler and standard-library objects are SDK-managed. No SDL/ncurses/audio library selected. No compiler trust or clean-room certificate.'}
(OUT/'sdk-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'archives':len(archives),'members':sum(len(v) for v in archives.values()),'headers':len(headers),'jsIncludes':len(includes),'librarySources':len(libraries),'librarySymbols':len(matched),'wasm':record['gameWasmSha256']}))

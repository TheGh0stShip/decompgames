"""Private source-only compatibility probe; not a release/distribution recipe."""
import pathlib, subprocess, os, json, hashlib, shutil, re, ast
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('D:/n64work/rogue-intake-2026-10-14')
SDK=pathlib.Path('D:/n64work/emsdk/upstream/emscripten')
OUT=pathlib.Path(os.environ.get('ROGUE_BUILD',str(ROOT/'guarded-v4')));OUT.mkdir(exist_ok=True)
env=os.environ.copy();env['EM_CONFIG']='D:/n64work/emsdk/.emscripten'
units=[x for x in sorted((ROOT/'source').glob('*.c')) if x.name not in ['mdport.c','xcrypt.c']]+[HERE/'terminal.c',HERE/'platform.c',HERE/'observe.c']
guarded=os.environ.get('ROGUE_GUARDED','1')=='1'
if guarded:
    text=(ROOT/'source/state.c').read_text()
    old='''    }

    if (d_list[i].d_func == NULL)
    {
        d_list[i].d_type = 0;
        d_list[i].d_arg = 0;
        d_list[i].d_time = 0;
    }'''
    assert text.count(old)==1
    text=text.replace(old,'''        /* Browser adaptation: clear only the current in-bounds slot. */
        if (d_list[i].d_func == NULL)
        {
            d_list[i].d_type = 0;
            d_list[i].d_arg = 0;
            d_list[i].d_time = 0;
        }
    }''')
    old='''    rs_write_int(savef, room);

    return(WRITESTAT);'''
    assert text.count(old)==1
    text=text.replace(old,'''    /* Browser adaptation: preserve passage references and null explicitly. */
    for (i = 0; i < MAXPASS; i++)
        if (&passages[i] == rp) room = MAXROOMS + i;
    rs_write_int(savef, room);

    return(WRITESTAT);''')
    old='    *rp = &rooms[i];'
    assert text.count(old)==1
    text=text.replace(old,'''    if (i == -1) *rp = NULL;
    else if (i >= 0 && i < MAXROOMS) *rp = &rooms[i];
    else if (i >= MAXROOMS && i < MAXROOMS + MAXPASS) *rp = &passages[i-MAXROOMS];
    else { format_error = TRUE; *rp = NULL; }''')
    modified=OUT/'guarded-state.c';modified.write_text(text,encoding='utf-8')
    units=[modified if x.name=='state.c' else x for x in units]
cmd=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe',str(SDK/'emcc.py'),*[str(x) for x in units],'-I'+str(HERE),'-I'+str(ROOT/'source'),'-DHAVE_CONFIG_H','-std=gnu17','-fwrapv','-O1','-sEMULATE_FUNCTION_POINTER_CASTS=1','-sASYNCIFY','-sALLOW_MEMORY_GROWTH','-sEXIT_RUNTIME=1','-sFORCE_FILESYSTEM=1','-sEXPORTED_RUNTIME_METHODS=FS,UTF8ToString','-Werror=implicit-function-declaration','-o',str(OUT/'game.js')]
run_id=len(list(OUT.glob('build-log-*.txt')))+1
p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(OUT/'build.log').write_text(p.stdout,encoding='utf-8')
(OUT/f'build-log-{run_id}.txt').write_text(p.stdout,encoding='utf-8')
(OUT/'build-result.json').write_text(json.dumps({'exitCode':p.returncode,'guardedNativeState':guarded,'command':cmd,'sources':[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in units]},indent=2))
vers=(ROOT/'source/vers.c').read_text()
def literal(name):
    lit=re.search(r'\b'+name+r'\[\]\s*=\s*("(?:\\.|[^"\\])*"|"[^"]*")',vers).group(1)
    return ast.literal_eval(lit).encode('latin1')
def count(name):
    source=(ROOT/'source/init.c').read_text()
    body=re.search(r'\b'+name+r'\[\]\s*=\s*\{(.*?)\};',source,re.S).group(1)
    return len(re.findall(r'"(?:\\.|[^"\\])*"',body))
spec={'schema':2,'build':hashlib.sha256((OUT/'game.wasm').read_bytes()).hexdigest() if p.returncode==0 else None,'enc':list(literal('encstr')),'stat':list(literal('statlist')),'version':literal('version').decode('ascii'),'release':'5.4.4','colors':count('rainbow'),'stones':count('stones'),'woods':count('wood'),'metals':count('metal')}
# Stones have one quoted name per record; numeric values are not content strings.
(OUT/'save-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
(OUT/'save-spec.js').write_text('var DGSaveSpec='+json.dumps(spec)+';\n')
shutil.copy2(HERE/'validate-save.js',OUT/'validate-save.js')
for name in ['probe.html','probe.js']:shutil.copy2(HERE/name,OUT/('index.html' if name=='probe.html' else name))
print(p.stdout[-800:] if p.returncode==0 else p.stdout[-16000:]);raise SystemExit(p.returncode)

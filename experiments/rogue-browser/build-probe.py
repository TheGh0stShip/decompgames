"""Private source-only compatibility probe; not a release/distribution recipe."""
import pathlib, subprocess, os, json, hashlib, shutil, re, ast, sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(os.environ.get('ROGUE_SOURCE_ROOT','D:/n64work/rogue-intake-2026-10-14'))
SDK=pathlib.Path(os.environ.get('ROGUE_EMSCRIPTEN','D:/n64work/emsdk/upstream/emscripten'))
OUT=pathlib.Path(os.environ.get('ROGUE_BUILD',str(ROOT/'guarded-v4')));OUT.mkdir(exist_ok=True)
env=os.environ.copy();env.setdefault('EM_CONFIG','D:/n64work/emsdk/.emscripten')
if os.environ.get('ROGUE_LINK_AUDIT')=='1':
    env['EMCC_DEBUG']='1' # Force JS compiler execution instead of its shared cache.
    env['ROGUE_TRACE_DIR']=str(OUT)
    env['NODE_OPTIONS']=env.get('NODE_OPTIONS','')+' --require="'+(HERE/'trace-emitted-js.cjs').as_posix()+'"'
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
if os.environ.get('ROGUE_SURVEY') == '1':
    units=[x for x in units if x.name!='new_level.c']+[HERE/'survey-world.c']
    for name in ['main.c','command.c','rip.c']:
        text=(ROOT/'source'/name).read_text()
        if name=='main.c':
            old='    fuse(swander, 0, WANDERTIME, AFTER);'
            assert text.count(old)==1
            text=text.replace(old,'    /* Authored campaign has fixed encounters; no wandering-spawn fuse. */')
        if name=='command.c':
            old='\tlevel++;'
            # Only the ordinary descent block is changed; MASTER remains disabled.
            start=text.index('void\nd_level()')
            at=text.index(old,start)
            text=text[:at]+text[at:].replace(old,'    if (level >= 3) { msg("The lift ends here. Take the lens and return above."); return; }\n'+old,1)
        if name=='rip.c':
            text=text.replace('#include "score.h"','#include "score.h"\n#include <emscripten.h>\n#undef bool\nEM_JS(void, survey_result, (int won), { if (Module.onSurveyResult) Module.onSurveyResult(won); });')
            text=text.replace('    signal(SIGINT, SIG_IGN);\n    purse -= purse / 10;','    survey_result(0);\n    signal(SIGINT, SIG_IGN);\n    purse -= purse / 10;')
            # Replace the complete reference grave layout and prose, keeping
            # native death, currency penalty, score confirmation and exit.
            text=re.sub(r'static char \*rip\[\] = \{.*?\n\};','',text,flags=re.S)
            death=text.index('void\ndeath(char monst)')
            start=text.index('    clear();',death)
            end=text.index('    move(LINES - 1, 0);',start)
            text=text[:start]+'''    clear();
    killer = killname(monst, FALSE);
    mvaddstr(6, 6, "SURVEY INTERRUPTED");
    mvprintw(9, 6, "The %s stopped your expedition.", killer);
    mvprintw(11, 6, "Recovered credits: %d", purse);
    mvaddstr(14, 6, "A fresh session sends a new navigator to the first station.");
'''+text[end:]
            start=text.index('    clear();',text.index('void\ntotal_winner()'))
            end=text.index('    oldpurse = purse;',start)
            text=text[:start]+'''    survey_result(1);
    clear();
    addstr("SURVEY COMPLETE\\n\\nThe lens is back at the surface.\\nAll three stations have been surveyed.\\n");
    mvaddstr(LINES - 1, 0, "Space opens the recovered equipment list.");
    refresh(); wait_for(' '); clear();
    mvaddstr(0, 0, "   Value  Recovered equipment\\n");
'''+text[end:]
        modified=OUT/('survey-'+name);modified.write_text(text,encoding='utf-8')
        units=[modified if x.name==name else x for x in units]
    import runpy
    replace_tables=runpy.run_path(str(HERE/'author-text.py'))['replace_tables']
    name_receipt=[]
    for index,unit in enumerate(units):
        if unit.name not in ['init.c','extern.c']: continue
        text,applied=replace_tables(unit.read_text(),unit.name)
        modified=OUT/('survey-'+unit.name);modified.write_text(text,encoding='utf-8')
        units[index]=modified;name_receipt.extend(applied)
    (OUT/'names-receipt.json').write_text(json.dumps(name_receipt,indent=2)+'\n')
    message_document=json.loads((HERE/'survey-messages.json').read_text())
    messages={r['referenceLiteralSha256']:r['text'] for r in message_document['messages']}
    literal_tokens=runpy.run_path(str(HERE/'audit-text.py'))['tokens']
    original_literal_hashes={hashlib.sha256(t[0].encode()).hexdigest() for p in (ROOT/'source').glob('*.c') if p.name not in ['mdport.c','xcrypt.c','new_level.c'] for t in literal_tokens(p.read_text())}
    reviewed={r['referenceLiteralSha256'] for r in json.loads((HERE/'survey-literal-contracts.json').read_text())['contracts']}
    message_receipt=[];remaining={}
    for index,unit in enumerate(units):
        # Authored adapter files have their own prose and no reference substitution.
        if unit.parent==HERE:continue
        text=unit.read_text();replacements=[]
        for token in literal_tokens(text):
            digest=hashlib.sha256(token[0].encode()).hexdigest()
            if digest in messages:
                replacements.append((token.start(),token.end(),json.dumps(messages[digest])))
                message_receipt.append({'source':unit.name,'referenceLiteralSha256':digest})
            else:
                if digest in original_literal_hashes and digest not in reviewed:raise AssertionError('Unreviewed reference literal in '+unit.name+': '+token[0])
                remaining.setdefault(token[0],[]).append({'source':unit.name,'line':text.count('\n',0,token.start())+1})
        for start,end,value in reversed(replacements):text=text[:start]+value+text[end:]
        modified=OUT/('text-'+unit.name);modified.write_text(text,encoding='utf-8');units[index]=modified
    (OUT/'messages-receipt.json').write_text(json.dumps(message_receipt,indent=2)+'\n')
    (OUT/'remaining-literals.json').write_text(json.dumps(remaining,indent=2)+'\n')
    (OUT/'text-gate.json').write_text(json.dumps({'referenceUniqueLiterals':len(original_literal_hashes),'authoredReplacementRecords':len(messages),'appliedReplacementOccurrences':len(message_receipt),'reviewedRetainedContracts':len(reviewed),'unknownReferenceLiterals':0,'referenceHeadersRemainBSD':True,'cleanRoomClaim':False},indent=2)+'\n')
cmd=[sys.executable,str(SDK/'emcc.py'),*[str(x) for x in units],'-I'+str(HERE),'-I'+str(OUT),'-I'+str(ROOT/'source'),'-DHAVE_CONFIG_H','-std=gnu17','-fwrapv','-O1','-sEMULATE_FUNCTION_POINTER_CASTS=1','-sASYNCIFY','-sALLOW_MEMORY_GROWTH','-sEXIT_RUNTIME=1','-sFORCE_FILESYSTEM=1','-sEXPORTED_RUNTIME_METHODS=FS,UTF8ToString','-Werror=implicit-function-declaration',*['-ffile-prefix-map='+str(p)+'='+name for p,name in [(ROOT,'REFERENCE'),(HERE,'ADAPTER'),(OUT,'GENERATED'),(SDK,'SDK')]],'-o',str(OUT/'game.js')]
if os.environ.get('ROGUE_LINK_AUDIT')=='1':cmd.extend(['-H','-Wl,--trace','-Wl,--why-extract='+str(OUT/'why-extract.tsv'),'-Wl,-Map='+str(OUT/'link-map.txt')])
run_id=len(list(OUT.glob('build-log-*.txt')))+1
p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(OUT/'build.log').write_text(p.stdout,encoding='utf-8')
(OUT/f'build-log-{run_id}.txt').write_text(p.stdout,encoding='utf-8')
(OUT/'build-result.json').write_text(json.dumps({'exitCode':p.returncode,'guardedNativeState':guarded,'command':cmd,'sources':[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in units]},indent=2))
vers=next(x for x in units if x.name.endswith('vers.c')).read_text()
def literal(name):
    lit=re.search(r'\b'+name+r'\[\]\s*=\s*("(?:\\.|[^"\\])*"|"[^"]*")',vers).group(1)
    return ast.literal_eval(lit).encode('latin1')
def count(name):
    source=next(x for x in units if x.name.endswith('init.c')).read_text()
    body=re.search(r'\b'+name+r'\[\]\s*=\s*\{(.*?)\};',source,re.S).group(1)
    return len(re.findall(r'"(?:\\.|[^"\\])*"',body))
spec={'schema':2,'build':hashlib.sha256((OUT/'game.wasm').read_bytes()).hexdigest() if p.returncode==0 else None,'enc':list(literal('encstr')),'stat':list(literal('statlist')),'version':literal('version').decode('ascii'),'release':'5.4.4','colors':count('rainbow'),'stones':count('stones'),'woods':count('wood'),'metals':count('metal')}
if os.environ.get('ROGUE_SURVEY')=='1':spec.update({'maxDepth':3,'printableWindow':True})
# Stones have one quoted name per record; numeric values are not content strings.
(OUT/'save-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
(OUT/'save-spec.js').write_text('var DGSaveSpec='+json.dumps(spec)+';\n')
shutil.copy2(HERE/'validate-save.js',OUT/'validate-save.js')
for name in ['probe.html','probe.js']:shutil.copy2(HERE/name,OUT/('index.html' if name=='probe.html' else name))
print(p.stdout[-800:] if p.returncode==0 else p.stdout[-16000:]);raise SystemExit(p.returncode)

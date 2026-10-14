import pathlib,json,hashlib,subprocess,os,shutil
ROOT=pathlib.Path('C:/Users/andre/AppData/Local/decomp-builds/glfighters-overgrowth-source-only-2026-10-14');ORIG=ROOT/'wedaly__GLFighters-SDL/port';OUT=ROOT/'vector-duel-candidate-v4';SRC=OUT/'src';SRC.mkdir(parents=True,exist_ok=True)
patches=[]
for p in ORIG.iterdir():
    if p.suffix not in ['.h','.cpp']:continue
    data=p.read_bytes();text=data.decode('utf-8')
    if p.name=='main.cpp':
        text=text.replace('#include "game.h"','#include "game.h"\n#include "observer.h"')
        assert text.count('SDL_INIT_VIDEO | SDL_INIT_AUDIO')==1;text=text.replace('SDL_INIT_VIDEO | SDL_INIT_AUDIO','SDL_INIT_VIDEO')
        assert text.count('  initialize_gl4es();')==1;text=text.replace('#ifdef __EMSCRIPTEN__\n  initialize_gl4es();\n#endif\n','')
        text=text.replace('  if (!initGame(SCREEN_WIDTH, SCREEN_HEIGHT)) {','#ifdef __EMSCRIPTEN__\n  initialize_gl4es(); // Own adapter: initialize after a real current GL context.\n#endif\n  if (!initGame(SCREEN_WIDTH, SCREEN_HEIGHT)) {')
        text=text.replace('  runGameEventLoop();','  vector_duel_mark_ready();\n  runGameEventLoop();')
        text=text.replace('  runGameEventLoopOnce(window, &quit);','  runGameEventLoopOnce(window, &quit);\n  if (!vector_duel_is_paused()) vector_duel_tick();')
        text=text.replace('    emscripten_cancel_main_loop();','    emscripten_cancel_main_loop();\n    disposeGame();\n    SDL_DestroyWindow(window);\n    window = NULL;\n    SDL_Quit();\n    vector_duel_mark_stopped();')
    elif p.name=='game.cpp':
        text=text.replace('#include "game.h"','#include "game.h"\n#include "observer.h"')
        text=text.replace('void restartRound(bool firstRound) {','void restartRound(bool firstRound) {\n  vector_duel_new_round();')
        text=text.replace('  // Swap buffers (double buffering)','  if (vector_duel_is_paused()) { lastFrameEndTicks = SDL_GetTicks64(); return; }\n  // Swap buffers (double buffering)')
        text=text.replace('  timetaken = endTicks - lastFrameEndTicks;','  timetaken = endTicks > lastFrameEndTicks ? endTicks - lastFrameEndTicks : 1; // Avoid zero elapsed-time division.')
        text=text.replace('lightsabers','energy batons').replace('lightsaber','energy baton')

        assert text.count('localframenum > 0 && localframenum > 100')==1;text=text.replace('localframenum > 0 && localframenum > 100','localframenum < 1 || localframenum > 20')
        old='  if (localframenum == 20) {\n    righthighleg[0][0][0] = 100;\n  }';assert old in text;text=text.replace(old,'  // Authored poses use their own frame-zero data, no legacy content-specific pose hack.')
    elif p.name=='sound.cpp':
        text='''// Independently authored MIT silent-edition backend. No audio API/device is initialized.
// Own PCM content is supplied separately; audible playback remains unavailable/unverified.
#include "sound.h"
bool loadSounds() { return true; }
void freeSounds() {}
void playSound(int id, int volume) { (void)id; (void)volume; }
'''
    modified=text.encode('utf-8');(SRC/p.name).write_bytes(modified)
    if modified!=data:patches.append({'path':p.name,'beforeSha256':hashlib.sha256(data).hexdigest(),'afterSha256':hashlib.sha256(modified).hexdigest(),'purpose':{'main.cpp':'Silent initialization, real-current-context renderer startup, native cleanup/Stop and read-only tick observer','game.cpp':'Bound own animations; preserve own poses; record native round boundaries; pause with input release and frame-clock reset; prevent zero-time division; rename energy equipment','sound.cpp':'Explicit silent edition; no mixer/codec/audio device in selected link'}[p.name]})
(SRC/'observer.h').write_text('''// Independently authored MIT diagnostic observer and product Stop adapter.
#pragma once
void vector_duel_mark_ready();
void vector_duel_tick();
void vector_duel_mark_stopped();
bool vector_duel_is_paused();
void vector_duel_new_round();
''',encoding='utf-8')
(SRC/'observer.cpp').write_text('''// Independently authored MIT. Reads native game state; never writes native actor/save/RNG values.
#include "observer.h"
#include "input.h"
#include "game.h"
#include <SDL2/SDL.h>
#include <emscripten.h>
#include <cstdio>
extern int health[], dead[], exists[], activity[], frame[], anim[], computercontrolled[];
extern float guyx[], guyy[];
extern void HandleKeyDown(int keyID);
static bool ready=false,stopped=false,paused=false; static unsigned int ticks=0,rounds=0;
extern bool AIOffensive;
bool vector_duel_is_paused(){return paused;}
void vector_duel_new_round(){++rounds;}
void vector_duel_mark_ready(){ready=true;}
void vector_duel_tick(){++ticks;}
void vector_duel_mark_stopped(){stopped=true;}
extern "C" {
EMSCRIPTEN_KEEPALIVE const char* vector_duel_state(){
 static char text[768];
 std::snprintf(text,sizeof(text),"{\\"ready\\":%s,\\"stopped\\":%s,\\"ticks\\":%u,\\"round\\":%u,\\"paused\\":%s,\\"offensive\\":%s,\\"players\\":[{\\"x\\":%.4f,\\"y\\":%.4f,\\"hp\\":%d,\\"dead\\":%d,\\"exists\\":%d,\\"activity\\":%d,\\"frame\\":%d,\\"animation\\":%d,\\"ai\\":%d},{\\"x\\":%.4f,\\"y\\":%.4f,\\"hp\\":%d,\\"dead\\":%d,\\"exists\\":%d,\\"activity\\":%d,\\"frame\\":%d,\\"animation\\":%d,\\"ai\\":%d}]}",ready?"true":"false",stopped?"true":"false",ticks,rounds,paused?"true":"false",AIOffensive?"true":"false",guyx[0],guyy[0],health[0],dead[0],exists[0],activity[0],frame[0],anim[0],computercontrolled[0],guyx[1],guyy[1],health[1],dead[1],exists[1],activity[1],frame[1],anim[1],computercontrolled[1]);return text;
}
EMSCRIPTEN_KEEPALIVE void vector_duel_pause(int value){paused=value!=0;for(int k=0;k<61;++k)setKeyState(k,false);}
EMSCRIPTEN_KEEPALIVE void vector_duel_action(int action){if(!ready||stopped)return;for(int k=0;k<61;++k)setKeyState(k,false);if(action==0)HandleKeyDown(KEY_RESPAWN_PLAYER_CHARACTERS_ID);if(action==1)HandleKeyDown(KEY_TOGGLE_OFFENSIVE_AI_ID);}
EMSCRIPTEN_KEEPALIVE void vector_duel_request_stop(){SDL_Event e{};e.type=SDL_QUIT;SDL_PushEvent(&e);}
}
''',encoding='utf-8')
site=OUT/'site';site.mkdir(exist_ok=True)
for name in ['index.html','player.js','player.css']:
    shutil.copyfile(pathlib.Path(__file__).resolve().parent/name,site/name)

env=os.environ.copy();env['EM_CONFIG']='D:/n64work/emsdk/.emscripten';env['EMSDK']='D:/n64work/emsdk';compiler=['D:/n64work/emsdk/python/3.13.3_64bit/python.exe','D:/n64work/emsdk/upstream/emscripten/em++.py'];objs=OUT/'objects';objs.mkdir(exist_ok=True);results=[]
for p in sorted(SRC.glob('*.cpp')):
    target=objs/(p.stem+'.o');cmd=compiler+['-std=c++20','-O2','-sUSE_SDL=2','-I'+str(ROOT/'ptitSeb__gl4es/include'),'-MD','-MF',str(objs/(p.stem+'.d')),'-c',str(p),'-o',str(target)]
    done=subprocess.run(cmd,env=env,capture_output=True,text=True);(objs/(p.stem+'.log')).write_text(done.stdout+done.stderr,encoding='utf-8');results.append({'source':p.name,'exitCode':done.returncode});print(p.name,done.returncode,flush=True)
    if done.returncode:print((done.stdout+done.stderr)[-2000:])
assert all(r['exitCode']==0 for r in results)
cmd=compiler+['-O2',*[str(p) for p in sorted(objs.glob('*.o'))],str(ROOT/'gl4es-apache-platform-v3/libGL.a'),'-sUSE_SDL=2','-sFULL_ES2=1','-sALLOW_MEMORY_GROWTH=1','-sASSERTIONS=1','-sEXPORTED_RUNTIME_METHODS=["UTF8ToString"]','--preload-file',str(ROOT/'vector-duel-authored-pack-v3/data')+'@/data','-Wl,--why-extract='+str(OUT/'why-extract.tsv'),'-Wl,--trace','-o',str(site/'game.js')]
done=subprocess.run(cmd,env=env,capture_output=True,text=True);(OUT/'link.log').write_text(done.stdout+done.stderr,encoding='utf-8');print('link',done.returncode,flush=True);assert done.returncode==0,done.stderr[-2000:]
report={'date':'2026-10-14','status':'Private authored-content boot candidate built; no player test yet','sourcePatches':patches,'objects':results,'silentBackend':True,'mixerLinked':False,'originalMediaLoaded':False,'runtimeFiles':[]}
for p in sorted(site.iterdir()):
    b=p.read_bytes();report['runtimeFiles'].append({'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'files':len(report['runtimeFiles']),'site':str(site)}))

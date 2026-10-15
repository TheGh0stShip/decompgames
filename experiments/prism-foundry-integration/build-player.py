#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build a private authored campaign player from verified source/object inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser(description=__doc__)
for name in ['base-build', 'pack', 'output', 'emscripten', 'em-config']:
    p.add_argument('--'+name, type=Path, required=True)
p.add_argument('--strip-campaign-tables',action='store_true',help='Generate a private globals/trigger derivative without original campaign placement roots.')
a = p.parse_args()
here = Path(__file__).resolve().parent
repo = here.parent.parent
base = a.base_build.resolve()
source = base/'source'
pack = a.pack.resolve()
out = a.output.resolve()
if out.exists():
    raise SystemExit('Choose a new output directory.')
sha = lambda data: hashlib.sha256(data).hexdigest()
reference = json.loads((repo/'docs/prism-foundry-content-2026-10-15.json').read_text())
report = json.loads((base/'result.json').read_text())
overrides = {r['target']: r for r in report['overlays']}
records = json.loads((repo/'experiments/moon-child-source-probe/source-inputs.json').read_text())['files']
for r in records:
    if r['path'] == 'Classes/framewrk/ffent.h':
        assert not (source/r['path']).exists()
        continue
    assert sha((source/r['path']).read_bytes()) == overrides.get(r['path'], r)['sha256'], r['path']
assert sha((source/'Platform/App/NullAudio.h').read_bytes()) == overrides['Platform/App/NullAudio.h']['sha256']
assert sha((pack/'provenance.json').read_bytes()) == reference['pack']['manifestSha256']
manifest = json.loads((pack/'provenance.json').read_text())
for r in manifest['files']:
    target = (pack/r['path']).resolve()
    assert target.is_relative_to(pack) and sha(target.read_bytes()) == r['sha256']
assert {r.relative_to(pack).as_posix() for r in pack.rglob('*') if r.is_file()} == {r['path'] for r in manifest['files']} | {'provenance.json'}
out.mkdir(parents=True)
generated = out/'FoundryCourseData.h'
subprocess.run([sys.executable, str(here/'make-levels.py'), '--pack', str(pack), '--output', str(generated)], check=True)
revision = reference['pack']['manifestSha256']
assert revision in (here/'save.js').read_text(encoding='utf-8')
(out/'FoundrySaveRevision.h').write_text('static const char FoundrySaveRevision[]="'+revision+'";\n',encoding='utf-8',newline='\n')

def replace_function(text, signature, body):
    start = text.index(signature+'\n{')
    brace = start+len(signature)+1
    # Existing functions can contain braces in comments/strings. Their closing
    # brace is at column zero; all nested braces in selected functions are indented.
    end = text.index('\n}', brace)+2
    return text[:start]+signature+'\n{\n'+body+'\n}'+text[end:]

mc = (source/'Classes/moonchild/mc.cpp').read_text()
assert mc.count('#define EDITOR\n') == 1
mc = mc.replace('#define EDITOR\n', '// Editor disabled for the authored campaign.\n')
mc = '#include "FoundryLevels.h"\n#include "FoundryProgress.h"\n#include <emscripten.h>\n'+mc
# No retail settings, recordings, movie/menu flow or progress imports are used.
mc = mc.replace('  load_highscores();', '  // Authored campaign: no retail high scores.')
mc = mc.replace('  load_options();', '  // Authored campaign: fixed ordinary controls.')
mc = mc.replace('  rec_prepmap();', '  // No recording playback.')
mc = mc.replace('  save_highscores();', '  // No retail high-score writes.')
mc = mc.replace('  save_options();', '  // No retail option writes.')
mc = mc.replace('configure_level(1,1);   // numbers starting from 1 (not 0)', '''FoundryConfigureLevels();
  configure_level(1,FoundryReadResume()+1);
  ingameflg=1; puzzleactiveflg=0; editflg=0; recplay=0;
  musicflg=0; sfxflg=0;
  prefs->leftkey=VK_LEFT; prefs->rightkey=VK_RIGHT;
  prefs->upkey=VK_UP; prefs->downkey=VK_DOWN;
  prefs->jumpkey=' '; prefs->shootkey='X';''', 1)
mc = mc.replace('  return (HEARTBEAT_FN) MC_startmovie;\n//#endif', '  return (HEARTBEAT_FN) MC_loadlevel;\n//#endif', 1)
mc = replace_function(mc, 'HEARTBEAT_FN MC_nextlevel(void)', '''  const int next=level+1;
  if (next>=3) { pauseflg=1; FoundryComplete=1; nextlvlflg=0; return (HEARTBEAT_FN) MC_heartbeat; }
  killlevel();
  configure_level(1,next+1);
  fadeout=0;
  return (HEARTBEAT_FN) MC_loadlevel;''')
mc = replace_function(mc, 'void check_keys(void)', '''  if (keytab['P'] || keytab[VK_ESCAPE]) {
    keytab['P']=0; keytab[VK_ESCAPE]=0;
    if (!FoundryComplete) pauseflg^=1;
  }
  if (keytab['R']) {
    keytab['R']=0; FoundryRetry=1;
  }
  handleinputloop();''')
mc = mc.replace('HEARTBEAT_FN MC_heartbeat(void)\n{\n  int i;', '''int FoundryComplete=0;
int FoundryRetry=0;
int FoundryTicks=0;
int FoundryRespawns=0;
extern "C" {
EMSCRIPTEN_KEEPALIVE int FoundryX() { return hoi && levelloadedflg ? hoi->x:-1; }
EMSCRIPTEN_KEEPALIVE int FoundryY() { return hoi && levelloadedflg ? hoi->y:-1; }
EMSCRIPTEN_KEEPALIVE int FoundryStatus(int field) {
  switch(field) {
    case 0:return levelloadedflg; case 1:return level; case 2:return pauseflg;
    case 3:return 7-player1.nrofblack; case 4:return FoundryComplete;
    case 5:return FoundryTicks; case 6:return FoundryRespawns;
    case 7:return restartx; case 8:return restarty; case 9:return editflg;
    case 10:return FoundryPrismMask(); case 11:return FoundryCheckpointActive(); case 12:return FoundryResumeUsed();
    default:return -1;
  }
}
}
HEARTBEAT_FN MC_heartbeat(void)
{
  int i;''')
# These declarations are needed by earlier functions; state exports are read-only.
mc = mc.replace('#include <emscripten.h>\n', '#include <emscripten.h>\nextern int FoundryComplete,FoundryRetry,FoundryTicks,FoundryRespawns;\n')
mc = mc.replace('  check_keys();\n', '''  check_keys();
  if (FoundryRetry) {
    FoundryRetry=0; FoundryComplete=0; pauseflg=0;
    const int target=level;
    FoundryResetCourse();
    killlevel(); configure_level(1,target+1); fadeout=0;
    return (HEARTBEAT_FN) MC_loadlevel;
  }
''', 1)
start = mc.index('HEARTBEAT_FN MC_heartbeat(void)\n{')
end = mc.index('\nvoid fullversion_display', start)
heartbeat = mc[start:end]
for call in ['  recorder();', '  editor(&player1);', '  mouse_handling();', '  levelspecific();', '  oogknippen();', '  colorcycles();', '  paraballetjes();', '  visual_updates();', '  level4flash(&player1);']:
    assert call in heartbeat, call
    heartbeat = heartbeat.replace(call, '  // Retail presentation/editor path omitted.')
heartbeat = heartbeat.replace('  if (pauseflg) return (HEARTBEAT_FN) MC_heartbeat;', '''  if (pauseflg) return (HEARTBEAT_FN) MC_heartbeat;
  ++FoundryTicks;
  if (player1.energy==0 || hoi->y>=FoundryGetCourse(level)->height-48) {
    player1.energy=33;
    hoi_init(hoi,restartx,restarty); ++FoundryRespawns;
    hoi->clear=nullptr;
  }''')
heartbeat = heartbeat.replace('  score_display(&player1);', '  // The wrapper presents the authored objective and pickup count.')
mc = mc[:start]+heartbeat+mc[end:]
if a.strip_campaign_tables:
    mc=replace_function(mc,'void framework_ExitGame(void)','''  killlevel();
  free(dotbase); dotbase=nullptr;
  free(dotcolbase); dotcolbase=nullptr;
  delete vidblitbuf; vidblitbuf=nullptr;
  disablefastfile();''')
    start=mc.index('HEARTBEAT_FN MC_heartbeat(void)\n{');end=mc.index('\nvoid fullversion_display',start)
    body=mc[start:end]
    oldstart=body.index('  if (exitflg == 1)')
    oldend=body.index('  if (nextlvlflg)',oldstart)
    body=body[:oldstart]+'''  if (exitflg) { FoundryRetry=1; return (HEARTBEAT_FN) MC_heartbeat; }
'''+body[oldend:]
    mc=mc[:start]+body+mc[end:]
mc = mc.replace('orgbonus = anim_retrieveanim("bonus");', 'orgbonus = anim_retrieveanim("bump"); // Authored pickup burst.')
mc = mc.replace('  sound_load();', '  // No audio files are shipped or opened.')
mc = mc.replace('  sound_destroy();', '  // No campaign sounds were loaded.')
# Ensure flying pickups have bounded HUD destinations without the retail HUD.
mc = mc.replace('  level_init();\n', '''  level_init();
  hoi->clear=nullptr; // No retail collapse effect during shutdown/retry.
  for(int slot=0;slot<8;++slot) { scoreposhold[slot*2]=24+slot*28; scoreposhold[slot*2+1]=24; }
''', 1)
(out/'mc.cpp').write_text(mc, encoding='utf-8', newline='\n')
start=mc.index('HEARTBEAT_FN MC_heartbeatstart(void)\n{')
end=mc.index('\n}',start)
mc=mc[:start]+mc[start:end].replace('  pauseflg = 0;','  pauseflg = FoundryComplete?1:0;')+mc[end:]
(out/'mc.cpp').write_text(mc, encoding='utf-8', newline='\n')
levels=(here/'FoundryLevels.cpp').read_text(encoding='utf-8')
levels='#include "FoundryProgress.h"\n'+levels
levels=levels.replace('    hoi=hoi_globinit(', '    FoundryBeginCourse(level);\n    hoi=hoi_globinit(',1)
levels=levels.replace('for (int i=0;i<3;++i) diamond_init(', 'for (int i=0;i<3;++i) if(FoundryPrismAvailable(i)) diamond_init(',1)
levels=levels.replace('    object_add(gate);', '    object_add(gate);\n    FoundryRestoreCourse();',1)
(out/'FoundryLevels.cpp').write_text(levels,encoding='utf-8',newline='\n')
diamond=(source/'Classes/moonchild/diamond.cpp').read_text(encoding='utf-8')
diamond='#include "FoundryProgress.h"\n'+diamond
diamond=diamond.replace('      bonus_init(object->x, object->y, 1, 1);','      FoundryPrismCollected(object->x,diamondblood->y);\n      bonus_init(object->x, object->y, 1, 1);',1)
(out/'diamond.cpp').write_text(diamond,encoding='utf-8',newline='\n')
if a.strip_campaign_tables:
    globalsText=(source/'Classes/moonchild/globals.cpp').read_text(encoding='utf-8')
    start=globalsText.index('SCR_TRIGGER_ITEM scr_triggertab[] = {');end=globalsText.index('\n};',start)+3
    globalsText=globalsText[:start]+'SCR_TRIGGER_ITEM scr_triggertab[]={{65535,0,nullptr}};'+globalsText[end:]
    start=globalsText.index('/* trigger lijsten voor level */')
    globalsText=globalsText[:start]+'// Authored descriptors are installed by FoundryConfigureLevels.\nLEVEL_DESCR levels[5][4]={};\n'
    assert 'init_level_' not in globalsText and 'triggerlist_' not in globalsText and 'lvl11.map' not in globalsText
    (out/'globals.cpp').write_text(globalsText,encoding='utf-8',newline='\n')
    (out/'campaign-trigger.cpp').write_text('// SPDX-License-Identifier: MIT\n// Authored campaign uses object callbacks for pickups/checkpoints/gates.\nvoid trigger() {}\n',encoding='utf-8',newline='\n')
host = (source/'Platform/App/Host.cpp').read_text().replace('"Moon Child FE"', '"Prism Foundry"')
host = host.replace('    LoadProgress();', '    // Authored campaign has no retail progress import.')
host = host.replace('    SaveProgress();', '    // No retail progress export.')
host += '\nvoid Host::RequestStop() { Running=false; }\nbool Host::IsReady() const { return Ready; }\n'
(out/'Host.cpp').write_text(host, encoding='utf-8', newline='\n')
header = (source/'Platform/App/Host.h').read_text().replace('    int Run();', '    int Run();\n    void RequestStop();\n    bool IsReady() const;')
(out/'Host.h').write_text(header, encoding='utf-8', newline='\n')
(out/'Main.cpp').write_text('''#include "Host.h"
#include <emscripten.h>
static Host host;
extern "C" EMSCRIPTEN_KEEPALIVE void FoundryStop() { host.RequestStop(); }
extern "C" EMSCRIPTEN_KEEPALIVE int FoundryIsRunning() { return host.IsReady()?1:0; }
int main() { return host.Run(); }
''', encoding='utf-8', newline='\n')
env = dict(os.environ, EM_CONFIG=str(a.em_config.resolve()))
includes = ['-I'+str(out), '-I'+str(here)]+['-I'+str(p) for p in sorted({p.parent for p in source.rglob('*') if p.suffix in ['.h','.hpp']})]
definitions = ['MOONCHILD_WINDOW_SDL2','MOONCHILD_RENDERER_GLES','MOONCHILD_INPUT_SDL2','MOONCHILD_AUDIO_NULL','MOONCHILD_USE_SDL','MOONCHILD_USE_SDL2','MOONCHILD_USE_OPENGL','MOONCHILD_DESKTOP_MODE','MOONCHILD_WEB','SDL_MAIN_HANDLED','MOONCHILD_APP_VERSION_STR="Prism Foundry private candidate"']
common = ['-O0','-g2','-std=c++11','-sUSE_SDL=2','-UNDEBUG', *['-D'+d for d in definitions], *includes]
replaced = {'Classes/moonchild/mc.cpp','Classes/moonchild/anim.cpp','Classes/moonchild/asset.cpp','Classes/moonchild/diamond.cpp','Platform/App/Host.cpp'}
if a.strip_campaign_tables:replaced|={'Classes/moonchild/globals.cpp','Classes/moonchild/levinits.cpp','Classes/moonchild/trigger.cpp'}
objects = []
retained = []
for r in reference['nativeVerification']['linkedAdaptedObjects']:
    if r['source'] in replaced:
        continue
    path = base/(r['source'].replace('/','__')+'.o')
    assert sha(path.read_bytes()) == r['sha256'], r['source']
    retained.append(r)
    objects.append(path)
receipt = {'scope':'Private authored campaign candidate; distribution/license closure and gameplay acceptance pending', 'retainedObjects':retained, 'newUnits':[], 'packManifestSha256':reference['pack']['manifestSha256'], 'gameStarted':False,'originalCampaignPlacementRootsRemoved':a.strip_campaign_tables}

def run(command, log):
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    (out/log).write_text(result.stdout+result.stderr, encoding='utf-8')
    return {'command':command,'exitCode':result.returncode,'log':log}

newPaths=[out/'mc.cpp', out/'Host.cpp', out/'Main.cpp', here/'animation.cpp', here/'assets.cpp', out/'FoundryLevels.cpp', here/'FoundryProgress.cpp', out/'diamond.cpp']
if a.strip_campaign_tables:newPaths+=[out/'globals.cpp',out/'campaign-trigger.cpp']
for path in newPaths:
    obj = out/(path.name+'.o')
    result = run([sys.executable,str(a.emscripten.resolve()/'em++.py'),*common,'-c',str(path),'-o',str(obj)], path.name+'.log')
    result.update({'source':str(path),'sha256':sha(path.read_bytes())})
    receipt['newUnits'].append(result)
    if result['exitCode']:
        break
    objects.append(obj)
if len(receipt['newUnits'])==len(newPaths) and all(r['exitCode']==0 for r in receipt['newUnits']):
    flags = ['-O0','-g2','-sUSE_SDL=2','-sENVIRONMENT=web','-sALLOW_MEMORY_GROWTH=1','-sFORCE_FILESYSTEM=1','-sEXIT_RUNTIME=0','-sMIN_WEBGL_VERSION=1','-sMAX_WEBGL_VERSION=1','-sASSERTIONS=2','-sSAFE_HEAP=1','-sERROR_ON_UNDEFINED_SYMBOLS=1','--embed-file',str(pack)+'@/data']
    receipt['link'] = run([sys.executable,str(a.emscripten.resolve()/'em++.py'),*[str(o) for o in objects],*flags,'-o',str(out/'foundry.js')], 'link.log')
    if receipt['link']['exitCode']==0:
        for name in ['player.html','index.html','save.js']:
            (out/name).write_bytes((here/name).read_bytes())
        receipt['outputs'] = [{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in [out/'foundry.js',out/'foundry.wasm',out/'player.html',out/'index.html',out/'save.js']]
(out/'result.json').write_text(json.dumps(receipt,indent=2)+'\n', encoding='utf-8')
print(json.dumps({'units':[r['exitCode'] for r in receipt['newUnits']], 'link':receipt.get('link',{}).get('exitCode'),'gameStarted':False}))
sys.exit(0 if receipt.get('link',{}).get('exitCode')==0 else 1)

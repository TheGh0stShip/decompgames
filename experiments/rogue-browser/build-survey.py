"""Private authored-map build, using the guarded port; text audit remains separate."""
import pathlib, json, os, subprocess, shutil, hashlib, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(os.environ.get('ROGUE_SOURCE_ROOT','D:/n64work/rogue-intake-2026-10-14'))
OUT = pathlib.Path(os.environ.get('ROGUE_BUILD', str(ROOT / 'survey-maps-v1')))
OUT.mkdir(exist_ok=True)
content = json.loads((HERE / 'survey-content.json').read_text())
def cstr(value): return json.dumps(value, ensure_ascii=True)
header = ['/* Generated CC0 layout data. */',
          'struct survey_object { int type, which, x, y; };',
          'struct survey_floor { const char *name, *briefing; int x,y,entry_x,entry_y,lift_x,lift_y; const char *rows[12]; int actors[2][2]; int item_count; struct survey_object items[3]; };',
          'static const struct survey_floor survey_floors[3] = {']
for floor in content['floors']:
    assert len(floor['rows']) == 12 and all(len(row) == 30 for row in floor['rows'])
    header.append('{' + ','.join([cstr(floor['name']), cstr(floor['briefing']), *map(str, floor['origin'] + floor['entry'] + floor['lift'])])
                  + ',{' + ','.join(map(cstr, floor['rows'])) + '},{' + ','.join('{' + ','.join(map(str,a['at'])) + '}' for a in floor['actors'])
                  + '},' + str(len(floor['items'])) + ',{' + ','.join('{' + ','.join(map(str,[ord(o['type']),o['which'],*o['at']])) + '}' for o in floor['items']) + '}},')
header.append('};')
(OUT / 'survey-levels.h').write_text('\n'.join(header) + '\n')
# The shared recipe applies native codec repairs before these exact scoped changes.
env = os.environ.copy(); env['ROGUE_BUILD'] = str(OUT); env['ROGUE_SURVEY'] = '1'
p = subprocess.run([sys.executable, str(HERE / 'build-probe.py')], env=env)
if p.returncode: raise SystemExit(p.returncode)
for name in ['probe.js','font-renderer.js','loader.js']:
    shutil.copy2(HERE / name, OUT / name)
shutil.copy2(HERE / 'survey.html', OUT / 'index.html')
(OUT / 'glyphs.js').write_text('var SurveyGlyphs=' + (HERE/'glyphs.json').read_text().strip() + ';\n')
load_files=['glyphs.js','font-renderer.js','save-spec.js','validate-save.js','probe.js','game.js','game.wasm']
(OUT/'load-manifest.json').write_text(json.dumps({'schema':1,'files':[{'path':name,'bytes':(OUT/name).stat().st_size,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()}for name in load_files]},indent=2)+'\n')
(OUT / 'content-build.json').write_text(json.dumps({'schema':1,'scope':'Private authored-map prototype; full reference prose replacement is pending.',
 'contentSha256':hashlib.sha256((HERE/'survey-content.json').read_bytes()).hexdigest(),
 'wasmSha256':hashlib.sha256((OUT/'game.wasm').read_bytes()).hexdigest()},indent=2)+'\n')

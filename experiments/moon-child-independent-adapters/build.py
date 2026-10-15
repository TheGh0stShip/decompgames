#!/usr/bin/env python3
"""Materialize pinned text inputs, replace two backends, compile; never run the game."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--emscripten', type=Path, required=True)
parser.add_argument('--em-config', type=Path, required=True)
parser.add_argument('--node', type=Path, required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
out = args.output.resolve()
if out.exists():
    raise SystemExit('Choose a new output directory.')
inputs = json.loads((here.parent / 'moon-child-source-probe/source-inputs.json').read_text('utf-8'))
verified = []
for record in inputs['files']:
    path = (args.source / record['path']).resolve()
    if not path.is_relative_to(args.source.resolve()):
        raise SystemExit('Invalid source path.')
    data = path.read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit('Source differs from pinned input: ' + record['path'])
    verified.append((record['path'], data))
stage = out / 'source'
for path, data in verified:
    target = stage / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
overlays = {
    'fastfile.cpp': 'Classes/framewrk/fastfile.cpp',
    'fastfile.h': 'Classes/framewrk/fastfile.h',
    'PlatformBackends.cpp': 'Platform/App/PlatformBackends.cpp',
    'NullAudio.h': 'Platform/App/NullAudio.h',
}
for local, target in overlays.items():
    (stage / target).write_bytes((here / local).read_bytes())
(stage / 'Classes/framewrk/ffent.h').unlink()

cmake = (stage / 'CMakeLists.txt').read_text('utf-8')
variables = {'MOONCHILD_GAME_DIR': 'Classes/moonchild', 'MOONCHILD_FRAMEWORK_DIR': 'Classes/framewrk', 'MOONCHILD_PLATFORM_DIR': 'Platform'}
units = []
for name in ['MOONCHILD_GAME_SOURCES', 'MOONCHILD_PLATFORM_SOURCES']:
    block = re.search(r'set\(' + name + r'\s+(.*?)\n\)', cmake, re.S).group(1)
    units += [variables[var] + '/' + path for var, path in re.findall(r'\$\{([^}]+)\}/([^\s]+)', block)]
excluded = ['Platform/Audio/AudioEngine.cpp', 'Platform/Audio/MP3MusicTrack.cpp']
assert all(path in units for path in excluded)
units = [path for path in units if path not in excluded]
units += ['Platform/Backends/Window/SDL2Window.cpp', 'Platform/Backends/Renderer/GLESRenderer.cpp', 'Libraries/glad/glad.c', 'Platform/Backends/Input/SDL2Input.cpp']
assert len(units) == 88 and len(units) == len(set(units))
definitions = ['MOONCHILD_WINDOW_SDL2', 'MOONCHILD_RENDERER_GLES', 'MOONCHILD_INPUT_SDL2', 'MOONCHILD_AUDIO_NULL', 'MOONCHILD_USE_SDL', 'MOONCHILD_USE_SDL2', 'MOONCHILD_USE_OPENGL', 'MOONCHILD_DESKTOP_MODE', 'MOONCHILD_WEB', 'SDL_MAIN_HANDLED', 'MOONCHILD_APP_VERSION_STR="1.1.1"']
includes = ['-I' + str(p) for p in sorted({p.parent for p in stage.rglob('*') if p.suffix in ['.h', '.hpp']})]
common = ['-O0', '-sUSE_SDL=2'] + ['-D' + d for d in definitions] + includes
env = dict(os.environ, EM_CONFIG=str(args.em_config.resolve()))
em = args.emscripten.resolve()

def run(command, log):
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    (out / log).write_text(result.stdout + result.stderr, 'utf-8')
    return {'command': command, 'exitCode': result.returncode, 'log': log}

def compile_unit(path):
    obj = out / (path.replace('/', '__') + '.o')
    c = path.endswith('.c')
    record = run([sys.executable, str(em / ('emcc.py' if c else 'em++.py')), *common, '-std=c11' if c else '-std=c++11', '-c', str(stage / path), '-o', str(obj)], obj.name + '.log')
    record['source'] = path
    return record

start = time.time()
with concurrent.futures.ThreadPoolExecutor(5) as executor:
    records = list(executor.map(compile_unit, units))
overlay_records = [{'local': local, 'target': target, 'bytes': len((here / local).read_bytes()), 'sha256': hashlib.sha256((here / local).read_bytes()).hexdigest()} for local, target in overlays.items()]
report = {'scope': 'Adapted asset-free build and synthetic adapter tests; no game execution, content or full license closure', 'pinnedInputFiles': len(verified), 'overlays': overlay_records, 'removedHeader': 'Classes/framewrk/ffent.h', 'excludedUnits': excluded + ['Platform/Backends/Audio/SDL2Audio.cpp'], 'units': records, 'gameStarted': False, 'dataPreloaded': False}
if all(r['exitCode'] == 0 for r in records):
    flags = ['-O0', '-sUSE_SDL=2', '-sALLOW_MEMORY_GROWTH=1', '-sFORCE_FILESYSTEM=1', '-sEXIT_RUNTIME=0', '-sMIN_WEBGL_VERSION=1', '-sMAX_WEBGL_VERSION=1', '-sINVOKE_RUN=0', '-sERROR_ON_UNDEFINED_SYMBOLS=1', '-lidbfs.js', '--pre-js', str(stage / 'Platform/Web/pre.js')]
    report['link'] = run([sys.executable, str(em / 'em++.py'), *[str(out / (p.replace('/', '__') + '.o')) for p in units], *flags, '-o', str(out / 'moon-fe.js')], 'link.log')
testcommand = [sys.executable, str(em / 'em++.py'), '-O0', '-std=c++11', '-Wall', '-Wextra', '-Werror', '-sENVIRONMENT=node', '-sSINGLE_FILE=1', '-sEXIT_RUNTIME=1', '-sASSERTIONS=2', '-I' + str(here), '-I' + str(stage / 'Platform/Core'), '-I' + str(stage / 'Classes/framewrk'), str(here / 'fastfile.cpp'), str(here / 'test-adapters.cpp'), str(out / 'Classes__framewrk__pcxff.cpp.o'), '-o', str(out / 'test-adapters.js')]
report['testCompile'] = run(testcommand, 'test-compile.log')
if report['testCompile']['exitCode'] == 0:
    report['testRun'] = run([str(args.node.resolve()), str(out / 'test-adapters.js')], 'test-run.log')
report['outputs'] = []
for name in ['moon-fe.js', 'moon-fe.wasm', 'test-adapters.js']:
    if (out / name).exists():
        data = (out / name).read_bytes()
        report['outputs'].append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
report['elapsedSeconds'] = round(time.time() - start, 3)
(out / 'result.json').write_text(json.dumps(report, indent=2) + '\n', 'utf-8')
summary = {'compiled': sum(r['exitCode'] == 0 for r in records), 'selected': len(units), 'link': report.get('link', {}).get('exitCode'), 'testCompile': report['testCompile']['exitCode'], 'testRun': report.get('testRun', {}).get('exitCode'), 'elapsedSeconds': report['elapsedSeconds']}
print(json.dumps(summary))
sys.exit(0 if summary['compiled'] == 88 and summary['link'] == 0 and summary['testRun'] == 0 else 1)

#!/usr/bin/env python3
"""Private feasibility probe only: no game media, no player, no source edits or unresolved-symbol allowances."""
import argparse
import concurrent.futures
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description='Compile an asset-free Moon Child FE source probe; never run a player.')
parser.add_argument('--source', required=True, type=pathlib.Path)
parser.add_argument('--output', required=True, type=pathlib.Path)
parser.add_argument('--emscripten', required=True, type=pathlib.Path)
parser.add_argument('--em-config', required=True, type=pathlib.Path)
args = parser.parse_args()
source = args.source.resolve()
output = args.output.resolve()
if output.exists():
    raise SystemExit('Choose a new output directory.')
inputs = json.loads((pathlib.Path(__file__).parent / 'source-inputs.json').read_text(encoding='utf-8'))
for record in inputs['files']:
    path = source / record['path']
    if not path.resolve().is_relative_to(source):
        raise SystemExit('Invalid source path.')
    data = path.read_bytes()
    if len(data) != record['bytes'] or hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit('Source differs from pinned input: ' + record['path'])
output.mkdir(parents=True)
cmake = (source / 'CMakeLists.txt').read_text(encoding='utf-8')
variables = {
    'MOONCHILD_GAME_DIR': 'Classes/moonchild',
    'MOONCHILD_FRAMEWORK_DIR': 'Classes/framewrk',
    'MOONCHILD_PLATFORM_DIR': 'Platform',
}
units = []
for name in ['MOONCHILD_GAME_SOURCES', 'MOONCHILD_PLATFORM_SOURCES']:
    block = re.search(r'set\(' + name + r'\s+(.*?)\n\)', cmake, re.S).group(1)
    for variable, path in re.findall(r'\$\{([^}]+)\}/([^\s]+)', block):
        units.append(variables[variable] + '/' + path)
units += [
    'Platform/Backends/Window/SDL2Window.cpp',
    'Platform/Backends/Renderer/GLESRenderer.cpp',
    'Libraries/glad/glad.c',
    'Platform/Backends/Input/SDL2Input.cpp',
    'Platform/Backends/Audio/SDL2Audio.cpp',
]
assert len(units) == len(set(units))
assert all((source / p).is_file() for p in units)
include_dirs = sorted({str(p.parent) for p in source.rglob('*') if p.suffix in ['.h', '.hpp']})
definitions = [
    'MOONCHILD_WINDOW_SDL2', 'MOONCHILD_RENDERER_GLES',
    'MOONCHILD_INPUT_SDL2', 'MOONCHILD_AUDIO_SDL2',
    'MOONCHILD_USE_SDL', 'MOONCHILD_USE_SDL2',
    'MOONCHILD_USE_OPENGL', 'MOONCHILD_DESKTOP_MODE',
    'MOONCHILD_WEB', 'SDL_MAIN_HANDLED',
    'MOONCHILD_APP_VERSION_STR="1.1.1"',
]
env = dict(os.environ)
env['EM_CONFIG'] = str(args.em_config.resolve())
emdir = args.emscripten.resolve()
common = ['-O0', '-sUSE_SDL=2', '-sUSE_ZLIB=1']
common += ['-D' + d for d in definitions]
common += ['-I' + d for d in include_dirs]

def compile_unit(path):
    obj = output / (path.replace('/', '__') + '.o')
    compiler = 'emcc.py' if path.endswith('.c') else 'em++.py'
    standard = '-std=c11' if path.endswith('.c') else '-std=c++11'
    command = [sys.executable, str(emdir / compiler), *common, standard, '-c', str(source / path), '-o', str(obj)]
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    (output / (obj.name + '.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
    record = {'source': path, 'exitCode': result.returncode, 'command': command}
    if result.returncode == 0:
        b = obj.read_bytes()
        record.update({'objectBytes': len(b), 'objectSha256': hashlib.sha256(b).hexdigest(), 'wasmObject': b[:4] == b'\0asm'})
    return record

started = time.time()
with concurrent.futures.ThreadPoolExecutor(5) as executor:
    records = list(executor.map(compile_unit, units))
report = {
    'scope': 'Compile exact selected source with installed SDK SDL2/zlib; no assets, no runtime execution, no complete dependency audit',
    'units': records,
    'selectedUnits': len(units),
    'succeededUnits': sum(r['exitCode'] == 0 for r in records),
    'sourcePatched': False,
    'dataPreloaded': False,
    'playerStarted': False,
}
failures = [r for r in records if r['exitCode'] != 0]
if not failures:
    flags = [
        '-O0', '-sUSE_SDL=2', '-sUSE_ZLIB=1', '-sALLOW_MEMORY_GROWTH=1',
        '-sFORCE_FILESYSTEM=1', '-sEXIT_RUNTIME=0', '-sMIN_WEBGL_VERSION=1',
        '-sMAX_WEBGL_VERSION=1', '-sINVOKE_RUN=0', '-sERROR_ON_UNDEFINED_SYMBOLS=1',
        '-lidbfs.js', '--pre-js', str(source / 'Platform/Web/pre.js'),
    ]
    command = [sys.executable, str(emdir / 'em++.py'), *[str(output / (p.replace('/', '__') + '.o')) for p in units], *flags, '-o', str(output / 'moon-fe.js')]
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    (output / 'link.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    report['link'] = {'command': command, 'exitCode': result.returncode}
    if result.returncode == 0:
        report['outputs'] = []
        for name in ['moon-fe.js', 'moon-fe.wasm']:
            b = (output / name).read_bytes()
            report['outputs'].append({'path': name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
report['elapsedSeconds'] = round(time.time() - started, 3)
(output / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'selected': len(units), 'compiled': report['succeededUnits'], 'link': report.get('link', {}).get('exitCode'), 'failureSources': [r['source'] for r in failures], 'elapsedSeconds': report['elapsedSeconds']}))
sys.exit(1 if failures or report.get('link', {}).get('exitCode') != 0 else 0)

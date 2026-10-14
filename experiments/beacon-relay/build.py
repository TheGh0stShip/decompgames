#!/usr/bin/env python3
"""Rebuild the PRIVATE source-port prototype; not distribution clearance.

Only the pinned author source and signed Microsoft framework package are inputs.
No cartridge, commercial game, media pack, XNA, FNA or original Emulator.cs is read.
"""
from pathlib import Path
import argparse,base64,hashlib,json,shutil,subprocess,urllib.request,zipfile
import content_patch

HERE=Path(__file__).resolve().parent
PIN='1b0ce45c75e05649ae91b44a8bb6b196684e4352'
SOURCE_SHA='657515f88328d0269fca3d5b83acbafb8bc61b24db7f5b6bff8a7d442fcb833d'
PACKAGE_SHA='4ee7b9a1b32a1a57638e51cd809d8f507ef26de17eb27e97ef50594e791c364c'
PACKAGE_URL='https://api.nuget.org/v3-flatcontainer/microsoft.netcore.app.runtime.mono.browser-wasm/9.0.20/microsoft.netcore.app.runtime.mono.browser-wasm.9.0.20.nupkg'
def digest(data):return hashlib.sha256(data).hexdigest()
def sri(path):return 'sha256-'+base64.b64encode(hashlib.sha256(path.read_bytes()).digest()).decode()
def fetch(url,path,expected):
    if path.exists() and digest(path.read_bytes())==expected:return
    data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'DecompGames-source-port-intake'}),timeout=120).read()
    if digest(data)!=expected:raise ValueError('Pinned input hash mismatch: '+url)
    path.write_bytes(data)
def main():
    args=argparse.ArgumentParser(description=__doc__);args.add_argument('--output',type=Path,required=True);args.add_argument('--cache',type=Path);opts=args.parse_args()
    out=opts.output.resolve();cache=(opts.cache or out/'inputs').resolve();cache.mkdir(parents=True,exist_ok=True)
    # Keep generated binaries out of this tracked source experiment.
    if out==HERE or HERE in out.parents:raise ValueError('Use an output outside experiments/beacon-relay')
    src=out/'src';site=out/'site';fw=site/'_framework';fw.mkdir(parents=True,exist_ok=True);src.mkdir(parents=True,exist_ok=True)
    source=cache/'Classic.cs';package=cache/'mono-browser-wasm-9.0.20.nupkg'
    fetch(f'https://raw.githubusercontent.com/NoelFB/Celeste/{PIN}/Source/PICO-8/Classic.cs',source,SOURCE_SHA);fetch(PACKAGE_URL,package,PACKAGE_SHA)
    if subprocess.check_output(['dotnet','--version'],text=True).strip()!='9.0.318':raise RuntimeError('This receipt requires .NET SDK 9.0.318')
    patched=content_patch.apply(source.read_bytes());(src/'Classic.cs').write_bytes(patched)
    for name in ['Geometry.cs','Host.cs','Bridge.cs','Probe.csproj']:shutil.copyfile(HERE/name,src/name)
    p=subprocess.run(['dotnet','build',str(src/'Probe.csproj'),'-c','Release','--nologo'],cwd=src,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (out/'build.log').write_text(p.stdout+p.stderr,encoding='utf-8')
    if p.returncode:raise RuntimeError('Compile failed; see build.log')
    assemblies=json.loads((HERE/'assembly-closure.json').read_text())
    with zipfile.ZipFile(package) as archive:
        for name in assemblies:
            if name=='Probe.dll':continue
            member='runtimes/browser-wasm/'+('native/' if name=='System.Private.CoreLib.dll' else 'lib/net9.0/')+name
            (fw/name).write_bytes(archive.read(member))
        for name in ['dotnet.js','dotnet.native.js','dotnet.runtime.js','dotnet.native.wasm']:
            (fw/name).write_bytes(archive.read('runtimes/browser-wasm/native/'+name))
        # Preserve the complete package notices; their presence is not selected dependency clearance.
        for name in ['LICENSE.TXT','THIRD-PARTY-NOTICES.TXT']:(site/name).write_bytes(archive.read(name))
    shutil.copyfile(src/'bin/Release/net9.0/Probe.dll',fw/'Probe.dll')
    resources={'coreAssembly':{n:sri(fw/n) for n in assemblies if n!='Probe.dll'},'assembly':{'Probe.dll':sri(fw/'Probe.dll')},'jsModuleNative':{'dotnet.native.js':sri(fw/'dotnet.native.js')},'jsModuleRuntime':{'dotnet.runtime.js':sri(fw/'dotnet.runtime.js')},'wasmNative':{'dotnet.native.wasm':sri(fw/'dotnet.native.wasm')}}
    config={'mainAssemblyName':'Probe.dll','globalizationMode':'invariant','debugLevel':0,'environmentVariables':{'DOTNET_SYSTEM_GLOBALIZATION_INVARIANT':'1'},'resources':resources}
    for path in [site/'boot.json',fw/'dotnet.boot.json']:path.write_text(json.dumps(config),encoding='utf-8')
    for name in ['index.html','game.js','AUTHOR-SOURCE-LICENSE.txt','AUTHORED-CODE-LICENSE.txt','CONTENT-CC0.txt','provenance.json']:shutil.copyfile(HERE/name,site/name)
    shutil.copytree(HERE/'notices',site/'notices',dirs_exist_ok=True)
    files=[{'path':p.relative_to(site).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(site.rglob('*')) if p.is_file()]
    (out/'files.json').write_text(json.dumps({'scope':'Three-course source-port candidate; selected grants reviewed, site/production acceptance separate','upstreamSourceSha256':SOURCE_SHA,'compiledSourceSha256':digest(patched),'contentPatch':'Six independently authored UI literals; gameplay algorithms retained','packageSha256':PACKAGE_SHA,'managedAssemblies':assemblies,'files':files},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'files':len(files),'managedAssemblies':len(assemblies),'probeSha256':digest((fw/'Probe.dll').read_bytes()),'buildErrors':0,'output':str(out)}))
if __name__=='__main__':main()

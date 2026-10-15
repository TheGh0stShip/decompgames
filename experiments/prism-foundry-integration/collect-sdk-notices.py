#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Preserve notice-bearing comments from previously mapped/verified SDK sources.

This mechanical comment inventory is supplementary to component licenses and
manual review. It does not establish notice completeness or binary provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.request

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--audit',type=Path,required=True)
p.add_argument('--sdk',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();sdk=a.sdk.resolve();audit=a.audit.resolve();out=a.output.resolve()
if out.exists():raise SystemExit('Choose a new output directory.')
r=json.loads((audit/'result.json').read_text(encoding='utf-8'))
assert r['verifiedPrimaryMatches']==380 and not r['fetchErrors'] and not r['mismatches']
out.mkdir(parents=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
norm=lambda b:b.replace(b'\r\n',b'\n')
comment=re.compile(rb'/\*.*?\*/|^[ \t]*//[^\n]*(?:\n[ \t]*//[^\n]*)*',re.S|re.M)
keyword=re.compile(rb'copyright|permission|public domain|SPDX|licen[cs]e|redistribut',re.I)
blocks={};occurrences=0
for record in r['records']:
    data=(audit/'source'/record['source']).read_bytes()
    assert sha(data)==record['sha256'] and data==(sdk/record['source']).read_bytes()
    for match in comment.finditer(data):
        block=match.group()
        if not keyword.search(block):continue
        entry=blocks.setdefault(block,{'sha256':sha(block),'bytes':len(block),'occurrences':[]})
        entry['occurrences'].append({'source':record['source'],'url':record['url'],'line':data[:match.start()].count(b'\n')+1,'byteOffset':match.start()})
        occurrences+=1
text=b'Selected SDK source-comment inventory\nSupplement to component license texts; not complete license clearance.\nComment bytes below are verbatim local inputs.\n'
metadata=[]
for index,(block,entry) in enumerate(blocks.items(),1):
    entry=dict(entry,id=index);metadata.append(entry)
    locations='\n'.join(x['source']+':'+str(x['line']) for x in entry['occurrences'])
    text+=('\n===== Block '+str(index)+' =====\n'+locations+'\nSHA-256: '+entry['sha256']+'\n\n').encode('utf-8')+block+b'\n'
notices=out/'selected-sdk-notice-comments.txt';notices.write_bytes(text)
recipes=[]
for item in r['buildRecipes']:
    local=(audit/'source'/item['source']).read_bytes();assert sha(local)==item['sha256']
    url='https://raw.githubusercontent.com/emscripten-core/emscripten/6.0.10/'+item['source']
    with urllib.request.urlopen(url,timeout=45) as response:primary=response.read()
    assert norm(primary)==norm(local)
    recipes.append(dict(item,url=url,primarySha256=sha(primary),primaryMatchesLocalAfterNewlineNormalization=True))
url='https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/src/video/yuv2rgb/LICENSE'
with urllib.request.urlopen(url,timeout=45) as response:yuv=response.read()
local=(sdk/'cache/ports/sdl2/SDL-release-2.32.10/src/video/yuv2rgb/LICENSE').read_bytes();assert norm(yuv)==norm(local)
(out/'SDL2-yuv2rgb-LICENSE.txt').write_bytes(yuv)
archive=sdk/'cache/ports/sdl2.32.10.zip';data=archive.read_bytes()
expected=re.search(rb"HASH = '([0-9a-f]+)'",(sdk/'tools/ports/sdl2.py').read_bytes()).group(1).decode('ascii')
assert hashlib.sha512(data).hexdigest()==expected
report={'scope':'380 mapped translation-unit sources checked against primary versions; supplementary source-comment inventory and SDL YUV license, not complete source/header/permission closure','sdkSourceAudit':r,'buildRecipes':recipes,'sourceCommentInventory':{'file':notices.name,'bytes':len(text),'sha256':sha(text),'uniqueBlocks':len(blocks),'occurrences':occurrences,'blocks':metadata,'method':'C block/contiguous // comments containing copyright, permission, public domain, SPDX, license/licence or redistribution keywords; exact bytes preserved; not an exhaustive license detector'},'additionalNotice':{'file':'SDL2-yuv2rgb-LICENSE.txt','url':url,'bytes':len(yuv),'sha256':sha(yuv),'primaryMatchesLocalAfterNewlineNormalization':True,'scope':'SDL YUV converter BSD-3-Clause; separate from SDL root zlib-style notice'},'cachedSDLArchive':{'name':archive.name,'bytes':len(data),'sha256':sha(data),'sha512':expected,'matchesPinnedSDKPortRecipeSha512':True},'gameStarted':False,'completeLicenseClearance':False}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'translationUnits':380,'primaryMatches':r['verifiedPrimaryMatches'],'uniqueCommentBlocks':len(blocks),'occurrences':occurrences,'noticeBytes':len(text),'SDLArchiveMatchesRecipe':True,'gameStarted':False}))

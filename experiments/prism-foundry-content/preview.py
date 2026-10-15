#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Render a labeled art/geometry preview, not a gameplay screenshot. Requires Pillow."""
import argparse
from pathlib import Path
from PIL import Image
import generate as content

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
canvas=content.Bitmap(1200,1100,1)
canvas.text('PRISM FOUNDRY - CONTENT PREVIEW',32,24,15,3)
canvas.text('AUTHORED ART AND COURSE GEOMETRY. NOT A GAMEPLAY SCREENSHOT.',32,62,10,2)
for i,sequence in enumerate([0,1,2,3,4,5,8,14,16,19]):
    for frame in [1,4]:
        image=content.courier(sequence,frame);scaled=content.Bitmap(64,96)
        for y in range(image.h):
            for x in range(image.w):scaled.rect(x*2,y*2,2,2,image.p[y*image.w+x])
        canvas.paste(scaled,32+i*112+(0 if frame==1 else 38),110)
    canvas.text(str(sequence),48+i*112,220,8,2)
for i,kind in enumerate(['prism','gate','cell','spark','orb','spring','burst']):
    canvas.paste(content.icon(kind,3),40+i*112,265)
    canvas.text(kind,32+i*112,370,10,2)
for index,course in enumerate(content.COURSES):
    y=425+index*210;canvas.text(course['title'],32,y,15,2)
    for x,yy,w,h in course['platforms']:canvas.rect(32+x//3,y+24+yy//5,w//3,max(2,h//5),5)
    for x,yy in course['prisms']:canvas.rect(32+x//3,y+24+yy//5,8,8,24)
    x,yy=course['gate'];canvas.rect(32+x//3,y+24+yy//5,14,18,14)
    x,yy=course['spawn'];canvas.rect(32+x//3,y+24+yy//5,8,10,20)
image=Image.frombytes('P',(canvas.w,canvas.h),bytes(canvas.p))
image.putpalette([value for rgb in content.PALETTE for value in rgb])
image.convert('RGB').save(args.output)
print('Rendered authored content preview; no player or game execution.')

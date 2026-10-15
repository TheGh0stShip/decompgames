#!/usr/bin/env python3
"""Author an original indexed-art/campaign pack; never read retail media or run a game."""
# SPDX-License-Identifier: MIT
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

# Hand-specified block glyphs for this pack, not a fetched font or game alphabet.
FONT = {
 'A':['01110','10001','10001','11111','10001','10001','10001'],
 'B':['11110','10001','10001','11110','10001','10001','11110'],
 'C':['01111','10000','10000','10000','10000','10000','01111'],
 'D':['11110','10001','10001','10001','10001','10001','11110'],
 'E':['11111','10000','10000','11110','10000','10000','11111'],
 'F':['11111','10000','10000','11110','10000','10000','10000'],
 'G':['01111','10000','10000','10111','10001','10001','01111'],
 'H':['10001','10001','10001','11111','10001','10001','10001'],
 'I':['11111','00100','00100','00100','00100','00100','11111'],
 'J':['00111','00010','00010','00010','10010','10010','01100'],
 'K':['10001','10010','10100','11000','10100','10010','10001'],
 'L':['10000','10000','10000','10000','10000','10000','11111'],
 'M':['10001','11011','10101','10101','10001','10001','10001'],
 'N':['10001','11001','10101','10011','10001','10001','10001'],
 'O':['01110','10001','10001','10001','10001','10001','01110'],
 'P':['11110','10001','10001','11110','10000','10000','10000'],
 'Q':['01110','10001','10001','10001','10101','10010','01101'],
 'R':['11110','10001','10001','11110','10100','10010','10001'],
 'S':['01111','10000','10000','01110','00001','00001','11110'],
 'T':['11111','00100','00100','00100','00100','00100','00100'],
 'U':['10001','10001','10001','10001','10001','10001','01110'],
 'V':['10001','10001','10001','10001','10001','01010','00100'],
 'W':['10001','10001','10001','10101','10101','10101','01010'],
 'X':['10001','10001','01010','00100','01010','10001','10001'],
 'Y':['10001','10001','01010','00100','00100','00100','00100'],
 'Z':['11111','00001','00010','00100','01000','10000','11111'],
 '0':['01110','10001','10011','10101','11001','10001','01110'],
 '1':['00100','01100','00100','00100','00100','00100','01110'],
 '2':['01110','10001','00001','00010','00100','01000','11111'],
 '3':['11110','00001','00001','01110','00001','00001','11110'],
 '4':['00010','00110','01010','10010','11111','00010','00010'],
 '5':['11111','10000','10000','11110','00001','00001','11110'],
 '6':['01111','10000','10000','11110','10001','10001','01110'],
 '7':['11111','00001','00010','00100','01000','01000','01000'],
 '8':['01110','10001','10001','01110','10001','10001','01110'],
 '9':['01110','10001','10001','01111','00001','00001','11110'],
 ':':['00000','00100','00100','00000','00100','00100','00000'],
 '-':['00000','00000','00000','11111','00000','00000','00000'],
 '.':['00000','00000','00000','00000','00000','00100','00100'],
 '/':['00001','00010','00010','00100','01000','01000','10000'],
 ' ':['00000']*7,
}

# Index zero is transparent/black. All other entries are authored here.
PALETTE = [(0,0,0),(11,18,32),(18,30,48),(28,45,62),(40,65,78),(56,85,94),
 (76,108,115),(104,136,139),(140,164,161),(199,215,196),(239,242,215),
 (13,70,75),(15,105,108),(23,148,141),(62,196,171),(135,236,199),
 (105,45,35),(157,61,37),(201,85,40),(238,130,49),(255,184,79),(255,223,140),
 (78,46,107),(117,65,148),(164,95,188),(206,145,223),(238,195,245),
 (70,85,116),(100,128,170),(145,173,213),(191,212,244),(235,245,255)]
PALETTE += [(max(0,min(255,16+i)),max(0,min(255,22+i)),max(0,min(255,32+i))) for i in range(224)]

def fnv32(data):
    value=2166136261
    for byte in data:value=((value^byte)*16777619)&0xffffffff
    return value

class Bitmap:
    def __init__(self,w,h,color=0):
        assert w>0 and h>0 and w%2==0
        self.w,self.h=w,h
        self.p=bytearray([color])*(w*h)
    def pixel(self,x,y,color):
        if 0<=x<self.w and 0<=y<self.h:self.p[y*self.w+x]=color
    def rect(self,x,y,w,h,color):
        for yy in range(max(y,0),min(y+h,self.h)):
            for xx in range(max(x,0),min(x+w,self.w)):self.pixel(xx,yy,color)
    def text(self,text,x,y,color=10,scale=1):
        for char in text.upper():
            assert char in FONT,char
            for row,line in enumerate(FONT[char]):
                for col,value in enumerate(line):
                    if value=='1':self.rect(x+col*scale,y+row*scale,scale,scale,color)
            x+=6*scale
    def paste(self,other,x,y):
        for yy in range(other.h):
            for xx in range(other.w):
                value=other.p[yy*other.w+xx]
                if value:self.pixel(x+xx,y+yy,value)
    def pcx(self):
        header=bytearray(128)
        header[:4]=bytes([10,5,1,8])
        struct.pack_into('<HHHHHH',header,4,0,0,self.w-1,self.h-1,self.w,self.h)
        header[65]=1
        struct.pack_into('<HH',header,66,self.w,1)
        body=bytearray()
        for y in range(self.h):
            row=self.p[y*self.w:(y+1)*self.w];x=0
            while x<self.w:
                value=row[x];run=1
                while x+run<self.w and row[x+run]==value and run<63:run+=1
                if run>1 or value>=192:body.extend([192+run,value])
                else:body.append(value)
                x+=run
        return bytes(header+body+bytes([12])+bytes(channel for rgb in PALETTE for channel in rgb))

def courier(sequence,frame):
    image=Bitmap(32,48)
    facing=sequence%2
    walk=sequence in [2,3,8,9,12,13]
    bob=1 if frame in [2,3,6,7] else 0
    crouch=sequence in [14,15]
    y=5+bob+(12 if crouch else 0)
    image.rect(9,y,16,14,4);image.rect(11,y+2,12,10,8)
    image.rect(12 if not facing else 19,y+6,4,3,15 if frame!=7 else 13)
    image.rect(6,y+15,20,17 if not crouch else 10,12)
    image.rect(8,y+17,16,12 if not crouch else 7,13)
    image.rect(11,y+19,10,5,20)
    image.rect(3 if not facing else 25,y+18,4,14,6)
    leg=3 if walk and frame<4 else -3 if walk else 0
    footy=40+(1 if bob else 0)
    if sequence in [4,5,8,9]:footy=36
    image.rect(9+leg,y+31 if not crouch else 39,5,max(3,footy-y-27),5)
    image.rect(19-leg,y+31 if not crouch else 39,5,max(3,footy-y-27),5)
    image.rect(7+leg,footy,8,4,8);image.rect(17-leg,footy,8,4,8)
    if sequence in [8,9]:
        image.rect(12,45,3,2,19);image.rect(18,44,3,3,20)
    if sequence in [6,7]:image.rect(9+frame//2,y+5,10,5,10)
    return image

def icon(kind,frame):
    size={'prism':48,'gate':64,'spark':16,'cell':24,'orb':16,'spring':32,'burst':32}.get(kind,24)
    image=Bitmap(size,96 if kind=='gate' else size)
    c=size//2
    if kind=='prism':
        for y in range(7,41):
            radius=max(0,15-abs(y-24))
            for x in range(c-radius,c+radius+1):image.pixel(x,y,24 if x<c else 14)
        image.rect(c-2,11+frame,3,10,26)
    elif kind=='gate':
        image.rect(7,4,50,88,4);image.rect(12,8,40,80,12)
        image.rect(17,13,30,70,1)
        for y in range(19,77,10):image.rect(21,y+(frame%3),22,2,14)
        image.rect(3,89,58,6,8)
    elif kind=='cell':
        image.rect(4,6,16,15,6);image.rect(7,3,10,4,8)
        image.rect(7,9,10,9,14);image.rect(11,10,3,7,15)
    elif kind=='orb':
        for y in range(2,14):
            for x in range(2,14):
                if (x-8)**2+(y-8)**2<36:image.pixel(x,y,19 if x<8 else 21)
    elif kind=='spring':
        image.rect(2,23,28,7,5)
        for y in range(7+(frame%3)*2,22,4):image.rect(8,y,16,2,20)
        image.rect(3,3+(frame%3)*2,26,5,8)
    else:
        radius=2+(frame%6)
        for n in range(8):
            angle=n*math.pi/4
            x=int(c+math.cos(angle)*radius);y=int(c+math.sin(angle)*radius)
            image.rect(x-1,y-1,3,3,15 if kind=='spark' else 20)
    return image

COURSES=[
 {'id':'assembly','title':'ASSEMBLY FLOOR','width':2048,'height':768,'spawn':[80,584],
  'platforms':[[0,640,896,128],[1024,640,1024,128],[320,576,224,32],[640,512,256,32],[1248,576,224,32],[1440,512,224,32]],
  'prisms':[[416,528],[752,464],[1520,464]],'checkpoint':[1168,584],'gate':[1888,544],
  'brief':'RECOVER THREE PRISMS. CROSS THE GAP. ENTER THE LIT GATE.'},
 {'id':'cooling','title':'COOLING LOOP','width':2304,'height':768,'spawn':[80,584],
  'platforms':[[0,640,672,128],[800,640,512,128],[1440,640,864,128],[288,576,192,32],[480,512,224,32],[896,576,192,32],[1120,512,224,32],[1568,576,224,32],[1760,512,224,32]],
  'prisms':[[544,464],[1184,464],[1824,464]],'checkpoint':[1504,584],'gate':[2144,544],
  'brief':'FOLLOW THE HIGH LEDGES. KEEP CLEAR OF THE TWO FLOOR GAPS.'},
 {'id':'night','title':'NIGHT SHIFT','width':2560,'height':896,'spawn':[80,712],
  'platforms':[[0,768,736,128],[864,768,640,128],[1632,768,928,128],[320,704,224,32],[544,640,256,32],[1024,704,224,32],[1248,640,256,32],[1728,704,224,32],[1952,640,256,32]],
  'prisms':[[608,592],[1312,592],[2016,592]],'checkpoint':[1696,712],'gate':[2400,672],
  'brief':'FINISH THE LAST SHIFT. BRING ALL THREE PRISMS TO THE EXIT.'},
]

def tilesheet():
    image=Bitmap(640,512)
    for tile in range(1,320):
        x=(tile%20)*32;y=(tile//20)*32
        if tile<10:
            image.text(str(tile),x+8,y+5,10,3)
        elif tile<20:
            image.rect(x+4,y+10,24,12,12 if tile%2 else 19)
            image.rect(x+6,y+12,20,8,14 if tile%2 else 21)
        else:
            image.rect(x,y,32,32,3+(tile%3));image.rect(x,y,32,3,7)
            image.rect(x+2,y+5,28,2,5);image.rect(x+2,y+27,28,2,2)
            image.rect(x+4,y+11,2,2,8);image.rect(x+26,y+22,2,2,8)
            if tile==21:image.rect(x,y,32,5,14)
            if tile==22:
                for xx in range(0,32,8):image.rect(x+xx,y+2,4,6,20)
            if tile==24:image.rect(x+13,y+5,6,22,14)
    return image

def backdrop():
    image=Bitmap(640,480,1)
    for row in range(480):
        for col in range(640):
            if (col+row//3)%96==0 or row%96==0:image.pixel(col,row,2)
    for x in range(12,640,72):
        image.rect(x,100+(x%5)*21,42,380,2)
        for y in range(112,420,48):image.rect(x+6,y,28,2,3)
    return image

def generate(output):
    if output.exists():raise SystemExit('Choose a new output directory.')
    output.mkdir(parents=True)
    files=[]
    def save(name,data,role,**extra):
        assert (output/name).resolve().is_relative_to(output.resolve())
        (output/name).write_bytes(data)
        files.append({'path':name,'role':role,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'fnv1a32':fnv32(data),**extra})
        if role=='verbatim CC0 legal code':
            files[-1].update(sourceUrl='https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt',authorship='Creative Commons license document; not authored campaign media',license='license document')
    def save_bitmap(name,image,role):
        save(name,image.pcx(),role,width=image.w,height=image.h,pixelSha256=hashlib.sha256(image.p).hexdigest(),pixelFnv1a32=fnv32(image.p))
    save('loose-content.marker',b'DecompGames Moon FE independent content v1\n','explicit loose-file selection')
    save_bitmap('foundry-tiles.pcx',tilesheet(),'authored tiles and HUD components')
    save_bitmap('foundry-back.pcx',backdrop(),'authored parallax architecture')
    palette=Bitmap(2,2)
    for name in ['palet.pcx','palet4.pcx','alldiams.pcx']:save_bitmap(name,palette,'authored palette alias for functional loader name')
    title=backdrop();title.text('PRISM FOUNDRY',58,100,15,6);title.text('THREE SHIFTS. NINE PRISMS.',95,172,10,2)
    title.text('MOVE LEFT OR RIGHT. JUMP TO REACH THE LEDGES.',56,240,10,2)
    title.text('RETURN TO EACH GATE WITH THREE PRISMS.',98,274,21,2)
    save_bitmap('title.pcx',title,'authored title and instructions')
    letters=Bitmap(640,160)
    for code in range(32,127):
        character=chr(code).upper()
        if character in FONT:letters.text(character,((code-32)%20)*32+7,((code-32)//20)*32+5,10,3)
    save_bitmap('char32.pcx',letters,'authored block glyph sheet')
    descriptions=[]
    # All 21 concrete native sequence positions, each with eight authored poses.
    for sequence in range(21):
        descriptions.append('S "courier-'+str(sequence)+'"')
        for frame in range(8):
            name=f'c{sequence:02d}-{frame}.pcx';save_bitmap(name,courier(sequence,frame),'authored courier animation')
            descriptions.append(' "'+name+'"')
    descriptions.append('A "moonchild"')
    descriptions += [' "courier-'+str(sequence)+'"' for sequence in range(21)]
    for animation,kind in [('moonrise','burst'),('skidcloud','spark'),('bullet1','orb'),('bump','spring'),('explosion','burst'),('heart','cell'),('smallheart','cell'),('diamond','prism'),('glim','spark'),('endoflevel','gate')]:
        descriptions.append('S "'+animation+'-frames"')
        for frame in range(8):
            name=f'{animation[:9]}{frame}.pcx';save_bitmap(name,icon(kind,frame),'authored '+kind+' animation')
            descriptions.append(' "'+name+'"')
        descriptions.append('A "'+animation+'"')
        descriptions += [' "'+animation+'-frames"']*21
    descriptions.append('S "digits"')
    for value in range(10):
        image=Bitmap(16,24);image.text(str(value),2,4,10,2)
        name=f'digit{value}.pcx';save_bitmap(name,image,'authored score glyph');descriptions.append(' "'+name+'"')
    descriptions.append('A "cyfers"');descriptions+=[' "digits"']*21
    descriptions.append('E')
    save('foundry.des',('\n'.join(descriptions)+'\n').encode(),'authored native animation descriptor')
    for course in COURSES:
        width,height=course['width'],course['height'];tiles=[0]*(width//32*height//32)
        collision=bytearray(width//16*((height+32)//16))
        for x,y,w,h in course['platforms']:
            assert all(value%32==0 for value in [x,y,w,h])
            for yy in range(y//32,(y+h)//32):
                for xx in range(x//32,(x+w)//32):tiles[yy*(width//32)+xx]=21 if yy==y//32 else 20
            for yy in range(y//16,(y+h)//16):
                for xx in range(x//16,(x+w)//16):collision[yy*(width//16)+xx]=1
        save(course['id']+'.map',struct.pack('<'+'H'*len(tiles),*tiles),'authored 32-pixel tile map',width=width,height=height)
        save(course['id']+'col.map',bytes(collision),'authored 16-pixel collision grid',width=width,heightWithMargin=height+32)
    spec={'title':'Prism Foundry','classification':'independent campaign planned for developer-source Moon Child FE port','courses':COURSES,'objective':'Collect three native prism pickups and enter the gate in each course.','audio':'No audio files; null backend required.','runtimeStatus':'Content only; no implemented integration, gameplay or balanced-route certificate.'}
    save('campaign.json',(json.dumps(spec,indent=2)+'\n').encode(),'authored course placements, goals and text')
    save('CC0.txt',(Path(__file__).with_name('CC0.txt')).read_bytes(),'content dedication')
    save('CC0-1.0-legalcode.txt',(Path(__file__).with_name('CC0-1.0-legalcode.txt')).read_bytes(),'verbatim CC0 legal code')
    paletteBytes=bytes(channel for rgb in PALETTE for channel in rgb)
    manifest={'schemaVersion':1,'project':'Prism Foundry content','authorship':'Independently authored procedural art, animation poses, palette, block glyphs, course geometry, placement specifications and text in generate.py by DecompGames contributors, 2026.','license':'CC0-1.0','generatorLicense':'MIT','referenceMedia':'None. No original game media, maps, screenshots, audio, font files or story text were inputs. Functional native format/interface names were inspected in pinned source; no clean-room isolation certification.','generatorSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'paletteSha256':hashlib.sha256(paletteBytes).hexdigest(),'paletteFnv1a32':fnv32(paletteBytes),'files':files,'runtimeIntegrated':False,'gameplayVerified':False}
    (output/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();manifest=generate(args.output.resolve())
    print(json.dumps({'files':len(manifest['files']),'bytes':sum(f['bytes'] for f in manifest['files']),'courses':len(COURSES),'runtimeIntegrated':False}))

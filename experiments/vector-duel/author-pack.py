"""Independently authored MIT generator; generated meshes, poses, maps, pixels and PCM are CC0.
Reads source loader contracts and our previously authored CC0 glyph definitions, never original media.
"""
import pathlib,re,struct,math,hashlib,json,random,wave,io
ROOT=pathlib.Path('C:/Users/andre/AppData/Local/decomp-builds/glfighters-overgrowth-source-only-2026-10-14')
SRC=ROOT/'wedaly__GLFighters-SDL/port';PACK=ROOT/'vector-duel-authored-pack-v3';PACK.mkdir(exist_ok=True)
records=[]
def put(path,b,kind,description):
    out=PACK/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
    records.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'kind':kind,'license':'CC0-1.0','origin':'Independently authored procedural design; no original media input','description':description})
def paths(file):return [p.removeprefix('./') for p in re.findall(r'"(\./data/[^"\n]+)"',(SRC/file).read_text(encoding='utf-8'))]
def bmp(w,h,pixel):
    stride=(w*3+3)&~3;body=bytearray()
    for y in reversed(range(h)):
        for x in range(w):r,g,b=pixel(x,y);body+=bytes((b,g,r))
        body+=b'\0'*(stride-w*3)
    return b'BM'+struct.pack('<IHHI',54+len(body),0,0,54)+struct.pack('<IiiHHIIiiII',40,w,h,1,24,0,len(body),2835,2835,0,0)+body
FONT=json.loads((pathlib.Path(__file__).resolve().parent/'glyphs.json').read_text())
assert len(FONT)>35
def glyph(x,y):
    cell=(y//16)*16+x//16;ch=chr((cell+32)%256).upper();bits=FONT.get(ch,FONT[' ']);px=(x%16-3)//3;py=(y%16-1)//3
    return (225,249,243) if 0<=px<3 and 0<=py<5 and bits[py*3+px]=='1' else (0,0,0)
palette={'Blue':(35,153,180),'Red':(215,122,43),'Green':(77,176,126),'Yellow':(220,195,80),'Black':(125,105,184)}
for i,path in enumerate(paths('textures.cpp')):
    if path.endswith('/Font.bmp'):
        put(path,bmp(256,256,glyph),'glyph atlas','Reuses our Beacon Relay independently authored CC0 five-row glyphs, rescaled into native256-cell atlas');continue
    color=next((v for k,v in palette.items() if '/'+k+'/' in path),(75+(i*13)%70,100+(i*7)%65,123+(i*11)%65))
    def pixel(x,y,color=color,i=i,path=path):
        sky=any('/'+name+'/' in path for name in ['Island','Lava','Snowy'])
        if sky:return (20+y//4,34+y//3,55+y//2) if (x//12+y//9+i)%7 else (52,91,112)
        stripe=(x+y+i*5)%19<3;rim=x<3 or x>60 or y<3 or y>60
        if any(n in path.lower() for n in ['smoke','puff','star','laser','lightning','blade']):
            dist=math.hypot(x-31.5,y-31.5);v=max(0,int(240*(1-dist/30)));return (v//2,v,v)
        if rim:return (18,29,42)
        if stripe:return tuple(min(255,c+50) for c in color)
        return tuple(max(0,c-((x//8+y//8)%2)*18) for c in color)
    put(path,bmp(64,64,pixel),'texture','Own teal/copper plates, woven diagonal grids or abstract horizon/effect patterns; no reference images')
def box(lo,hi):
    x0,y0,z0=lo;x1,y1,z1=hi
    faces=[((0,0,1),[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]),((0,0,-1),[(x1,y0,z0),(x0,y0,z0),(x0,y1,z0),(x1,y1,z0)]),((1,0,0),[(x1,y0,z1),(x1,y0,z0),(x1,y1,z0),(x1,y1,z1)]),((-1,0,0),[(x0,y0,z0),(x0,y0,z1),(x0,y1,z1),(x0,y1,z0)]),((0,1,0),[(x0,y1,z1),(x1,y1,z1),(x1,y1,z0),(x0,y1,z0)]),((0,-1,0),[(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)])]
    out=[];uv=[(0,0),(1,0),(1,1),(0,1)]
    for normal,pts in faces:
        for k in [0,1,2,0,2,3]:out.extend((*uv[k],*normal,*pts[k]))
    return out
dimensions={'Hip':((-1,-.45,-.6),(1,.45,.6)),'Torso':((-1.3,0,-.7),(1.3,3.1,.7)),'Head':((-.95,0,-.85),(.95,1.8,.85)),'Head2':((-1,0,-.7),(1,1.8,.7)),'Upperarm':((-.42,-2.5,-.42),(.42,0,.42)),'Upperleg':((-.5,-2.5,-.5),(.5,0,.5)),'Lowerarm':((-.34,-1.8,-.34),(.34,0,.34)),'Lowerleg':((-.4,-2.5,-.4),(.4,0,.4)),'Hand':((-.43,-.65,-.4),(.43,.2,.4)),'Foot':((-.65,-.3,-.5),(.65,.45,1.1)),'Floor':((-5,-.4,-5),(5,.4,5)),'Wall':((-1,-9,-4),(1,9,4)),'Rope':((-.2,-10,-.2),(.2,10,.2)),'LightSabre':((-.004,-.006,-.004),(.004,.024,.004)),'Sword':((-.22,0,-.22),(.22,5.5,.22)),'JetPack':((-.35,-.45,-.35),(.35,.45,.35))}
for path in paths('models.cpp'):
    name=path.rsplit('/',1)[1];verts=box(*dimensions.get(name,((-.55,-.35,-.35),(.55,.85,.35))))
    assert len(verts)%8==0 and 0<len(verts)//8<=1000
    put(path,struct.pack('>I',len(verts)//8)+struct.pack('>'+str(len(verts))+'f',*verts),'mesh','Own block-robot/arena/tool cuboid geometry with outward normals; dimensions fit native attachment contract')
g=(SRC/'game.cpp').read_text(encoding='utf-8');anim_block=g.split('const char *animationPaths[] = {',1)[1].split('};',1)[0]
animations=[p.removeprefix('./') for p in re.findall(r'"(\./data/animations/[^"\n]+)"',anim_block)];assert len(animations)==45
fields=['leftlowarm','lefthigharm','rightlowarm','righthigharm','lefthand','leftfoot','righthand','rightfoot','head','torsorotation','hippos','hiprot','torsorot','leftlowleg','lefthighleg','rightlowleg','righthighleg','speed']
for path in animations:
    name=path.rsplit('/',1)[1];values=[];frames=4 if name=='JumpStraight' else (8 if name in ['Run','Idle','Idle2'] else 20)
    for axis in range(3):
        for frame in range(frames):
            phase=frame*math.tau/frames;v={key:0 for key in fields};v['speed']=6500;v['hippos']=60 if axis==2 else 0
            if axis==0:
                v['lefthigharm']=8;v['righthigharm']=-8
                if name in ['Run','RopeClimb']:
                    v['lefthighleg']=round(32*math.sin(phase));v['righthighleg']=-v['lefthighleg'];v['leftlowleg']=round(max(0,math.sin(phase))*25);v['rightlowleg']=round(max(0,-math.sin(phase))*25);v['lefthigharm']=-v['lefthighleg']//2;v['righthigharm']=-v['righthighleg']//2;v['speed']=8500
                elif name.startswith(('Sword','Stab','JetStab','DuckStab','Shoot','Gren')):
                    v['righthigharm']=-55-round(35*math.sin(phase));v['rightlowarm']=-15;v['lefthigharm']=-25;v['speed']=8500
                elif any(s in name for s in ['Fall','Land','Die','Splat','Pain','Gah','Breakee','Throwee','Wallhit']):
                    v['torsorot']=round(12*math.sin(phase));v['lefthigharm']=-35;v['righthigharm']=35
                elif name in ['Flip','Roll','SpinAttack']:
                    v['hiprot']=round(frame*360/20);v['lefthighleg']=-40;v['righthighleg']=40
                elif 'Duck' in name:v['leftlowleg']=55;v['rightlowleg']=55;v['lefthighleg']=-40;v['righthighleg']=-40
                elif name.startswith('Jet'):v['lefthigharm']=35;v['righthigharm']=-35;v['lefthighleg']=-10;v['righthighleg']=10
            if axis==2 and 'Idle' in name:v['head']=round(3*math.sin(phase))
            values.extend(v[k] for k in fields)
    assert len(values)==3*frames*18
    put(path,struct.pack('>i',frames)+struct.pack('>'+str(len(values))+'i',*values),'animation','Own deterministic4/8/20-frame joint-angle action design; native animation IDs retained solely as loader contracts')
map_values=[]
for x in range(100):
    for y in range(100):
        floor=1 if y==39 and 22<=x<=77 else 0
        wall=1 if x in [22,77] and 34<=y<=39 else 0
        if y==35 and 38<=x<=43:floor=1
        if y==33 and 61<=x<=66:floor=1
        map_values.extend((floor,wall))
spawns=[(x,39) for x in [46,47,48,49,50,55,51,52,53,54,56,57,58,59,60,61]]
map_values.extend(v for xy in spawns for v in xy)
put('data/maps/NormalMap',struct.pack('>'+str(len(map_values))+'i',*map_values),'map','Own enclosed Foundry Deck arena, two raised shelves and sixteen safe spawn candidates; no original map read')
for i,path in enumerate(paths('sound.cpp')):
    rng=random.Random(731+i);samples=2205;data=bytearray()
    for n in range(samples):
        t=n/22050;envelope=(1-n/samples)**2;tone=math.sin(math.tau*(220+i*17)*t+9*t*t);noise=rng.uniform(-1,1);data+=struct.pack('<h',round(4500*envelope*(.7*tone+.3*noise)))
    stream=io.BytesIO()
    with wave.open(stream,'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(22050);wav.writeframes(data)
    put(path,stream.getvalue(),'audio','Own deterministic synthesized PCM chirp/noise; retained as authored content but not played by silent edition')
assert len(records)==173
manifest={'edition':'Vector Duel private authored-content candidate','generator':'Independently authored MIT code; generated content CC0-1.0','contentCompleteForStartupLoaders':True,'releaseComplete':False,'originalMediaInputs':[],'referenceInputs':['Pinned native loader path/format declarations','Own Beacon Relay CC0 glyph definitions (glyphs.json)'],'audio':'Own PCM supplied; silent edition initializes no audio device','gameplay':'Unverified; successful file generation is not gameplay','files':records}
(PACK/'asset-provenance.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'files':len(records),'bytes':sum(x['bytes'] for x in records),'kindCounts':{k:sum(x['kind']==k for x in records) for k in sorted(set(x['kind'] for x in records))}}))

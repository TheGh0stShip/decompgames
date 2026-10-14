"""Independently authored additions to the project's own CC0 3x5 glyph family."""
import hashlib,json,pathlib
HERE=pathlib.Path(__file__).resolve().parent
base=HERE.parent/'vector-duel/glyphs.json'
glyphs=json.loads(base.read_text(encoding='utf-8'))
patterns={
 '.':['000','000','000','000','010'], ',':['000','000','000','010','100'],
 '+':['000','010','111','010','000'], '#':['101','111','101','111','101'],
 '@':['010','101','111','100','011'], '*':['101','010','111','010','101'],
 '?':['110','001','010','000','010'], '%':['101','001','010','100','101'],
 '=':['000','111','000','111','000'], '|':['010','010','010','010','010'],
 '[':['110','100','100','100','110'], ']':['011','001','001','001','011'],
 '(' :['010','100','100','100','010'], ')':['010','001','001','001','010'],
 '<':['001','010','100','010','001'], '>':['100','010','001','010','100'],
 '\\':['100','100','010','001','001'], '_':['000','000','000','000','111'],
 "'":['010','010','000','000','000'], '"':['101','101','000','000','000'],
 ';':['000','010','000','010','100'], '$':['010','011','110','011','010'],
 '&':['010','101','010','101','011'], '^':['010','101','000','000','000'],
 '`':['100','010','000','000','000'], '{':['011','010','100','010','011'],
 '}':['110','010','001','010','110'], '~':['000','010','101','000','000'],
}
for char,rows in patterns.items():glyphs[char]=''.join(rows)
for char in 'abcdefghijklmnopqrstuvwxyz':glyphs[char]=glyphs[char.upper()]
assert set(glyphs)=={chr(c)for c in range(32,127)}
assert all(len(bits)==15 and set(bits)<=set('01')for bits in glyphs.values())
target=HERE/'glyphs.json';target.write_text(json.dumps(glyphs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
record={'kind':'Independent font component only; full game content edition incomplete','license':'CC0-1.0','originalMediaInputs':[],
 'referenceInputs':[{'path':'experiments/vector-duel/glyphs.json','sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'origin':'Own Beacon Relay/Vector Duel CC0 block-glyph family'}],
 'design':'Independently authored 3x5 binary row patterns for punctuation and game symbols; lowercase deliberately shares uppercase forms. No retail font or screenshot reference.',
 'files':[{'path':'glyphs.json','bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'characters':95,'license':'CC0-1.0'}],
 'notClearedByThisComponent':['Game prose and names','Dungeon layouts','Full expressive content in compiled source','Renderer integration/visual acceptance']}
(HERE/'font-provenance.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'characters':95,'license':'CC0-1.0','sha256':record['files'][0]['sha256']}))

"""Freeze the reviewed reference-literal contracts of the private text edition.
Unknown reference literals are rejected by the build; this is no rights certificate.
"""
import pathlib,json,ast,hashlib,re
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('D:/n64work/rogue-intake-2026-10-14')
original=json.loads((ROOT/'text-inventory.json').read_text())
remaining=json.loads((ROOT/'survey-text-v4/remaining-literals.json').read_text())
options={'terse','flush','jump','seefloor','passgo','tombstone','inven','name','fruit','file','True','False','(T or F)','(O, S, or C)','no'}
selectors={'mT','rogue.save','ROGUEOPTS','SEED','-s','-d','-r','names','edit','n','r','w','r+','w+'}
format_pattern=re.compile(r'%(?:[-+ #0]*\d*(?:\.\d+)?|\*)[hlL]*[diuoxXfFeEgGcs%]')
review=[]
for token,locations in remaining.items():
    if token not in original:continue
    value=ast.literal_eval(token)
    if token==list(original)[947] or token==list(original)[948]:reason='Native save byte-codec constants; BSD algorithm data, not media.'
    elif value=='%dx1' or (re.fullmatch(r'[0-9%x/]+',value) and 'x' in value):reason='Native combat dice expression, including mutable flytrap template.'
    elif value in options:reason='Native preference parser selector, boolean or input-key label.'
    elif value in selectors:reason='Native path, environment, command-line, file-mode or disabled MASTER selector.'
    elif value in ['red','silver','blue']:reason='Generic color name used by native field-effect code; no palette file or artwork.'
    elif value=='--More--':reason='Input continuation marker; ordinary UI label and test synchronization contract.'
    elif value=='5.4.4':reason='Native save release identifier.'
    elif value in ['(L)','(R)']:reason='Left/right equipment slot identifiers.'
    elif not re.search('[A-Za-z]',value):reason='Whitespace or punctuation used for native formatting.'
    elif not re.search('[A-Za-z]',re.sub(r'\b(?:A|a|s|x|inpack|or)\b','',format_pattern.sub('',value))):reason='Printf/serialization format and grammatical article/plural marker; no narrative prose.'
    else:raise AssertionError('Unreviewed literal '+token)
    review.append({'referenceLiteralSha256':hashlib.sha256(token.encode()).hexdigest(),'reason':reason,'locations':locations})
(HERE/'survey-literal-contracts.json').write_text(json.dumps({'schema':1,'scope':'Exact reviewed retained C string contracts; reference copyright headers and code remain BSD. Names/prose/layout/font are separately authored.','contracts':review},indent=2)+'\n')
print(f'{len(review)} reference literals individually classified.')

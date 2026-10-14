"""Inventory C literals lexically, excluding comments and include directives.
This records a replacement backlog; it does not certify authorship or licensing.
"""
import pathlib, re, json, ast, collections
ROOT=pathlib.Path('D:/n64work/rogue-intake-2026-10-14/source')
TOKEN=re.compile(r'/\*[\s\S]*?\*/|//[^\n]*|\'(?:\\.|[^\'\\])*\'|"(?:\\.|[^"\\])*"')
def tokens(text):
    for match in TOKEN.finditer(text):
        if not match[0].startswith('"'): continue
        line=text[text.rfind('\n',0,match.start())+1:match.start()]
        if re.match(r'\s*#\s*include',line):continue
        yield match
if __name__=='__main__':
    entries=collections.defaultdict(list)
    for path in sorted(ROOT.glob('*.c')):
        if path.name in ['mdport.c','xcrypt.c','new_level.c']:continue
        text=path.read_text()
        for match in tokens(text):entries[match[0]].append({'file':path.name,'line':text.count('\n',0,match.start())+1})
    out=ROOT.parent/'text-inventory.json';out.write_text(json.dumps(entries,indent=2)+'\n')
    lines=[f'{i}: {literal} [{locations[0]["file"]}:{locations[0]["line"]}]' for i,(literal,locations) in enumerate(entries.items())]
    (ROOT.parent/'text-inventory.txt').write_text('\n'.join(lines)+'\n')
    print(f'{len(entries)} unique string tokens; inventory saved privately.')

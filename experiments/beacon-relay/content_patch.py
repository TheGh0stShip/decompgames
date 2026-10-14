"""Replace UI/content literals in the hash-pinned source; preserve gameplay algorithms.

Line numbers refer only to Classic.cs SHA-256
657515f88328d0269fca3d5b83acbafb8bc61b24db7f5b6bff8a7d442fcb833d.
Original expressive text is not embedded in this patch or shipped source archive.
"""
import hashlib,re
REPLACEMENTS={873:'LIGHT',995:'BEACON RELAY#GATHER A LIGHT#REACH THE SIGNAL',1162:'RETRY:',1185:'BEACON',1187:'BEACON',1674:'START'}
def apply(data):
    if hashlib.sha256(data).hexdigest()!='657515f88328d0269fca3d5b83acbafb8bc61b24db7f5b6bff8a7d442fcb833d':raise ValueError('Unexpected author-source input')
    lines=data.decode('utf-8').splitlines(keepends=True)
    for line,new_text in REPLACEMENTS.items():
        before=lines[line-1]
        if not re.search(r'"[^"\r\n]*"',before):raise ValueError('Expected literal at pinned source line '+str(line))
        lines[line-1]=re.sub(r'"[^"\r\n]*"','"'+new_text+'"',before,count=1)
    return ''.join(lines).encode('utf-8')

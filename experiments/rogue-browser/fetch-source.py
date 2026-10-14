"""Reproduce the pinned text-only private snapshot; no archive or media download."""
import argparse, concurrent.futures, hashlib, json, pathlib, urllib.request
HERE=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path('D:/n64work/rogue-intake-2026-10-14/source'))
args=parser.parse_args()
snapshot=json.loads((HERE.parent.parent/'docs/rogue-source-snapshot-2026-10-14.json').read_text(encoding='utf-8'))
def fetch(record):
    relative=pathlib.PurePosixPath(record['path'])
    if relative.is_absolute() or '..' in relative.parts or record['bytes']>1000000:
        raise ValueError('Invalid allowlisted path/size')
    target=args.output.joinpath(*relative.parts)
    if target.exists():
        data=target.read_bytes()
    else:
        request=urllib.request.Request(record['url'],headers={'User-Agent':'DecompGames-pinned-source-probe'})
        with urllib.request.urlopen(request,timeout=45) as response:
            data=response.read(record['bytes']+1)
    if len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:
        raise ValueError('Pinned source mismatch: '+record['path'])
    if not target.exists():
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    return record['path']
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    records=list(pool.map(fetch,snapshot['records']))
print(json.dumps({'pin':snapshot['pin'],'verifiedTextFiles':len(records),'mediaDownloaded':False}))

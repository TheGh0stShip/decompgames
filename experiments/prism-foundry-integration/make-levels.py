#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Emit course constants only from the committed CC0 authored-pack specification."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pack',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
manifest=json.loads((args.pack/'provenance.json').read_text())
record=next(f for f in manifest['files'] if f['path']=='campaign.json')
data=(args.pack/'campaign.json').read_bytes();assert hashlib.sha256(data).hexdigest()==record['sha256']
courses=json.loads(data)['courses'];assert len(courses)==3
lines=['// CC0-1.0: independently authored course constants; generator is MIT.','#pragma once','static const FoundryCourse FoundryCourses[3]={']
for course in courses:
    assert len(course['prisms'])==3 and 0<course['width']<32768 and 0<course['height']<32768
    strings=[course['title'],course['id']+'.map',course['id']+'col.map']
    numbers=[course['width'],course['height'],*course['spawn'],*course['checkpoint'],*course['gate']]
    assert all(isinstance(value,int) and 0<=value<32768 for value in numbers)
    fields=[*[json.dumps(value) for value in strings],*[str(value) for value in numbers]]
    fields+=['{'+','.join(str(point[axis]) for point in course['prisms'])+'}' for axis in [0,1]]
    lines.append('    {'+','.join(fields)+'},')
lines.append('};')
if args.output.exists():raise SystemExit('Choose a new output file.')
args.output.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print('Generated three course definitions from the authored campaign.json.')

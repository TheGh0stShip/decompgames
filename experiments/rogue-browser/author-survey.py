"""Author fixed survey layouts from geometric constraints; no reference maps read.
Generator: MIT. Generated layouts, names and briefings: CC0-1.0.
"""
import json, pathlib, hashlib
HERE = pathlib.Path(__file__).resolve().parent
floors = []
for index, (name, briefing, barriers) in enumerate([
    ('Intake Gallery', 'Find the lift beyond the divided gallery.', [(12, 1, 7, 4), (21, 4, 10, 7)]),
    ('Relay Deck', 'Cross the relay deck. Keep a repair vial for the return.', [(9, 1, 9, 6), (19, 2, 10, 4)]),
    ('Lens Vault', 'Recover the survey lens, then return through all three lifts.', [(11, 2, 10, 5), (22, 1, 8, 3)]),
], 1):
    rows = [list('-' * 30)] + [list('|' + '.' * 28 + '|') for _ in range(10)] + [list('-' * 30)]
    for x, lo, hi, gap in barriers:
        for y in range(lo, hi + 1):
            if y != gap: rows[y][x] = '|'
    floors.append({'name': name, 'briefing': briefing, 'origin': [2, 4],
                   'rows': [''.join(row) for row in rows], 'entry': [1, 1], 'lift': [27, 10],
                   'actors': [{'type': 'B', 'at': [7, 2]}, {'type': 'B', 'at': [24, 8]}],
                   'items': [{'type': '!', 'which': 5, 'at': [3, 1]},
                             {'type': ':', 'which': 0, 'at': [5, 8]}]
                   + ([{'type': ',', 'which': 0, 'at': [26, 2]}] if index == 3 else [])})
document = {'schema': 1, 'title': 'Signal Survey', 'license': 'CC0-1.0',
            'authorship': 'DecompGames contributors, 2026; independently arranged geometric layouts. No reference layout input.',
            'mechanics': 'Rogue native movement, combat, inventory, health, item effects and ascent victory. Fixed authored encounters replace procedural level generation and wandering spawns.',
            'floors': floors}
target = HERE / 'survey-content.json'
target.write_text(json.dumps(document, indent=2) + '\n', encoding='utf-8')
print(hashlib.sha256(target.read_bytes()).hexdigest())

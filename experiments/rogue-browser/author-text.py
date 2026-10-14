"""Author named presentation tables. Script MIT; generated table values CC0.
These replacements use the inspected source's field structure, not clean-room isolation.
Only exact named initializer blocks are replaced, so gameplay numbers stay intact.
"""
import pathlib, re, json
HERE=pathlib.Path(__file__).resolve().parent
TABLES={
 'monsters': ['abrasion drone','hinge moth','cable runner','furnace sentinel','echo mote','grip vine','gale carrier','hammer walker','insulation slug','joint crawler','kite skimmer','ledger thief','mirror watcher','net snatcher','ore hauler','phase drifter','quartz charger','recoil worm','seam worm','tower guardian','underdeck charger','valve stalker','wake drifter','exchange mimic','yard prowler','zero walker'],
 'arm_info': ['canvas shell','woven shell','rivet shell','laminate shell','mesh shell','ribbed shell','belted shell','forged shell'],
 'pot_info': ['signal blur','false contours','corrosion','power surge','phase sight','repair','actor scan','field scan','training boost','deep repair','overdrive','power reset','blackout','lift field'],
 'ring_info': ['shielding','torque boost','torque lock','seam scan','phase sight','ornament','noise broadcast','aim assist','impact boost','self repair','ration saver','short hop','quiet step','shell seal'],
 'scr_info': ['actor blur','deck chart','actor lock','standby','shell tuning','vial analysis','sheet analysis','tool analysis','shell analysis','band and rod analysis','actor repulsion','ration scan','short hop','tool tuning','actor summon','lock release','noise broadcast','shell seal'],
 'weap_info': ['impact handle','long cutter','tension launcher','launcher pin','short cutter','heavy cutter','needle pin','rotor disk','pole cutter'],
 'ws_info': ['illumination','phase veil','arc discharge','heat pulse','chill pulse','shape change','force pulse','actor overdrive','actor slowdown','energy transfer','idle cycle','remote hop','near hop','field cancel'],
 'tr_name': ['a loose panel','a pin launcher','a standby vent','a clamp plate','a hop field','a corrosive needle','a wash nozzle','an unknown sensor'],
 'rainbow': ['mist stripe','sun stripe','sea stripe','night stripe','sand stripe','leaf stripe','rose stripe','clay stripe','ink stripe','snow stripe','ash stripe','moss stripe','copper stripe','slate stripe','violet stripe','teal stripe','rust stripe','plum stripe','ochre stripe','coral stripe','mint stripe','pearl stripe','olive stripe','lemon stripe','cobalt stripe','dawn stripe','lime stripe'],
 'sylls': ['lum','vei','tor','nal','si','dru','kel','vem','pon','za','fen','rho','ki','bel','tou','var','lin','quo','dal'],
 'stones': ['mist ceramic','sun ceramic','sea ceramic','night ceramic','sand ceramic','leaf ceramic','rose ceramic','clay ceramic','ink ceramic','snow ceramic','ash ceramic','moss ceramic','copper ceramic','slate ceramic','violet ceramic','teal ceramic','rust ceramic','plum ceramic','ochre ceramic','coral ceramic','mint ceramic','pearl ceramic','olive ceramic','lemon ceramic','cobalt ceramic','dawn ceramic'],
 'wood': ['mist fiber','sun fiber','sea fiber','night fiber','sand fiber','leaf fiber','rose fiber','clay fiber','ink fiber','snow fiber','ash fiber','moss fiber','copper fiber','slate fiber','violet fiber','teal fiber','rust fiber','plum fiber','ochre fiber','coral fiber','mint fiber','pearl fiber','olive fiber','lemon fiber','cobalt fiber','dawn fiber','lime fiber','smoke fiber','berry fiber','stone fiber','aqua fiber','earth fiber','cream fiber'],
 'metal': ['mist alloy','sun alloy','sea alloy','night alloy','sand alloy','leaf alloy','rose alloy','clay alloy','ink alloy','snow alloy','ash alloy','moss alloy','copper alloy','slate alloy','violet alloy','teal alloy','rust alloy','plum alloy','ochre alloy','coral alloy','mint alloy','pearl alloy'],
}
def replace_tables(text, source_name):
    applied=[]
    for name, values in TABLES.items():
        pattern=r'(\b'+re.escape(name)+r'\s*\[[^\]]*\]\s*=\s*\{)(.*?)(\}\s*;)'
        match=re.search(pattern,text,re.S)
        if not match:continue
        body=match[2]
        if name=='sylls':body='\n    '+', '.join(json.dumps(v) for v in values)+'\n'
        else:
            tokens=list(re.finditer(r'"(?:\\.|[^"\\])*"',body))
            # Monster damage expressions are code contracts, not names.
            if name=='monsters':tokens=[m for m in tokens if not re.fullmatch(r'"[0-9%x/]+"',m[0])]
            assert len(tokens)==len(values),(name,len(tokens),len(values))
            for token,value in reversed(list(zip(tokens,values))):body=body[:token.start()]+json.dumps(value)+body[token.end():]
        text=text[:match.start(2)]+body+text[match.end(2):]
        applied.append({'source':source_name,'table':name,'count':len(values)})
    # Food's original favorite-fruit spelling was stored as character constants.
    if source_name=='extern.c':
        text,n=re.subn(r"\{ 's', 'l', 'i', 'm', 'e', '-', 'm', 'o', 'l', 'd', '\\0' \}", '"trail berry"',text)
        assert n==1
    return text,applied
if __name__=='__main__':
    (HERE/'survey-names.json').write_text(json.dumps({'schema':1,'license':'CC0-1.0','author':'DecompGames contributors, 2026','tables':TABLES},indent=2)+'\n')

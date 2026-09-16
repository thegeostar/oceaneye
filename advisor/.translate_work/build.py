import json,glob,os,sys
W=os.path.dirname(os.path.abspath(__file__))
units=json.load(open(os.path.join(W,'units.json')))
byid={u['id']:u for u in units}
part={}
for f in sorted(glob.glob(os.path.join(W,'t_*.json'))):
    part.update({int(k):v for k,v in json.load(open(f)).items()})
bytext={}
for i,v in part.items():
    if i in byid: bytext.setdefault(byid[i]['text'],v)
tr={}
for u in units:
    if u['id'] in part: tr[str(u['id'])]=part[u['id']]
    elif u['text'] in bytext: tr[str(u['id'])]=bytext[u['text']]
json.dump(tr,open(os.path.join(W,'trans.json'),'w'),ensure_ascii=False,indent=1)
miss=[u for u in units if str(u['id']) not in tr]
print(f'translated {len(tr)}/{len(units)} | missing {len(miss)}')
if '-v' in sys.argv:
    seen=set()
    for u in miss:
        if u['text'] in seen: continue
        seen.add(u['text'])
        print(f"{u['id']}|p{u['page']}|{u['kind'][:2]}|{u['size']}> {u['text']}")
    print(f'### {len(seen)} unique strings still to translate')

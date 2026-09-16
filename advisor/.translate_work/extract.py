import pymupdf, re, json, statistics, os
W=os.path.dirname(os.path.abspath(__file__))
CJK=re.compile(r'[一-鿿]'); CAP=re.compile(r'^\s*[图表]\s*\d')
NUM=re.compile(r'[\d.,\s%×+\-—–]+')
SRC=os.path.join(os.path.dirname(W),'【7】基于深度学习的水下图像超分辨率重建与目标检测方法研究1.pdf')
d=pymupdf.open(SRC)

pages=[]
for pno,page in enumerate(d):
    imgs=[pymupdf.Rect(page.get_image_bbox(i)) for i in page.get_images(full=True) if page.get_image_bbox(i)]
    ls=[]
    for b in page.get_text('dict')['blocks']:
        if b['type']!=0: continue
        for l in b['lines']:
            sp=l['spans']
            if not sp or not ''.join(s['text'] for s in sp).strip(): continue
            ls.append(dict(bbox=list(l['bbox']), text=''.join(s['text'] for s in sp),
                           size=round(statistics.median([s['size'] for s in sp]),2),
                           bold=any('Bold' in s['font'] for s in sp)))
    ls.sort(key=lambda l: l['bbox'][3])
    clusters=[]
    for l in ls:
        if clusters and abs(l['bbox'][3]-clusters[-1][0]['bbox'][3])<2.5: clusters[-1].append(l)
        else: clusters.append([l])
    ls=[]
    for c in clusters:
        c.sort(key=lambda l: l['bbox'][0]); ls.extend(c)
    merged=[]
    for l in ls:
        if merged:
            p=merged[-1]
            same=abs(p['bbox'][3]-l['bbox'][3])<2.5 and abs(p['size']-l['size'])<0.4
            gap=l['bbox'][0]-p['bbox'][2]
            numeric=bool(NUM.fullmatch(l['text'])) or bool(NUM.fullmatch(p['text']))
            if same and not numeric and -1<=gap<max(8.0,l['size']*2.3):
                p['text']+=l['text']
                p['bbox']=[min(p['bbox'][0],l['bbox'][0]),min(p['bbox'][1],l['bbox'][1]),
                           max(p['bbox'][2],l['bbox'][2]),max(p['bbox'][3],l['bbox'][3])]
                p['bold']=p['bold'] or l['bold']; continue
        merged.append(dict(l))
    pages.append((merged,imgs))

def prose_ok(l,bx):
    x0,y0,x1,y1=l['bbox']
    return (CJK.search(l['text']) and 11.4<=l['size']<=12.6 and y0>78 and y1<800
            and bx-3<=x0<=bx+40 and not CAP.match(l['text']) and not l['bold']
            and not re.search(r'\.{6,}',l['text']))

units=[]
for pno,(ls,imgs) in enumerate(pages,start=1):
    xs=[l['bbox'][0] for l in ls if 11.4<=l['size']<=12.6 and (l['bbox'][2]-l['bbox'][0])>360]
    bx=min(xs) if xs else 57
    i=0
    while i<len(ls):
        l=ls[i]
        if not CJK.search(l['text']): i+=1; continue
        w=l['bbox'][2]-l['bbox'][0]
        if prose_ok(l,bx) and w>360:
            grp=[l]; j=i+1
            while j<len(ls):
                n=ls[j]
                if not prose_ok(n,bx): break
                if n['bbox'][1]-grp[-1]['bbox'][3] > l['size']*1.6: break
                grp.append(n); j+=1
                if (n['bbox'][2]-n['bbox'][0])<360: break
            r=pymupdf.Rect(min(g['bbox'][0] for g in grp),min(g['bbox'][1] for g in grp),
                           max(g['bbox'][2] for g in grp),max(g['bbox'][3] for g in grp))
            if any((r&im).get_area()>4 for im in imgs):
                for g in grp:
                    units.append(dict(page=pno,kind='inplace',rect=list(g['bbox']),size=g['size'],
                                      bold=g['bold'],text=re.sub(r'\s+',' ',g['text']).strip(),nlines=1))
            else:
                units.append(dict(page=pno,kind='prose',rect=list(r),size=l['size'],bold=False,
                                  text=re.sub(r'\s+',' ',''.join(g['text'] for g in grp)).strip(),nlines=len(grp)))
            i=j
        else:
            units.append(dict(page=pno,kind='inplace',rect=list(l['bbox']),size=l['size'],
                              bold=l['bold'],text=re.sub(r'\s+',' ',l['text']).strip(),nlines=1))
            i+=1
for n,u in enumerate(units): u['id']=n
json.dump(units,open(os.path.join(W,'units.json'),'w'),ensure_ascii=False,indent=1)
pr=sum(1 for u in units if u['kind']=='prose')
print('units',len(units),'| prose',pr,'| inplace',len(units)-pr)

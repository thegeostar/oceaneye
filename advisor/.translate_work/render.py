import pymupdf, json, sys, re, unicodedata, os
W=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(os.path.dirname(W),'【7】基于深度学习的水下图像超分辨率重建与目标检测方法研究1.pdf')
CJK=re.compile(r'[一-鿿　-〿＀-￯]')
units=json.load(open(os.path.join(W,'units.json')))
tr=json.load(open(os.path.join(W,'trans.json')))
out=sys.argv[1]
only=set(int(x) for x in sys.argv[2:]) if len(sys.argv)>2 else None

SUB={'—':'-','–':'-','―':'-','‘':"'",'’':"'",'“':'"','”':'"','…':'...','≤':'<=','≥':'>=',
     '−':'-','⊙':'(.)','⊕':'(+)','⊗':'(x)','∩':'^','∪':'U','∈':' in ','∠':'angle ',
     '→':'->','←':'<-','∇':'grad ','√':'sqrt','∑':'sum','∫':'int','≈':'~=','≠':'!=',
     '𝒜':'A','𝒫':'P','β':'beta','α':'alpha','σ':'sigma','λ':'lambda','μ':'mu','ε':'eps',
     'Φ':'Phi','θ':'theta','η':'eta','ν':'nu','ℒ':'L','✓':'Y','　':' ','×':'x'}
def safe(t):
    t=''.join(SUB.get(c,c) for c in t)
    t=unicodedata.normalize('NFKC',t)
    return ''.join(c if ord(c)<0x100 else '?' for c in t)

doc=pymupdf.open(SRC)
PAGE_L,PAGE_R,BODY_R=45,551,545

def clip_rect(R,foreign):
    r=pymupdf.Rect(R); mid=(r.y0+r.y1)/2
    for f in foreign:
        inter=(r&f)
        if inter.get_area()<=0.5: continue
        if inter.get_area()/(f.get_area() or 1)>0.60: continue
        if f.y1<=mid: r.y0=max(r.y0,f.y1+0.35)
        else:         r.y1=min(r.y1,f.y0-0.35)
    return r if r.height>3 else pymupdf.Rect(R)

def fit_box(page,box,text,maxsize,align,bold,minsize=6.0):
    font='tibo' if bold else 'tiro'; s=maxsize
    while s>=minsize:
        if page.insert_textbox(box,text,fontsize=s,fontname=font,align=align,render_mode=3)>=0:
            page.insert_textbox(box,text,fontsize=s,fontname=font,align=align); return s
        s-=0.25
    page.insert_textbox(box,text,fontsize=minsize,fontname=font,align=align); return minsize

todo={}
for u in units:
    if only and u['page'] not in only: continue
    if str(u['id']) in tr and tr[str(u['id'])].strip(): todo.setdefault(u['page'],[]).append(u)

for pno,us in sorted(todo.items()):
    page=doc[pno-1]
    spans=[]
    for b in page.get_text('dict')['blocks']:
        if b['type']!=0: continue
        for l in b['lines']:
            for sp in l['spans']:
                if sp['text'].strip():
                    spans.append((pymupdf.Rect(sp['bbox']),bool(CJK.search(sp['text']))))
    rects={}
    for u in us:
        R=pymupdf.Rect(u['rect'])
        foreign=[r for r,c in spans if not c and (r&R).get_area()>0.5]
        rects[u['id']]=clip_rect(R,foreign)
        page.add_redact_annot(rects[u['id']])
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    for u in us:
        en=safe(tr[str(u['id'])].strip())
        if not en: continue
        R=rects[u['id']]; r0=pymupdf.Rect(u['rect']); bold=bool(u.get('bold'))
        if u['kind']=='prose':
            box=pymupdf.Rect(r0.x0,R.y0-1.0,max(r0.x1,BODY_R),r0.y1+3.0)
            fit_box(page,box,en,min(u['size'],11.0),pymupdf.TEXT_ALIGN_JUSTIFY,bold)
        elif '@@' in en:
            left,right=[p.strip() for p in en.split('@@',1)]
            fnt='tibo' if bold else 'tiro'
            cy=(R.y0+R.y1)/2; h=max(R.height,u['size']*1.15)
            x0=r0.x0; x1=max(r0.x1,BODY_R); s=u['size']
            while s>=6.0:
                lw=pymupdf.get_text_length(left+'  ',fontname=fnt,fontsize=s)
                rw=pymupdf.get_text_length('  '+right,fontname=fnt,fontsize=s)
                if lw+rw+12<=(x1-x0): break
                s-=0.25
            dw=pymupdf.get_text_length('.',fontname=fnt,fontsize=s) or 1
            nd=max(2,int(((x1-x0)-lw-rw)/dw))
            page.insert_textbox(pymupdf.Rect(x0,cy-h*0.70,x1,cy+h*0.85),
                                left+'  '+'.'*nd+'  '+right,fontsize=s,fontname=fnt,
                                align=pymupdf.TEXT_ALIGN_LEFT)
        else:
            cx=(r0.x0+r0.x1)/2; cy=(R.y0+R.y1)/2; h=max(R.height,u['size']*1.15)
            centred = abs(cx-298.0)<26 or r0.x0>96
            if centred:
                s=u['size']
                while s>=5.5:
                    half=pymupdf.get_text_length(en,fontname='tibo' if bold else 'tiro',fontsize=s)/2+1
                    if cx-half>=PAGE_L and cx+half<=PAGE_R: break
                    s-=0.25
                half=max(pymupdf.get_text_length(en,fontname='tibo' if bold else 'tiro',fontsize=s)/2+1,6)
                box=pymupdf.Rect(max(PAGE_L,cx-half),cy-h*0.70,min(PAGE_R,cx+half),cy+h*0.85)
                fit_box(page,box,en,s,pymupdf.TEXT_ALIGN_CENTER,bold,5.5)
            else:
                box=pymupdf.Rect(r0.x0,cy-h*0.70,BODY_R,cy+h*0.85)
                fit_box(page,box,en,u['size'],pymupdf.TEXT_ALIGN_LEFT,bold,6.0)
doc.save(out,garbage=3,deflate=True)
print('wrote',out,'| pages touched',len(todo),'| units',sum(len(v) for v in todo.values()))

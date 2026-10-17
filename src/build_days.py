import runpy, html, re, json
g=runpy.run_path('build_map2.py'); t=runpy.run_path('build_todo.py'); h=runpy.run_path('hints.py')
data,paths,xy,TITLES=g['data'],g['paths'],g['xy'],g['TITLES']; T=t['T']; H,SHORT,SPLIT=h['H'],h['SHORT'],h['SPLIT']
E=html.escape
COL=['#1d3a8a','#d6336c','#2f7d4f','#c2410c','#57534e']
DATES=['2026-12-31','2027-01-01','2027-01-02','2027-01-03','2027-01-04']
META=[
 dict(eyebrow="New Year's Eve",long='Thursday, December 31',hotel='Hilton Garden Inn Times Square South',art='nye',
      lead="Land, drop bags, then the holiday classics: Macy's windows, an Empire State view lunch, the tree, Fifth Ave and Central Park at sunset. Then dress up for Bond 45 and a midnight birthday toast.",
      wear='Warm coat and walking shoes by day. Festive cocktail wear for Bond 45, plus a coat you can check.',
      sticker='Midnight toast'),
 dict(eyebrow='Your birthday',long='Friday, January 1',hotel='Hilton Garden Inn Times Square South',art='bday',
      lead='Bagels, two ferries past the Statue of Liberty, the Charging Bull, a Din Tai Fung birthday lunch, Times Square in daylight, Bryant Park, then Toloache and the Rockettes. Early bedtime.',
      wear='Warm layers and a hat for the ferry decks, which get windy. Dressy casual for the Rockettes.',
      sticker='Happy birthday!'),
 dict(eyebrow='The big day out',long='Saturday, January 2',hotel='Hilton Garden Inn Times Square South',art='mid',
      lead='First-session skating at Rockefeller, the 9/11 Memorial, Golden Diner, Chinatown and Little Italy, SoHo shopping, Grand Central, Summit at sunset, and dinner at Carbone.',
      wear="Pants or tights for Summit's mirrored floors (no short skirts, no stilettos). Carbone: no shorts or open-toed shoes, and dressy is the norm.",
      sticker='Skate · shop · Summit'),
 dict(eyebrow='Brooklyn',long='Sunday, January 3',hotel='Hampton Inn Brooklyn Downtown',art='bk',
      lead="Early Mass at St. Patrick's, coffee across the street, then Brooklyn: donuts, the Promenade, the Brooklyn Bridge walk, Juliana's pizza, DUMBO and Pebble Beach at sunset, and River Café.",
      wear="Comfortable shoes for the bridge. River Café is dressy, and jackets are required for men.",
      sticker='Bridge at sunset'),
 dict(eyebrow='Heading home',long='Monday, January 4',hotel='Home',art='fly',
      lead='A scheduled Uber from the Brooklyn hotel to LaGuardia for the 10:30am flight.',
      wear='Travel comfy.',sticker='See you soon, NYC'),
]
TB={}
for r in T: TB.setdefault(r[2],{})[r[0]]=r
def bk(i,prefer='now'):
    v=TB[i]; return v.get(prefer) or v.get('later') or v.get('now')
TD={
 0:[('b','x-stella34'),('b','2-bond-45-nye'),('b','12a-uber-lga-arrival'),('d',"Screenshot the Bond 45 confirmation email"),('d',"Pack the NYE outfit in your carry-on in case bags are late"),('d',"Ask the front desk to hold your bags at 11")],
 1:[('b','5-din-tai-fung','later'),('b','3-toloache'),('b','13a-nyc-ferry-st-george'),('x','Rockettes, 7:00pm','Booked'),('d',"Check Utopia's Jan 1 hours on Google"),('d','Buy NYC Ferry tickets in the app ($4.50 each)'),('d','Rockettes tickets ready on your phone')],
 2:[('b','10-rockefeller-rink'),('b','9-911-museum'),('b','7-golden-diner','later'),('b','8-summit'),('b','6-carbone','later'),('b','11-losers-roll','later'),('d','Rink, museum and Summit tickets ready on your phone'),('d','Pants or tights for Summit')],
 3:[('b','1-river-cafe'),('d',"Check the Epiphany Sunday Mass times that week"),('d','Pack your bags before Mass'),('d','Book the 9:00 Uber to Brooklyn in the app'),('d','Confirm the DUMBO stop in the NYC Ferry app'),('d','Jacket for River Café')],
 4:[('b','12b-uber-brooklyn-departure'),('d','Pack the night before'),('d','Check the flight status at 7am')],
}
MTA={'A':'#0039A6','C':'#0039A6','E':'#0039A6','B':'#FF6319','D':'#FF6319','F':'#FF6319','M':'#FF6319','N':'#FCCC0A','Q':'#FCCC0A','R':'#FCCC0A','W':'#FCCC0A','1':'#EE352E','2':'#EE352E','3':'#EE352E','4':'#00933C','5':'#00933C','6':'#00933C','7':'#B933AD','G':'#6CBE45','L':'#A7A9AC'}
def bullets(txt):
    s=E(txt)
    def rep(m): return '<span class="lines">'+''.join(f'<span class="sub" style="background:{MTA[c]};color:{"#111" if MTA[c]=="#FCCC0A" else "#fff"}">{c}</span>' for c in m.group(1).split('/'))+'</span>'
    return re.sub(r'(?<![\w/])((?:[ACEBDFMNQRW1-7])(?:/[ACEBDFMNQRW1-7])*)(?= (?:from|train)\b)',rep,s)
def short_t(x):
    x=x.replace('~','');x=x.replace(':00','');return x
def mins(x):
    m=re.search(r'(\d+)(?::(\d+))?(am|pm)',x); hh=int(m.group(1))%12+(12 if m.group(3)=='pm' else 0); return hh*60+int(m.group(2) or 0)
for d in data:
    prev=-1
    for s in d['stops']:
        m=mins(s['time'])
        if m<prev: m+=1440
        s['min']=m; prev=m
def lab(x,y,fs,anc,tm,name,col,two=False):
    if two: inner=lambda c:f'<tspan class="lt" {c}>{E(tm)}</tspan><tspan x="{x:.2f}" dy="1.1em">{E(name)}</tspan>'
    else: inner=lambda c:f'<tspan class="lt" {c}>{E(tm)}</tspan> {E(name)}'
    a=f'x="{x:.2f}" y="{y:.2f}" font-size="{fs:.2f}" text-anchor="{anc}"'
    return f'<text {a} class="lbl halo" aria-hidden="true">{inner("")}</text><text {a} class="lbl">{inner(f"fill={chr(34)}{col}{chr(34)}")}</text>'
def mapsvg(di,d,cap,nums):
    col=COL[di]; S=[s for s in d['stops'] if s['n'] in nums]
    P={s['n']:xy(s['lat'],s['lon']) for s in S}
    xs=[p[0] for p in P.values()]; ys=[p[1] for p in P.values()]
    w=max(max(xs)-min(xs),8); hh=max(max(ys)-min(ys),8); span=max(w,hh)
    fs=span/15 if len(S)>3 else span/9; r=fs*0.62
    places={}
    for s in S: places.setdefault(s['key'],[]).append(s)
    def place(fs):
        r=fs*0.62
        placed=[]; pins=[]; labels=[]
        allp=list(P.values())
        for k,vis in places.items():
            x,y=P[vis[0]['n']]; ns=[v['n'] for v in vis]
            name=SHORT.get(vis[0]['label'],vis[0]['label']); tm=short_t(vis[0]['time'])+(f' +{len(vis)-1}' if len(vis)>1 else '')
            pins.append(f'<g class="dpin" tabindex="0" role="button" aria-label="Stop {",".join(map(str,ns))}: {E(vis[0]["label"])} at {E(tm)}" data-n="{ns[0]}"><circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{col}" class="pinc"/><text x="{x:.2f}" y="{y+r*0.38:.2f}" font-size="{r*1.05:.2f}" class="pinn">{ns[0] if len(ns)==1 else ns[0]}</text></g>')
            lw=(len(name)+len(tm)+1)*fs*0.63; best=None
            for dx,dy,anc in [(r*1.5,fs*0.35,'start'),(-r*1.5,fs*0.35,'end'),(0,-r*1.6,'middle'),(0,r*1.6+fs*0.75,'middle'),(r*1.4,-fs*0.7,'start'),(-r*1.4,-fs*0.7,'end'),(r*1.4,fs*1.35,'start'),(-r*1.4,fs*1.35,'end'),(r*1.4,-fs*1.9,'start'),(-r*1.4,-fs*1.9,'end'),(r*1.4,fs*2.4,'start'),(-r*1.4,fs*2.4,'end'),(0,-r*1.6-fs*1.1,'middle'),(0,r*1.6+fs*1.85,'middle')]:
                lx=x+dx-(lw if anc=='end' else lw/2 if anc=='middle' else 0); ly=y+dy-fs*0.85; box=(lx,ly,lx+lw,ly+fs*1.05)
                hit=sum(3 for b in placed if not (box[2]<b[0] or box[0]>b[2] or box[3]<b[1] or box[1]>b[3]))
                hit+=sum(1 for q in allp if box[0]-r<q[0]<box[2]+r and box[1]-r<q[1]<box[3]+r and q!=(x,y))
                if best is None or hit<best[0]: best=(hit,dx,dy,anc,box)
                if hit==0: break
            _,dx,dy,anc,box=best; placed.append(box)
            labels.append(lab(x+dx,y+dy,fs,anc,tm,name,col))
        bx0=min([q[0] for q in placed]+[min(xs)-r]); by0=min([q[1] for q in placed]+[min(ys)-r]); bx1=max([q[2] for q in placed]+[max(xs)+r]); by1=max([q[3] for q in placed]+[max(ys)+r])
        return r,pins,labels,placed,(bx0,by0,bx1,by1)
    for _ in range(8):
        r,pins,labels,placed,(bx0,by0,bx1,by1)=place(fs)
        ratio=(bx1-bx0+2*fs)/fs
        if ratio<=32: break
        fs*= (ratio/32)**0.5
    if ratio>32:
        fs=span/10; r=fs*0.62; pins=[]; labels=[]; placed=[]
        items=[]
        for k,vis in places.items():
            x,y=P[vis[0]['n']]; ns=[v['n'] for v in vis]
            name=SHORT.get(vis[0]['label'],vis[0]['label']); tm=short_t(vis[0]['time'])+(f' +{len(vis)-1}' if len(vis)>1 else '')
            pins.append(f'<g class="dpin" tabindex="0" role="button" aria-label="Stop {",".join(map(str,ns))}: {E(vis[0]["label"])} at {E(tm)}" data-n="{ns[0]}"><circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{col}" class="pinc"/><text x="{x:.2f}" y="{y+r*0.38:.2f}" font-size="{r*1.05:.2f}" class="pinn">{ns[0]}</text></g>')
            items.append((x,y,name,tm))
        mx=sorted(i[0] for i in items)[len(items)//2]
        L=[i for i in items if i[0]<mx]; R=[i for i in items if i[0]>=mx]
        for side,grp,colx,anc in [(0,L,min(xs)-2.2*fs,'end'),(1,R,max(xs)+2.2*fs,'start')]:
            grp.sort(key=lambda i:i[1]); prev=-1e9
            for x,y,name,tm in grp:
                ly=max(y-fs*0.2,prev+fs*2.7); prev=ly; lw=max(len(name),len(tm))*fs*0.63
                ex=colx+(0.3*fs if anc=='end' else -0.3*fs)
                labels.append(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{ex:.2f}" y2="{ly+fs*0.2:.2f}" stroke="{col}" stroke-width="{fs*0.08:.2f}" opacity=".7"/>')
                labels.append(lab(colx,ly,fs,anc,tm,name,col,True))
                bx=(colx-lw if anc=='end' else colx); placed.append((bx,ly-fs*0.9,bx+lw,ly+fs*1.4))
        labels=[l for l in labels if l.startswith('<line')]+[l for l in labels if not l.startswith('<line')]
        bx0=min([q[0] for q in placed]+[min(xs)-r]); by0=min([q[1] for q in placed]+[min(ys)-r]); bx1=max([q[2] for q in placed]+[max(xs)+r]); by1=max([q[3] for q in placed]+[max(ys)+r])
    m=fs*1.0; bx0-=m;by0-=m;bx1+=m;by1+=m; W_=bx1-bx0; H_=by1-by0
    if H_<W_*0.5: c=(by0+by1)/2; H_=W_*0.5; by0=c-H_/2
    if W_<H_*0.8: c=(bx0+bx1)/2; W_=H_*0.8; bx0=c-W_/2
    seg=[]
    st=d['stops']
    for a,b in zip(st,st[1:]):
        if a['n'] in nums and b['n'] in nums: seg.append(f'M{P[a["n"]][0]:.2f},{P[a["n"]][1]:.2f} L{P[b["n"]][0]:.2f},{P[b["n"]][1]:.2f}')
    return (f'<figure class="mapwrap"><div class="mapcap">{E(cap)}</div><svg class="dmap" viewBox="{bx0:.1f} {by0:.1f} {W_:.1f} {H_:.1f}" role="img" aria-label="{E(cap)} map, stops {", ".join(map(str,sorted(nums)))}">'
            f'<rect x="{bx0-50:.0f}" y="{by0-50:.0f}" width="{W_+100:.0f}" height="{H_+100:.0f}" class="water"/><use href="#landshapes"/>'
            f'<path d="{" ".join(seg)}" fill="none" stroke="{col}" stroke-width="{r*0.32:.2f}" stroke-dasharray="{r*0.9:.2f} {r*0.6:.2f}" stroke-linecap="round"/>'
            +''.join(l for l in labels if l.startswith('<line'))+''.join(pins)+''.join(l for l in labels if not l.startswith('<line'))+'</svg></figure>')
# --- art ---
def bld(x,w,hh,base=110): return f'<rect x="{x}" y="{base-hh}" width="{w}" height="{hh}"/>'
def skyline(extra=''):
    b=[(0,30,40),(28,22,58),(48,34,46),(80,18,70),(96,30,52),(124,26,64),(148,40,44),(186,22,80),(206,30,56),(234,24,48),(256,36,62),(290,20,74),(308,28,50),(334,38,60),(370,22,44),(390,30,68),(418,26,54),(442,34,40),(474,22,58),(494,32,48),(524,26,66),(548,30,44),(576,24,56)]
    s=''.join(bld(*t) for t in b)
    esb='<path d="M150 110V52h6V40h5V28h4V12h2V2h1v10h2v16h4v12h5v12h6v58z"/>'
    chr_='<path d="M396 110V46h4l4-10 4-8 3-10 2-12 2 12 3 10 4 8 4 10h4v64z"/>'
    return f'<svg class="sky" viewBox="0 0 600 112" preserveAspectRatio="xMidYMax meet" aria-hidden="true"><g class="skyg">{s}{esb}{chr_}</g>{extra}</svg>'
def fireworks():
    out=''
    for cx,cy,c in [(70,28,'#f5c518'),(300,18,'#f472b6'),(520,30,'#93c5fd')]:
        for k in range(12):
            import math; a=k*math.pi/6; out+=f'<line x1="{cx+5*math.cos(a):.1f}" y1="{cy+5*math.sin(a):.1f}" x2="{cx+16*math.cos(a):.1f}" y2="{cy+16*math.sin(a):.1f}" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
    return out
def confetti():
    import random; random.seed(4); cols=['#f5c518','#f472b6','#60a5fa','#34d399']
    return ''.join(f'<rect x="{random.randint(5,595)}" y="{random.randint(2,40)}" width="5" height="9" rx="1" fill="{random.choice(cols)}" transform="rotate({random.randint(0,90)} {0} {0})"/>' for _ in range(28)).replace('rotate(','rotate(')
def bridge():
    return ('<svg class="sky" viewBox="0 0 600 112" preserveAspectRatio="xMidYMax meet" aria-hidden="true"><g class="skyg">'
     '<rect x="0" y="86" width="600" height="6"/>'
     '<path d="M150 112V22h40v90h-12V60a8 8 0 0 0-16 0v52z"/><path d="M410 112V22h40v90h-12V60a8 8 0 0 0-16 0v52z"/>'
     '<path d="M0 30 Q85 84 170 22 Q300 110 430 22 Q515 84 600 30" fill="none" stroke-width="3" class="cable"/>'
     +''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="86" class="cable" stroke-width="1"/>' for x,y in [(30,44),(60,58),(95,64),(125,58),(215,52),(250,68),(300,76),(350,68),(385,52),(475,58),(505,64),(540,58),(570,44)])+
     '</g></svg>')
def plane(): return '<path d="M470 30l40 8 22-14 6 3-14 16 26 6 6-6 5 2-6 10 2 3-10 2-6 6-4-2 3-8-26-6-12 18-7-1 6-22-38-8z" fill="#f5c518"/>'
ART={'nye':lambda:skyline(fireworks()),'bday':lambda:skyline(confetti()),'mid':lambda:skyline(),'bk':bridge,'fly':lambda:skyline(plane())}
# --- todo items ---
def todo_html(di):
    out=[]
    for it in TD[di]:
        if it[0]=='b':
            r=bk(it[1],it[2] if len(it)>2 else 'now'); key=f'b:{r[2]}:{r[0]}'
            when='Book now' if r[0]=='now' else r[1]
            out.append(f'<li><label><input type="checkbox" data-k="{E(key)}"><span><strong>{E(r[3])}</strong> <em class="when">{E(when)}</em><br><small>{E(r[5])}</small> <a href="{E(r[6])}" target="_blank" rel="noopener">{E(r[7])}</a></span></label></li>')
        elif it[0]=='x':
            out.append(f'<li class="booked"><span class="tick" aria-hidden="true">✓</span><span><strong>{E(it[1])}</strong> <em class="when">{E(it[2])}</em></span></li>')
        else:
            out.append(f'<li><label><input type="checkbox" data-k="d:{di}:{E(it[1][:30])}"><span>{E(it[1])}</span></label></li>')
    return '<ul class="todo">'+''.join(out)+'</ul>'
# --- book page ---
rows=[]
for r in T:
    key=f'b:{r[2]}:{r[0]}'
    rows.append(f'<li><label><input type="checkbox" data-k="{E(key)}"><span><span class="whenbig">{E("Now" if r[0]=="now" else r[1])}</span><strong>{E(r[3])}</strong> · <span class="for">{E(r[4])}</span><br><small>{E(r[5])}</small> <a href="{E(r[6])}" target="_blank" rel="noopener">{E(r[7])}</a></span></label></li>')
bookpanel=f'''<section class="dpanel bookp" role="tabpanel" id="p0" aria-labelledby="t0" style="--c:#b45309" hidden>
<div class="post"><div class="stamp">Booking list</div><h2 class="dtitle">Everything to book</h2><p class="lead">In the order each one opens. Ticks save on this phone and match the ticks on each day's page. Nothing is booked yet except the Rockettes.</p></div>
<ol class="todo bigtodo">{"".join(rows)}</ol></section>'''
tabs=['<button type="button" role="tab" id="t0" aria-controls="p0" aria-selected="false" tabindex="-1" style="--c:#b45309"><span class="tday">To do</span><span class="tdate">Book</span></button>']
panels=[bookpanel]
for di,(d,m) in enumerate(zip(data,META)):
    col=COL[di]; pid=di+1
    tabs.append(f'<button type="button" role="tab" id="t{pid}" aria-controls="p{pid}" aria-selected="false" tabindex="-1" style="--c:{col}"><span class="tday">{E(d["name"].split(" ",1)[0])}</span><span class="tdate">{E(d["name"].split(" ",1)[1])}</span></button>')
    items=[]
    for s in d['stops']:
        go,tips=H.get((di,s['n']),(None,[]))
        how=''
        if s.get('how'):
            how=f'<div class="how"><span class="howt">{bullets(go or s["how"])}</span> <a href="{E(s["apple"])}" target="_blank" rel="noopener">Apple Maps</a> · <a href="{E(s["google"])}" target="_blank" rel="noopener">Google</a></div>'
        tip=''.join(f'<li>{E(x)}</li>' for x in tips)
        note=s['note'] if s['note'] and not any(s['note'].split('.')[0] in x for x in tips) else s['note']
        items.append(f'<li class="stop" data-n="{s["n"]}" data-min="{s["min"]}" data-name="{E(s["label"])}" data-time="{E(s["time"])}" data-how="{E(go or s.get("how",""))}" data-g="{E(s.get("google",""))}">{how}<div class="row"><span class="num">{s["n"]}</span><div class="body"><div class="time">{E(s["time"])}</div><div class="name">{E(s["label"])}</div>{f"<div class=note>{E(note)}</div>" if note else ""}{f"<ul class=tips>{tip}</ul>" if tip else ""}<div class="addr">{E(s["addr"])}</div></div><button type="button" class="done" aria-pressed="false" data-k="s:{di}:{s["n"]}" aria-label="Mark {E(s["label"])} done">✓</button></div></li>')
    maps=''.join(mapsvg(di,d,cap,set(ns)) for cap,ns in SPLIT[di])
    nav=(f'<button type="button" class="pn" data-go="{pid-1}">← {"Book" if pid==1 else data[di-1]["name"]}</button>')+(f'<button type="button" class="pn" data-go="{pid+1}">{data[di+1]["name"]} →</button>' if di<len(data)-1 else '<span></span>')
    panels.append(f'''<section class="dpanel" role="tabpanel" id="p{pid}" aria-labelledby="t{pid}" style="--c:{col}" data-date="{DATES[di]}" hidden>
<div class="post">{ART[m["art"]]()}<div class="stamp">Day {di+1} · {E(m["eyebrow"])}</div><h2 class="dtitle">{E(m["long"])}</h2><p class="dsub">{E(TITLES[di])}</p><span class="sticker">{E(m["sticker"])}</span><p class="lead">{E(m["lead"])}</p>
<dl class="facts"><div><dt>Stops</dt><dd>{len(d["stops"])}</dd></div><div><dt>Sleep</dt><dd>{E(m["hotel"])}</dd></div></dl></div>
<div class="live" hidden></div>
<div class="dgrid"><div class="maps">{maps}<p class="mapnote">Tap a number to jump to that stop. Times are next to each name.</p></div>
<div><h3 class="h3">The plan</h3><ol class="stops">{"".join(items)}</ol></div></div>
<div class="extras"><div class="xcard"><h3>To do</h3>{todo_html(di)}</div><div class="xcard"><h3>What to wear</h3><p>{E(m["wear"])}</p></div></div>
<nav class="pnav" aria-label="Day navigation">{nav}</nav></section>''')
CSS=open('days.css').read(); JS=open('days.js').read()
checker='<svg class="checker" viewBox="0 0 240 8" preserveAspectRatio="none" aria-hidden="true">'+''.join(f'<rect x="{i*8}" y="{(i%2)*4}" width="8" height="4"/>' for i in range(30))+'</svg>'
body=('<style>'+CSS+'</style><div class="trip">'
 '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="landshapes">'+''.join(f'<path d="{p}" class="land"/>' for p in paths)+'</g></defs></svg>'
 +checker+'<div class="tripmode" id="tripmode"></div>'
 +f'<div class="dtabs" role="tablist" aria-label="Trip days">{"".join(tabs)}</div>'+''.join(panels)+'</div><script>'+JS+'</script>')
open('days-body.html','w').write(body); print('ok',len(body))

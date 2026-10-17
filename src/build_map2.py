import json, math, html
raw=json.load(open('map-stops.json')); C=json.load(open('map-coords.json')); geo=json.load(open('boroughs.geojson'))
R=list(raw.values()); HIL=R[0][1]; HAM=R[3][2]
# (stop key, time, short label, note)
D=[
 [(R[0][0],'10:00am','LaGuardia (LGA)','Land. Uber/taxi to the hotel.'),(HIL,'~11:00am','Hilton Garden Inn (hotel)','Bag drop.'),(R[0][8],'11:30am',"Macy's windows",'Holiday windows on Broadway and 34th; buffer if the flight is late.'),(R[0][8],'1:30pm','Stella 34 Trattoria','Lunch on Macy\'s 6th floor, with Empire State Building views. Book on OpenTable.'),(R[0][3],'3:00pm','Rockefeller tree','Tree, Channel Gardens and the plaza.'),(R[0][4],'3:30pm','Bergdorf Goodman','Holiday windows.'),(R[0][5],'~3:40pm','Tiffany & Co.','Fifth Ave flagship windows.'),(R[0][6],'~3:50pm','The Plaza','Hotel lobby and fountain.'),(R[0][7],'4:00pm','Gapstow Bridge','Central Park Pond skyline photo, close to sunset.'),(HIL,'4:40pm','Hilton Garden Inn (hotel)','Change for NYE. Leave 5:45.'),(R[0][9],'6:30pm','Bond 45','NYE party: dinner, open bar, midnight toast.'),(HIL,'~12:30am','Hilton Garden Inn (hotel)','Walk back after midnight.')],
 [(HIL,'~8:40am','Hilton Garden Inn (hotel)','Leave for breakfast.'),(R[1][0],'9:00am','Utopia Bagels','Birthday breakfast. Then E train at Lexington Av/53 St to World Trade Center.'),(R[1][1],'~10:45am','NYC Ferry · Vesey St','St. George route, ride past the Statue of Liberty.'),(R[1][2],'~11:10am','St. George terminal','Switch to the free Staten Island Ferry.'),(R[1][3],'~11:50am','Whitehall terminal','Back in Manhattan.'),(R[1][4],'~12:05pm','Charging Bull','Then Wall St, and the R/W to 49 St.'),(R[1][5],'1:00pm','Din Tai Fung','Birthday lunch. Reservations open Dec 2 at midnight.'),(R[1][6],'2:30pm','Times Square','Daylight look and the red TKTS steps.'),(R[1][7],'3:00pm','Bryant Park Winter Village','Holiday market and rink.'),(R[1][8],'~3:20pm','NYPL lions','Library is closed Jan 1; the lions are outside.'),(HIL,'3:45pm','Hilton Garden Inn (hotel)','Rest and change.'),(R[1][9],'5:00pm','Toloache','Birthday dinner before the show.'),(R[1][10],'7:00pm','Radio City (Rockettes)','Booked. Then straight to bed.'),(HIL,'~8:45pm','Hilton Garden Inn (hotel)','Early night.')],
 [(HIL,'6:45am','Hilton Garden Inn (hotel)','Leave for breakfast.'),(R[2][0],'7:00am','Liberty Bagels','Quick breakfast.'),(R[2][1],'8:00am','Rockefeller Rink','First skating session.'),(R[2][8],'9:45am','9/11 Memorial & Museum','Timed entry.'),(R[2][2],'11:00am','Golden Diner','Brunch. Set Resy Notify or join the walk-in list ~10:45.'),(R[2][3],'12:15pm','Canal Street','Chinatown walk.'),(R[2][4],'~12:40pm','Little Italy (Mulberry St)',''),(R[2][5],'1:15pm','Old Friend Photobooth','Walk-in photobooth.'),(R[2][6],'1:45pm','New York or Nowhere','SoHo shopping on Prince, Spring, Broadway and Greene.'),(R[2][7],'~2:45pm',"Loser's (optional)",'Cinnamon roll pickup if you got a pre-order.'),(R[2][9],'3:45pm','Grand Central','Main concourse and the ceiling.'),(R[2][10],'~4:00pm','Summit One Vanderbilt','Sunset is about 4:40.'),(HIL,'5:40pm','Hilton Garden Inn (hotel)','Change for dinner.'),(R[2][11],'7:00pm','Carbone','Dinner.'),(HIL,'~9:30pm','Hilton Garden Inn (hotel)','')],
 [(HIL,'6:30am','Hilton Garden Inn (hotel)','Check out and leave bags with the front desk.'),(R[3][0],'7:00am',"St. Patrick's Cathedral",'Mass.'),(R[3][1],'8:00am',"Ralph's Coffee truck",'Coffee across from the cathedral.'),(HIL,'8:30am','Hilton Garden Inn (hotel)','Pick up bags.'),(HAM,'~9:30am','Hampton Inn Brooklyn (hotel)','Uber at 9:00. Drop bags.'),(R[3][3],'10:00am','Cloudy Donut','Donuts in Brooklyn Heights.'),(R[3][4],'10:30am','Brooklyn Heights Promenade','Skyline and Statue views.'),(R[3][9],'11:30am','Brooklyn Bridge walk','Walk into Manhattan in daylight.'),(R[3][10],'12:30pm','Pier 11 ferry','NYC Ferry back to DUMBO.'),(R[3][5],'~12:45pm','DUMBO ferry landing',''),(R[3][7],'1:00pm',"Juliana's Pizza",'No reservations; expect a short line.'),(HAM,'2:15pm','Hampton Inn Brooklyn (hotel)','Check in and rest.'),(R[3][6],'3:45pm',"Jane's Carousel",'Open until 5:50pm.'),(R[3][5],'~4:05pm','DUMBO · Washington St','The Manhattan Bridge photo.'),(R[3][8],'4:15pm','Pebble Beach','Sunset is about 4:41.'),(R[3][11],'7:00pm','The River Café','Dinner. Jackets required for men.'),(HAM,'~9:30pm','Hampton Inn Brooklyn (hotel)','')],
 [(HAM,'7:45am','Hampton Inn Brooklyn (hotel)','Scheduled UberX to LGA.'),(R[4][1],'~8:30am','LaGuardia (LGA)','Flight at 10:30am.')]]
LAT0,LAT1,LON0,LON1=40.625,40.782,-74.085,-73.862
K=math.cos(math.radians(40.72)); W=1000; H=round(W*(LAT1-LAT0)/((LON1-LON0)*K))
def xy(lat,lon): return ((lon-LON0)/(LON1-LON0)*W, (LAT1-lat)/(LAT1-LAT0)*H)
paths=[]
for f in geo['features']:
    g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    for poly in polys:
        ring=poly[0]
        if len(ring)<20: continue
        step=max(1,len(ring)//400)
        paths.append('M'+' L'.join('%.1f,%.1f'%xy(la,lo) for lo,la in ring[::step])+' Z')
COL=['#2563eb','#db2777','#059669','#d97706','#6b7280']
NAMES=['Thu Dec 31','Fri Jan 1','Sat Jan 2','Sun Jan 3','Mon Jan 4']
TITLES=['Arrival, Midtown and NYE','Birthday: ferries, Din Tai Fung, Rockettes','Skating, downtown, SoHo, Summit, Carbone','Mass, then Brooklyn at sunset','Fly home']
def hav(a,b):
    la1,lo1,la2,lo2=map(math.radians,[a[0],a[1],b[0],b[1]])
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*6371*math.asin(math.sqrt(h))
FERRY={('NYC Ferry · Vesey St','St. George terminal'):'NYC Ferry, about 20 min',('St. George terminal','Whitehall terminal'):'Staten Island Ferry, about 25 min, free',('Pier 11 ferry','DUMBO ferry landing'):'NYC Ferry, about 10 min'}
def links(ca,cb,walk):
    am='w' if walk else 'r'; gm='walking' if walk else 'transit'
    return (f'https://maps.apple.com/?saddr={ca[0]},{ca[1]}&daddr={cb[0]},{cb[1]}&dirflg={am}',f'https://www.google.com/maps/dir/?api=1&origin={ca[0]},{ca[1]}&destination={cb[0]},{cb[1]}&travelmode={gm}')
data=[];VB=[];svg_days=[];sections=[]
for di,stops in enumerate(D):
    col=COL[di]; seq=[]
    for i,(k,t,lbl,note) in enumerate(stops):
        c=C[k]; addr=', '.join(k.split(',')[1:]).strip()
        seq.append(dict(n=i+1,key=k,time=t,label=lbl,note=note,lat=c[0],lon=c[1],addr=addr))
    legs=[]
    for i in range(len(seq)-1):
        a,b=seq[i],seq[i+1]; ca=(a['lat'],a['lon']); cb=(b['lat'],b['lon'])
        km=hav(ca,cb); walk=round(km*1.3/4.8*60)
        how=FERRY.get((a['label'],b['label'])) or ('Same place' if km<0.05 else f'About {max(1,walk)} min walk' if walk<=25 else f'{km*0.621:.1f} mi: subway or Uber')
        iswalk=walk<=25 and (a['label'],b['label']) not in FERRY
        ap,gg=links(ca,cb,iswalk); legs.append(dict(i=i,frm=a['n'],to=b['n'],how=how,apple=ap,google=gg))
        b['how']=how; b['apple']=ap; b['google']=gg; b['from']=a['label']
    # unique places
    places={}
    for s in seq: places.setdefault(s['key'],[]).append(s)
    core=[(s['lat'],s['lon']) for s in seq if not (s['lat']>40.77 and s['lon']>-73.9) and s['lat']>40.65] or [(s['lat'],s['lon']) for s in seq]
    xs=[xy(*c)[0] for c in core]; ys=[xy(*c)[1] for c in core]
    pad=45; vx,vy=min(xs)-pad,min(ys)-pad; vw,vh=max(xs)-min(xs)+2*pad,max(ys)-min(ys)+2*pad
    side=max(vw,vh*1.2,300); vx-=(side-vw)/2; vh2=side/1.2; vy-=(vh2-vh)/2
    VB.append('%.0f %.0f %.0f %.0f'%(vx,vy,side,vh2))
    line=' '.join('%.1f,%.1f'%xy(s['lat'],s['lon']) for s in seq)
    g=[f'<g class="day" data-day="{di}"><polyline points="{line}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 4" vector-effect="non-scaling-stroke" opacity="0.8"/>']
    for k,vis in places.items():
        x,y=xy(vis[0]['lat'],vis[0]['lon']); nums=[v['n'] for v in vis]
        lab=vis[0]['label']+' · '+', '.join(str(n) for n in nums)
        g.append(f'<g class="pin" role="button" tabindex="0" aria-label="Stop {", ".join(map(str,nums))}: {html.escape(vis[0]["label"])}" data-day="{di}" data-n="{",".join(map(str,nums))}" data-x="{x:.2f}" data-y="{y:.2f}" style="cursor:pointer"><circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{col}" stroke="#fff" stroke-width="1.5" vector-effect="non-scaling-stroke"/><text class="num" x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" fill="#fff" font-weight="700">{nums[0]}</text><text class="lbl" x="{x:.2f}" y="{y:.2f}" fill="#0f172a" font-weight="600" stroke="#fff" stroke-linejoin="round" paint-order="stroke">{html.escape(lab)}</text></g>')
    g.append('</g>'); svg_days.append(''.join(g))
    data.append(dict(name=NAMES[di],color=col,stops=seq))
    rows=''.join(f'<tr id="leg-{di}-{l["to"]}" data-day="{di}" data-from="{l["frm"]}" data-to="{l["to"]}"><td data-numeric>{l["frm"]}→{l["to"]}</td><td>{html.escape(seq[l["i"]]["label"])} → <strong>{html.escape(seq[l["i"]+1]["label"])}</strong></td><td>{seq[l["i"]+1]["time"]}</td><td>{l["how"]}</td><td><a href="{l["apple"]}" target="_blank" rel="noopener">Apple Maps</a> · <a href="{l["google"]}" target="_blank" rel="noopener">Google Maps</a></td></tr>' for l in legs)
    full='https://www.google.com/maps/dir/'+'/'.join(f'{s["lat"]},{s["lon"]}' for s in seq)
    sections.append(f'''<section class="a-section" id="day-{di}"><h2 class="a-section__title"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{col};margin-right:8px"></span>{NAMES[di]} · {TITLES[di]}</h2>
<p class="a-section__note"><a href="{full}" target="_blank" rel="noopener">Open the whole day as one route in Google Maps</a></p>
<div class="a-table-scroll"><table class="a-table"><caption class="a-visually-hidden">{NAMES[di]} legs</caption><thead><tr><th scope="col" data-numeric>Leg</th><th scope="col">From → to</th><th scope="col">Arrive</th><th scope="col">How</th><th scope="col">Live directions</th></tr></thead><tbody>{rows}</tbody></table></div></section>''')
ax=[list(map(float,v.split())) for v in VB[:4]]
x0=min(b[0] for b in ax);y0=min(b[1] for b in ax);x1=max(b[0]+b[2] for b in ax);y1=max(b[1]+b[3] for b in ax)
side=max(x1-x0,(y1-y0)*1.2);x0-=(side-(x1-x0))/2;hh=side/1.2;y0-=(hh-(y1-y0))/2
ALLVB='%.0f %.0f %.0f %.0f'%(x0,y0,side,hh)
PARK='<polygon points="%s" fill="#bbf7d0" stroke="#86efac" vector-effect="non-scaling-stroke"/>'%' '.join('%.1f,%.1f'%xy(a,b) for a,b in [(40.7681,-73.9819),(40.7642,-73.9730),(40.7968,-73.9493),(40.8006,-73.9582)])
NB=[('Central Park',40.772,-73.968),('Midtown',40.757,-73.998),('SoHo',40.7235,-74.004),('Chinatown',40.7155,-73.9985),('Lower East Side',40.7175,-73.984),('Financial District',40.7065,-74.0085),('DUMBO',40.7045,-73.984),('Brooklyn Heights',40.6965,-73.9945),('Downtown Brooklyn',40.6905,-73.984)]
BIG=[('MANHATTAN',40.775,-73.975),('BROOKLYN',40.668,-73.955),('QUEENS',40.745,-73.895),('STATEN ISLAND',40.632,-74.072),('HUDSON RIVER',40.745,-74.035),('EAST RIVER',40.738,-73.966)]
nb=''.join('<text class="nb" x="%.1f" y="%.1f" fill="#64748b" font-style="italic" text-anchor="middle">%s</text>'%(*xy(la,lo),t) for t,la,lo in NB)
big=''.join('<text class="big" x="%.1f" y="%.1f" fill="#94a3b8" letter-spacing="2" text-anchor="middle">%s</text>'%(*xy(la,lo),t) for t,la,lo in BIG)
btns='<button type="button" class="daybtn" data-day="all" data-vb="%s">All days</button>'%ALLVB+''.join(f'<button type="button" class="daybtn" data-day="{i}" data-vb="{VB[i]}"><span class="dot" style="background:{COL[i]}"></span>{NAMES[i]}</button>' for i in range(5))
body=f'''<section class="a-section">
<p class="a-prose">Pick a day to zoom in and see every stop labeled. Drag to move the map; use + and −, double-tap, or pinch to zoom in on crowded spots like DUMBO. <strong>Tap any pin</strong> for its time, address and one-tap directions from the previous stop. Numbers are the visiting order; a place you pass more than once (like the hotel) lists every visit.</p>
<div class="daybar" role="group" aria-label="Choose a day">{btns}</div>
<figure class="a-panel mapfig"><div class="zoomctl" role="group" aria-label="Zoom"><button type="button" id="zin" aria-label="Zoom in">+</button><button type="button" id="zout" aria-label="Zoom out">−</button><button type="button" id="zreset" aria-label="Reset view">⟲</button></div><svg id="tripmap" viewBox="{VB[0]}" role="img" aria-label="Map of Manhattan and Brooklyn with trip stops" preserveAspectRatio="xMidYMid meet">
<rect x="-2000" y="-2000" width="5000" height="5000" fill="#dbeafe"/><g fill="#f8fafc" stroke="#94a3b8" stroke-width="0.8">{''.join(f'<path d="{p}" vector-effect="non-scaling-stroke"/>' for p in paths)}</g>{PARK}{big}{nb}{''.join(svg_days)}</svg></figure>
<div id="stopinfo" class="a-panel stopinfo" aria-live="polite"><p class="a-section__note">Tap a pin to see details here.</p></div>
</section><hr>
{'<hr>'.join(sections)}
<script id="tripdata" type="application/json">{json.dumps(data)}</script>
<script>
(function(){{
var T=JSON.parse(document.getElementById('tripdata').textContent);
var svg=document.getElementById('tripmap'),info=document.getElementById('stopinfo'),cur='0';
var btns=document.querySelectorAll('.daybtn');
function esc(s){{return String(s).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
function layout(){{
  var vb=svg.viewBox.baseVal,w=svg.getBoundingClientRect().width||800,s=vb.width/w;
  var r=(w<500?9:10)*s,fs=(w<500?10:12)*s,boxes=[];
  svg.querySelectorAll('.nb').forEach(function(t){{t.setAttribute('font-size',(11*s).toFixed(2));t.style.display=cur==='all'?'none':'';}});
  svg.querySelectorAll('.big').forEach(function(t){{t.setAttribute('font-size',(13*s).toFixed(2));}});
  var pins=[].slice.call(svg.querySelectorAll('g.day:not([style*="none"]) .pin'));
  pins.forEach(function(p){{var x=+p.dataset.x,y=+p.dataset.y;boxes.push([x-r,y-r,x+r,y+r]);}});
  pins.forEach(function(p){{
    var x=+p.dataset.x,y=+p.dataset.y,c=p.querySelector('circle'),n=p.querySelector('.num'),l=p.querySelector('.lbl');
    var all=cur==='all';c.setAttribute('r',(all?0.75*r:r).toFixed(2));n.setAttribute('font-size',((all?0.75:1)*fs*0.95).toFixed(2));
    l.style.display=all?'none':'';if(all)return;
    l.setAttribute('font-size',fs.toFixed(2));l.setAttribute('stroke-width',(3*s).toFixed(2));
    var tw=l.textContent.length*fs*0.56,th=fs*1.1,g=r+3*s;
    var cand=[[x+g,y+fs*0.35,'start',x+g,y-th/2,x+g+tw,y+th/2],[x-g,y+fs*0.35,'end',x-g-tw,y-th/2,x-g,y+th/2],[x,y-g-fs*0.25,'middle',x-tw/2,y-g-th,x+tw/2,y-g],[x,y+g+fs*0.9,'middle',x-tw/2,y+g,x+tw/2,y+g+th],
      [x+g,y-g,'start',x+g,y-g-th,x+g+tw,y-g],[x+g,y+g+fs*0.7,'start',x+g,y+g,x+g+tw,y+g+th],[x-g,y-g,'end',x-g-tw,y-g-th,x-g,y-g],[x-g,y+g+fs*0.7,'end',x-g-tw,y+g,x-g,y+g+th]];
    var far=cand.map(function(c){{var dx=(c[3]+c[5])/2-x,dy=(c[4]+c[6])/2-y;return [c[0]+dx*0.9,c[1]+dy*0.9,c[2],c[3]+dx*0.9,c[4]+dy*0.9,c[5]+dx*0.9,c[6]+dy*0.9];}});cand=cand.concat(far);
    var pick=cand[0];
    for(var i=0;i<cand.length;i++){{var b=cand[i].slice(3),hit=boxes.some(function(o){{return b[0]<o[2]&&b[2]>o[0]&&b[1]<o[3]&&b[3]>o[1];}});if(!hit){{pick=cand[i];break;}}}}
    l.setAttribute('x',pick[0].toFixed(2));l.setAttribute('y',pick[1].toFixed(2));l.setAttribute('text-anchor',pick[2]);boxes.push(pick.slice(3));
  }});
}}
function show(d){{
  cur=d;svg.querySelectorAll('g.day').forEach(function(g){{g.style.display=(d==='all'||g.dataset.day===d)?'':'none';}});
  btns.forEach(function(b){{var on=b.dataset.day===d;b.setAttribute('aria-pressed',String(on));if(on)svg.setAttribute('viewBox',b.dataset.vb);}});
  layout();
}}
function select(p){{
  var d=+p.dataset.day,ns=p.dataset.n.split(',').map(Number),day=T[d];
  var visits=day.stops.filter(function(s){{return ns.indexOf(s.n)>-1;}}),s0=visits[0];
  var h='<p class="a-section__note"><span class="dot" style="background:'+day.color+'"></span>'+esc(day.name)+' · stop '+ns.join(', ')+'</p><h3 class="a-section__title">'+esc(s0.label)+'</h3>';
  if(s0.addr)h+='<p>'+esc(s0.addr)+'</p>';
  h+='<ul>';visits.forEach(function(v){{h+='<li><strong>'+esc(v.time)+'</strong> (stop '+v.n+')'+(v.note?': '+esc(v.note):'')+(v.how?'<br><span class="a-section__note">From '+esc(v.from)+': '+esc(v.how)+' · <a href="'+v.apple+'" target="_blank" rel="noopener">Apple Maps</a> · <a href="'+v.google+'" target="_blank" rel="noopener">Google Maps</a></span>':'')+'</li>';}});h+='</ul>';
  h+='<p><a href="https://maps.apple.com/?q='+encodeURIComponent(s0.label)+'&ll='+s0.lat+','+s0.lon+'" target="_blank" rel="noopener">Open this place in Apple Maps</a> · <a href="https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(s0.key)+'" target="_blank" rel="noopener">Google Maps</a></p>';
  info.innerHTML=h;
  svg.querySelectorAll('.pin.sel').forEach(function(x){{x.classList.remove('sel');}});p.classList.add('sel');
  document.querySelectorAll('tr.hl').forEach(function(x){{x.classList.remove('hl');}});
  ns.forEach(function(n){{var r=document.getElementById('leg-'+d+'-'+n);if(r)r.classList.add('hl');}});
  if(cur==='all')show(String(d));
}}
btns.forEach(function(b){{b.addEventListener('click',function(){{show(b.dataset.day);}});}});
svg.querySelectorAll('.pin').forEach(function(p){{p.addEventListener('click',function(){{select(p);}});p.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();select(p);}}}});}});

var drag=null,pts={{}},moved=false;
function vb(){{var v=svg.viewBox.baseVal;return [v.x,v.y,v.width,v.height];}}
function scale(){{return svg.viewBox.baseVal.width/(svg.getBoundingClientRect().width||800);}}
function zoomAt(f,px,py){{var v=vb(),r=svg.getBoundingClientRect();var fx=px==null?0.5:(px-r.left)/r.width,fy=py==null?0.5:(py-r.top)/r.height;var w=Math.min(Math.max(v[2]*f,40),1100),h=w*v[3]/v[2];svg.setAttribute('viewBox',[v[0]+(v[2]-w)*fx,v[1]+(v[3]-h)*fy,w,h].join(' '));layout();}}
document.getElementById('zin').addEventListener('click',function(){{zoomAt(0.6);}});
document.getElementById('zout').addEventListener('click',function(){{zoomAt(1/0.6);}});
document.getElementById('zreset').addEventListener('click',function(){{show(cur);}});
svg.addEventListener('wheel',function(e){{if(!e.ctrlKey&&!e.metaKey&&!e.altKey)return;e.preventDefault();zoomAt(e.deltaY<0?0.85:1/0.85,e.clientX,e.clientY);}},{{passive:false}});
svg.addEventListener('dblclick',function(e){{e.preventDefault();zoomAt(0.6,e.clientX,e.clientY);}});
svg.addEventListener('pointerdown',function(e){{pts[e.pointerId]=[e.clientX,e.clientY];moved=false;drag={{v:vb(),x:e.clientX,y:e.clientY,s:scale(),d:null}};var k=Object.keys(pts);if(k.length===2){{var a=pts[k[0]],b=pts[k[1]];drag.d=Math.hypot(a[0]-b[0],a[1]-b[1]);drag.c=[(a[0]+b[0])/2,(a[1]+b[1])/2];}}}});
window.addEventListener('pointermove',function(e){{if(!drag||!pts[e.pointerId])return;pts[e.pointerId]=[e.clientX,e.clientY];var k=Object.keys(pts);
  if(k.length===2&&drag.d){{var a=pts[k[0]],b=pts[k[1]],d=Math.hypot(a[0]-b[0],a[1]-b[1]);svg.setAttribute('viewBox',drag.v.join(' '));zoomAt(drag.d/d,drag.c[0],drag.c[1]);moved=true;return;}}
  var dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>4)moved=true;if(!moved)return;
  svg.setAttribute('viewBox',[drag.v[0]-dx*drag.s,drag.v[1]-dy*drag.s,drag.v[2],drag.v[3]].join(' '));}});
function up(e){{delete pts[e.pointerId];if(!Object.keys(pts).length){{if(drag&&moved)layout();drag=null;}}else if(drag){{drag.v=vb();drag.d=null;var k=Object.keys(pts);drag.x=pts[k[0]][0];drag.y=pts[k[0]][1];}}}}
window.addEventListener('pointerup',up);window.addEventListener('pointercancel',up);
svg.addEventListener('click',function(e){{if(moved){{e.stopPropagation();e.preventDefault();}}}},true);
window.addEventListener('resize',layout);
show('0');
}})();
</script>
<style>
.daybar{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}}
.daybtn{{font:inherit;padding:6px 12px;border-radius:999px;border:1px solid #94a3b8;background:transparent;color:inherit;cursor:pointer;min-height:36px}}
.daybtn[aria-pressed="true"]{{border-color:currentColor;font-weight:700;box-shadow:inset 0 0 0 1px currentColor}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}}
.mapfig{{padding:0;overflow:hidden;margin:0;position:relative}}
#tripmap{{touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}}
.zoomctl{{position:absolute;top:8px;right:8px;display:flex;flex-direction:column;gap:4px;z-index:1}}
.zoomctl button{{width:36px;height:36px;border-radius:8px;border:1px solid #94a3b8;background:#fff;color:#0f172a;font-size:18px;line-height:1;cursor:pointer}}
#tripmap{{width:100%;height:auto;aspect-ratio:6/5;display:block}}
.pin:focus{{outline:none}} .pin:focus circle,.pin.sel circle{{stroke:#0f172a;stroke-width:3}}
.stopinfo{{margin-top:12px}} .stopinfo ul{{margin:8px 0;padding-left:18px}}
tr.hl td{{background:rgba(250,204,21,.25)}}
</style>'''
open('map-body.html','w').write(body)
print('ok',len(body),VB)

import json, html
B={b['id']:b for b in json.load(open('bookings.json'))}
E=html.escape
def g(i,k): return (B[i].get(k) or '') if i in B else ''
# (phase, when, id, title, target, action, link, link_label, status, note)
T=[
('now', 'Open now', '10-rockefeller-rink', 'Rockefeller Center rink', 'Sat Jan 2 · 9:00am session', 'Buy the 9:00am session (60 min) for 2. Your Oct 25 cart showed $180 for two, so check the itemized price before paying.', 'https://www.rockefellercenter.com/tickets/the-rink-at-rockefeller-center', 'Rink tickets', 'onsale', 'Sales are final, but you can reschedule up to 24 hours before.'),
('now', 'Open now, then check daily', 'x-jellycat', 'Jellycat Diner at FAO Schwarz', 'Thu Dec 31 · about 3:00pm', 'Reserve a free slot for about 3:00pm, right after the tree (Stella 34 ends around 2:30). If Thursday is full, check daily: a few same-day slots get released.', 'https://faoschwarz.com/', 'FAO Schwarz', 'check', "About $50 per plush. Slots go fast. If you can't get one, the tree stop works without it."),
('now', 'Open now', '9-911-museum', '9/11 Museum guided tour', 'Sat Jan 2 · 11:00am', "Guided tours run seasonally (March to early January), so first check that Jan 2 is offered under Visit > Tickets and Tours > Guided Tours on 911memorial.org. If it isn't, buy a regular timed ticket for 11:00am.", 'https://visit.911memorial.org/webstore/shop/viewItems.aspx?c=museum&cg=tickets', 'Museum tickets', 'check', 'Tickets were refundable or exchangeable up to 24 hours before.'),
('now', 'Check now, then every few days', '8-summit', 'SUMMIT One Vanderbilt tickets', 'Sat Jan 2 · 4:00pm entry', 'Book a 4:00pm entry the moment Jan 2 appears (4:15 if you add AUTOPHOTO). Sunset is about 4:40.', 'https://summitov.com/tickets/', 'SUMMIT tickets', 'unconfirmed', "January wasn't on sale on Oct 16, but the rink's January opened by Oct 25. About $44 plus a $13 sunset surcharge."),
('now', 'Open now', '12a-uber-lga-arrival', 'Uber Reserve: LGA to hotel', 'Thu Dec 31 · ~10:00am pickup', 'In the Uber app, tap Reserve and schedule a pickup at LGA to 326 W 37th St. Add your flight number so it follows delays.', 'https://www.uber.com/global/en/r/airports/lga/pickup/', 'Uber LGA pickup', 'confirmed', 'Free cancellation until 1 hour before pickup.'),
('now', 'Open now', '12b-uber-brooklyn-departure', 'Uber Reserve: Brooklyn hotel to LGA', 'Mon Jan 4 · 7:45am pickup', 'Schedule a 7:45am pickup from 125 Flatbush Ave Ext to LGA (10:30 flight).', 'https://www.uber.com/us/en/ride/how-it-works/reserve/', 'Uber Reserve', 'confirmed', ''),
('later', 'Tue Nov 3 · 2:00pm ET (1:00pm Central)', 'x-carnegie-club', 'The Carnegie Club: Sinatra Saturdays', 'Sat Jan 2 · 8:00pm show', 'Reserve a table for 2 on OpenTable or carnegie-club.com. Confirm the showtime, dress code and any cover when you book.', 'https://www.carnegie-club.com/', 'Carnegie Club', 'unconfirmed', "The opening time comes from your Claude plan; I couldn't confirm it on their site. Tables are held about 10 min past showtime."),
('later', 'Thu Dec 3 (30 days ahead)', '7-golden-hof', 'Golden HOF lunch', 'Sat Jan 2 · 1:30pm', 'Book 1:30pm for 2 on Resy once Jan 2 appears. Check at midnight ET and again that morning.', 'https://resy.com/cities/new-york-ny/venues/golden-hof?date=2027-01-02&seats=2', 'Resy', 'check', 'Walk-in tables are always held. $50 per person to cancel within 6 hours.'),
('later', 'Fri Dec 4 (30 days ahead)', '1-cafe-mogador', 'Café Mogador dinner', 'Sun Jan 3 · 7:45pm', 'Book 7:45pm for 2 on Resy once Jan 3 appears. Check at midnight ET and again that morning.', 'https://resy.com/cities/new-york-ny/venues/cafe-mogador-williamsburg?date=2027-01-03&seats=2', 'Resy', 'check', 'Walk-ins are welcome too.'),
('later', 'Week of Dec 21', '13a-nyc-ferry-st-george', 'Check the NYC Ferry Jan 1 schedule', 'Fri Jan 1 · ~10:45am', "Look up the New Year's Day holiday schedule for the St. George route and tell me the times so I can adjust Jan 1. No booking needed: buy tickets in the NYC Ferry app ($5 each way).", 'https://www.ferry.nyc/routes-and-schedules/st-george/', 'NYC Ferry St. George', 'check', "The 2027 holiday schedule isn't posted yet."),
('later', 'Sat Dec 26', '2-bond-45-nye', 'Bond 45 cancellation deadline', 'Thu Dec 31', 'Last day to cancel Bond 45 without a fee.', 'https://www.bond45ny.com/new-years-eve/', 'Bond 45', 'confirmed', ''),
]
DONE=[('Stella 34 Trattoria', "Thu Dec 31 · 1:30pm, Macy's 6th floor"), ('Bond 45 NYE package', 'Thu Dec 31 · 6:30pm. Free cancellation ends Dec 26'), ("Del Frisco's Double Eagle", 'Fri Jan 1 · 5:00pm'), ('Rockettes, Radio City', 'Fri Jan 1 · 7:00pm'), ('Carnegie Diner, 205 W 57th St', 'Sat Jan 2 · 6:15pm'), ('Hotels: Hilton Garden Inn Times Square South, Hampton Inn Brooklyn', 'Booked')]
NONE=["St. Patrick's Mass, Sun 8:00am (check Epiphany times the week of Dec 28)", "Juliana's Pizza (no reservations)", 'Wah Fung No. 1 and Mei Lai Wah (cash only, walk-in)', 'AUTOPHOTO, Mure & Grand, LEGO Store, Coach, Abercrombie & Fitch, Trump Tower (walk-in)', "Utopia Bagels, Liberty Bagels, Ralph's Coffee, Cloudy Donut (walk-in)", 'Staten Island Ferry (free)']
DUO='<p><a class="btn2" href="https://resy.com/cities/new-york-ny/venues/duomo51-italian-restaurant-and-rooftop?date=2026-12-31&amp;seats=2" target="_blank" rel="noopener">Duomo51 on Resy</a></p>'
CH={'confirmed':('chip ok','Confirmed'),'available':('chip ok','Table seen Oct 16'),'check':('chip warn','Needs a check'),'unconfirmed':('chip warn','Release time unconfirmed'),'onsale':('chip ok','On sale')}
def item(n,t):
    ph,when,i,title,target,action,link,ll,st,note=t
    cls,lab=CH[st]; key=f'b{n}'
    price=g(i,'price'); canc=g(i,'cancellation')
    extra=''.join(f'<p><strong>{k}:</strong> {E(v)}</p>' for k,v in [('Price',price),('Cancellation',canc)] if v and ph=='now' or (v and k=='Price' and ph=='later' and i not in ('2-bond-45-nye','11-losers-roll','13a-nyc-ferry-st-george')))
    srcs=' · '.join(f'<a href="{E(u)}" target="_blank" rel="noopener">source {j+1}</a>' for j,u in enumerate(B.get(i,{}).get('sources',[])[:4]))
    return f'''<li class="todo"><label class="tl"><input type="checkbox" data-key="{key}"> <span><strong>{E(title)}</strong> <span class="{cls}">{lab}</span><br><span class="a-section__note">{E(when)} → for {E(target)}</span></span></label>
<p>{E(action)}</p><p><a class="btn2" href="{E(link)}" target="_blank" rel="noopener">{E(ll)}</a></p>{f'<p class="a-section__note">{E(note)}</p>' if note else ''}
<details class="a-disclosure"><summary>Price, cancellation and sources</summary>{extra or '<p>No published price or policy found.</p>'}<p class="a-section__note">{srcs}</p></details></li>'''
now=[t for t in T if t[0]=='now']; later=[t for t in T if t[0]=='later']
n=0; nowh=''; laterh=''
for t in now: n+=1; nowh+=item(n,t)
for t in later: n+=1; laterh+=item(n,t)
body=f'''<section class="a-section"><p class="a-prose">Everything you need to book, in the order it becomes available. Tick things off as you go: the checkmarks are saved on this device. <strong>Do the "Open now" list this week.</strong> For the release-day items, add the alarms below to your phone calendar.</p>
<p><a class="btn2" href="booking-alarms.ics">Add booking alarms to my calendar</a> <span class="a-section__note">Adds alarms 40 and 10 minutes before each release. On iPhone, tap it in Safari, then tap "Add All". Delete any older "NYC trip" alarms first so you don't get doubles.</span></p>
<p class="a-section__note" id="progress" aria-live="polite"></p></section><hr>
<section class="a-section"><h2 class="a-section__title">Open now: book this week</h2><ol class="todos">{nowh}</ol></section><hr>
<section class="a-section"><h2 class="a-section__title">Release days and later deadlines</h2><ol class="todos" start="{len(now)+1}">{laterh}</ol></section><hr>
<section class="a-section"><h2 class="a-section__title">Already booked</h2><ul>{''.join(f'<li><strong>{E(a)}</strong>: {E(b)}</li>' for a,b in DONE)}</ul>
<h2 class="a-section__title">No booking needed</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in NONE)}</ul></section>
<script>
(function(){{
var K='nyc-trip-todo-v1',s={{}};try{{s=JSON.parse(localStorage.getItem(K)||'{{}}');}}catch(e){{}}
var boxes=document.querySelectorAll('input[data-key]');
function upd(){{var d=0;boxes.forEach(function(b){{if(b.checked)d++;b.closest('li').classList.toggle('done',b.checked);}});document.getElementById('progress').textContent=d+' of '+boxes.length+' done';}}
boxes.forEach(function(b){{b.checked=!!s[b.dataset.key];b.addEventListener('change',function(){{s[b.dataset.key]=b.checked;try{{localStorage.setItem(K,JSON.stringify(s));}}catch(e){{}}upd();}});}});upd();
}})();
</script>
<script id="icsdata" type="text/plain">ICS_PLACEHOLDER</script>
<style>.todos{{padding-left:1.4em}}.todo{{margin:0 0 18px}}.chip{{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;margin-left:4px;white-space:nowrap}}.chip.ok{{background:#dcfce7;color:#166534}}.chip.warn{{background:#fef3c7;color:#92400e}}.btn2{{display:inline-block;padding:9px 14px;border-radius:8px;border:1px solid #1e3a8a;background:#1e40af;color:#fff!important;text-decoration:none;font-weight:600;font-size:15px;cursor:pointer}}.todo{{overflow-wrap:anywhere}}.tl{{display:flex;gap:10px;align-items:flex-start;cursor:pointer}}.tl input{{width:22px;height:22px;margin-top:2px;flex:none}}.todo.done>p,.todo.done>details{{opacity:.5}}.todo.done .tl strong{{text-decoration:line-through}}</style>'''
# ICS (UTC; ET = UTC-5 in Dec)
EV=[('20261103T185000Z', 'Carnegie Club opens 2:00pm ET: book Sat Jan 2 Sinatra show', 'https://www.carnegie-club.com/'), ('20261105T150000Z', 'Check SUMMIT: is Jan 2 on sale? Book 4:00pm', 'https://summitov.com/tickets/'), ('20261112T150000Z', 'Check SUMMIT again: Jan 2 4:00pm', 'https://summitov.com/tickets/'), ('20261203T045000Z', 'Golden HOF: Resy Jan 2 1:30pm should open', 'https://resy.com/cities/new-york-ny/venues/golden-hof?date=2027-01-02&seats=2'), ('20261203T140000Z', 'Golden HOF morning check: Resy Jan 2 1:30pm', 'https://resy.com/cities/new-york-ny/venues/golden-hof?date=2027-01-02&seats=2'), ('20261204T045000Z', 'Cafe Mogador: Resy Jan 3 7:45pm should open', 'https://resy.com/cities/new-york-ny/venues/cafe-mogador-williamsburg?date=2027-01-03&seats=2'), ('20261204T140000Z', 'Cafe Mogador morning check: Resy Jan 3 7:45pm', 'https://resy.com/cities/new-york-ny/venues/cafe-mogador-williamsburg?date=2027-01-03&seats=2'), ('20261222T150000Z', 'Check NYC Ferry Jan 1 holiday schedule (St. George)', 'https://www.ferry.nyc/routes-and-schedules/st-george/'), ('20261226T150000Z', 'Last day to cancel Bond 45 without a fee', 'https://www.bond45ny.com/new-years-eve/'), ('20261228T150000Z', 'Check Jan 1-2 hours (bagels, Wah Fung, Mei Lai Wah, Mure & Grand, LEGO, A&F) and Epiphany Mass times', 'https://www.saintpatrickscathedral.org/'), ('20270101T170000Z', 'Check the Carnegie Club showtime for tomorrow', 'https://www.carnegie-club.com/')]
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//NYC trip//EN','CALSCALE:GREGORIAN']
for j,(dt,s,u) in enumerate(EV):
    end=dt[:11]+'%02d'%(int(dt[11:13])+(0 if int(dt[11:13])>=50 else 0))+dt[13:]
    L+=['BEGIN:VEVENT',f'UID:nyc-trip-{j}@devin',f'DTSTAMP:20261102T200000Z',f'DTSTART:{dt}',f'DURATION:PT20M',f'SUMMARY:{s}',f'URL:{u}',f'DESCRIPTION:{u}','BEGIN:VALARM','ACTION:DISPLAY',f'DESCRIPTION:{s}','TRIGGER:-PT30M','END:VALARM','BEGIN:VALARM','ACTION:DISPLAY',f'DESCRIPTION:{s}','TRIGGER:PT0M','END:VALARM','END:VEVENT']
L.append('END:VCALENDAR'); ics='\n'.join(L)
open('nyc-trip-booking-alarms.ics','w').write(ics.replace('\n','\r\n'))
open('todo-body.html','w').write(body.replace('ICS_PLACEHOLDER',ics))
print('ok',n)

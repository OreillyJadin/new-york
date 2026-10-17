import json, html
B={b['id']:b for b in json.load(open('bookings.json'))}
E=html.escape
def g(i,k): return (B[i].get(k) or '') if i in B else ''
# (phase, when, id, title, target, action, link, link_label, status, note)
T=[
('now','Open now','2-bond-45-nye','Bond 45 New Year\'s Eve party','Thu Dec 31 · 6:30pm','Call 212-869-4545 and book the $300 Celebration Package (not the $700 ball-drop package). Ask: is the tip included, what is the cancellation fee after Dec 26, which floor, and a table for two.','https://www.bond45ny.com/new-years-eve/','Bond 45 NYE page','confirmed','Their OpenTable listing shows a different $700 package; make sure you get the $300 one.'),
('now','Open now','1-river-cafe','The River Café dinner','Sun Jan 3 · 7:00pm','Book on OpenTable for 2 at 7:00pm now. They take bookings a year ahead, so Jan 3 has been open since Jan 3, 2026, and holiday-week dinners fill first. OpenTable didn\'t show me the Jan 3 time list, so if 7pm isn\'t there, call the restaurant.','https://www.opentable.com/r/the-river-cafe-brooklyn','OpenTable','check','Jackets required for men. OpenTable warns of a late-cancellation charge (about $195 per person), so put the deadline in your calendar.'),
('now','Open now','3-toloache','Toloache birthday dinner','Fri Jan 1 · 5:00pm','Book on Resy. A 5:00pm table for 2 was showing when I checked. Add a note that you have a 7pm show.','https://resy.com/cities/new-york-ny/venues/toloache-50th-st?date=2027-01-01&seats=2','Resy','available','Checked Oct 16; tables can go.'),
('now','Open now','x-stella34','Stella 34 Trattoria view lunch','Thu Dec 31 · 1:30pm','Book on OpenTable for 2 at 1:30pm and ask for a window table (Empire State Building view). Tables for 2 from 1:00 to 2:00 were showing on Oct 16.','https://www.opentable.com/r/stella-34-trattoria-new-york','OpenTable','available','It\'s on the 6th floor of Macy\'s, right after your 11:30 windows stop.'),
('now','Open now','9-911-museum','9/11 Memorial & Museum','Sat Jan 2 · 9:45am entry','Buy timed tickets ($24–$36 each).','https://visit.911memorial.org/webstore/shop/viewItems.aspx?c=museum&cg=tickets','Museum tickets','check','On sale since Jul 2 (they sell 6 months ahead). Refundable or exchangeable up to 24 hours before.'),
('now','Open now','12a-uber-lga-arrival','Uber Reserve: LGA to hotel','Thu Dec 31 · ~10:00am pickup','In the Uber app, tap Reserve and schedule a pickup at LGA to 326 W 37th St. Add your flight number so it follows delays.','https://www.uber.com/global/en/r/airports/lga/pickup/','Uber LGA pickup','confirmed','Free cancellation until 1 hour before pickup.'),
('now','Open now','12b-uber-brooklyn-departure','Uber Reserve: Brooklyn hotel to LGA','Mon Jan 4 · 7:45am pickup','Schedule a 7:45am pickup from 125 Flatbush Ave Ext to LGA (10:30 flight).','https://www.uber.com/us/en/ride/how-it-works/reserve/','Uber Reserve','confirmed',''),
('now','Open now','11-losers-roll','Loser\'s cinnamon roll (optional)','Sat Jan 2 pickup','Sign up for their newsletter now. Pre-orders drop weekly (usually Monday or Tuesday), so the Jan 2 drop is likely Dec 28 or 29.','https://www.loserseatinghouse.com/subscribe','Newsletter sign-up','check','$19.99 per roll. Pickup dates can\'t be changed.'),
('now','Open now','7-golden-diner','Golden Diner: set Resy Notify','Sat Jan 2 · 11:00am','Turn on Resy Notify for Jan 2 now so you get pinged if a table opens.','https://resy.com/cities/new-york-ny/venues/golden-diner?date=2027-01-02&seats=2','Resy','check',''),
('now','Open now','6-carbone','Carbone: set Resy Notify','Sat Jan 2 · 7:00pm','Turn on Resy Notify for Jan 2 now as a backup for release day.','https://resy.com/cities/new-york-ny/venues/carbone?date=2027-01-02&seats=2','Resy','check',''),
('later','Sun Nov 1 · check, then every few days','8-summit','SUMMIT One Vanderbilt tickets','Sat Jan 2 · 3:30–4:00pm entry','January isn\'t on sale yet. Check on Nov 1 and every few days after, and book a 3:30 or 4:00pm entry the moment Jan 2 appears (sunset is about 4:40).','https://summitov.com/tickets/','SUMMIT tickets','unconfirmed','On Oct 16 the calendar was on sale through Dec 31 and all of January was greyed out (not released yet, not sold out). Dec 31 showed 3:30 and 4:00pm slots with a +$13 sunset surcharge on the $44 ticket. Summit doesn\'t publish when the next month opens, and I found no past-year pattern.'),
('later','Sun Nov 1 · check, then every few days','10-rockefeller-rink','Rockefeller Center rink','Sat Jan 2 · 8:00am session','January isn\'t on sale yet. Check on Nov 1 and every few days after, and book an 8:00am session on Jan 2 when it appears.','https://www.rockefellercenter.com/tickets/the-rink-at-rockefeller-center','Rink tickets','unconfirmed','On Oct 16 the calendar was on sale through Dec 31 and all of January was greyed out (not released yet, not sold out). Dec 31\'s first session is 7:00am at $39, so early sessions do run and your 8am plan should work. Past seasons went on sale Aug to Oct, but I found no record of when later months open.'),
('later','Wed Dec 2 · 12:00am ET (Tue night)','5-din-tai-fung','Din Tai Fung birthday lunch','Fri Jan 1 · 1:00pm','Be on at midnight (Tuesday night into Wednesday) and book 1:00pm for 2.','https://dtf.com/en-us/locations/new-york','Din Tai Fung NY','confirmed','When this location opened, the NYT reported reservations gone within minutes. If you miss it, they run an on-site walk-in waitlist. Release rule confirmed on their FAQ. They point to Yelp in some places and their own site in others, so open the page a few days before to see which one is live.'),
('later','Thu Dec 3 · 12:00am ET (or Fri Dec 4)','7-golden-diner','Golden Diner brunch','Sat Jan 2 · 11:00am','Check Resy at midnight Wednesday night, and again at midnight Thursday night if it isn\'t up yet.','https://resy.com/cities/new-york-ny/venues/golden-diner?date=2027-01-02&seats=2','Resy','confirmed','Resy\'s own guide (Sept 2026) says 30 days ahead at midnight, brunch included. If Jan 2 isn\'t showing at midnight Wednesday, check again Thursday at midnight. One guide reports a $50-per-person no-show fee. If you miss it, join the walk-in list about 10:45.'),
('later','Thu Dec 3 · 10:00am ET','6-carbone','Carbone dinner','Sat Jan 2 · 7:00pm','Be on Resy right at 10:00am. Have the app open, logged in and card saved. Grab any time from 6 to 9pm; tables go in seconds.','https://resy.com/cities/new-york-ny/venues/carbone?date=2027-01-02&seats=2','Resy','confirmed','Carbone\'s Resy page says 30 days ahead at 10:00am ET. Reddit (2024) and Grub Street (2023) say tables are gone by 10:01, so be refreshing at 9:59. Amex Platinum/Gold cardholders can get Resy priority access. Carbone has no bar seats, so walk-ins aren\'t realistic.'),
('later','Week of Dec 21','13a-nyc-ferry-st-george','Check the NYC Ferry Jan 1 schedule','Fri Jan 1 · ~10:45am','Look up the New Year\'s Day holiday schedule for the St. George route and tell me the times so I can adjust Jan 1. No booking needed: buy tickets in the NYC Ferry app ($5 each way).','https://www.ferry.nyc/routes-and-schedules/st-george/','NYC Ferry St. George','check','The 2027 holiday schedule isn\'t posted yet.'),
('later','Sat Dec 26','2-bond-45-nye','Bond 45 cancellation deadline','Thu Dec 31','Last day to cancel Bond 45 without a fee.','https://www.bond45ny.com/new-years-eve/','Bond 45','confirmed',''),
('later','Mon Dec 28 or Tue Dec 29','11-losers-roll','Loser\'s pre-order drop (optional)','Sat Jan 2 pickup','Watch your email and order the moment the drop opens.','https://www.loserseatinghouse.com/subscribe','Loser\'s','unconfirmed','Drops usually go out Monday or Tuesday with no set time. Time Out (Feb 2026) says they sell out almost as soon as they\'re posted. Leftovers get posted on their Instagram stories.'),
]
DONE=[('Rockettes, Radio City','Fri Jan 1 · 7:00pm (booked)'),('Hotels: Hilton Garden Inn Times Square South, Hampton Inn Brooklyn','Booked (tell me if not)')]
NONE=["St. Patrick's Mass, Sun 7:00am (confirmed on their schedule)","Juliana's Pizza (no reservations)","Old Friend Photobooth (walk-in)","Jane's Carousel (pay at the carousel)","Ralph's Coffee, Utopia Bagels, Liberty Bagels, Cloudy Donut (walk-in)","Staten Island Ferry (free)"]
DUO='<p><a class="btn2" href="https://resy.com/cities/new-york-ny/venues/duomo51-italian-restaurant-and-rooftop?date=2026-12-31&amp;seats=2" target="_blank" rel="noopener">Duomo51 on Resy</a></p>'
CH={'confirmed':('chip ok','Confirmed'),'available':('chip ok','Table seen Oct 16'),'check':('chip warn','Needs a check'),'unconfirmed':('chip warn','Release time unconfirmed')}
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
<p><button type="button" class="btn2" id="ics">Add booking alarms to my calendar</button> <span class="a-section__note">Downloads a calendar file with alarms 40 and 10 minutes before each release. On iPhone, open it and tap "Add All".</span></p>
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
document.getElementById('ics').addEventListener('click',function(){{
var blob=new Blob([document.getElementById('icsdata').textContent.trim().replace(/\\n/g,'\\r\\n')],{{type:'text/calendar'}});
var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='nyc-trip-booking-alarms.ics';document.body.appendChild(a);a.click();a.remove();}});
}})();
</script>
<script id="icsdata" type="text/plain">ICS_PLACEHOLDER</script>
<style>.todos{{padding-left:1.4em}}.todo{{margin:0 0 18px}}.chip{{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;margin-left:4px;white-space:nowrap}}.chip.ok{{background:#dcfce7;color:#166534}}.chip.warn{{background:#fef3c7;color:#92400e}}.btn2{{display:inline-block;padding:9px 14px;border-radius:8px;border:1px solid #1e3a8a;background:#1e40af;color:#fff!important;text-decoration:none;font-weight:600;font-size:15px;cursor:pointer}}.todo{{overflow-wrap:anywhere}}.tl{{display:flex;gap:10px;align-items:flex-start;cursor:pointer}}.tl input{{width:22px;height:22px;margin-top:2px;flex:none}}.todo.done>p,.todo.done>details{{opacity:.5}}.todo.done .tl strong{{text-decoration:line-through}}</style>'''
# ICS (UTC; ET = UTC-5 in Dec)
EV=[('20261101T140000Z','Check SUMMIT and the rink: is Jan 2 on sale yet?','https://summitov.com/tickets/'),
('20261108T140000Z','Check again: SUMMIT and rink Jan 2 tickets','https://www.rockefellercenter.com/tickets/the-rink-at-rockefeller-center'),
('20261202T045000Z','Din Tai Fung opens at midnight: book Jan 1 1:00pm','https://dtf.com/en-us/locations/new-york'),
('20261203T045000Z','Golden Diner may open at midnight: Resy Jan 2 11am','https://resy.com/cities/new-york-ny/venues/golden-diner?date=2027-01-02&seats=2'),
('20261203T145000Z','Carbone opens 10:00am: Resy Jan 2 7pm','https://resy.com/cities/new-york-ny/venues/carbone?date=2027-01-02&seats=2'),
('20261204T045000Z','Golden Diner backup midnight: check Resy Jan 2 11am','https://resy.com/cities/new-york-ny/venues/golden-diner?date=2027-01-02&seats=2'),
('20261222T150000Z','Check NYC Ferry Jan 1 holiday schedule (St. George)','https://www.ferry.nyc/routes-and-schedules/st-george/'),
('20261226T150000Z','Last day to cancel Bond 45 without a fee','https://www.bond45ny.com/new-years-eve/'),
('20261228T150000Z',"Loser's cinnamon roll drop: watch email (Mon/Tue)",'https://www.loserseatinghouse.com/subscribe')]
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//NYC trip//EN','CALSCALE:GREGORIAN']
for j,(dt,s,u) in enumerate(EV):
    end=dt[:11]+'%02d'%(int(dt[11:13])+(0 if int(dt[11:13])>=50 else 0))+dt[13:]
    L+=['BEGIN:VEVENT',f'UID:nyc-trip-{j}@devin',f'DTSTAMP:20261016T200000Z',f'DTSTART:{dt}',f'DURATION:PT20M',f'SUMMARY:{s}',f'URL:{u}',f'DESCRIPTION:{u}','BEGIN:VALARM','ACTION:DISPLAY',f'DESCRIPTION:{s}','TRIGGER:-PT30M','END:VALARM','BEGIN:VALARM','ACTION:DISPLAY',f'DESCRIPTION:{s}','TRIGGER:PT0M','END:VALARM','END:VEVENT']
L.append('END:VCALENDAR'); ics='\n'.join(L)
open('nyc-trip-booking-alarms.ics','w').write(ics.replace('\n','\r\n'))
open('todo-body.html','w').write(body.replace('ICS_PLACEHOLDER',ics))
print('ok',n)

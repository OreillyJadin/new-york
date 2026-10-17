import runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path('build_days.py')
data,META,H,T,TITLES=g['data'],g['META'],g['H'],g['T'],g['TITLES']
o=[]
w=o.append
w("# NYC trip brief (Dec 31, 2026 to Jan 4, 2027)\n")
w("Paste or upload this whole file into Claude. It is the current, confirmed plan, built in Devin and checked on Oct 16, 2026.\n")
w("## Notes for Claude\n")
w("- This file is the source of truth. Don't re-suggest options that were already ruled out (listed under \"Decided, don't revisit\").")
w("- Only suggest restaurants or tickets once you've checked they have availability on that exact date. A normal-day table or general hours isn't enough.")
w("- Group stops by neighborhood, use the subway wherever it's practical, and give step-by-step directions (line, station, direction).")
w("- Give real links, say how far ahead each booking opens, and flag anything you couldn't verify.")
w("- When the plan changes, return the full updated day in the same format as below (time | stop | address | how to get there | hints), so it can be copied back into the trip website later.")
w("- Nothing has been booked except the Rockettes. Never say something is booked unless she confirms it.\n")
w("## Fixed facts\n")
w("- Two travelers. Her birthday is Jan 1.")
w("- Arrive LaGuardia (LGA) about 10:00am Thu Dec 31. Fly home from LGA Mon Jan 4 at 10:30am.")
w("- Hotel Dec 31 to Jan 3 morning: Hilton Garden Inn New York Times Square South, 326 W 37th St.")
w("- Hotel Jan 3 to Jan 4: Hampton Inn Brooklyn Downtown, 125 Flatbush Ave Ext.")
w("- Booked: Rockettes Christmas Spectacular, Fri Jan 1 at 7:00pm (Radio City).")
w("- NYE: Bond 45's $300 per person Celebration Package (dinner, open bar, DJ, champagne toast), from 6:30pm. Not the $700 package on OpenTable.\n")
w("## Decided, don't revisit\n")
for x in ["Bond 45 over PHD at Dream Downtown (PHD had bad NYE reviews and needed a separate dinner).",
 "Stella 34 (Macy's 6th floor, Empire State view) for NYE lunch at 1:30. Duomo51 had no NYE lunch tables, so it's out.",
 "Toloache at 5pm on Jan 1 before the Rockettes (replaced Nubeluz and Victor's Café).",
 "Din Tai Fung is the Jan 1 birthday lunch at 1pm (replaced John's of Bleecker St).",
 "No Rockefeller tree at night on Jan 1; early bedtime after the Rockettes.",
 "Summit One Vanderbilt is Sat Jan 2 around sunset (3:30 to 4:00pm entry).",
 "Golden Diner at 11am Sat Jan 2. Loser's cinnamon roll is optional.",
 "Cloudy Donut replaced Peter Pan (Greenpoint was out of the way).",
 "Sunday Jan 3: DUMBO and Pebble Beach walk at the start of sunset, then a later dinner at River Café at 7pm.",
 "Edge and Top of the Rock are skipped (Summit covers it). The Rockettes are the show, so no Broadway musical."]:
    w("- "+x)
w("")
for di,(d,m) in enumerate(zip(data,META)):
    w(f"## {m['long']}: {m['eyebrow']}\n")
    w(f"*{TITLES[di]}*. Sleep: {m['hotel']}.\n")
    w(m['lead']+"\n")
    w(f"**What to wear:** {m['wear']}\n")
    for s in d['stops']:
        go,tips=H.get((di,s['n']),(None,[]))
        how=go or s.get('how')
        w(f"{s['n']}. **{s['time']} · {s['label']}**, {s['addr']}")
        if how: w(f"   - Getting there: {how}")
        if s['note']: w(f"   - {s['note']}")
        for t in tips: w(f"   - {t}")
    w("")
w("## Bookings, in the order they open\n")
w("All times Eastern. \"Now\" means it was already bookable on Oct 16, 2026.\n")
for r in T:
    when='Now' if r[0]=='now' else r[1]
    w(f"- **{when}: {r[3]}** ({r[4]}). {r[5]} Link: {r[6]}" + (f" Confidence: {r[8]}." if r[8] else "") + (f" {r[9]}" if len(r)>9 and r[9] else ""))
w("")
w("## Things still unconfirmed\n")
for x in ["Utopia Bagels' Jan 1 hours (normally 6am to 4pm daily).",
 "NYC Ferry's Jan 1 holiday schedule for the St. George route. Check the week of Dec 21.",
 "Exact Jan 2 rink session times and Summit Jan 2 slots: January wasn't on sale yet on Oct 16. Check Nov 1 and every few days.",
 "Golden Diner's release night: Resy says 30 days ahead at midnight, so try midnight Wed Dec 2 into Thu Dec 3, and again a night later.",
 "Carbone's 10:00am release time is reported by Resy's page and Reddit, not by Carbone itself.",
 "Epiphany Sunday (Jan 3) Mass times at St. Patrick's. Check that week."]:
    w("- "+x)
open('nyc-trip-brief-for-claude.md','w').write("\n".join(o)+"\n")
print(len("\n".join(o)))

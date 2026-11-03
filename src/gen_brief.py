import runpy, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    g=runpy.run_path('build_days.py')
data,META,H,T,TITLES=g['data'],g['META'],g['H'],g['T'],g['TITLES']
o=[]
w=o.append
w("# NYC trip brief (Dec 31, 2026 to Jan 4, 2027)\n")
w("Paste or upload this whole file into Claude. It is the current, confirmed plan, built in Devin. Updated Nov 2, 2026 to match her Oct 27 Claude plan, with Stella 34 booked at 1:30, Abercrombie & Fitch and Trump Tower on Fifth Ave, a Wall Street walk on Jan 1, and Jan 3 starting with 8am Mass.\n")
w("## Notes for Claude\n")
w("- This file is the source of truth. Don't re-suggest options that were already ruled out (listed under \"Decided, don't revisit\").")
w("- Only suggest restaurants or tickets once you've checked they have availability on that exact date. A normal-day table or general hours isn't enough.")
w("- Group stops by neighborhood, use the subway wherever it's practical, and give step-by-step directions (line, station, direction).")
w("- Give real links, say how far ahead each booking opens, and flag anything you couldn't verify.")
w("- When the plan changes, return the full updated day in the same format as below (time | stop | address | how to get there | hints), so it can be copied back into the trip website later.")
w("- Booked so far: Stella 34 (Dec 31, 1:30pm), Bond 45 (Dec 31, 6:30pm), Del Frisco's Double Eagle (Jan 1, 5:00pm), the Rockettes (Jan 1, 7:00pm), Carnegie Diner (Jan 2, 6:15pm) and both hotels. Never say anything else is booked unless she confirms it.\n")
w("## Fixed facts\n")
w("- Two travelers. Her birthday is Jan 1.")
w("- Arrive LaGuardia (LGA) about 10:00am Thu Dec 31. Fly home from LGA Mon Jan 4 at 10:30am.")
w("- Hotel Dec 31 to Jan 3 morning: Hilton Garden Inn New York Times Square South, 326 W 37th St.")
w("- Hotel Jan 3 to Jan 4: Hampton Inn Brooklyn Downtown, 125 Flatbush Ave Ext.")
w("- Booked: Stella 34 Trattoria, Thu Dec 31 at 1:30pm (Macy's 6th floor). Del Frisco's Double Eagle, Fri Jan 1 at 5:00pm (1221 6th Ave). Rockettes Christmas Spectacular, Fri Jan 1 at 7:00pm (Radio City). Carnegie Diner, Sat Jan 2 at 6:15pm (205 W 57th St).")
w("- NYE: Bond 45's $300 per person Celebration Package (dinner, open bar, DJ, champagne toast), from 6:30pm. Booked; free cancellation ends Dec 26. Not the $700 package on OpenTable.\n")
w("## Decided, don't revisit\n")
for x in ['Bond 45 over PHD at Dream Downtown (PHD had bad NYE reviews and needed a separate dinner).', "Stella 34 (Macy's 6th floor, Empire State view) is booked for NYE lunch at 1:30. Duomo51 had no NYE lunch tables.", 'Dec 31 after lunch: the tree, Jellycat Diner at FAO Schwarz (~3pm), the LEGO Store (optional), Coach at 685 5th Ave (optional), Abercrombie & Fitch at 720 5th Ave, Trump Tower (725 5th Ave), then Tiffany, Bergdorf, The Plaza and Gapstow Bridge at sunset.', "Jan 1: after the Charging Bull, a Wall Street walk (Trinity Church to 55 Wall St), then the J from Broad St to Canal St. Lunch is free time around Chinatown, Little Italy and SoHo (Wah Fung No. 1 is lunch (cash only) and Mei Lai Wah is the pastry stop; one Mure & Grand stop, the Little Italy one), then Del Frisco's at 5pm (booked) before the Rockettes. Din Tai Fung and Toloache are dropped.", 'No Rockefeller tree at night on Jan 1; early bedtime after the Rockettes.', "Sat Jan 2: rink 9:00am, 9/11 Museum guided tour 11:00am, Golden HOF 1:30pm (Korean bar & grill at 16 W 48th St, replaced Golden Diner because it's less busy and a short walk to Summit; AUTOPHOTO is an optional stop between lunch and Summit, about 2:50, via the F train), Summit 4:00pm, Carnegie Diner 6:15pm (booked), Carnegie Club Sinatra show 8:00pm. Carbone and Loser's are dropped.", 'Cloudy Donut replaced Peter Pan (Greenpoint was out of the way).', "Sun Jan 3: 8:00am Mass at St. Patrick's and everything after shifted about an hour later. No hotel return after Juliana's; a Brooklyn Bridge Park stroll, then DUMBO and Pebble Beach at sunset, then about 2 hours at the Hampton Inn, then Café Mogador Williamsburg (133 Wythe Ave, Moroccan) at 7:45pm, not booked yet; Resy opens about Dec 4. River Café, Lori Jayne (left Alphaville in 2025, closed Sundays) and Swoony's (closed Sundays) were ruled out. Jane's Carousel is dropped.", 'Also dropped: Tenement Museum, Top of the Rock, Bryant Park Winter Village. Edge is skipped (Summit covers it). The Rockettes are the show, so no Broadway musical.']:
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
w("All times Eastern. \"Now\" means it was already bookable as of her Oct 27, 2026 plan.\n")
for r in T:
    when='Now' if r[0]=='now' else r[1]
    w(f"- **{when}: {r[3]}** ({r[4]}). {r[5]} Link: {r[6]}" + (f" Confidence: {r[8]}." if r[8] else "") + (f" {r[9]}" if len(r)>9 and r[9] else ""))
w("")
w("## Things still unconfirmed\n")
for x in ['Jan 1 and Jan 2 hours for Utopia Bagels, Liberty Bagels, Wah Fung, Mei Lai Wah and Mure & Grand, and Dec 31 hours for the LEGO Store and Abercrombie & Fitch. Check the week of Dec 28.', "NYC Ferry's Jan 1 holiday schedule for the St. George route. Check the week of Dec 21. If it isn't running, ride the free Staten Island Ferry round trip from Whitehall.", "Summit Jan 2 slots: January wasn't on sale on Oct 16. Check every few days.", 'Whether the 9/11 Museum guided tour runs on Jan 2 (tours run March to early January).', 'Carnegie Club: the reservation opening (Tue Nov 3, 2pm ET per her Claude plan), the Jan 2 showtime, dress code and any cover.', "Golden HOF (Jan 2) and Café Mogador (Jan 3) Resy release: both calendars ran exactly 30 days ahead on Nov 2, 2026, so about Dec 3 and Dec 4; time of day not posted.", "Epiphany Sunday (Jan 3) Mass times at St. Patrick's. Check that week."]:
    w("- "+x)
open('nyc-trip-brief-for-claude.md','w').write("\n".join(o)+"\n")
print(len("\n".join(o)))

# New York, Dec 31 to Jan 4

Trip website, served by GitHub Pages at https://oreillyjadin.github.io/new-york/

- `index.html`: day-by-day plan with maps, times, hints and to-dos (the main page)
- `map.html`: full-trip map with every stop
- `bookings.html`: booking to-do list in the order things open
- `itinerary.html`: printable itinerary
- `booking-alarms.ics`: calendar alarms for every booking release
- `trip-brief-for-claude.md`: the whole current plan as text, to paste into another AI chat

## Updating

The pages are generated from `src/`. Data lives in `src/build_map2.py` (stops), `src/hints.py` (hints, directions, map splits) and `src/build_todo.py` (bookings).

    cd src
    python3 build_days.py        # writes days-body.html
    python3 gen_brief.py         # writes nyc-trip-brief-for-claude.md

`days-body.html` is then compiled into a standalone page with the Devin interactive-artifact compiler and copied to `index.html`. Each page is a single self-contained file with no outside requests, apart from the Apple and Google Maps links you tap yourself.

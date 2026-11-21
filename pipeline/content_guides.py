# content_guides.py — guide / comparison / blog pages for the battery EMD sites.
#
# Consumed by build_sites.py: every entry is rendered by the build (never
# hand-edit sites/ HTML), registered in the sitemap, and linked from the
# homepage "Guides & explainers" section. Queue + topical maps:
# ~/workspace/battery-per-wh/research/topical-maps-2026-11-21/
#
# Entry fields:
#   slug, title, desc, h1, blurb — page identity (title/desc may use {placeholders})
#   lede    — answer-first intro, raw HTML, placeholders allowed
#   filter  — None (no table) | a FILTERS key | "brand:A+B" | "brand:A+B@filterkey"
#   table_heading — heading above the live product table
#   sections — [(h2, [raw-HTML blocks])] — placeholders allowed in blocks
#   faqs    — [(q, a)] page-specific; falls back to the site's FAQs
#   related — slugs (clusters or guides on the same site) for cross-links
#
# Placeholders (computed live from the page's own table rows at build time):
#   {n} {minppw} {medppw} {maxppw} {minprice} {maxprice} {date}
#   {cheap_title} {cheap_brand} {cheap_price} {cheap_ppw} {cheap_cap}
#   {low5k} {med5k} {low10k} {med10k}  — cost of 5.12/10.24kWh at the low/median $/Wh
#   per brand present in the rows: {brand_n} {brand_min_price} {brand_min_ppw}
#   {brand_cheap_title}  (brand key = lowercase, non-alphanumerics -> _)
#
# House rules: no invented ratings or prices (numbers come from the catalog via
# placeholders, or are dated external context labeled as such); no "best/#1"
# editorial crowning — verdicts are the $/Wh sort, a stated method.

GUIDES = {
"48vlifepo4battery.com": [
    {
        "slug": "home-battery-system",
        "title": "Home Battery System Cost: DIY 48V vs Installed, Priced per kWh",
        "desc": "What a home battery system actually costs in {date}: a DIY 48V LiFePO4 build priced live per kWh from makers' stores, vs installed-system quotes of $10,000–$25,000.",
        "h1": "Home Battery System Costs: The DIY 48V Build vs the Installed Quote",
        "blurb": "The sleeper comparison: what 10–20kWh of home storage costs built from 48V batteries at live $/kWh, vs a $10K–$25K installed system.",
        "lede": "A home battery system has two price tags depending on how you buy it. Installed brands (a wall battery fitted by a solar company) are quoted at <b>$10,000–$25,000 installed</b> in current buying guides. The same stored energy built DIY from 48V LiFePO4 batteries tracks at <b>${medppw}/Wh median ({low10k}–{med10k} for 10.24kWh of batteries)</b> across the {n} models below — before inverter and fitting. This page prices both paths honestly, with the live table as the evidence.",
        "filter": "all",
        "table_heading": "The batteries a DIY home system is built from — live prices",
        "sections": [
            ("The two ways to buy the same kWh", [
                "<p>Every home battery system is three things: battery cells in a box, an inverter that speaks to the grid and your panels, and the labor/permits to connect them. Installed brands bundle all three into one quote, which is why their per-kWh price is high: roundups of installed systems in 2026 cite <b>$10,000–$25,000 all-in</b> for roughly 10–13.5kWh of storage — about $750–$1,900 per kWh installed.</p>",
                "<p>The DIY path unbundles it. You buy the batteries on this page (at the live $/kWh in the table), add a hybrid inverter (a planning estimate of $900–$2,500 for a 5–8kW unit, not a price we track), plus rack, cable and an electrician's day if you don't self-install. At today's median of ${medppw}/Wh, the battery portion of a 10.24kWh system is {med10k} — the single biggest line item is also the one with the live price on it.</p>",
            ]),
            ("What the extra money buys in an installed system", [
                "<ul><li><b>Permits and inspection</b> handled by the installer — required for grid-tied systems in most US jurisdictions either way.</li><li><b>One warranty throat to choke</b>: a single 10-year warranty vs separate battery/inverter warranties.</li><li><b>Whole-home automatic transfer</b> with a fitted panel, vs the critical-loads sub-panel most DIY builds use.</li><li><b>No homework</b>: no inverter-compatibility lists, no cable sizing, no settings.</li></ul>",
                "<p>None of that changes the storage math. A kWh from a rack module at $0.17–$0.23/Wh stores the same energy as a kWh in a $1,000/kWh installed box; the difference is labor, integration and warranty structure. Buyers who are comfortable speccing an inverter pay roughly a third to a half for the same backup.</p>",
            ]),
            ("How much system does a house actually need?", [
                "<table><thead><tr><th>Goal</th><th>Storage</th><th>Battery cost at today's prices</th></tr></thead><tbody>"
                "<tr><td>Essentials through the night (fridge, lights, internet, phones)</td><td>5.12kWh (1 module)</td><td class='num'>{low5k}–{med5k}</td></tr>"
                "<tr><td>Essentials + furnace blower + a few outlets, ~24h</td><td>10.24kWh (2 modules)</td><td class='num'>{low10k}–{med10k}</td></tr>"
                "<tr><td>Whole-home posture: well pump, mini-split, most circuits</td><td>20.48kWh (4 modules)</td><td class='num'>2× the 10kWh row</td></tr>"
                "</tbody></table>",
                "<p>Battery cost is only the storage line — add the inverter estimate above and, for grid-tied work, an electrician. Our <a href=\"/10kwh-battery/\">10kWh battery page</a> breaks the most common target down by build path, and the <a href=\"/home-battery-backup/\">home battery backup table</a> shows every 48V model ranked the same way.</p>",
            ]),
        ],
        "faqs": [
            ("How much does a home battery system cost in 2026?",
             "Installed systems are quoted at $10,000–$25,000 in current buying guides for about 10–13.5kWh. A DIY system built from 48V LiFePO4 batteries prices its storage live on this page — recently a median of ${medppw}/Wh, so {med10k} for 10.24kWh of batteries — plus a hybrid inverter (roughly $900–$2,500) and any electrical labor."),
            ("Is a DIY home battery system legal to grid-tie?",
             "Grid-tied systems generally need permits, listed equipment and inspection wherever you live — the DIY/installed distinction is about who does the paperwork, not whether it exists. Off-grid and backup-only systems behind a transfer switch face fewer requirements in many areas, but local code always wins; check before you build."),
            ("How long will a 10kWh home battery system run a house?",
             "It depends entirely on what stays on. Essentials (fridge, lights, internet, ~300W average) run roughly 30 hours on 10.24kWh. Add a furnace blower and usage climbs; run an electric range or AC and the same bank lasts a few hours. Size from loads, not from the house's square footage."),
        ],
        "related": ["10kwh-battery", "home-battery-backup", "solar-storage-batteries"],
    },
    {
        "slug": "10kwh-battery",
        "title": "10kWh Battery: Three Ways to Build It, Priced Live by $/Wh",
        "desc": "Three real ways to get a 10kWh battery — one 48V 200Ah unit, two server rack modules, or a wall-mount — each priced from live maker-store data, refreshed {date}.",
        "h1": "A 10kWh Battery, Three Ways — Each Priced from Live Listings",
        "blurb": "One big unit, two rack modules, or a wall battery: what 10kWh actually costs today, path by path.",
        "lede": "There is no single product called a '10kWh battery' — there are three ways to assemble one, and they price differently. At today's live numbers, 10.24kWh of 48V LiFePO4 storage costs between <b>{low10k}</b> (at the cheapest tracked $/Wh, ${minppw}) and <b>{med10k}</b> at the median across the {n} models in the table below. The paths below use the table on this page as their price source — pick the rows, the math is shown.",
        "filter": "all",
        "table_heading": "Every 48V model the three paths are built from",
        "sections": [
            ("Path 1 — one 48V 200Ah battery (10.24kWh in a single case)", [
                "<p>A 48V 200Ah battery stores 51.2V × 200Ah = 10,240Wh by itself. It is the simplest install: one box, one set of cables, one BMS. The trade-offs are weight (a 200Ah floor battery is a two-person lift), a single point of failure, and a $/Wh that usually sits above the rack modules — the 200Ah-class rows in the table below show today's spread.</p>",
            ]),
            ("Path 2 — two server rack modules (2 × 5.12kWh)", [
                "<p>The value path, and the one installers use: two standard 48V 100Ah rack modules in parallel. Rack modules are routinely the cheapest rows in the table (the format is a commodity), they carry CAN/RS485 inverter communications the big floor batteries often lack, and the bank grows one module at a time — start at 10.24kWh, add a third module next year for 15.36kWh. Our sister tracker <a href=\"https://serverrackbatteries.com/10kwh-battery-bank/\">prices this exact build</a> on rack modules only.</p>",
            ]),
            ("Path 3 — a wall-mounted 10kWh unit", [
                "<p>Wall-mount 48V batteries (typically 51.2V 200Ah in a slim case) trade money for tidiness: no rack cabinet, no floor footprint, one clean box. Expect to pay a $/Wh premium over Path 2 for the same stored energy — the table makes the premium visible instead of arguable. This path suits garages and utility rooms where the install has to look finished.</p>",
            ]),
            ("Which path should you take?", [
                "<ul><li><b>Cheapest per kWh, plans to expand:</b> Path 2, rack modules.</li><li><b>Simplest wiring, one-and-done:</b> Path 1, single 200Ah unit.</li><li><b>Cleanest install, space-constrained:</b> Path 3, wall-mount — and price the premium in the table first.</li></ul>",
                "<p>Whichever path: the inverter must be a 48V model whose battery list (or voltage-based settings) covers your pick, and 10kWh of backup is a loads question before it is a shopping question — see the runtime framing on our <a href=\"/home-battery-system/\">home battery system page</a>.</p>",
            ]),
        ],
        "faqs": [
            ("How much does a 10kWh battery cost?",
             "Built from 48V LiFePO4 batteries at live maker prices, 10.24kWh of storage currently runs {low10k} at the cheapest tracked $/Wh to {med10k} at the median — batteries only. Packaged wall batteries and installed systems cost more per kWh; the table on this page is the live evidence."),
            ("How many 48V 100Ah batteries make 10kWh?",
             "Two. Each 48V 100Ah module stores 5.12kWh (51.2V × 100Ah), so two in parallel give 10.24kWh. Four give 20.48kWh. Modules must be the same brand and model, and the bank must stay within the model's parallel limit."),
            ("What will a 10kWh battery run?",
             "Roughly: a fridge, lights, internet and phones for about a day and a half; a typical critical-loads panel (adding a furnace blower) for about a day; or heavy loads like electric cooking and AC for a few hours. Runtime = 10,240Wh ÷ your average load in watts, minus ~10–15% inverter losses."),
        ],
        "related": ["home-battery-system", "server-rack-batteries", "home-battery-backup"],
    },
    {
        "slug": "price-per-watt-hour",
        "title": "Price per Watt-Hour: The Only Fair Way to Compare Battery Prices",
        "desc": "Why $/Wh beats sticker price and amp-hours when comparing batteries — the method behind every table on this site, with worked examples from live listings.",
        "h1": "Price per Watt-Hour, Explained with Live Numbers",
        "blurb": "The method behind every ranking on this site: why a $449 battery can be cheaper than a $300 one.",
        "lede": "Nobody searches for 'price per watt hour' — the phrase measures near zero volume, and this page exists anyway, because <b>$/Wh is the method behind every table on this site</b>. Sticker prices can't be compared across battery sizes; amp-hours can't be compared across voltages. Price per watt-hour fixes both. Right now, across {n} tracked 48V models, stored energy runs from <b>${minppw}/Wh to ${maxppw}/Wh</b> — a spread most shoppers never see because no maker publishes it against its competitors.",
        "filter": "top15",
        "ctx_filter": "all",
        "stats": False,
        "table_heading": "The 15 cheapest 48V batteries by $/Wh right now",
        "sections": [
            ("The worked example (today's live cheapest)", [
                "<p>The current $/Wh leader in the table below is the <b>{cheap_title}</b> at {cheap_price}. Its capacity is {cheap_cap}, so the math is {cheap_price} ÷ its watt-hours = <b>${cheap_ppw}/Wh</b>. Do the same division for any battery — price ÷ (volts × amp-hours) — and every product in this category lands on one comparable scale, whatever its size or shape.</p>",
            ]),
            ("Why amp-hours mislead", [
                "<table><thead><tr><th>Battery</th><th>Sticker</th><th>Energy</th><th>True cost</th></tr></thead><tbody>"
                "<tr><td>12V 100Ah</td><td>$250</td><td>1,280Wh</td><td class='num'>$0.195/Wh</td></tr>"
                "<tr><td>48V 100Ah</td><td>$900</td><td>5,120Wh</td><td class='num'>$0.176/Wh</td></tr>"
                "<tr><td>12V 314Ah</td><td>$450</td><td>4,019Wh</td><td class='num'>$0.112/Wh</td></tr>"
                "</tbody></table>",
                "<p>All three are '100Ah-class or bigger' products a shopper might cross-shop, and the biggest sticker hides the cheapest energy. Within one voltage, larger batteries almost always win on $/Wh (one case, one BMS, more cells); across voltages, amp-hours are meaningless until multiplied by volts. (Illustrative stickers — the live table below and on the homepage uses real, refreshed prices.)</p>",
            ]),
            ("When $/Wh is not the whole story", [
                "<ul><li><b>Features cost money:</b> self-heating, Bluetooth monitoring and inverter communications raise $/Wh — sometimes worth it (a frozen battery that can't charge is worth $0/Wh).</li><li><b>Form factor:</b> rack modules are cheap per Wh but need a rack and a 48V inverter; a drop-in 12V costs more per Wh and installs in minutes.</li><li><b>Warranty and support:</b> a premium brand at $0.30/Wh with a 10-year US warranty can be the rational buy over a $0.15/Wh no-name — $/Wh ranks price, not risk.</li></ul>",
                "<p>Our tables therefore sort by $/Wh and show the brand, capacity and price alongside — the sort is the method, the row is the context. The full method, including how prices are gathered and how stale data is hidden, is on the <a href=\"/about/\">about page</a>.</p>",
            ]),
        ],
        "faqs": [
            ("How do I calculate price per watt-hour?",
             "Divide the price by the battery's watt-hours. Watt-hours = nominal volts × amp-hours (a 51.2V 100Ah battery = 5,120Wh). A $860 battery at 5,120Wh costs $0.168/Wh. Multiply by 1,000 for $/kWh ($168/kWh)."),
            ("What is a good price per watt-hour for LiFePO4?",
             "It moves with the market, which is why this site tracks it live: the 48V table currently spans ${minppw}–${maxppw}/Wh with a ${medppw} median. As a orientation, bare batteries and rack modules sit at the low end; small, feature-heavy and premium-brand packs sit at the high end."),
            ("Why don't manufacturers advertise $/Wh?",
             "Because it makes premium pricing visible. A brand whose battery costs twice the $/Wh of a competitor's prefers to sell capacity stories, cycle counts and features. A price-per-unit table is the one comparison no single maker will publish against the whole market — so we do."),
        ],
        "related": ["48v-100ah-lifepo4-battery", "how-to-choose", "home-battery-system"],
    },
    {
        "slug": "whole-home-battery-backup",
        "title": "Whole-Home Battery Backup: How Much Storage a House Really Needs",
        "desc": "Whole-home backup is a loads problem, not a product: runtime math for 10, 20 and 30kWh banks, what stays on, and what the batteries cost at live $/Wh.",
        "h1": "Whole-Home Battery Backup, Priced and Sized Honestly",
        "blurb": "What 'whole-home' really takes: the load table, the 20kWh reality, and live battery costs.",
        "lede": "'Whole-home battery backup' (2,400 searches a month on each of its two phrasings) promises the whole house, but the honest version is a load table and a runtime division. A 10.24kWh bank runs essentials for about a day; genuine whole-home posture — well pump, HVAC blower, most circuits — starts at <b>20kWh and four rack-class modules</b>. The batteries for that bank currently cost <b>{low10k}–{med10k} per 10.24kWh</b> at live prices across the {n} models below. Here is the math before the shopping.",
        "filter": "all",
        "table_heading": "The 48V batteries whole-home banks are built from",
        "sections": [
            ("The load table nobody shows you", [
                "<table><thead><tr><th>Load</th><th>Draw</th><th>On 10.24kWh</th><th>On 20.48kWh</th></tr></thead><tbody>"
                "<tr><td>Fridge + lights + internet + phones</td><td>~300W avg</td><td>~28 hrs</td><td>~56 hrs</td></tr>"
                "<tr><td>Above + furnace blower (gas heat)</td><td>~600W avg</td><td>~14 hrs</td><td>~28 hrs</td></tr>"
                "<tr><td>Above + well pump cycling</td><td>~800W avg</td><td>~10 hrs</td><td>~21 hrs</td></tr>"
                "<tr><td>Above + mini-split AC (cycling)</td><td>~1,400W avg</td><td>~6 hrs</td><td>~12 hrs</td></tr>"
                "<tr><td>Electric range / dryer / EV charging</td><td>3,000W+</td><td>under 3 hrs</td><td>under 6 hrs</td></tr>"
                "</tbody></table>",
                "<p>Averages assume typical duty cycles and ~12% inverter losses; your furnace blower and pump will differ. The pattern is the point: each comfort load roughly halves runtime, and cooking/EV loads end the conversation — whole-home systems shed them by design, via a critical-loads panel or smart load management.</p>",
            ]),
            ("Critical loads vs true whole-home", [
                "<p>Most 'whole-home' installs are actually <b>critical-loads systems with a big bank</b>: a sub-panel carries the circuits that matter, and the 240V luxuries stay dark. True whole-home (a 200A service backed up wholesale) needs a high-power inverter stack and usually 30kWh+ — at live prices the batteries alone pass {med10k} well before that, which is why the honest middle is: 20kWh, a critical-loads panel, and a generator inlet for the multi-day outage.</p>",
                "<p>Sizing steps: (1) list the loads from the table you refuse to lose; (2) multiply their average watts by your target hours; (3) divide by 5,120Wh per module and round up; (4) check the answer against the table below — the $/Wh column is your storage cost, and our <a href=\"/home-battery-system/\">home battery system page</a> compares the DIY total against installed quotes.</p>",
            ]),
        ],
        "faqs": [
            ("How many kWh do I need for whole-home battery backup?",
             "For essentials-plus-comfort (fridge, lights, internet, furnace blower, well pump) through a full day, plan on ~20kWh — four 5.12kWh modules. Ten kWh covers the same loads for roughly half a day. True whole-service backup including electric cooking and AC starts around 30kWh and a much larger inverter."),
            ("Can a battery bank run my well pump and furnace?",
             "Yes — both are standard critical loads. A well pump's startup surge (often 2–3× its running watts) is the sizing constraint: the inverter must cover the surge, and the battery's discharge rating must feed it. That is an inverter spec check, not a storage problem."),
            ("What does a 20kWh DIY bank cost in batteries?",
             "At today's live prices, 10.24kWh of 48V storage runs {low10k} at the cheapest tracked $/Wh to {med10k} at the median — so roughly double that for 20.48kWh, before inverter, rack and electrical work. The table on this page is refreshed several times a day."),
        ],
        "related": ["home-battery-backup", "home-battery-system", "10kwh-battery"],
    },
    {
        "slug": "48v-314ah-lifepo4-battery",
        "title": "48V 314Ah LiFePO4 Batteries: 16kWh in One Case, Priced by $/Wh",
        "desc": "The 314Ah class stores ~16kWh in a single 48V battery and holds the portfolio's lowest $/Wh. Live prices for every 48V 280–330Ah model, refreshed {date}.",
        "h1": "48V 314Ah LiFePO4: The Biggest Single-Case Value in 48V",
        "blurb": "One case, ~16kWh, and the lowest $/Wh in the 48V catalog — the 314Ah class compared live.",
        "lede": "A 48V 314Ah battery stores about <b>16,000Wh in one case</b> — as much as three standard 100Ah modules — and because one case and one BMS carry all of it, the class holds the lowest $/Wh in this catalog: the current leader is <b>{cheap_price} (${cheap_ppw}/Wh)</b>. Only {n} models are tracked in this class today, so the table is short; the comparison math below is where the decision lives.",
        "filter": "ah280_330",
        "table_heading": "48V 314Ah-class batteries, ranked by $/Wh",
        "sections": [
            ("One 314Ah vs three 100Ah modules", [
                "<table><thead><tr><th></th><th>1 × 314Ah</th><th>3 × 100Ah</th></tr></thead><tbody>"
                "<tr><td>Energy</td><td>~16.0kWh</td><td>15.36kWh</td></tr>"
                "<tr><td>Cases / BMS units</td><td>1</td><td>3</td></tr>"
                "<tr><td>Wiring</td><td>One pair of cables</td><td>Busbar + 3 pairs, balanced leads</td></tr>"
                "<tr><td>Failure mode</td><td>Whole bank down</td><td>One module down, 2/3 capacity remains</td></tr>"
                "<tr><td>Expansion</td><td>Parallel a second 314Ah (32kWh)</td><td>Add modules one 5.12kWh step at a time</td></tr>"
                "</tbody></table>",
                "<p>The $/Wh column in the table prices the first option; the <a href=\"/48v-100ah-lifepo4-battery/\">100Ah table</a> prices the second. Neither is universally right: single-case wins on cost and simplicity, modules win on redundancy and incremental growth.</p>",
            ]),
            ("Who should not buy one", [
                "<ul><li><b>Anyone who can't move it:</b> a 314Ah 48V battery is a ~300 lb class object. Plan the install location before the purchase.</li><li><b>Anyone building incrementally on a budget:</b> the first step is the whole 16kWh; modules let you start at 5.12kWh.</li><li><b>Anyone whose inverter caps battery current low:</b> one BMS must supply the full discharge — check its continuous rating against your inverter's draw.</li></ul>",
            ]),
        ],
        "faqs": [
            ("How many kWh is a 48V 314Ah battery?",
             "51.2V × 314Ah ≈ 16.1kWh nominal; makers rate these units at about 16kWh. That equals roughly three 48V 100Ah modules (15.36kWh) in a single case."),
            ("Why is the 314Ah class cheaper per Wh?",
             "Fixed costs — case, BMS, terminals, shipping — are spread over 16kWh instead of 5.12kWh, and the cells themselves are the high-volume 314Ah format the industry standardized on. The table shows the result: this class holds the catalog's lowest $/Wh."),
            ("Can I parallel two 48V 314Ah batteries?",
             "Generally yes — most models in this class support parallel connection (commonly up to 4–16 units). Match brand and model, and confirm the limit and the communications wiring on the product page before ordering."),
        ],
        "related": ["48v-100ah-lifepo4-battery", "10kwh-battery", "solar-storage-batteries"],
    },
    {
        "slug": "off-grid-48v-battery-bank",
        "title": "Off-Grid 48V Battery Bank Sizing: Daily Cycles, Autonomy Days, Live Costs",
        "desc": "Off-grid banks are sized to daily consumption and cloudy-day autonomy, not outage hours. The method, a sizing table, and live 48V prices — refreshed {date}.",
        "h1": "Building an Off-Grid 48V Battery Bank That Survives November",
        "blurb": "Daily-cycle sizing for cabins and homesteads: consumption first, autonomy second, modules third.",
        "lede": "An off-grid bank is not a backup battery — it is the power company. Sizing flips accordingly: you start from <b>daily consumption</b> (not outage loads) and multiply by <b>autonomy days</b> (how many sunless days the bank must bridge). A frugal cabin at 5kWh/day with 2 days of autonomy needs 10kWh usable — call it 12kWh of nameplate — while a full homestead at 20kWh/day needs four times that. The {n} batteries below build either, at a live median of <b>${medppw}/Wh</b>.",
        "filter": "all",
        "table_heading": "48V batteries for off-grid banks, ranked by $/Wh",
        "sections": [
            ("The sizing table (nameplate, before you shop)", [
                "<table><thead><tr><th>Lifestyle</th><th>Daily use</th><th>2 days autonomy</th><th>Modules (5.12kWh)</th></tr></thead><tbody>"
                "<tr><td>Weekend cabin (lights, fridge, devices)</td><td>~3kWh</td><td>~7.5kWh nameplate</td><td>2</td></tr>"
                "<tr><td>Frugal full-time (efficient home, gas heat/cooking)</td><td>~8kWh</td><td>~20kWh nameplate</td><td>4</td></tr>"
                "<tr><td>Typical homestead (well pump, workshop, laundry)</td><td>~15kWh</td><td>~37kWh nameplate</td><td>8</td></tr>"
                "<tr><td>Comfort off-grid (mini-splits, EV top-ups)</td><td>25kWh+</td><td>62kWh+ nameplate</td><td>12+</td></tr>"
                "</tbody></table>",
                "<p>Nameplate includes the two off-grid realities: you plan to use ~80% of rated capacity day-to-day (LiFePO4 allows it, but headroom extends life), and autonomy is calculated on usable energy. The other half of the design is generation: the array must refill a day's use in a winter day's sun, or the biggest bank only delays the generator.</p>",
            ]),
            ("Why 48V is the off-grid default", [
                "<ul><li><b>Current stays sane:</b> a 5kW load draws ~100A at 48V vs ~400A at 12V — thinner cables, smaller breakers, less heat.</li><li><b>Inverter selection:</b> the serious off-grid inverter-chargers (and every hybrid worth its warranty) are 48V machines.</li><li><b>Daily cycling economics:</b> at one cycle a day, cycle life is calendar life — a 6,000-cycle bank is a 16-year asset, which is why the $/Wh you pay for it matters more off-grid than anywhere else. The table's sort is the whole argument.</li></ul>",
                "<p>For the grid-tied cousin of this math — sizing against outages instead of seasons — see the <a href=\"/whole-home-battery-backup/\">whole-home backup guide</a>; for the solar-first framing, the <a href=\"/solar-storage-batteries/\">solar storage table</a>.</p>",
            ]),
        ],
        "faqs": [
            ("How big should an off-grid battery bank be?",
             "Daily consumption × autonomy days ÷ 0.8 (usable share). A home using 10kWh/day that wants 2 sunless days needs ~25kWh nameplate — five 5.12kWh modules. Measure or honestly estimate daily kWh first; it is the number everything else multiplies."),
            ("How long does an off-grid LiFePO4 bank last?",
             "At one cycle per day, a bank rated 4,000–6,000 cycles reaches its cycle rating in 11–16 years, and LiFePO4 typically continues at reduced capacity beyond it. Calendar aging, heat and chronic undercharging from an undersized array are the usual real-world limiters."),
            ("Can I add modules to an off-grid bank later?",
             "Yes, within the model's parallel limit and ideally within the first year or two, matching brand and model. Off-grid banks commonly grow in stages — array first, bank second, or the reverse — as budget allows."),
        ],
        "related": ["solar-storage-batteries", "whole-home-battery-backup", "48v-314ah-lifepo4-battery"],
    },
    {
        "slug": "how-to-charge-48v-lifepo4-battery",
        "title": "How to Charge a 48V LiFePO4 Battery: 58.4V Settings, Closed-Loop, Mistakes",
        "desc": "The correct charge profile for a 51.2V LiFePO4 pack: 58.4V absorption, no equalization, when closed-loop comms matter, and the charger mistakes that shorten battery life.",
        "h1": "Charging a 48V LiFePO4 Battery: The 58.4V Rule",
        "blurb": "One voltage to remember, three ways to deliver it, and the lead-acid settings to never use.",
        "lede": "A '48V' LiFePO4 battery is a 51.2V pack, and it charges at <b>58.4V absorption</b> (16 cells × 3.65V) — that single number, plus 'no equalization, ever,' is most of this guide. Whether the voltage comes from an inverter-charger, a solar controller or a bench charger matters less than the profile being a lithium one. What follows is the settings table and the failure modes.",
        "filter": None,
        "sections": [
            ("The settings (for voltage-based charging)", [
                "<table><thead><tr><th>Parameter</th><th>48V LiFePO4 (51.2V pack)</th><th>Notes</th></tr></thead><tbody>"
                "<tr><td>Absorption / bulk target</td><td>58.4V (some makers specify 56.8–58.4V)</td><td>Hold briefly; LiFePO4 needs no long absorption soak</td></tr>"
                "<tr><td>Float</td><td>54.0–54.4V, or float off</td><td>For standby systems; cyclic systems can skip float</td></tr>"
                "<tr><td>Equalization</td><td><b>OFF — never</b></td><td>Equalize voltages (60V+) trip or damage the BMS</td></tr>"
                "<tr><td>Low-temp charge cutoff</td><td>0°C / 32°F</td><td>The BMS should enforce it; the charger setting is the second lock</td></tr>"
                "<tr><td>Charge current</td><td>0.2–0.5C typical (20–50A per 100Ah)</td><td>Check the model's max; slower is gentler</td></tr>"
                "</tbody></table>",
                "<p>If your battery talks to your inverter (CAN/RS485 closed-loop), the BMS sets these values itself and the table becomes a cross-check rather than an input — one reason rack modules, which almost all have comms, are forgiving in inverter systems. The <a href=\"/server-rack-batteries/\">rack-format page</a> covers that class.</p>",
            ]),
            ("The three charging mistakes that actually hurt", [
                "<ul><li><b>The lead-acid charger with equalization:</b> a 48V golf-cart or forklift charger that runs an automatic equalize cycle will push the pack over-voltage until the BMS disconnects — repeatedly, every charge. If the charger can't disable equalization, it can't charge lithium.</li><li><b>Charging below freezing:</b> lithium plates permanently when charged under 0°C. Unheated garage installs need a BMS with low-temp cutoff (verify it — not all have it) or a self-heating model.</li><li><b>Bank charging with mixed states of charge:</b> paralleling a full module with an empty one creates a large equalizing current between them. Bring modules to a similar voltage before connecting, and charge the bank as one battery thereafter.</li></ul>",
                "<p>Charging from solar follows the same profile through the MPPT's lithium setting; charging from the grid or a generator is the inverter-charger's job. Either way the battery only cares about the voltage curve and the temperature — see the batteries themselves, ranked by $/Wh, on the <a href=\"/\">48V table</a>.</p>",
            ]),
        ],
        "faqs": [
            ("What voltage should I charge a 48V LiFePO4 battery to?",
             "58.4V for a 51.2V (16-cell) pack — some manufacturers specify a 56.8–58.4V window, and their manual wins. Never use a charger whose profile exceeds 58.4V or runs an equalization stage."),
            ("Can I use my 48V lead-acid golf cart charger on LiFePO4?",
             "Only if it has a lithium profile or its equalization can be fully disabled and its output capped at 58.4V. Most basic lead-acid cart chargers fail one of those tests; a LiFePO4-profile 58.4V charger is the correct replacement."),
            ("How long does a 48V 100Ah battery take to charge?",
             "At a 50A charge rate, about 2 hours from empty plus a short absorption tail; at 20A, about 5 hours. In inverter systems the practical limit is usually the inverter-charger's charge rating or the solar array, not the battery."),
        ],
        "related": ["golf-cart-batteries", "solar-storage-batteries", "how-to-choose"],
    },
    {
        "slug": "eco-worthy-vs-litime-48v",
        "title": "Eco-Worthy vs LiTime 48V LiFePO4: Rack, Golf Cart and 16kWh, Live $/Wh",
        "desc": "Two different 48V catalogs: Eco-Worthy's {eco_worthy_n} tracked models (rack module, 16kWh floor battery, backup kit) vs LiTime's {litime_n} across golf cart, floor and rack — live $/Wh, refreshed {date}.",
        "h1": "Eco-Worthy vs LiTime 48V: Concentrated vs Everywhere",
        "blurb": "Eco-Worthy bets on a rack module and one huge floor battery; LiTime covers golf carts to rack. Live $/Wh sorts out the overlap.",
        "lede": "At 48V these brands barely overlap — and that is the comparison. Eco-Worthy's tracked catalog is <b>{eco_worthy_n} models</b>: a server rack module, a 16kWh-class floor battery, and a battery-plus-inverter backup kit. LiTime's is <b>{litime_n} models</b>, from 30Ah golf-cart packs to 100Ah floor and rack units. Where they do meet, the numbers are close: the cheapest stored energy across both catalogs is <b>${minppw}/Wh</b>, and the current leader is the <b>{cheap_title}</b> at {cheap_price}. Pick your job first below; then let the table price it.",
        "filter": "brand:Eco-Worthy+LiTime",
        "table_heading": "Eco-Worthy and LiTime 48V batteries, ranked by $/Wh",
        "sections": [
            ("The job decides the brand before price does", [
                "<table><thead><tr><th>Job</th><th>Eco-Worthy</th><th>LiTime</th></tr></thead><tbody>"
                "<tr><td>Home storage in a rack</td><td>Cubix100 100Ah rack module — its home-storage bet</td><td>ComFlex 100Ah rack module, plus a shelf of 100Ah floor units</td></tr>"
                "<tr><td>Big single-case storage (~16kWh)</td><td>314Ah-class floor battery — the $/Wh leader on this page</td><td>No 314Ah rival tracked; its big end is a 150Ah golf/UTV pack</td></tr>"
                "<tr><td>Golf cart conversion</td><td>Not its fight in this catalog</td><td>30Ah/60Ah GC2-format packs, 100Ah cart batteries and a full conversion kit</td></tr>"
                "<tr><td>One-box home backup</td><td>A 5.12kWh battery + 3.5kW inverter kit, priced as one row in the table</td><td>Batteries only — the inverter is a separate purchase</td></tr>"
                "</tbody></table>",
                "<p>That table is the honest summary: if your job is a golf cart, this head-to-head is over before price enters it, and the <a href=\"/golf-cart-batteries/\">golf cart table</a> is the right page. If your job is home storage, both brands are live options and the $/Wh column below is the arbiter.</p>",
            ]),
            ("Where they meet: the 100Ah / 5.12kWh class", [
                "<p>The overlap class is 48V 100Ah — 5,120Wh, the standard storage brick. Eco-Worthy fields it as a single rack module with inverter communications. LiTime fields it nine ways in this catalog: rack, floor, marine, Bluetooth and Victron-ready variants at several price tiers. Same stored energy in every one of those rows, so the spread between them is the price of format and features, stated in $/Wh instead of adjectives.</p>",
                "<ul><li><b>Rack format</b> buys CAN/RS485 closed-loop inverter pairing and one-module-at-a-time expansion — the home-storage default.</li><li><b>Floor format</b> buys simpler placement where no rack exists, often at a small $/Wh premium.</li><li><b>The 314Ah outlier:</b> Eco-Worthy's big floor battery undercuts every 100Ah row on $/Wh because one case and one BMS carry ~16kWh — the trade is a very heavy install and an all-or-nothing failure mode, detailed on the <a href=\"/48v-314ah-lifepo4-battery/\">314Ah page</a>.</li></ul>",
                "<p>One caution on the kit row: Eco-Worthy's home-backup bundle prices a battery <i>and</i> an inverter together, so its $/Wh reads high against bare batteries. It is in the table because the maker sells it that way — compare it against a battery-plus-inverter total, not against bare-battery rows.</p>",
            ]),
        ],
        "faqs": [
            ("Is Eco-Worthy or LiTime cheaper at 48V?",
             "By $/Wh, the current leader across both catalogs is the {cheap_title} at {cheap_price} (${cheap_ppw}/Wh). In the shared 100Ah class the brands sit within a few cents per watt-hour of each other and maker sales move the lead — the live table, refreshed several times a day, is the standing answer."),
            ("Which brand is better for a 48V golf cart conversion?",
             "In the catalogs tracked here, LiTime is the golf-cart brand: it fields GC2-format 30Ah/60Ah packs, cart-specific 100Ah units and a complete conversion kit, while Eco-Worthy's tracked 48V line is storage-focused. Whichever pack you choose, its continuous discharge rating must cover your controller's draw, and it needs a 58.4V LiFePO4-profile charger."),
            ("Can I parallel Eco-Worthy and LiTime 48V batteries together?",
             "Makers advise against it: match brand, model and age in a parallel bank, and closed-loop inverter communication needs one BMS protocol in charge. Build the bank from a single model — the per-module $/Wh saving compounds with every module you add."),
        ],
        "related": ["48v-100ah-lifepo4-battery", "48v-314ah-lifepo4-battery", "golf-cart-batteries"],
    },
    {
        "slug": "48v-lifepo4-series-parallel-guide",
        "title": "48V LiFePO4 in Series & Parallel: Why Parallel Is the Only Move",
        "desc": "Series-wiring 48V LiFePO4 would make a 102.4V battery almost no inverter accepts — and most makers prohibit it. Parallel is the scaling path: bank sizes priced live, busbar current math, and the expansion rules.",
        "h1": "48V LiFePO4 in Series and Parallel: Parallel Is the Whole Game",
        "blurb": "At 48V the series door is closed and parallel does all the scaling: bank sizes, current math, and adding modules without unbalancing the bank.",
        "lede": "At 12V, series and parallel are both tools. At 48V the answer flips: <b>series is effectively closed</b> — two 51.2V packs in series make a 102.4V battery that mainstream inverters cannot use and most makers explicitly prohibit — while <b>parallel is the designed scaling path</b>, commonly rated for <b>4–16 modules</b> depending on the model. Every bank this site prices, from a 10.24kWh backup to a 20kWh whole-home build, is a parallel story. The tracked 48V catalog ({n} models) currently starts at <b>${minppw}/Wh</b>; this guide is the parallel math that turns those rows into a bank.",
        "filter": None,
        "sections": [
            ("Why series stops at 48V", [
                "<table><thead><tr><th>Wiring two 48V 100Ah packs</th><th>Result</th><th>Verdict</th></tr></thead><tbody>"
                "<tr><td>In series</td><td>102.4V nominal · 100Ah · 10.24kWh, charging near 116.8V</td><td><b>Not a supported system voltage</b> — no mainstream 48V inverter accepts it, and the packs' BMS hardware is built for 51.2V-class service</td></tr>"
                "<tr><td>In parallel</td><td>51.2V · 200Ah · 10.24kWh</td><td>The standard bank step — same voltage, double the energy and double the available discharge current</td></tr>"
                "</tbody></table>",
                "<p>Higher-voltage storage does exist, but as a different product category: factory-matched high-voltage stacks with their own inverters, not loose 48V packs wired nose-to-tail. Within this category the rule is simple — <b>if a model's documentation does not explicitly rate it for series use, series is prohibited</b>, and in this catalog that documentation essentially never does. Treat any 'just wire two for 96V' forum advice as a warranty-voiding experiment: the first BMS to trip in a series string absorbs voltage it was never built for.</p>",
            ]),
            ("Parallel bank sizes, priced at today's $/Wh", [
                "<table><thead><tr><th>Modules in parallel (100Ah each)</th><th>Bank size</th><th>Batteries at the cheapest tracked $/Wh</th><th>Batteries at the median $/Wh</th></tr></thead><tbody>"
                "<tr><td>1</td><td>5.12kWh</td><td class='num'>{low5k}</td><td class='num'>{med5k}</td></tr>"
                "<tr><td>2</td><td>10.24kWh</td><td class='num'>{low10k}</td><td class='num'>{med10k}</td></tr>"
                "<tr><td>4</td><td>20.48kWh</td><td class='num'>2× the 10.24kWh row</td><td class='num'>2× the 10.24kWh row</td></tr>"
                "<tr><td>8</td><td>40.96kWh</td><td class='num'>4× the 10.24kWh row</td><td class='num'>4× the 10.24kWh row</td></tr>"
                "</tbody></table>",
                "<p>Costs are the battery line only, computed from the live $/Wh figures in the lede — rack, busbar, inverter and electrical work are separate, and the <a href=\"/10kwh-battery/\">10kWh page</a> works the most common target in full. Module size changes the step, not the method: a 314Ah floor battery is ~16kWh in a single case, so one unit parallels the way three 100Ah modules do — the <a href=\"/48v-314ah-lifepo4-battery/\">314Ah page</a> covers that class. What never changes is the ceiling: stay inside the model's stated parallel limit, however generous the bank table looks.</p>",
            ]),
            ("Current is the real design constraint", [
                "<p>Parallel wiring adds more than capacity — it adds discharge current, because each module's BMS contributes its rating to the bank. It also concentrates that current in your cabling. Size the copper from the inverter, not from the batteries:</p>",
                "<table><thead><tr><th>Inverter size</th><th>DC draw at 51.2V (approx.)</th><th>Wiring implication</th></tr></thead><tbody>"
                "<tr><td>3kW</td><td>~60A</td><td>One module can feed it; standard interconnects cope</td></tr>"
                "<tr><td>5kW</td><td>~100A</td><td>Two modules' BMS headroom; busbar territory begins</td></tr>"
                "<tr><td>8kW</td><td>~160A</td><td>Busbar with equal-length module leads — daisy-chained cables starve the far modules</td></tr>"
                "<tr><td>12kW</td><td>~235A</td><td>Serious copper and a main fuse rated for the full bank; professional design territory</td></tr>"
                "</tbody></table>",
                "<ul><li><b>Busbar over daisy-chain</b> once you pass two modules: every module gets its own equal-length pair to a common busbar, so current (and wear) shares evenly instead of favoring the module nearest the inverter.</li><li><b>Fuse the bank, not just the inverter:</b> a fuse or breaker per module string plus a main disconnect is the standard defensive layout for multi-module banks.</li><li><b>Communications are part of parallel wiring:</b> in an inverter system one module is the master — set the address/DIP switches per the manual and daisy-chain the CAN/RS485 link module to module, then master to inverter. A bank whose modules cannot agree on state of charge will charge unevenly no matter how good the copper is.</li></ul>",
            ]),
            ("Adding modules later, without unbalancing the bank", [
                "<ol><li><b>Same brand, same model.</b> A bank is one product repeated; a different model's BMS will not share current or communicate as an equal.</li><li><b>Sooner beats later.</b> Add within the first year or two where you can — a fresh module paralleled with a heavily cycled one will be dragged toward the older bank's behavior.</li><li><b>Match voltage before you connect.</b> Charge (or discharge) the new module until its resting voltage sits within a few tenths of a volt of the bank's, then connect. Skipping this dumps a large equalizing current through the interconnects the moment the terminals meet.</li><li><b>Re-commission the communications.</b> New module gets the next address, the master re-reads the bank, and the inverter's battery capacity setting goes up by 5.12kWh per module.</li><li><b>Re-check the ceiling.</b> The model's parallel limit and the inverter's maximum charge/discharge current both still apply to the enlarged bank.</li></ol>",
                "<p>Planned from the start, expansion is the format's whole advantage — it is why the <a href=\"/off-grid-48v-battery-bank/\">off-grid bank guide</a> and the <a href=\"/server-rack-batteries/\">rack-format page</a> both build their sizing around parallel steps rather than one heroic battery.</p>",
            ]),
        ],
        "faqs": [
            ("Can I connect 48V LiFePO4 batteries in series?",
             "Assume no. Two 51.2V packs in series produce 102.4V nominal — beyond the ratings of 48V-class BMS hardware and outside the battery input range of mainstream 48V inverters — and most makers prohibit it outright. Unless a model's documentation explicitly rates it for series use (rare in this class), series wiring risks BMS damage and voids the warranty. Higher-voltage systems exist as factory-matched stacks, a different product category."),
            ("How many 48V LiFePO4 batteries can I put in parallel?",
             "Commonly 4–16 units, depending on the model — rack modules often sit at the generous end because parallel expansion is their design brief. The exact limit is stated on the product page, and the bank must also respect the inverter's maximum battery current and capacity settings."),
            ("Can I parallel a rack battery with a floor battery?",
             "Electrically both are 51.2V, but makers advise one brand and model per bank: BMS behavior differs, current shares unevenly, and closed-loop inverter communication needs a single protocol in charge — a mixed bank usually falls back to voltage-based charging and loses the smart features you paid for. The tables on this site price single-model banks; the saving from mixing rarely survives the compromises."),
        ],
        "related": ["48v-100ah-lifepo4-battery", "server-rack-batteries", "off-grid-48v-battery-bank"],
    },
    {
        "slug": "golf-cart-lithium-conversion-mistakes",
        "title": "Golf Cart Lithium Conversion Mistakes: The 7 That Cost Money",
        "desc": "Most failed 48V golf cart lithium conversions are not battery failures — they are charger, current-rating and wiring mistakes made before the pack ever turns a wheel. The seven, priced against live packs.",
        "h1": "Golf Cart Lithium Conversion Mistakes: The Pack Is Rarely the Problem",
        "blurb": "Seven conversion mistakes — the wrong charger, an undersized discharge rating, reused corroded cables — and the checklist that avoids all of them.",
        "lede": "A 48V lithium conversion looks like a battery swap and behaves like a small electrical project. The packs themselves are the reliable part — the {n} golf-cart models in the live table below start at <b>${minppw}/Wh</b> (cheapest today: <b>{cheap_title}</b> at {cheap_price}) — while the failures cluster around everything the pack connects to: the charger it inherits, the controller current it must feed, and wiring that was already tired under lead-acid. These are the seven mistakes that turn a good pack into a bad conversion, in the order they usually bite.",
        "filter": "golf",
        "table_heading": "The 48V golf cart packs this guide is priced against, ranked by $/Wh",
        "sections": [
            ("Mistakes 1–3: the electrical mismatches", [
                "<p><b>1. Keeping the lead-acid charger.</b> The single most common conversion failure. A 48V lead-acid cart charger is built to push a finishing voltage lead-acid likes and, on many models, to run an automatic equalization stage — voltages a LiFePO4 pack's BMS will (correctly) refuse by disconnecting, mid-charge, every charge. If the old charger has no lithium profile and cannot cap output at <b>58.4V</b> with equalization fully off, it is not a charger for your new pack; it is a recurring fault. Budget the LiFePO4-profile charger as part of the conversion, not as an accessory — the full settings table is in the <a href=\"/how-to-charge-48v-lifepo4-battery/\">48V charging guide</a>.</p>",
                "<p><b>2. Buying amp-hours and ignoring discharge current.</b> A cart controller does not sip: acceleration and hills ask for short, heavy current draws, and the pack's <i>continuous discharge rating</i> (set by its cells and BMS) is the number that decides whether the cart pulls cleanly or sags and cuts out under load. This is where the table's small rows mislead the unwary: a single 30Ah GC2-format pack is a building block meant to be paralleled into a set, not a whole cart battery, and its current ceiling is a fraction of a 100Ah pack's. Match the pack (or paralleled set) to your controller's rating first; the $/Wh column only gets a vote after the current math passes.</p>",
                "<p><b>3. Forgetting the cart's own charge gatekeeper.</b> Some carts — Club Car's onboard computer is the famous case — route charging through electronics programmed around lead-acid behavior, and a lithium pack behind them charges erratically or not at all until the conversion addresses it (a bypass or a kit designed for the cart). It is also why complete conversion kits exist as a category: one row in the table below is a battery-plus-hardware kit priced as a single product. Before ordering any pack, search your exact cart model plus 'OBC' and 'lithium conversion' — ten minutes of reading beats a weekend of troubleshooting.</p>",
            ]),
            ("Mistakes 4–7: the physical and system oversights", [
                "<p><b>4. Reusing tired cables and skipping the fuse.</b> Conversion day reveals cables that were 'fine' for years: green corrosion at the lugs, insulation rubbed thin, a main cable one gauge optimistic. Lead-acid's internal resistance forgave some of that; lithium's low resistance delivers fault current far faster, which makes a proper main fuse or breaker and clean, correctly gauged cables more important after the swap, not less. If a cable looks questionable next to the old pack, it does not get promoted to the new one.</p>",
                "<p><b>5. Being surprised by the missing 250 pounds.</b> A six-battery 48V lead-acid set typically weighs in the region of 350–400 lb; a single 100Ah lithium pack is roughly a quarter of that (typical class figures, not tracked prices). The cart will ride higher, handle lighter and stop differently, and weight that used to sit low and central is simply gone. None of this is a reason to stay with lead — the acceleration and hill-climbing gains are the point of converting — but check the pack is properly secured in the tray (an unsecured 100 lb pack in a cart that now corners lighter is its own mistake), and expect to re-learn the cart's braking feel on the first drives.</p>",
                "<p><b>6. Mixing chemistries or models 'temporarily'.</b> One old lead-acid left in the string, or a second lithium pack of a different model paralleled in later, unbalances everything: the odd unit charges and discharges on a different curve, ages fast, and drags the bank with it. A conversion is all one chemistry, one brand, one model — and if range anxiety is the worry, the honest fix is the next capacity step in the table, not a hybrid string.</p>",
                "<p><b>7. No plan for a cold garage.</b> Carts live in unheated sheds, and a LiFePO4 pack must not be <i>charged</i> below freezing (0°C / 32°F) — discharging in the cold is fine, charging plates lithium and permanently costs capacity. If your cart charges outdoors through a northern winter, low-temperature charge protection on the pack's BMS is not a premium feature, it is the feature — verify it on the product page of any row below, or make 'charge it in the warm' a hard household rule.</p>",
            ]),
            ("The pre-flight checklist (run it before you pay)", [
                "<table><thead><tr><th>Check</th><th>Pass looks like</th></tr></thead><tbody>"
                "<tr><td>Charger</td><td>LiFePO4 profile, 58.4V cap, equalization off or absent — bought or verified, not assumed</td></tr>"
                "<tr><td>Discharge rating</td><td>Pack (or paralleled GC2 set) continuous rating covers your controller's draw, hills included</td></tr>"
                "<tr><td>Cart electronics</td><td>Your model's onboard-computer / charging path checked for a lithium path or bypass</td></tr>"
                "<tr><td>Cables & protection</td><td>Clean lugs, correct gauge, main fuse/breaker fitted, pack physically secured</td></tr>"
                "<tr><td>One chemistry</td><td>All lead-acid out; bank is a single brand and model</td></tr>"
                "<tr><td>Cold plan</td><td>Low-temp charge protection verified, or charging happens somewhere above freezing</td></tr>"
                "</tbody></table>",
                "<p>Run those six and the remaining decision is the pleasant one: which row of the table. The <a href=\"/golf-cart-batteries/\">golf cart table</a> carries the same packs with the full buying notes, and the <a href=\"/eco-worthy-vs-litime-48v/\">Eco-Worthy vs LiTime 48V comparison</a> covers the two brands that dominate this catalog if your cart build grows into a storage build.</p>",
            ]),
        ],
        "faqs": [
            ("What is the most common golf cart lithium conversion mistake?",
             "Keeping the lead-acid charger. Its finishing and equalization voltages exceed what a 51.2V LiFePO4 pack accepts (58.4V cap), so the pack's BMS disconnects mid-charge, repeatedly. A LiFePO4-profile 58.4V charger — or an old charger verifiably set to one — is part of the conversion cost."),
            ("How big a lithium battery does a 48V golf cart need?",
             "Most conversions land on a single 100Ah-class pack (5.12kWh) — the cheapest of them in the live table is the {cheap_title} at {cheap_price}. Smaller GC2-format packs are building blocks to parallel into a set, not standalone cart batteries. Whatever the capacity, the pack's continuous discharge rating must cover the controller's draw; capacity alone does not make a pack suitable."),
            ("Can I mix one lithium battery with my remaining lead-acid batteries?",
             "No. The two chemistries charge and discharge on different curves and at different voltages per unit, so a mixed string unbalances immediately: the lithium unit is overworked, the lead-acid units are undercharged, and both age fast. Convert the whole string at once."),
        ],
        "related": ["golf-cart-batteries", "how-to-charge-48v-lifepo4-battery", "eco-worthy-vs-litime-48v"],
    },
    {
        "slug": "48v-vs-12v-for-solar",
        "title": "48V vs 12V for Solar: Current, Cable Loss and Inverter Classes Decide It",
        "desc": "For solar, voltage is a current decision: the same 3,000W inverter draws ~234A at 12V and ~59A at 48V. The cable-loss math, the size thresholds, and live 48V prices — refreshed {date}.",
        "h1": "48V vs 12V for Solar: The Same Watts, a Quarter of the Current",
        "blurb": "12V wins small and mobile; 48V wins everything stationary above ~2kW. The current table and loss math that draw the line.",
        "lede": "This is not a chemistry fight — both sides are the same LiFePO4 cells. It is a <b>current</b> fight. Power is volts × amps, so moving a given load at 48V instead of 12V needs <b>one quarter of the amps</b>, and cable losses fall with the <i>square</i> of current. That single fact sorts the solar world: 12V serves small, mobile, low-power systems well, and 48V takes over as soon as an inverter passes roughly <b>2kW</b> or a bank passes roughly <b>5kWh</b>. The 48V side of the argument is priced live below — {n} tracked models from <b>${minppw}/Wh</b> — and our sister tracker prices the 12V side the same way.",
        "filter": "all",
        "table_heading": "The 48V batteries this comparison lands on, ranked by $/Wh",
        "sections": [
            ("The current table (memorize this, not the marketing)", [
                "<table><thead><tr><th>Inverter / load</th><th>Draw at 12.8V</th><th>Draw at 51.2V</th><th>What that means for cable</th></tr></thead><tbody>"
                "<tr><td>1,000W</td><td>~78A</td><td>~20A</td><td>Both easy; 12V still in ordinary cable sizes</td></tr>"
                "<tr><td>2,000W</td><td>~156A</td><td>~39A</td><td>12V needs heavy, short, expensive runs; 48V is routine</td></tr>"
                "<tr><td>3,000W</td><td>~234A</td><td>~59A</td><td>12V is specialist territory; 48V still unremarkable</td></tr>"
                "<tr><td>5,000W</td><td>~391A</td><td>~98A</td><td>Effectively 48V-only for a sane install</td></tr>"
                "</tbody></table>",
                "<p>Draws are watts ÷ nominal pack voltage, before inverter inefficiency — real draws run roughly 10% higher, which only widens the gap. Cable loss is I²R: at four times the current, the <i>same</i> cable wastes sixteen times the power as heat, and the voltage drop (four times larger in volts, on a system voltage four times smaller) is sixteen times worse in percentage terms. You can buy your way out at 12V with very thick, very short copper — past 2kW you are mostly paying to postpone the conclusion.</p>",
            ]),
            ("Where 12V genuinely wins", [
                "<ul><li><b>Vehicles and boats:</b> the alternator, starter, lights and most accessories already speak 12V. A van or RV house bank at 12V charges from the engine through a DC-DC charger and runs native 12V loads with no conversion — the whole reason our sister site's <a href=\"https://12vlifepo4battery.com/van-life-battery-sizing/\">van-life sizing guide</a> stays at 12V.</li><li><b>Small solar:</b> a cabin or shed system under ~1kW of inverter and a battery or two has no current problem to solve, and 12V gear is the cheapest and most available in the category.</li><li><b>One-battery simplicity:</b> a single drop-in 12V pack plus a small inverter is an afternoon install; a 48V system is an inverter-charger, a bank plan and a wiring standard.</li></ul>",
                "<p>The 12V catalog is also deeper and its small packs are cheaper in absolute dollars — compare it live on <a href=\"https://12vlifepo4battery.com/\">12vlifepo4battery.com</a>, ranked by the same $/Wh method. What 12V cannot do is repeal the current table above.</p>",
            ]),
            ("Where 48V takes over — and the trap in between", [
                "<ul><li><b>Whole-home and off-grid solar:</b> hybrid inverter-chargers in the 3–12kW class are 48V machines, rack modules with closed-loop BMS communication are a 48V format, and banks of 10–40kWh wire in parallel without heroic copper. This site's <a href=\"/solar-storage-batteries/\">solar storage table</a> and <a href=\"/off-grid-48v-battery-bank/\">off-grid bank guide</a> are this world.</li><li><b>The in-between trap is 24V thinking applied at 48V scale:</b> builders sometimes series two or four 12V packs to reach a higher voltage instead of buying native 48V units. Series strings of drop-ins carry per-pack BMS limits and balancing headaches detailed in the <a href=\"/48v-lifepo4-series-parallel-guide/\">series-parallel guide</a> — if the system is 48V, buy 48V batteries.</li><li><b>Expansion economics:</b> at 48V the next 5.12kWh is one rack module on a busbar. At 12V, banks past ~5kWh mean paralleling many packs, each with its own BMS and leads, and current-sharing gets fussier with every addition.</li></ul>",
                "<table><thead><tr><th>Your system</th><th>Verdict</th></tr></thead><tbody>"
                "<tr><td>Van, RV, boat, &lt;1kW inverter</td><td>12V — native loads, alternator charging, deepest small-pack catalog</td></tr>"
                "<tr><td>Cabin / shed solar, 1–2kW, 1–2 batteries</td><td>Either — decide by whether it will ever grow; growth argues 48V now</td></tr>"
                "<tr><td>Home backup or off-grid, 3kW+, 10kWh+</td><td>48V — current, inverter class and rack format all point the same way</td></tr>"
                "</tbody></table>",
            ]),
        ],
        "faqs": [
            ("Is 48V better than 12V for solar?",
             "For stationary systems above roughly 2kW of inverter or 5kWh of storage, yes — a quarter of the current, a sixteenth of the cable loss on the same copper, and access to the mainstream hybrid inverter-chargers and rack modules. Below that, or in a vehicle, 12V's native loads, alternator charging and deeper small-pack catalog make it the practical choice."),
            ("Can I series four 12V batteries to make a 48V solar bank?",
             "Some 12V models permit 4-in-series use and some prohibit it — the model's stated series limit decides, and each pack's BMS must be rated for the full string voltage. Even when permitted, a series string balances worse and fails less gracefully than native 48V units, which is why this site prices native 48V batteries for 48V systems."),
            ("Does 48V save money, or just cable?",
             "Both, past the threshold: the batteries themselves are priced live in the table (currently from ${minppw}/Wh), thinner copper and smaller breakers cut install cost, and the rack format that dominates 48V storage is routinely the cheapest stored energy in either catalog. Under the threshold, a 12V system's cheaper small gear wins the total."),
        ],
        "related": ["solar-storage-batteries", "off-grid-48v-battery-bank", "48v-lifepo4-series-parallel-guide"],
    },
],
"12vlifepo4battery.com": [
    {
        "slug": "100ah-lifepo4-battery",
        "title": "100Ah LiFePO4 Battery: 12V, 24V and 48V Compared by $/Wh",
        "desc": "A 100Ah LiFePO4 battery is three different products depending on voltage — 1,280Wh, 2,560Wh or 5,120Wh. Live 12V prices ranked by $/Wh, refreshed {date}.",
        "h1": "100Ah LiFePO4 Batteries: Voltage Changes Everything",
        "blurb": "The voltage-free phrase, decoded: what 100Ah means at 12V, 24V and 48V — and the live 12V table.",
        "lede": "Search for a '100Ah LiFePO4 battery' and every top result is a 12V product — because at 100Ah, voltage is the whole story. A 12V 100Ah battery stores <b>1,280Wh</b>; a 48V 100Ah stores <b>5,120Wh</b>, four times the energy behind the same '100Ah' label. This page compares all three voltages honestly, then ranks the 12V models — the ones most buyers actually want — by live $/Wh: {n} models, from <b>${minppw}/Wh</b>.",
        "filter": "ah90_115",
        "table_heading": "12V 100Ah LiFePO4 batteries, ranked by $/Wh",
        "sections": [
            ("Same 100Ah, three different batteries", [
                "<table><thead><tr><th>Voltage</th><th>Energy at 100Ah</th><th>Typical job</th><th>Where it lives</th></tr></thead><tbody>"
                "<tr><td>12V (12.8V nominal)</td><td>1,280Wh</td><td>RVs, boats, trolling motors, small solar</td><td>This page's table</td></tr>"
                "<tr><td>24V (25.6V nominal)</td><td>2,560Wh</td><td>Large trolling motors, trucks, mid-size off-grid</td><td>Thinner market — fewer makers, less price competition</td></tr>"
                "<tr><td>48V (51.2V nominal)</td><td>5,120Wh</td><td>Home storage, golf carts, server racks</td><td><a href=\"https://48vlifepo4battery.com/48v-100ah-lifepo4-battery/\">48V 100Ah table</a> on our sister site</td></tr>"
                "</tbody></table>",
                "<p>Amp-hours measure charge, not energy. Comparing a 12V 100Ah at $200 against a 48V 100Ah at $900 by sticker — or by 'cost per Ah' — gets the answer backwards: the 48V battery holds 4× the energy. The only fair cross-voltage unit is $/Wh, which is how every table here is sorted.</p>",
            ]),
            ("Buying the 12V version: the three checks that matter", [
                "<ul><li><b>Group size:</b> Group 24 and Group 31 are the common cases; measure your battery box before ordering — a 100Ah label says nothing about dimensions.</li><li><b>Low-temperature protection:</b> a BMS that blocks charging below freezing is essential for RV, marine and ice-season use; not every budget 100Ah has it.</li><li><b>Series rating:</b> if you might wire two for 24V later, the model must be series-rated (many are 4S-capable; some budget packs are parallel-only).</li></ul>",
                "<p>Beyond those, the table is the decision: every row stores the same 1,280Wh, so the $/Wh column is a pure price ranking. The dedicated <a href=\"/12v-100ah-lifepo4-battery/\">12V 100Ah page</a> goes deeper on this class; the <a href=\"/how-to-choose/\">buying guide</a> covers the rest of the checklist.</p>",
            ]),
        ],
        "faqs": [
            ("How many watt-hours is a 100Ah LiFePO4 battery?",
             "It depends on voltage: 12V × 100Ah = 1,280Wh (at 12.8V nominal), 24V = 2,560Wh, 48V = 5,120Wh. Always convert to watt-hours before comparing prices across voltages."),
            ("How long will a 12V 100Ah LiFePO4 battery run a fridge?",
             "A modern fridge draws roughly 1–1.5kWh per day. A 12V 100Ah battery holds 1,280Wh, of which about 1,090Wh is usable through an inverter — so expect most of a day to a full day for the fridge alone, longer for efficient 12V compressor fridges that skip the inverter."),
            ("Is a 100Ah LiFePO4 better than two 50Ah?",
             "Usually, on price: one 100Ah pack has one BMS and one case, so its $/Wh is typically lower, and wiring is simpler. Two smaller packs give redundancy and fit split battery boxes. The table's $/Wh column settles the price side for the models tracked here."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-200ah-lifepo4-battery", "how-to-choose"],
    },
    {
        "slug": "litime-vs-renogy-12v-100ah",
        "title": "LiTime vs Renogy 12V 100Ah: Live Prices, Lineup Depth, $/Wh",
        "desc": "The two deepest 12V catalogs head to head in the 100Ah class — live $/Wh, cheapest models and lineup depth from maker-store prices, refreshed {date}.",
        "h1": "LiTime vs Renogy: The 12V 100Ah Price Fight, Live",
        "blurb": "Value brand vs premium brand in the market's most popular size — settled with live prices, not review scores.",
        "lede": "In the 12V 100Ah class, LiTime and Renogy are the two catalogs with real depth — <b>{litime_n} LiTime models and {renogy_n} Renogy models</b> are tracked in the table below. The live numbers frame the rivalry: LiTime's cheapest 100Ah-class model is <b>{litime_min_price} (${litime_min_ppw}/Wh)</b>; Renogy's is <b>{renogy_min_price} (${renogy_min_ppw}/Wh)</b>. Everything else is positioning — here is what the positioning is worth.",
        "filter": "brand:LiTime+Renogy@ah90_115",
        "table_heading": "LiTime and Renogy 12V 100Ah-class batteries, ranked by $/Wh",
        "sections": [
            ("Two different bets on the same battery", [
                "<p><b>LiTime's bet is price per watt-hour.</b> Its 100Ah line spans bare-bones packs through Bluetooth and low-temperature variants, and its cheapest rows anchor the bottom of this table. The catalog is wide because the strategy is: a LiTime at every feature tier, each priced to be the $/Wh problem for everyone else.</p>",
                "<p><b>Renogy's bet is the system around the battery.</b> Renogy sells panels, charge controllers, inverters and monitoring as one ecosystem, and its battery prices carry that premium — its Pro and smart lines add self-heating and app monitoring, and its retail presence (including marketplace storefronts) is broader. Buyers already inside the Renogy ecosystem pay for one support door and matched components.</p>",
            ]),
            ("Reading the table like a buyer", [
                "<ul><li><b>Same energy, every row:</b> all models here are ~1,280Wh, so $/Wh is a pure price comparison — no capacity excuses.</li><li><b>Feature tiers explain the spread:</b> within each brand, the jump from the cheapest row buys Bluetooth, low-temp protection or self-heating. Decide which features you need before comparing stickers across brands.</li><li><b>Depth is a tiebreaker:</b> {litime_n} vs {renogy_n} tracked models means both brands will have a variant that fits your box and your charger; neither leaves you stranded on sizing.</li></ul>",
                "<p>For the full class — including the budget brands undercutting both — see the complete <a href=\"/12v-100ah-lifepo4-battery/\">12V 100Ah table</a>. If your shortlist is really 'value vs premium,' the two cheapest rows of each brand in the table above are the honest shortlist.</p>",
            ]),
        ],
        "faqs": [
            ("Is LiTime or Renogy cheaper for 12V 100Ah?",
             "On live maker-store prices, LiTime's cheapest 100Ah-class model is {litime_min_price} (${litime_min_ppw}/Wh) against Renogy's {renogy_min_price} (${renogy_min_ppw}/Wh). Renogy's premium buys its ecosystem and smart features; the table shows the current gap rather than a remembered one."),
            ("Are LiTime and Renogy batteries the same capacity?",
             "In this class, yes: both brands' 100Ah models store 1,280Wh (12.8V × 100Ah). Differences are BMS features (Bluetooth, low-temperature protection, self-heating), case size, warranty terms and price — not energy."),
            ("Can I mix LiTime and Renogy batteries in one bank?",
             "Manufacturers advise against mixing brands, models or ages in a series/parallel bank — BMS behaviors differ and the weakest unit limits the string. Pick one brand per bank; the price difference is rarely worth the imbalance risk."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "100ah-lifepo4-battery", "12v-200ah-lifepo4-battery"],
    },
    {
        "slug": "12v-lifepo4-battery-for-solar",
        "title": "12V LiFePO4 Batteries for Solar: Panel-to-Battery Sizing, Live Prices",
        "desc": "Which 12V LiFePO4 batteries makers sell for solar, how much panel a 100Ah battery can absorb, and live $/Wh prices — refreshed {date}.",
        "h1": "12V LiFePO4 for Solar: Sized Right, Priced by $/Wh",
        "blurb": "Solar-marketed 12V packs, the panel-to-battery ratios that keep them full, ranked live.",
        "lede": "A solar battery's job is different from an RV battery's: it cycles daily, sits at partial charge, and must drink everything the panels make by mid-afternoon. The {n} models below are the 12V LiFePO4 batteries makers position for solar and off-grid use, ranked by $/Wh from <b>${minppw}</b>. The sizing ratios come first, because the wrong ratio wastes panels or starves the bank.",
        "filter": "solar_kw",
        "table_heading": "12V LiFePO4 batteries sold for solar, ranked by $/Wh",
        "sections": [
            ("Panel-to-battery ratios that work", [
                "<table><thead><tr><th>Battery</th><th>Energy</th><th>Sensible panel range</th><th>Full charge from empty*</th></tr></thead><tbody>"
                "<tr><td>12V 100Ah</td><td>1,280Wh</td><td>200–400W</td><td>~4–5 sun-hours at 300W</td></tr>"
                "<tr><td>12V 200Ah</td><td>2,560Wh</td><td>400–800W</td><td>~4–5 sun-hours at 600W</td></tr>"
                "<tr><td>12V 314Ah</td><td>4,019Wh</td><td>600–1,200W</td><td>~4–5 sun-hours at 900W</td></tr>"
                "</tbody></table>",
                "<p>*After controller losses, on a clear day, with the battery as the only load. Undersize the panels and a big bank never fills (a LiFePO4 tolerates that, but you paid for capacity you can't fill); oversize them and a small bank is full by 10am while harvest is thrown away. Daily cycling is also where LiFePO4's cycle life pays: at one cycle a day, a 4,000-cycle rating is a decade of service.</p>",
            ]),
            ("Solar-specific checks", [
                "<ul><li><b>Charge controller profile:</b> your MPPT must have a lithium/LiFePO4 profile (14.2–14.6V absorption, no equalization). A lead-acid-only controller undercharges and can damage the BMS over time.</li><li><b>Low-temp protection:</b> an unheated shed or cabin install needs a BMS that blocks sub-freezing charging — solar charges whenever the sun shines, including at -5°F.</li><li><b>Idle draw:</b> a battery that sits in a cabin system all winter should have a true off state or very low self-discharge; LiFePO4's ~1–3%/month is one of its quiet advantages over lead-acid.</li></ul>",
                "<p>For loads-first sizing (what the bank must run, not what the panels make), the <a href=\"/how-to-choose/\">12V buying guide</a> starts from watt-hours of demand; the <a href=\"/rv-batteries/\">RV page</a> covers the same batteries in a vehicle context.</p>",
            ]),
        ],
        "faqs": [
            ("How many solar panels do I need for a 12V 100Ah LiFePO4 battery?",
             "Roughly 200–400W of panel. At 300W and 4–5 good sun-hours, you harvest about 1.2–1.5kWh on a clear day — enough to refill a 1,280Wh battery from empty while covering light daytime loads. More panel helps in winter and cloudy climates."),
            ("Can a 12V LiFePO4 battery sit at partial charge?",
             "Yes — unlike lead-acid, LiFePO4 is comfortable at partial state of charge and does not sulfate. Storing it around 50–80% and cycling daily is normal solar service; avoid only the extremes of sitting at 100% for months in high heat."),
            ("Do I need a special charge controller for LiFePO4 solar?",
             "You need one with a LiFePO4/lithium profile: 14.2–14.6V absorption, no equalization stage, and ideally a low-temperature charge cutoff paired with the battery's own BMS protection. Most modern MPPT controllers include the profile."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-314ah-lifepo4-battery", "how-to-choose"],
    },
    {
        "slug": "how-long-will-12v-100ah-run-a-fridge",
        "title": "How Long Will a 12V 100Ah Battery Run a Fridge? The Honest Math",
        "desc": "Runtime depends on the fridge, not the battery: duty-cycle math for home fridges, 12V compressor fridges and mini fridges on 1,280Wh — plus the batteries, priced live.",
        "h1": "How Long a 12V 100Ah Battery Runs a Fridge (It's the Fridge's Fault)",
        "blurb": "One battery, three fridges, three very different answers — the duty-cycle math, done openly.",
        "lede": "The battery is the constant — <b>1,280Wh</b>, of which about <b>980Wh reaches a home fridge</b> after inverter losses. The fridge is the variable: a modern full-size fridge eats 1.0–1.5kWh a day (answer: <b>most of a day</b>), while a 12V compressor fridge sips 0.35–0.6kWh a day (answer: <b>2–3 days</b>). The table below shows the arithmetic for each fridge class, and the live table under it prices the batteries.",
        "filter": "ah90_115",
        "table_heading": "The 12V 100Ah batteries this math runs on",
        "sections": [
            ("Runtime by fridge class", [
                "<table><thead><tr><th>Fridge</th><th>Daily energy</th><th>Runtime on 1 × 100Ah</th><th>Runtime on 2 × 100Ah</th></tr></thead><tbody>"
                "<tr><td>12V compressor fridge/freezer (35–55L)</td><td>0.35–0.6kWh</td><td>~2–3 days (no inverter)</td><td>~4–6.5 days</td></tr>"
                "<tr><td>Modern full-size home fridge</td><td>1.0–1.5kWh</td><td>~16–23 hrs</td><td>~1.3–2 days</td></tr>"
                "<tr><td>Older / garage fridge</td><td>1.5–2.5kWh</td><td>~9–15 hrs</td><td>~1–1.3 days</td></tr>"
                "<tr><td>Mini fridge</td><td>0.7–1.0kWh</td><td>~1–1.4 days</td><td>~2–3 days</td></tr>"
                "</tbody></table>",
                "<p>Daily-energy figures are typical consumption ranges, not measurements of your fridge — the next section shows how to get your number. Home-fridge runtimes assume a pure-sine inverter at ~85% efficiency and a battery used to ~90% depth, which LiFePO4 tolerates daily.</p>",
            ]),
            ("Why the nameplate watts lie (duty cycle)", [
                "<p>A fridge rated '150W' does not draw 150W all day — its compressor cycles, typically running 30–50% of the time in a cool room and 60%+ in a hot garage. Runtime math must use <b>average</b> watts: nameplate × duty cycle. 150W × 40% = 60W average = 1.44kWh/day, which is why the home-fridge row above lands where it does. The reliable way to know yours: a plug-in energy meter (Kill A Watt style) over 48 hours gives you the exact kWh/day — a $20 measurement that replaces every estimate on this page.</p>",
                "<p>Two levers extend runtime more than any battery upgrade: keep the fridge out of the heat (duty cycle falls), and skip the inverter where you can — a 12V compressor fridge runs straight off the battery, which is why its row laps the field. If the goal is multi-day fridge backup, the <a href=\"/12v-200ah-lifepo4-battery/\">200Ah class</a> doubles every number in the table at a lower $/Wh.</p>",
            ]),
        ],
        "faqs": [
            ("How long will a 100Ah LiFePO4 run a 12V fridge?",
             "A 12V compressor fridge uses about 0.35–0.6kWh per day, and a 100Ah LiFePO4 delivers ~1,150Wh DC without inverter losses — so roughly 2 to 3 days, depending on ambient temperature and how often the lid opens."),
            ("Will a 12V 100Ah battery run a full-size fridge overnight?",
             "Yes, with margin: overnight (8–10 hours) a modern home fridge needs roughly 0.4–0.6kWh, and the battery delivers ~0.98kWh through an inverter. A full day is the realistic ceiling; two days needs a second battery or the 200Ah class."),
            ("Does the inverter waste a lot of battery?",
             "About 15%: conversion losses plus the inverter's own idle draw (10–25W just being on — up to 0.5kWh/day if left idling, which is why the runtime table assumes sensible use). A DC fridge avoids both penalties entirely."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "100ah-lifepo4-battery", "12v-200ah-lifepo4-battery"],
    },
    {
        "slug": "12v-lifepo4-charging-guide",
        "title": "12V LiFePO4 Charging Guide: 14.4V Profile, Charge Times, Cold Rules",
        "desc": "How to charge a 12V LiFePO4 battery correctly: 14.2–14.6V absorption, no float requirement, no equalization — plus charge-time math by charger size.",
        "h1": "Charging a 12V LiFePO4 Battery: The 14.4V Profile",
        "blurb": "The settings table, the charge-time table, and the two charger habits that shorten a lithium battery's life.",
        "lede": "Charge a 12V LiFePO4 at <b>14.2–14.6V absorption</b> (14.4V is the safe middle), with <b>no equalization and no required float</b> — that is the whole profile, and most charging damage comes from chargers that can't do it. Below: the settings, how long charging actually takes by charger size, and the cold-weather rule that matters more than both.",
        "filter": None,
        "sections": [
            ("The settings table", [
                "<table><thead><tr><th>Parameter</th><th>12V LiFePO4 (12.8V pack)</th><th>Notes</th></tr></thead><tbody>"
                "<tr><td>Absorption</td><td>14.2–14.6V</td><td>Short hold; the pack is ~full when current tapers at 14.4V</td></tr>"
                "<tr><td>Float</td><td>13.5V or off</td><td>Needed only for standby/backup duty</td></tr>"
                "<tr><td>Equalization</td><td><b>Never</b></td><td>Desulfation pulses are a lead-acid ritual lithium can't use</td></tr>"
                "<tr><td>Charge current</td><td>0.2–0.5C (20–50A per 100Ah)</td><td>Per the model's spec sheet</td></tr>"
                "<tr><td>Low-temp cutoff</td><td>No charging below 0°C / 32°F</td><td>BMS-enforced on packs with low-temp protection</td></tr>"
                "</tbody></table>",
            ]),
            ("Charge times (100Ah battery, from empty)", [
                "<table><thead><tr><th>Charger</th><th>Time to ~full</th><th>Typical source</th></tr></thead><tbody>"
                "<tr><td>10A</td><td>~10–11 hrs</td><td>Small bench charger, stock RV converter on lithium profile</td></tr>"
                "<tr><td>20A</td><td>~5–5.5 hrs</td><td>Mid-size LiFePO4 charger</td></tr>"
                "<tr><td>40A</td><td>~2.5–3 hrs</td><td>Fast charger / strong alternator DC-DC</td></tr>"
                "<tr><td>300W solar (real-world ~250W)</td><td>~5–6 sun-hours</td><td>One good panel day, nothing else drawing</td></tr>"
                "</tbody></table>",
                "<p>LiFePO4's flat voltage curve is why the times are nearly linear: unlike lead-acid, it accepts full current until ~90% charged, so a 20A charger really does halve the 10A time. It's also why voltage alone can't tell you the state of charge — a resting 13.3V and 13.1V can be 60% and 25%. Use a shunt monitor or a Bluetooth BMS readout, not a voltmeter guess.</p>",
            ]),
            ("The cold rule, and the charger you already own", [
                "<p><b>Never charge below freezing without protection.</b> Charging a frozen LiFePO4 plates lithium metal onto the cells — permanent capacity loss, invisible until the battery fades early. If the battery will live anywhere that gets cold (RV, boat shed, ice season), low-temperature charge protection in the BMS is the feature that matters most; it is called out per-model in our <a href=\"/12v-100ah-lifepo4-battery/\">100Ah comparison</a>.</p>",
                "<p>Your existing lead-acid charger is fine <i>if</i> it has a lithium mode or its voltages land in the table above with equalization off. Many RV converters have a lithium switch on newer models; older ones charge to ~13.6–14.4V without equalizing and will fill a LiFePO4 to roughly 90% — usable, not ideal. When in doubt, the battery maker's listed profile wins over any generic advice, including this page.</p>",
            ]),
        ],
        "faqs": [
            ("What voltage fully charges a 12V LiFePO4 battery?",
             "14.2–14.6V at the charger (absorption), after which the pack rests at about 13.3–13.4V fully charged. The pack is 12.8V nominal — '12V' is the class name, not the charged voltage."),
            ("Can I leave a LiFePO4 battery on a float charger?",
             "A lithium-aware float at ~13.5V is fine for standby duty. What's harmful is a lead-acid maintainer that periodically pushes high-voltage desulfation pulses. For storage, the healthiest state is ~50–80% charge, charger disconnected."),
            ("Why does my LiFePO4 battery stop charging in winter?",
             "If it has low-temperature protection, the BMS is doing its job: it blocks charging below 0°C to prevent lithium plating. Warm the battery (use, sun, a heated space) and charging resumes. Models without the protection will accept the charge and quietly lose capacity."),
        ],
        "related": ["rv-batteries", "12v-lifepo4-battery-for-solar", "how-to-choose"],
    },
    {
        "slug": "eco-worthy-vs-litime-12v",
        "title": "Eco-Worthy vs LiTime 12V LiFePO4: Depth vs the $/Wh Floor, Live Prices",
        "desc": "Eco-Worthy tracks {eco_worthy_n} 12V models; LiTime tracks {litime_n}. The head-to-head on live $/Wh, the two capacity classes they share, and what lineup depth is worth — refreshed {date}.",
        "h1": "Eco-Worthy vs LiTime 12V: A Short Catalog Against a Deep One",
        "blurb": "Four tracked Eco-Worthy models vs LiTime's deep 12V bench — where each brand actually wins on live $/Wh.",
        "lede": "This is not a fair fight in catalog size — and the table shows why that barely matters. We track <b>{eco_worthy_n} Eco-Worthy 12V models against {litime_n} LiTime models</b>, yet the cheapest stored energy on this page is Eco-Worthy's: the <b>{cheap_title}</b> at {cheap_price} (<b>${cheap_ppw}/Wh</b>). LiTime's depth buys choice — a size and a feature tier for nearly every job. Eco-Worthy's narrow line buys focus: it only shows up where it can price hard. The table below, ranked by $/Wh, is the evidence.",
        "filter": "brand:Eco-Worthy+LiTime",
        "table_heading": "Every tracked Eco-Worthy and LiTime 12V battery, ranked by $/Wh",
        "sections": [
            ("Four models vs forty-five: what depth actually buys", [
                "<p><b>Eco-Worthy's 12V line, as tracked here, is two bets:</b> a 100Ah pack (1,280Wh — the RV, marine and small-solar staple) and a 314Ah pack (4,019Wh — the big single-case value play), each in two case variants. That is the whole catalog: {eco_worthy_n} rows. If your job is one of those two sizes, Eco-Worthy is in the fight; if it isn't, the brand simply doesn't sell you a battery.</p>",
                "<p><b>LiTime's line is the opposite strategy:</b> {litime_n} tracked 12V rows spanning small fish-finder packs, a full 100Ah feature ladder (bare, Bluetooth, low-temperature and self-heating tiers), 200Ah and 300Ah-plus classes, and trolling-motor and RV specials. Depth means the exact tier you need exists — and that some of those tiers carry $/Wh figures a two-size catalog never has to defend. Read LiTime's rows by capacity class, not by brand average: its cheapest-per-Wh rows and its smallest packs sit at opposite ends of this table.</p>",
            ]),
            ("Where they actually meet: 100Ah and 314Ah", [
                "<table><thead><tr><th>Class</th><th>Who fields what</th><th>How to judge it</th></tr></thead><tbody>"
                "<tr><td>12V 100Ah (1,280Wh)</td><td>Eco-Worthy: two 100Ah variants. LiTime: the deepest ladder in the class</td><td>Compare row by row in the table — Bluetooth, low-temp protection and self-heating explain the spread</td></tr>"
                "<tr><td>12V 314Ah (4,019Wh)</td><td>Eco-Worthy's two variants are the two cheapest rows on this page; LiTime answers nearby with 300Ah and 320Ah packs</td><td>One case, one BMS, ~4kWh: the big single-case class is where Eco-Worthy's $/Wh bottoms out</td></tr>"
                "<tr><td>Everything else (12–460Ah)</td><td>LiTime only, in this catalog</td><td>Small packs cost far more per Wh by nature — price them against the job, not against the big packs</td></tr>"
                "</tbody></table>",
                "<p>The pattern generalizes: within a shared class, the two brands price within cents per watt-hour of each other, and the $/Wh sort — not the badge — picks the row. Across classes there is no contest to judge: a 12Ah fish-finder pack and a 314Ah bank battery are different tools, and the table keeps them honest by pricing the energy in each.</p>",
                "<p>Shortlisting? Start from the class pages — <a href=\"/12v-100ah-lifepo4-battery/\">12V 100Ah</a> or <a href=\"/12v-314ah-lifepo4-battery/\">12V 314Ah</a> — where these two brands also face Renogy and SunGoldPower, then come back here for the brand-level picture. The earlier <a href=\"/litime-vs-renogy-12v-100ah/\">LiTime vs Renogy 100Ah comparison</a> covers LiTime's other big rivalry.</p>",
            ]),
        ],
        "faqs": [
            ("Is Eco-Worthy or LiTime cheaper for 12V LiFePO4?",
             "On live prices, the cheapest stored energy in this head-to-head is the {cheap_title} at {cheap_price} (${cheap_ppw}/Wh) — an Eco-Worthy 314Ah model. In the shared 100Ah class the brands price closely and the lead changes with maker sales, which is why the table above refreshes several times a day instead of declaring a permanent winner."),
            ("Why does LiTime have so many more 12V models than Eco-Worthy?",
             "Different strategies: LiTime builds a variant for every feature tier and niche (Bluetooth, low-temperature, self-heating, trolling, small packs), while Eco-Worthy's tracked 12V catalog concentrates on 100Ah and 314Ah. Depth helps when you need a specific feature or size; it does not by itself lower the $/Wh of the classes both brands sell."),
            ("Can I mix Eco-Worthy and LiTime batteries in one 12V bank?",
             "Makers advise against mixing brands, models or ages in a series/parallel bank — BMS behavior and internal resistance differ, and the weakest unit limits the string. Pick one brand per bank; the table prices that commitment class by class."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-314ah-lifepo4-battery", "litime-vs-renogy-12v-100ah"],
    },
    {
        "slug": "12v-lifepo4-series-parallel-guide",
        "title": "12V LiFePO4 in Series & Parallel: The 4-in-Series Ceiling, Wiring, Matching Rules",
        "desc": "How series and parallel wiring actually work for 12V LiFePO4: series adds volts (four 12V packs = a 48V system), parallel adds amp-hours, the 4-in-series ceiling most models carry, and the matching rules that keep a bank balanced.",
        "h1": "12V LiFePO4 in Series and Parallel: Volts Up or Amp-Hours Up",
        "blurb": "Series raises voltage, parallel raises capacity: the configuration table, the 4S ceiling, and the matching rules to check before you wire a bank.",
        "lede": "Most 12V LiFePO4 batteries can be wired in series, in parallel, or both — and the two moves do opposite jobs. <b>Series adds voltage</b>: two packs in series are a 24V battery, four are a 48V battery, and the amp-hours do not change. <b>Parallel adds amp-hours</b> at the same 12V. The catch is that the permission slip lives in each model's spec sheet, not in the chemistry: many models cap at <b>4 in series</b>, some budget packs are parallel-only, and every bank must be one brand, one model, one age. The wiring math and the rules are below; the batteries themselves are ranked by $/Wh on the <a href=\"/\">12V table</a> — {n} models tracked, with the cheapest stored energy currently at <b>${minppw}/Wh</b>.",
        "filter": None,
        "sections": [
            ("What each wiring actually builds (100Ah packs)", [
                "<table><thead><tr><th>Configuration</th><th>Voltage</th><th>Capacity</th><th>Energy</th><th>Typical job</th></tr></thead><tbody>"
                "<tr><td>1 battery</td><td>12.8V</td><td>100Ah</td><td>1,280Wh</td><td>RV, boat or small solar, as-is</td></tr>"
                "<tr><td>2 in parallel (2P)</td><td>12.8V</td><td>200Ah</td><td>2,560Wh</td><td>A bigger 12V bank — every charger and appliance you own still works</td></tr>"
                "<tr><td>2 in series (2S)</td><td>25.6V</td><td>100Ah</td><td>2,560Wh</td><td>24V trolling motors and inverter systems</td></tr>"
                "<tr><td>4 in series (4S)</td><td>51.2V</td><td>100Ah</td><td>5,120Wh</td><td>A 48V system assembled from 12V packs</td></tr>"
                "<tr><td>2S2P (4 batteries)</td><td>25.6V</td><td>200Ah</td><td>5,120Wh</td><td>A 24V bank with doubled runtime</td></tr>"
                "<tr><td>4S4P (16 batteries)</td><td>51.2V</td><td>400Ah</td><td>20,480Wh</td><td>The commonly published ceiling — a home-scale bank built entirely from 12V units</td></tr>"
                "</tbody></table>",
                "<p>Read the 2S and 2P rows together: identical energy, different shape. Series is how you reach a higher-voltage system (which moves the same power at lower current — thinner cable, less heat, and access to the efficient 24V/48V inverter class). Parallel is how you grow a 12V system without replacing a single charger, alternator or appliance. Pick the shape your loads need first; the battery count follows.</p>",
            ]),
            ("The limits: 4 in series is common, guaranteed is not", [
                "<p>There is no chemistry-wide wiring limit — there is a per-model one, set by the BMS. Series is the demanding direction: in a 4S string each battery's BMS sits at a different point in a 51.2V circuit, and the pack must be built and rated for it. That is why the published ceilings cluster where they do — <b>up to 4 in series is the common rating</b> among models that allow series at all, parallel allowances are usually equal or larger, and a meaningful minority of budget packs are <b>parallel-only</b>. A model whose spec sheet is silent on series has answered the question: do not series-wire it.</p>",
                "<ul><li><b>Same brand, model, capacity and age</b> — all four, in both directions. The bank behaves like its weakest unit, and mixed units make that unit weaker.</li><li><b>Buy the bank at once where you can.</b> A second purchase a year later is a different production batch; if you must expand, do it early and re-check voltages before connecting (next section).</li><li><b>The charger follows the string, not the battery.</b> A 2S bank charges at ~29.2V and a 4S bank at 58.4V — your 12V charger cannot charge a series string as a unit, and the inverter/charger must be a model for the target voltage.</li><li><b>Discharge current does not multiply in series.</b> A 4S string of 100A-BMS batteries is still a 100A battery system, just at 51.2V. Parallel is the direction that adds current.</li></ul>",
                "<p>Before ordering for a wired bank, open the product page for your exact model and find its series/parallel line — the <a href=\"/12v-100ah-lifepo4-battery/\">100Ah table</a> and the <a href=\"/12v-200ah-lifepo4-battery/\">200Ah table</a> link every tracked model to its maker page, which is where that line lives.</p>",
            ]),
            ("Parallel wiring that shares current fairly", [
                "<ol><li><b>Charge every battery individually to full</b> with a 12V LiFePO4 charger (14.2–14.6V — the <a href=\"/12v-lifepo4-charging-guide/\">charging guide</a> has the profile), let them rest, and confirm the resting voltages sit within about a tenth of a volt of each other. Paralleling a full pack with an empty one sends a large equalizing current through the interconnects the moment the terminals meet.</li><li><b>Connect negatives, then positives</b>, with the bank disconnected from loads and charger.</li><li><b>Take power off diagonally</b>: the main positive lead on the first battery, the main negative lead on the last. Diagonal take-off forces current through every interconnect instead of letting the nearest battery do all the work. On banks of three or more, a busbar with equal-length leads per battery does the same job better.</li><li><b>Fuse the bank</b> — a fuse on the main positive sized to your cabling and loads, as close to the batteries as practical.</li></ol>",
                "<p>Done this way, a parallel bank behaves like one big battery: one charger, one state of charge, current shared roughly evenly. Done carelessly — mismatched voltages, corner take-off, mixed models — the nearest or strongest pack cycles hardest, ages fastest, and quietly caps the whole bank. The same fairness logic is why the <a href=\"/12v-lifepo4-battery-for-solar/\">solar sizing guide</a> treats the bank, not the individual battery, as the unit the panels must fill.</p>",
            ]),
            ("Series strings: the two ways they fail", [
                "<p><b>Failure one — the string goes dark.</b> In series there is one current path, so if any single battery's BMS disconnects (over-current, a temperature limit, a fault), the whole string stops — a 48V inverter fed by four 12V packs has no partial mode. Size the string so one pack's discharge rating comfortably covers the load, and treat a string shutdown as a per-battery diagnosis, not a system failure.</p>",
                "<p><b>Failure two — drift.</b> Each BMS balances the cells inside its own battery, but nothing balances one battery against the next. Over months the packs settle at slightly different states of charge; the weakest reaches empty first and caps the string's usable capacity, and reaches full first on charge and trips early. The maintenance is cheap and scheduled: every few months, or whenever runtime sags, charge each battery individually to full and re-check the set — the same individual charge you did before assembly. An external battery equalizer wired across the string can slow drift, but it does not replace matched batteries or the periodic individual charge.</p>",
            ]),
        ],
        "faqs": [
            ("How many 12V LiFePO4 batteries can I connect in series?",
             "Four is the common published ceiling — 4S gives 51.2V, a 48V system — for models that allow series at all. It is a per-model specification, not a chemistry rule: some models allow fewer, and some budget packs prohibit series entirely. The product page for your exact model is the authority; never exceed its stated limit."),
            ("Can I wire a 100Ah and a 200Ah LiFePO4 battery in parallel?",
             "Makers advise against mixing capacities, brands, models or ages in one bank. In parallel, different internal resistances share current unevenly and the packs sit at different depths of discharge; in series, a mixed string is capped by its smallest battery and drifts out of balance quickly. Build the bank from identical units bought together — matched sets are also the honest way to use the $/Wh table on the homepage, since the price is per matched battery."),
            ("Do batteries in a series string need a balancer?",
             "Each battery's internal BMS balances its own cells, but nothing balances one whole battery against the next in a string. Standard practice: charge every battery individually to full before assembly, then re-check individual voltages every few months and top up any that drift. An external equalizer across the string can slow the drift, but it is an addition to that routine, not a substitute for it."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-200ah-lifepo4-battery", "12v-lifepo4-battery-for-solar"],
    },
    {
        "slug": "lifepo4-vs-lead-acid-cost",
        "title": "LiFePO4 vs Lead-Acid Cost: Cost per Delivered kWh, Not Sticker Price",
        "desc": "The lead-acid battery is cheaper to buy and roughly ten times more expensive to use. Cost-per-cycle math for a 12V 100Ah swap, with the LiFePO4 side priced live — refreshed {date}.",
        "h1": "LiFePO4 vs Lead-Acid: The Sticker Lies, the Cycle Count Doesn't",
        "blurb": "Usable capacity and cycle life, priced out: what a delivered kWh costs from each chemistry over its working life.",
        "lede": "Compare stickers and lead-acid wins: a 12V 100Ah AGM battery typically retails around $180–$250 (a market range — we don't track lead-acid prices), while the cheapest tracked 100Ah LiFePO4 in the table below is the <b>{cheap_title}</b> at {cheap_price}. Compare what each battery <b>delivers over its life</b> and the answer inverts by about an order of magnitude: lead-acid gives up roughly half its capacity to the 50% depth-of-discharge rule and a few hundred cycles to chemistry, so its cost per delivered kWh lands near <b>$0.63</b>, against roughly <b>$0.06</b> for LiFePO4 on the same math. This page shows the arithmetic, not an adjective.",
        "filter": "ah90_115",
        "table_heading": "The LiFePO4 side of the comparison — every tracked 12V 100Ah model, live",
        "sections": [
            ("The worked example: one 100Ah slot, two chemistries", [
                "<table><thead><tr><th></th><th>12V 100Ah lead-acid (AGM)</th><th>12V 100Ah LiFePO4</th></tr></thead><tbody>"
                "<tr><td>Sticker (typical / live cheapest)</td><td>~$200 typical retail</td><td class='num'>{cheap_price} (table below)</td></tr>"
                "<tr><td>Nameplate energy</td><td>1,280Wh</td><td>1,280Wh</td></tr>"
                "<tr><td>Usable per cycle</td><td>~640Wh (50% DoD before life collapses)</td><td>~1,024Wh (80% DoD, routine)</td></tr>"
                "<tr><td>Cycles at that depth (planning figures)</td><td>~500</td><td>~3,000 (conservative for the class)</td></tr>"
                "<tr><td>Lifetime energy delivered</td><td>~320kWh</td><td>~3,070kWh</td></tr>"
                "<tr><td><b>Cost per delivered kWh</b></td><td class='num'><b>~$0.63</b></td><td class='num'><b>~$0.06</b></td></tr>"
                "</tbody></table>",
                "<p>The lead-acid figures are standard planning numbers for the chemistry (50% depth-of-discharge, ~500 cycles at that depth, ~$200 typical retail) — labeled as such because this site tracks LiFePO4 prices live and lead-acid prices not at all. The LiFePO4 cycle figure is deliberately conservative: makers in this class commonly rate 4,000+ cycles, and we used 3,000 so the comparison does not depend on believing a datasheet. Even if you halve LiFePO4's life and double lead-acid's, lithium still wins the per-kWh ledger several times over. The gap is structural — usable fraction × cycle count — not a sale price.</p>",
            ]),
            ("What ten years of daily cycling actually costs", [
                "<p>Run the worked example as a calendar. A daily-cycled lead-acid bank reaches its ~500 cycles in under a year and a half, so a ten-year RV, cabin or solar installation buys the same battery <b>six or seven times</b> — roughly $1,200–$1,400 of lead-acid purchases, plus the labor of swapping 60 lb batteries and the capacity fade in between (a lead-acid at cycle 400 is not the battery you bought). The LiFePO4 side of the ledger is one purchase at the live prices below, with a second battery a plausible year-ten event rather than a scheduled one.</p>",
                "<ul><li><b>Weight is a cost too:</b> ~60 lb vs ~24 lb for the same 100Ah slot — in a van or boat that difference is fuel, payload and handling, every trip.</li><li><b>Charge efficiency:</b> lead-acid returns roughly 80–85% of what you put in (and crawls through its last 20%); LiFePO4 returns ~95%+ and accepts full current almost to full. On solar, the wasted fifth of a lead-acid charge is panels you bought for nothing.</li><li><b>The honest exception:</b> a battery that barely cycles — an engine starter, or a backup pack floated for years and used twice — never lives long enough to collect LiFePO4's cycle dividend. There, lead-acid's low sticker is a real saving, not a trap. LiFePO4 also cannot crank an engine unless the model is specifically rated for it.</li></ul>",
                "<p>So the decision rule is a single question: <b>how many cycles will this battery actually serve?</b> Daily or weekly cycling (solar, RV living, trolling, off-grid) makes LiFePO4 the cheaper battery by a wide margin. Rare-use standby keeps lead-acid rational. Everything else — brand, Bluetooth, case color — is priced in the table.</p>",
            ]),
            ("Making the swap without buying twice", [
                "<ul><li><b>Charger profile:</b> your existing converter works only if it can hold a lithium profile (14.2–14.6V, no equalization) — the <a href=\"/12v-lifepo4-charging-guide/\">charging guide</a> has the settings table.</li><li><b>Size by usable Wh, not Ah:</b> one 100Ah LiFePO4 replaces roughly two 100Ah lead-acids in delivered energy, so a like-for-like Ah swap over-buys capacity — a pleasant surprise, but budget for the bank you need.</li><li><b>Low-temperature protection</b> matters if the battery charges anywhere unheated; lead-acid tolerates cold charging that damages unprotected lithium.</li></ul>",
            ]),
        ],
        "faqs": [
            ("Is LiFePO4 worth the extra cost over lead-acid?",
             "For anything cycled regularly, yes — on planning figures, a 100Ah LiFePO4 delivers roughly ten times the lifetime energy of a 100Ah AGM at a similar sticker, putting its cost per delivered kWh near $0.06 against lead-acid's ~$0.63. For a rarely cycled starter or standby battery, lead-acid's cheaper sticker can be the rational buy."),
            ("How many lead-acid batteries equal one LiFePO4?",
             "In delivered energy over a working life, roughly six to seven 100Ah AGMs match one 100Ah LiFePO4 (~500 usable cycles each against ~3,000+). In per-cycle usable capacity alone, one LiFePO4 roughly equals two lead-acids of the same Ah rating, because it can use ~80% of its capacity against lead-acid's ~50%."),
            ("Can I just drop a LiFePO4 battery into my lead-acid system?",
             "Mechanically yes — same voltage class, same terminals. Electrically, check two things first: the charger needs a lithium profile (14.2–14.6V absorption, no equalization or desulfation), and alternator-charged systems (vans, boats) need a DC-DC charger so the alternator is not asked to feed a low-resistance lithium bank directly."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-lifepo4-charging-guide", "how-to-choose"],
    },
    {
        "slug": "12v-battery-for-cpap",
        "title": "12V Battery for CPAP Camping: Nights per Charge, by Humidifier Setting",
        "desc": "A CPAP's battery appetite is set by its heater, not its motor: runtime tables for therapy-only, humidifier and heated-tube settings on 100Ah and 200Ah, priced live.",
        "h1": "A 12V Battery for CPAP Camping: The Heater Decides Your Nights",
        "blurb": "Therapy-only sips ~20W; the heated humidifier and tube can quadruple it. Nights per charge, worked openly.",
        "lede": "The CPAP motor is not the load — the <b>heaters</b> are. Run therapy-only (humidifier off, standard tube) and a typical machine averages roughly <b>15–25W</b>, so a 12V 100Ah battery's ~970Wh of delivered energy lasts <b>about 5–8 nights</b>. Turn the heated humidifier and heated tube up and the same machine can draw <b>60–90W</b> — the same battery is a <b>1–2 night</b> battery. Every camping-CPAP decision is that one settings choice, priced against the {n} 100Ah-class batteries in the live table below (cheapest today: <b>{cheap_title}</b> at {cheap_price}, ${cheap_ppw}/Wh).",
        "filter": "ah90_115",
        "table_heading": "The 12V 100Ah batteries this math runs on, ranked by $/Wh",
        "sections": [
            ("Nights per charge, by setting (8-hour nights)", [
                "<table><thead><tr><th>CPAP setup</th><th>Average draw (planning range)</th><th>Energy per night</th><th>Nights on 100Ah (~970Wh delivered)</th><th>Nights on 200Ah (~1,940Wh)</th></tr></thead><tbody>"
                "<tr><td>Therapy only — humidifier off, standard tube</td><td>15–25W</td><td>120–200Wh</td><td>~5–8</td><td>~10–16</td></tr>"
                "<tr><td>Heated humidifier on, heated tube off</td><td>35–50W</td><td>280–400Wh</td><td>~2–3</td><td>~5–7</td></tr>"
                "<tr><td>Humidifier + heated tube, high settings</td><td>60–90W</td><td>480–720Wh</td><td>~1–2</td><td>~3–4</td></tr>"
                "</tbody></table>",
                "<p>Draw ranges are planning figures for common travel and home machines (higher pressure settings sit toward the top of each range); your machine's exact appetite is on its power-supply label and in its manual. 'Delivered' energy assumes you plan on ~80% of the battery's 1,280Wh nameplate and lose a little in the DC converter — the reserve is deliberate, because a battery that dies at 4 a.m. on night three is worse than a conservative plan. The 200Ah column is the same math on the <a href=\"/12v-200ah-lifepo4-battery/\">200Ah class</a>.</p>",
            ]),
            ("Use the DC converter, not an inverter", [
                "<p>Almost every CPAP is a DC machine wearing an AC brick: the therapy unit itself runs on low-voltage DC, and the maker sells a 12V DC converter for vehicle and battery use. Powering it through an AC inverter instead pays three taxes: conversion loss on the way up to AC and back down, the inverter's own idle draw (commonly 10–25W — over an 8-hour night that is 80–200Wh, up to a full therapy-only night, spent powering nothing), and one more box to pack. The DC converter route is why the table above can use a ~970Wh delivered figure at all.</p>",
                "<ul><li><b>Buy the maker's converter for your exact model</b> — CPAP DC inputs are model-specific (voltage and connector), and a generic adapter that under-volts the machine can fault it mid-night.</li><li><b>Turn the heaters down before you buy a bigger battery:</b> dropping from heated-tube-max to therapy-only is worth more nights than doubling the battery, and it is free. A passive (water-filled, unheated) humidifier is the middle setting many campers settle on.</li><li><b>Test the whole rig at home for a full night first</b>, at the settings you will actually use, and note the battery's state of charge in the morning. That one rehearsal replaces every estimate on this page with your number — do not let the first real test be the trip.</li></ul>",
            ]),
            ("Sizing the trip, honestly", [
                "<p>Work backwards from nights × your row in the table. A weekend (2–3 nights) at therapy-only or modest humidity fits inside one 100Ah battery with reserve — the class in the table below, where the same 1,280Wh in every row makes $/Wh a pure price ranking. A week with the humidifier running is a 200Ah conversation, or a 100Ah plus a way to recharge (vehicle DC-DC on driving days, or a folding panel at camp — the <a href=\"/12v-lifepo4-battery-for-solar/\">solar page</a> prices that pairing). And a note that outranks the math: if your therapy is not optional, carry the reserve — size for the worst row you might actually run, not the best row you hope to.</p>",
            ]),
        ],
        "faqs": [
            ("How long will a 12V 100Ah battery run a CPAP?",
             "It depends almost entirely on the heaters. Therapy-only (humidifier off), a typical machine averages 15–25W and a 100Ah battery delivers roughly 5–8 eight-hour nights. With a heated humidifier, plan on 2–3 nights; with humidifier and heated tube at high settings, 1–2 nights. The maker's 12V DC converter (not an AC inverter) is assumed in all three figures."),
            ("Can I run my CPAP straight off a 12V battery?",
             "Not straight — through the machine maker's 12V DC converter for your exact model. CPAPs run on low-voltage DC internally but at model-specific voltages and connectors; the official converter steps the battery's 12V to what the machine expects. Never improvise the connection with a generic adapter."),
            ("Is a 100Ah battery enough for a week of CPAP camping?",
             "At therapy-only settings, yes — 5–8 nights covers most weeks, with the top of the range needing the lower-draw end. With a heated humidifier every night, no: a week needs roughly 2,000–2,800Wh delivered, which means the 200Ah class, a second 100Ah, or a recharge source during the trip."),
        ],
        "related": ["12v-100ah-lifepo4-battery", "12v-200ah-lifepo4-battery", "rv-batteries"],
    },
    {
        "slug": "ice-fishing-battery-guide",
        "title": "LiFePO4 Battery for Ice Fishing: Cold Rules, Sonar Loads, Shuttle Sizes",
        "desc": "Ice fishing runs on small batteries in deep cold: what a flasher, a forward-facing sonar and shanty lights actually draw per day, which pack size covers it, and the below-freezing charging rule.",
        "h1": "Ice Fishing with LiFePO4: Small Packs, Deep Cold, Honest Runtime",
        "blurb": "A flasher day costs ~90Wh; a forward-facing-sonar day costs ~300Wh. The pack sizes that cover each — and why charging, not discharging, is the cold problem.",
        "lede": "Ice fishing is the one use on this site where the battery lives at <b>-10°C or colder</b> and the loads are measured in tens of watts. A flasher-only day on the ice costs roughly <b>90Wh</b>; a forward-facing-sonar day costs roughly <b>300Wh</b>. That puts the decision in the small-pack class — the {n} tracked models of 60Ah and under below, from <b>${minppw}/Wh</b> — and makes one cold rule more important than any capacity figure: <b>a LiFePO4 battery can discharge in the cold, but it must not be charged below freezing</b> unless it heats itself first. This guide works both halves: the day math, then the cold math.",
        "filter": "ah5_60",
        "table_heading": "Small 12V LiFePO4 packs (60Ah and under), ranked by $/Wh",
        "sections": [
            ("What a day on the ice actually draws (8 hours)", [
                "<table><thead><tr><th>Load</th><th>Draw (planning range)</th><th>Energy per 8h day</th></tr></thead><tbody>"
                "<tr><td>Flasher / basic sonar</td><td>8–12W</td><td>~65–95Wh</td></tr>"
                "<tr><td>Color sonar/GPS combo</td><td>15–20W</td><td>~120–160Wh</td></tr>"
                "<tr><td>Forward-facing sonar (display + sonar box)</td><td>20–30W</td><td>~160–240Wh</td></tr>"
                "<tr><td>LED shanty lights + phone top-ups</td><td>5–10W</td><td>~40–80Wh</td></tr>"
                "</tbody></table>",
                "<p>Planning ranges, not measurements of your unit — the rating is printed on each device, and a shuttle battery with a percentage readout settles it after one trip. Note the shape: even the heaviest electronic day (forward-facing sonar plus lights, ~300Wh) is a quarter of what a single 100Ah battery holds. On the ice, the constraint is rarely total energy — it is pack size, weight on the sled, and temperature.</p>",
            ]),
            ("Picking the pack: days per charge, cold-adjusted", [
                "<table><thead><tr><th>Pack</th><th>Nameplate</th><th>Cold-day planning usable (~75%)</th><th>Flasher days (~90Wh/day)</th><th>Forward-facing days (~300Wh/day)</th></tr></thead><tbody>"
                "<tr><td>12Ah</td><td>154Wh</td><td>~115Wh</td><td>~1</td><td>Not enough</td></tr>"
                "<tr><td>30Ah</td><td>384Wh</td><td>~290Wh</td><td>~3</td><td>~1</td></tr>"
                "<tr><td>50Ah</td><td>640Wh</td><td>~480Wh</td><td>~5</td><td>~1.5</td></tr>"
                "</tbody></table>",
                "<p>The ~75% planning figure bundles two cold realities: a LiFePO4 pack sitting at deep-cold temperatures delivers measurably less than its room-temperature rating, and you still leave a reserve rather than skating home on an empty shuttle. Both penalties shrink if the pack rides in an insulated shuttle box and sleeps indoors — a warm 30Ah outperforms a frozen 50Ah, which is why the cheapest capacity upgrade on the ice is a foam-lined box. The table below prices the class; note that small packs always cost more per watt-hour than the big RV-class batteries (one BMS and case spread over fewer Wh) — you are paying for portability, and the $/Wh column shows exactly how much.</p>",
            ]),
            ("The cold rules (the section that saves batteries)", [
                "<ul><li><b>Discharge cold, charge warm.</b> Using the pack at -20°C is hard on runtime but not on the battery's life. Charging below 0°C is the opposite: it plates lithium onto the cells and permanently costs capacity. Charge indoors, overnight, at room temperature — which conveniently matches how ice fishing days actually run.</li><li><b>Low-temperature protection is the spec to verify.</b> A BMS with low-temp charge cutoff refuses a frozen charge instead of taking the damage. Not every small pack has it; it is the first line to check on the product page of any model in the table.</li><li><b>Self-heating is the exception that proves the rule:</b> the self-heating 30Ah class in the table (LiTime's LiHeat ice-fishing pack is the tracked example) warms its own cells before accepting a charge, which is what makes charging in a heated shanty or fish house legitimate. Its higher $/Wh is the visible price of that heater — worth it only if your routine actually charges away from a warm room.</li><li><b>Augers are a different battery.</b> Dedicated auger packs are tool batteries, not 12V LiFePO4 shuttles; nothing in the table is a substitute for one, and no shuttle pack should be asked to drill.</li></ul>",
                "<p>Come summer, the same packs go straight into the kayak and the trolling-motor shuttle — the <a href=\"/marine-trolling-motor-batteries/\">marine table</a> is the warm-water version of this page, and the <a href=\"/12v-lifepo4-charging-guide/\">charging guide</a> covers the year-round profile behind the cold rules.</p>",
            ]),
        ],
        "faqs": [
            ("What size LiFePO4 battery do I need for ice fishing?",
             "Match it to the sonar: a flasher-only angler is covered for a long day by a 12Ah pack and for a weekend by a 30Ah. Forward-facing sonar changes the class — budget ~300Wh per day, so a 30Ah is a one-day pack and a 50Ah gives a day and a half with cold reserve. Lights and phone charging add ~40–80Wh per day on top."),
            ("Can a LiFePO4 battery be used in freezing weather?",
             "Yes for discharging — expect reduced runtime in deep cold (plan on roughly three-quarters of nameplate for a pack that sits cold all day, less penalty if it rides insulated). The hard limit is charging: never charge a standard LiFePO4 below 0°C / 32°F. Either charge it warm indoors, choose a model whose BMS blocks cold charging, or use a self-heating model that warms itself first."),
            ("Why are ice-fishing batteries so much more expensive per watt-hour?",
             "Fixed costs — the BMS, case and terminals — are spread over 150–600Wh instead of several thousand, and the cold features (low-temp protection, self-heating, sealed shuttle-ready cases) are real hardware. The table's $/Wh column makes the portability premium explicit instead of hiding it in a sticker price."),
        ],
        "related": ["marine-trolling-motor-batteries", "12v-lifepo4-charging-guide", "12v-100ah-lifepo4-battery"],
    },
    {
        "slug": "van-life-battery-sizing",
        "title": "Van Life Battery Sizing: The Load-Audit Worksheet, Worked in Amp-Hours",
        "desc": "Van battery sizing fails on guessed loads, not bad batteries: audit a day's real watt-hours, divide by usable capacity, land on 100Ah, 200Ah or 314Ah — priced live, refreshed {date}.",
        "h1": "Van Life Battery Sizing: Audit the Day Before You Buy the Battery",
        "blurb": "A worksheet, not a guess: what a fridge, a fan, a heater and a laptop actually cost per day, and the Ah class each total lands in.",
        "lede": "Most van batteries are the wrong size for the same reason: they were bought from a forum post instead of a load audit. The audit takes ten minutes — list what runs, for how long, and add the watt-hours. A frugal weekend van audits near <b>700Wh a day</b>; a full-time van with a fridge, heater and remote-work gear audits near <b>1,500–2,000Wh a day</b> — and those two vans need different battery classes. The van-sized class tracked here (100Ah to 314Ah, priced in the live table below) runs from <b>${minppw}/Wh</b>; this worksheet lands you on the right row of it.",
        "filter": "ah90_330",
        "table_heading": "Van-sized 12V LiFePO4 batteries (100Ah–314Ah class), ranked by $/Wh",
        "sections": [
            ("Step 1 — the load audit (planning ranges, per day)", [
                "<table><thead><tr><th>Load</th><th>Planning draw</th><th>Hours</th><th>Wh per day</th></tr></thead><tbody>"
                "<tr><td>12V compressor fridge</td><td>~40–60W, cycling about half the time</td><td>24</td><td>~480–720</td></tr>"
                "<tr><td>Roof fan</td><td>~20–40W</td><td>6–10</td><td>~150–350</td></tr>"
                "<tr><td>Diesel/gas heater fan + pump (winter)</td><td>~15–30W running</td><td>8–12</td><td>~150–300</td></tr>"
                "<tr><td>Laptop + phones + lights</td><td>mixed</td><td>—</td><td>~150–300</td></tr>"
                "<tr><td>Starlink / mobile router</td><td>~40–75W while on</td><td>6–10</td><td>~300–600</td></tr>"
                "<tr><td>Water pump, USB, standby odds and ends</td><td>mixed</td><td>—</td><td>~50–100</td></tr>"
                "</tbody></table>",
                "<p>Planning ranges, not measurements — your fridge's duty cycle in a hot van and your heater's in a cold one move their rows the most, which is why winter full-timers audit a second, colder version of this table. Two rows deserve emphasis: the fridge is the only load that never sleeps, and the satellite internet row rivals it — a remote-work van's battery is mostly a fridge-and-Starlink battery. Inverter-powered loads (an induction hob, a kettle) draw hard but briefly; count them at their real minutes, not their sticker watts × a guessed hour.</p>",
            ]),
            ("Step 2 — the formula, and the class each total lands in", [
                "<p><b>Amp-hours to buy = daily Wh × days between charges ÷ (12.8V × 0.8)</b>. The 0.8 is deliberate headroom: plan to use about 80% of nameplate so a cloudy day or a long drive-less stretch is an inconvenience, not a dead fridge. Worked at two days between charges:</p>",
                "<table><thead><tr><th>Van profile</th><th>Daily audit</th><th>Ah the formula asks for</th><th>Class that answers it</th></tr></thead><tbody>"
                "<tr><td>Weekender: fridge, fan, lights, phones</td><td>~700Wh</td><td>~137Ah</td><td>200Ah class — one pack, margin for a hot weekend</td></tr>"
                "<tr><td>Full-time, no satellite internet</td><td>~1,200Wh</td><td>~234Ah</td><td>314Ah class, or 200Ah + reliable daily charging</td></tr>"
                "<tr><td>Full-time remote work, winter</td><td>~2,000Wh</td><td>~391Ah</td><td>314Ah + a second pack in parallel, sized with the <a href=\"/12v-lifepo4-series-parallel-guide/\">series-parallel guide</a></td></tr>"
                "</tbody></table>",
                "<p>Note where the honest answers land: the single 100Ah pack (1,280Wh) is a <i>one-day</i> battery for all but the leanest audits, which is why the table below starts at the 100Ah class but the worksheet keeps walking past it. The $/Wh pattern helps the bigger answer: in the live table the 314Ah class holds the catalog floor (${minppw}/Wh — the {cheap_title} at {cheap_price}), because one case and one BMS carry 4,019Wh. In vans, unusually, the bigger battery is both the capacity answer and the value answer — if it fits the build's battery box.</p>",
            ]),
            ("Step 3 — size the refill, not just the tank", [
                "<p>A van battery is refilled three ways, and the weakest of them sets your real autonomy. <b>Driving:</b> a DC-DC charger fed by the alternator typically restores a few hundred watt-hours per driving hour — a van that moves every second day can run a class smaller than the formula's answer. <b>Roof solar:</b> a van roof fits roughly 400–800W of panels, which in summer replaces a frugal day's audit and in winter replaces a fraction of it; the <a href=\"/12v-lifepo4-battery-for-solar/\">12V solar page</a> prices that pairing. <b>Shore power:</b> resets everything, and vans that camp plugged-in half the time should not buy batteries for the other half's worst case.</p>",
                "<ul><li><b>Stationary in winter is the sizing case:</b> no driving, short solar days, heater running — if the battery survives that audit, every other season is easy.</li><li><b>Charge speed is a spec too:</b> check the pack's maximum charge current against your DC-DC charger's output; a big bank behind a small charger is a slow bank.</li><li><b>Stay at 12V in a van:</b> alternator charging and native 12V loads are the vehicle's whole electrical ecosystem — the case for ever going 48V in a stationary build is laid out on our sister site's <a href=\"https://48vlifepo4battery.com/48v-vs-12v-for-solar/\">48V vs 12V comparison</a>, and a van is not it.</li></ul>",
            ]),
        ],
        "faqs": [
            ("How big a battery do I need for van life?",
             "From your audit: amp-hours = daily watt-hours × days between charges ÷ (12.8 × 0.8). A ~700Wh/day weekend van at two days lands near 137Ah (buy the 200Ah class); a ~1,200Wh/day full-time van lands near 234Ah (the 314Ah class); a winter remote-work van near 2,000Wh/day needs roughly 391Ah — a 314Ah plus a paralleled second pack."),
            ("Is 100Ah enough for a van?",
             "For a lean one-day-at-a-time setup, yes — 1,280Wh nameplate, about 1,024Wh planned-usable, covers a fridge, lights and phones for roughly a day, and daily driving or solar keeps it topped up. It is not enough for two stationary days with a fridge in summer heat, which is the trip profile that strands most 100Ah vans."),
            ("Why does the 314Ah class cost less per watt-hour?",
             "Fixed costs — case, BMS, terminals — spread over 4,019Wh instead of 1,280Wh, and 314Ah is the industry's high-volume cell format. The live table shows the result: the class currently holds this catalog's $/Wh floor. The trade-offs are weight (a ~60–70 lb class lift) and a single point of failure versus two smaller paralleled packs."),
        ],
        "related": ["rv-batteries", "12v-200ah-lifepo4-battery", "12v-314ah-lifepo4-battery"],
    },
],
"serverrackbatteries.com": [
    {
        "slug": "eco-worthy-cubix100-vs-litime-comflex",
        "title": "Eco-Worthy Cubix100 vs LiTime ComFlex vs SunGoldPower: Rack Prices by $/Wh",
        "desc": "The three value rack modules compared on live maker prices: Cubix100, SunGoldPower SG48100P and LiTime ComFlex — $860-class storage ranked by $/Wh, refreshed {date}.",
        "h1": "Cubix100 vs ComFlex — with SunGoldPower Spoiling the Fight",
        "blurb": "The two named value modules, plus the third brand priced between them. Live $/Wh decides it.",
        "lede": "Every 48V 100Ah rack module stores the same 5.12kWh, so this comparison is pure price and packaging. The live table below tracks {n} modules; the three value contenders are the Eco-Worthy Cubix100 at <b>{eco_worthy_min_price} (${eco_worthy_min_ppw}/Wh)</b>, the SunGoldPower SG48100P at <b>{sungoldpower_min_price} (${sungoldpower_min_ppw}/Wh)</b>, and the LiTime ComFlex at <b>{litime_min_price} (${litime_min_ppw}/Wh)</b>. Ranked by $/Wh — the method stated up front — the order is the table's order.",
        "filter": "brand:Eco-Worthy+LiTime+SunGoldPower",
        "table_heading": "Eco-Worthy, SunGoldPower and LiTime rack modules, ranked by $/Wh",
        "sections": [
            ("What separates three identical-capacity modules?", [
                "<ul><li><b>Price per Wh:</b> the headline. On today's numbers the spread between the cheapest and priciest of the three is roughly $240 for identical stored energy — money that buys a second module's worth of progress every fourth purchase.</li><li><b>Heating:</b> SunGoldPower's self-heating variant (the SGH48100T row in the table) suits unheated garages and sheds; the Cubix100 and base SG48100P assume a conditioned space or a warm climate.</li><li><b>Communications:</b> all three brands publish inverter compatibility lists (CAN/RS485). The deciding check is your exact inverter model on the maker's list — see our <a href=\"/inverter-compatibility/\">inverter compatibility guide</a>.</li><li><b>Multi-pack rows:</b> SunGoldPower sells 2- and 4-module bundles in the same feed; their per-unit math differs from the single-module rows, so compare singles to singles.</li></ul>",
            ]),
            ("The verdict, by the stated method", [
                "<p>Sorted by $/Wh, the cheapest stored energy in this comparison today is the <b>{cheap_title}</b> at {cheap_price} (${cheap_ppw}/Wh). That is the whole verdict — this site does not hands-on test, and it does not crown a 'best' module. If your inverter's closed-loop list favors one brand, or you need self-heating, the table prices that preference precisely: you can see exactly what the feature costs per watt-hour instead of guessing.</p>",
                "<p>Building a bank? The <a href=\"/10kwh-battery-bank/\">10kWh bank page</a> prices the two-module build, and <a href=\"/how-many-server-rack-batteries/\">the sizing guide</a> works out how many modules your loads actually need.</p>",
            ]),
        ],
        "faqs": [
            ("Which is cheaper, the Eco-Worthy Cubix100 or the LiTime ComFlex?",
             "On live prices today: the Cubix100 is {eco_worthy_min_price} (${eco_worthy_min_ppw}/Wh) and the ComFlex is {litime_min_price} (${litime_min_ppw}/Wh), with SunGoldPower's SG48100P between them at {sungoldpower_min_price}. All three store 5.12kWh, so $/Wh is the complete price story; features and inverter lists are the tiebreakers."),
            ("Can I parallel a Cubix100 with a ComFlex in one bank?",
             "Makers advise matching brand, model and age in a parallel bank — different BMS units share current unevenly and closed-loop communication needs one protocol master. Build the bank from one module type; the table's per-module saving compounds with every module you add."),
            ("Do these rack batteries include the rack cabinet?",
             "Typically not — the module price is the battery in its rack-mount case; cabinets, busbars and cables are separate line items. Factor them into a bank build (the 10kWh bank page on this site lists what else a build needs)."),
        ],
        "related": ["48v-100ah-server-rack-battery", "10kwh-battery-bank", "inverter-compatibility"],
    },
    {
        "slug": "server-rack-battery-price-per-kwh",
        "title": "Server Rack Battery Price per kWh: The Live League Table",
        "desc": "What a kWh of server rack storage costs right now, brand by brand — the $/kWh ranking the editorial listicles don't publish, refreshed {date}.",
        "h1": "Server Rack Battery Price per kWh, Ranked Live",
        "blurb": "The league table for rack storage: every module's true $/kWh, refreshed several times a day.",
        "lede": "Ranked lists of rack batteries sort by an editor's judgment. This page sorts by the only reproducible metric: <b>price per kWh</b>. Across the {n} modules tracked below, rack storage currently runs from <b>${minppw}/Wh</b> at the low end to a <b>${medppw}/Wh median</b> — multiply by 1,000 for $/kWh. When a listicle tells you a module is 'best value' without showing this column, it is asking you to trust it. Here, the column is the page.",
        "filter": "all",
        "table_heading": "Every tracked rack module, ranked by $/Wh (=$/kWh ÷ 1,000)",
        "sections": [
            ("How to read the spread", [
                "<ul><li><b>The floor (~$0.17/Wh):</b> value-brand 100Ah modules with standard features. This is close to the commodity price of the format.</li><li><b>The middle (~$0.20–0.23/Wh):</b> self-heating variants, stronger warranty brands, and newer models — features priced visibly.</li><li><b>The tail:</b> multi-pack bundle rows (2× and 4× listings carry bundle prices in the feed, so their per-unit math reads differently) and any premium or low-volume listings. Compare single modules to single modules.</li></ul>",
                "<p>Per-kWh is also the only honest way to compare a rack module against the alternatives: a packaged wall battery or an installed system quotes storage at several times this page's median per kWh (see the cost breakdown on our sister site's <a href=\"https://48vlifepo4battery.com/home-battery-system/\">home battery system page</a>) — the difference is integration and labor, not stored energy.</p>",
            ]),
            ("What moves a module's $/kWh", [
                "<ul><li><b>Cell format:</b> the industry-standard 100Ah module is the cheapest unit of storage; odd sizes pay a novelty premium.</li><li><b>Heating:</b> a self-heating BMS adds cost per module — worth it only where the bank actually gets cold.</li><li><b>Brand tier:</b> warranty length, US support presence and UL listings are real costs that show up in $/kWh. The metric prices them; it doesn't dismiss them.</li><li><b>Sales:</b> maker-store promotions move individual rows weekly — which is why this table refreshes several times a day instead of freezing a 'checked on' date.</li></ul>",
                "<p>Ready to act on the numbers? The <a href=\"/eco-worthy-cubix100-vs-litime-comflex/\">three-way value comparison</a> works the cheapest end of this table in detail, and the <a href=\"/how-many-server-rack-batteries/\">sizing guide</a> turns your loads into a module count.</p>",
            ]),
        ],
        "faqs": [
            ("What is a good price per kWh for a server rack battery?",
             "On live maker prices, value-brand 100Ah modules cluster near the bottom of this table (currently from ${minppw}/Wh — the $/kWh column shows the same figure × 1,000), with a tracked median of ${medppw}/Wh. Anything at or below the median is competitively priced for the format; the table shows where each module sits today."),
            ("Why do some rack batteries cost twice as much per kWh?",
             "Features (self-heating, premium BMS), brand and warranty tier, certifications, and bundle pricing in store feeds. The $/kWh column separates the energy price from the feature price so you can decide what the extras are worth to you."),
            ("Is $/kWh the same as $/Wh?",
             "Yes — $/kWh is $/Wh × 1,000. A module at $0.192/Wh costs $192 per kWh. This site shows both columns in every table because home-storage shoppers think in kWh and battery shoppers think in Wh."),
        ],
        "related": ["eco-worthy-cubix100-vs-litime-comflex", "48v-100ah-server-rack-battery", "10kwh-battery-bank"],
    },
    {
        "slug": "server-rack-battery-vs-powerwall-cost",
        "title": "Server Rack Bank vs Powerwall: A Line-by-Line Cost Breakdown",
        "desc": "What 15kWh of storage costs as a DIY rack bank vs an installed wall battery — every line item, with the rack side priced live from maker stores.",
        "h1": "Rack Bank vs Installed Wall Battery: Where the Money Actually Goes",
        "blurb": "Same 15kWh, two very different invoices — batteries, gateway, labor and permits, itemized.",
        "lede": "Compare like with like: about <b>15kWh of storage</b>. As an installed wall battery (Powerwall-class), that capacity is commonly quoted at <b>$11,000–$16,000 installed</b> in 2026 market coverage — a figure we cite as context, not a tracked price. As a rack bank, the batteries are three modules from the live table below (the cheapest is <b>{cheap_title}</b> at {cheap_price}), and the rest of the invoice is hardware and labor you can price line by line. This page itemizes both.",
        "filter": "all",
        "table_heading": "The rack modules this breakdown prices",
        "sections": [
            ("The two invoices, side by side", [
                "<table><thead><tr><th>Line item</th><th>DIY rack bank (~15.36kWh)</th><th>Installed wall battery (~13.5–15kWh)</th></tr></thead><tbody>"
                "<tr><td>Batteries</td><td>3 modules at the table's live prices</td><td>Included in the unit price</td></tr>"
                "<tr><td>Inverter / gateway</td><td>Hybrid inverter, est. $900–$2,500</td><td>Included (integrated)</td></tr>"
                "<tr><td>Rack / mounting</td><td>Cabinet or wall brackets, est. $150–$600</td><td>Included</td></tr>"
                "<tr><td>Electrical work</td><td>Your time, or an electrician for the transfer panel</td><td>Included in install labor</td></tr>"
                "<tr><td>Permits & inspection</td><td>Your paperwork (still required grid-tied)</td><td>Handled by installer</td></tr>"
                "<tr><td>Warranty</td><td>Per-component (battery, inverter separate)</td><td>Single 10-year system warranty</td></tr>"
                "</tbody></table>",
                "<p>Estimates are planning figures, labeled as such; the only live-tracked numbers on this page are the module prices in the table. Even taking the high end of every estimate, the rack path lands at roughly half the installed quote — the gap is integration, labor and warranty structure, exactly the lines the table makes visible.</p>",
            ]),
            ("The honest middle path", [
                "<p>Most rack-bank owners don't DIY the whole invoice: they buy modules and inverter themselves, then hire an electrician for the grid-side work (transfer panel, permits, inspection). That keeps the battery savings — the largest line — while the regulated work stays professional. What you give up versus the installed route is the single warranty and the app-polished whole-home automation; what you gain, beyond price, is expansion: a fourth module next year costs one module, not a second system.</p>",
                "<p>Decide with your actual constraint. Cash-constrained and handy: rack. Time-constrained or selling the house soon (a permitted, warrantied system appraises cleaner): installed. Either way, price the storage itself first — the <a href=\"/server-rack-battery-price-per-kwh/\">$/kWh league table</a> is the number both invoices are built on.</p>",
            ]),
        ],
        "faqs": [
            ("How much cheaper is a rack bank than a Powerwall?",
             "On the batteries alone, dramatically: three rack modules (15.36kWh) at live prices cost a fraction of an installed wall battery's $11,000–$16,000 typical installed range. After adding an inverter, rack and electrical work, a DIY or hybrid install usually lands around half the installed quote — with separate warranties instead of one system warranty."),
            ("Does a rack bank work with solar like a Powerwall does?",
             "Yes — paired with a hybrid inverter, a rack bank charges from solar, backs up loads on outage, and time-shifts energy the same way. The differences are packaging, software polish and warranty structure, not the underlying function."),
            ("Can a rack bank be permitted and inspected?",
             "Yes, when built from listed equipment and installed to code — the permit path is the same as any energy storage system; the difference is who shepherds the paperwork (you or your electrician, instead of an installer's office)."),
        ],
        "related": ["server-rack-battery-price-per-kwh", "home-energy-storage", "eco-worthy-cubix100-vs-litime-comflex"],
    },
    {
        "slug": "server-rack-battery-for-off-grid-solar",
        "title": "Server Rack Batteries for Off-Grid Solar: Sizing from Winter Sun, Priced Live",
        "desc": "Off-grid rack banks are sized from daily use, autonomy days and the worst month's sun — not outage hours. Module counts and live battery costs, refreshed {date}.",
        "h1": "Server Rack Batteries for Off-Grid Solar: The Bank Is Only Half the System",
        "blurb": "Daily-cycle sizing for cabins and homesteads: autonomy math, the winter-array rule, and what the modules cost live.",
        "lede": "A rack bank on an off-grid solar system has a harder job than a backup bank: it is cycled <b>every day</b>, refilled only by whatever sun the worst month offers, and expected to bridge multi-day storms. The sizing therefore starts from daily consumption and autonomy days, not outage loads. The hardware is the easy part — the {n} modules in the live table below all store the same 5.12kWh, run from <b>${minppw}/Wh</b>, and parallel into banks of any size. What follows is the math that decides how many of them an off-grid life actually needs.",
        "filter": "all",
        "table_heading": "Every tracked rack module — the off-grid building block, ranked by $/Wh",
        "sections": [
            ("Sizing: daily use × autonomy ÷ usable share", [
                "<table><thead><tr><th>Off-grid lifestyle</th><th>Daily use</th><th>2 days autonomy (usable)</th><th>Modules to buy*</th><th>Batteries at live floor–median $/Wh</th></tr></thead><tbody>"
                "<tr><td>Frugal cabin (fridge, lights, devices, no electric heat)</td><td>~5kWh</td><td>10kWh</td><td>3 (15.36kWh nameplate)</td><td class='num'>3 × {low5k}–{med5k}</td></tr>"
                "<tr><td>Full-time efficient home (gas cooking/heat, well pump)</td><td>~10kWh</td><td>20kWh</td><td>5 (25.6kWh nameplate)</td><td class='num'>5 × {low5k}–{med5k}</td></tr>"
                "<tr><td>Homestead (workshop, laundry, freezer, pump)</td><td>~15kWh</td><td>30kWh</td><td>8 (40.96kWh nameplate)</td><td class='num'>8 × {low5k}–{med5k}</td></tr>"
                "</tbody></table>",
                "<p>*Module counts round nameplate up so the bank cycles around 80% depth on a normal day — LiFePO4 allows deeper, but daily 100% cycling spends the cycle life you bought the bank for. Battery costs are computed per module from the live table's floor and median $/Wh (one module = 5.12kWh); inverter, array and rack are separate lines. For the grid-tied version of this math — sizing against outages instead of seasons — see <a href=\"/home-energy-storage/\">rack batteries for home storage</a>.</p>",
            ]),
            ("The winter rule: the array must refill a day, in the worst month", [
                "<p>A bank sized perfectly still fails in December if the array cannot replace a day's use in a short winter day. The planning rule: <b>array kW ≈ daily kWh ÷ worst-month peak sun hours</b>. A 10kWh/day home under 2.5 winter sun-hours needs roughly a 4kW array just to break even on an average December day — before storm reserves. That is why off-grid systems are designed array-first and bank-second, and why the autonomy column above stops at two days: beyond that, a small generator run a few hours per storm is almost always cheaper than the extra modules and panels that would replace it. Size the bank for weather, the array for the season, and let the generator cover the tail.</p>",
                "<ul><li><b>Daily cycling is the economic case for this format:</b> at one cycle a day, a module rated in the thousands of cycles is a decade-plus asset, and its $/Wh — the table's sort — is the price of every one of those days.</li><li><b>Closed-loop communications matter more off-grid:</b> with no grid to fall back on, the inverter must charge exactly as the BMS directs; every module class in the table offers CAN/RS485 pairing — verify your inverter on the maker's list via our <a href=\"/inverter-compatibility/\">compatibility guide</a>.</li><li><b>Cold sheds need heat:</b> a bank in an unheated outbuilding cannot charge below freezing, and two of the tracked module lines are self-heating variants (SunGoldPower's SGH48100T and Vatrer's heated rows in the table). In a heated space, that premium buys nothing — the $/Wh column prices the choice either way.</li></ul>",
            ]),
            ("Reading the table like an off-grid buyer", [
                "<p>Two cautions before you multiply a row by eight. First, the SunGoldPower 2-pack and 4-pack bundle rows carry bundle prices against single-module watt-hours in the feed, so their $/Wh reads artificially high — price a bank from the <b>single-module rows</b>. Second, a bank is one model repeated: pick the module whose inverter list, heating and parallel limit fit, then hold that choice for every expansion — mixing models in a parallel bank is the classic off-grid own-goal. The <a href=\"/how-many-server-rack-batteries/\">module-count guide</a> cross-checks the sizing table against specific loads, and the <a href=\"/server-rack-battery-price-per-kwh/\">$/kWh league table</a> tracks how the module prices themselves move.</p>",
            ]),
        ],
        "faqs": [
            ("How many server rack batteries do I need for off-grid solar?",
             "From your daily use: modules = daily kWh × autonomy days ÷ 0.8 usable share ÷ 5.12kWh per module, rounded up. A 10kWh/day home wanting two sunless days needs five modules (25.6kWh nameplate). Measure daily consumption first — it is the number everything else multiplies."),
            ("Can server rack batteries run a home completely off-grid?",
             "Yes — that is a standard use of the format: rack modules plus an off-grid or hybrid inverter and a correctly sized array. The constraints are system design, not the batteries: the array must replace a day's use in the worst month's sun, and the inverter must be an off-grid-capable model paired (ideally closed-loop) with the modules."),
            ("Do I need self-heating rack batteries for an off-grid cabin?",
             "Only if the bank will sit somewhere that drops below freezing while it needs to charge — an unheated shed or garage in a northern winter. LiFePO4 cannot accept a charge below 0°C without damage, so off-grid solar (which charges whenever the sun shines, cold or not) is exactly the case self-heating models exist for. In a heated utility space, standard modules are the cheaper $/Wh."),
        ],
        "related": ["home-energy-storage", "how-many-server-rack-batteries", "10kwh-battery-bank"],
    },
    {
        "slug": "rack-battery-winter-heating-guide",
        "title": "Heated Server Rack Batteries: When Self-Heating Is Worth the Premium",
        "desc": "A rack battery can discharge in deep cold but must never charge below freezing. Which installs actually need a self-heating module, what the heater costs in $/Wh, and the free alternatives — priced live.",
        "h1": "Heated Server Rack Batteries: Pay for the Heater Only If Your Bank Gets Cold",
        "blurb": "Self-heating modules solve exactly one problem — charging below freezing. The location test that decides if you have it, and what the fix costs per Wh.",
        "lede": "Every module in the live table below stores the same 5.12kWh and discharges happily in deep cold. The winter problem is narrower and sharper: <b>a LiFePO4 battery must not accept a charge below 0°C / 32°F</b>, and a solar-fed bank in an unheated building is offered a charge precisely on cold, bright mornings. Self-heating modules — tracked here from two brands, SunGoldPower's SGH48100T line and Vatrer's heated rows — exist for that one moment. Across the {n} tracked modules, prices run from <b>${minppw}/Wh</b>; this guide prices the heater against its alternatives so you only buy it when your building actually demands it.",
        "filter": "all",
        "table_heading": "Every tracked rack module — the heated rows sit among their standard siblings, ranked by $/Wh",
        "sections": [
            ("What a self-heating module actually does", [
                "<p>Inside a self-heating module, heating elements sit against the cells and the BMS runs a strict sequence when a charge is offered at low temperature: <b>warm first, charge second</b>. Incoming charge energy (from the inverter or array) is diverted to the heaters until the cells cross a safe threshold — typically a few degrees above freezing — and only then does charging current reach the cells. Two honest costs follow: the warm-up energy is not stored (on a very cold morning it is a real slice of a small winter array's output), and the first charge of the day starts late by the warm-up time. What the heater buys is the thing no setting can substitute for: a bank that can accept winter sun in an unheated space without plating lithium onto its cells and permanently spending capacity.</p>",
                "<p>Note what self-heating is <i>not</i>: it does not keep the bank warm around the clock (that would drain it), it does not improve cold <i>discharge</i> capacity, and it does not help a bank that lives somewhere warm. It is a charge-gate, opened on cold mornings — which is why the decision below is about your building, not your climate zone in the abstract.</p>",
            ]),
            ("The location test: do you actually need it?", [
                "<table><thead><tr><th>Where the bank lives</th><th>Winter reality</th><th>Verdict</th></tr></thead><tbody>"
                "<tr><td>Heated basement, utility room, conditioned garage</td><td>Bank stays above freezing all winter</td><td><b>Skip the heater.</b> Standard modules at the table's floor are the rational buy; the heating premium buys a feature that never runs</td></tr>"
                "<tr><td>Attached unheated garage, mild-winter region</td><td>Dips near freezing on the coldest nights; solar charging is a daytime event as the space warms</td><td><b>Judgment call.</b> A BMS with low-temperature charge cutoff (verify it on the product page) protects the bank by refusing frozen charges — you lose some cold-morning charging, not the battery</td></tr>"
                "<tr><td>Detached shed, barn, off-grid cabin — northern winter</td><td>Bank sits below freezing for weeks and the array offers charge whenever the sun appears</td><td><b>Buy the heated module, or move the bank.</b> This is the exact install self-heating exists for; the alternative is a heated/insulated battery space, costed below</td></tr>"
                "</tbody></table>",
                "<p>The middle row is where most buyers over-buy. A low-temp cutoff and a heater solve different problems: the cutoff <i>protects</i> (no charge until the bank warms on its own), the heater <i>enables</i> (charge now, warmed by the charge itself). Grid-backed banks in a garage can usually afford to wait for warmth — the grid covers the gap. Off-grid banks cannot: a refused charge on the one sunny day in a storm week is a generator run, which is why our <a href=\"/server-rack-battery-for-off-grid-solar/\">off-grid rack guide</a> treats heating as a first-order spec for unheated installs.</p>",
            ]),
            ("What the heater costs, in the table's own numbers", [
                "<p>Read the premium within each brand, single-module rows only (the 2- and 4-pack bundle rows in the feed carry bundle prices and read artificially high on $/Wh). On today's table, Vatrer's heated rows sit roughly <b>$80–$140 above its standard rows</b> of the same module, and SunGoldPower's self-heating SGH48100T sits about <b>$54 above</b> the standard SG48100P — in $/Wh terms, a premium on the order of one to three cents per watt-hour for the heater. Against the alternatives, that is cheap insurance where it is needed: insulating and heating a battery closet is a build project plus a permanent parasitic load, and relocating a bank indoors is free only if the indoor space, the wire run and the household all agree to it.</p>",
                "<ul><li><b>Bank math softens the premium:</b> the heater is priced per module, so a four-module bank pays it four times — but it also needs it four times, since every module in a cold bank faces the same frozen mornings. There is no 'one heated module warms the rack' shortcut.</li><li><b>Mixing heated and standard modules</b> in one cold bank defeats the purpose — the standard modules still cannot charge frozen. A cold bank is all-heated, or heated by its room.</li><li><b>Check the trigger, not just the badge:</b> confirm on the product page that the model's heating is automatic and BMS-controlled (some implementations differ in the temperature at which heating engages), and that your inverter's charge current comfortably covers the warm-up draw plus charging.</li></ul>",
                "<p>Decided you need it? The heated rows are identifiable in the table by name, and the <a href=\"/server-rack-battery-price-per-kwh/\">$/kWh league table</a> shows where they sit against the whole market. Decided you don't? You just saved the premium on every module in the bank — spend the attention instead on the <a href=\"/inverter-compatibility/\">inverter pairing</a>, which matters in every season.</p>",
            ]),
        ],
        "faqs": [
            ("Can a server rack battery charge below freezing?",
             "A standard LiFePO4 module must not: charging below 0°C / 32°F plates lithium and permanently costs capacity, which is why protected BMS units refuse the charge. Self-heating modules are the exception — they warm their cells with incoming charge energy before accepting it. Discharging in the cold is fine for both types, with reduced capacity until the bank warms."),
            ("Which server rack batteries are self-heating?",
             "In the catalog tracked here, two brands field them: SunGoldPower's SGH48100T line and Vatrer's heated 100Ah rows, both identifiable by name in the live table. On today's prices the heating premium runs roughly $54–$140 per module over the same brand's standard module — the table shows the current figures."),
            ("Is a self-heating rack battery worth it in a garage?",
             "Only if the garage actually drops below freezing while the bank needs to charge. In a heated or attached garage in a mild-winter region, a standard module with low-temperature charge cutoff is usually enough — it refuses the rare frozen charge and loses a morning, not the battery. In an unheated detached building in a northern winter, especially off-grid, self-heating is the difference between a bank that works all winter and one that sits protected but empty."),
        ],
        "related": ["server-rack-battery-for-off-grid-solar", "inverter-compatibility", "48v-100ah-server-rack-battery"],
    },
],
}

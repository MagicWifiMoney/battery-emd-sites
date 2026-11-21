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
],
}

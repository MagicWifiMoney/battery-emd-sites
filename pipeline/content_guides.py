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
],
}

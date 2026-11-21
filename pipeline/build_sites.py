#!/usr/bin/env python3
"""
build_sites.py — render the three EMD sites from data/products.json.

Sites (each standalone, no redirects, cross-linked):
  48vlifepo4battery.com   — 48V bare + rack batteries
  12vlifepo4battery.com   — 12V bare batteries
  serverrackbatteries.com — server-rack batteries

Playbook rules baked in (Notion AEO/GEO Playbook, Part 3):
  * All text in raw HTML (SSR static), JSON-LD, sitemap, robots allowing AI crawlers
  * Answer-first intros with live numbers + dates (quotable)
  * Affiliate disclosure + method on every site; no invented ratings; no fake was-prices
    (compare_at shown only when the maker feed itself lists it)
  * Focused page counts (~9-11 pages/site), no thin-page spam
Compliance: maker-store prices only; Amazon appears only as a no-price search
link with NO affiliate tag (Stage A). Affiliate swap point: product url field —
after Awin/Impact approval the fetcher/config maps urls to network deep links.
Freshness: prices carry the fetched_at date in copy; a JS guard hides numeric
prices when data is >72h old and shows "Check price" instead.
"""
import json, re, html, statistics
from pathlib import Path
from datetime import datetime, timezone

try:
    from content_guides import GUIDES
except ImportError:
    GUIDES = {}

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "products.json"
OUT = ROOT / "sites"

# ---------- classification ----------
def volts(p):
    if p.get("voltage"):
        return float(p["voltage"])
    m = re.search(r"\b(12\.8|25\.6|38\.4|51\.2|12|24|36|48)\s?v\b", p["title"], re.I)
    if m:
        return float(m.group(1))
    if p.get("ah") and p.get("wh"):
        return round(p["wh"] / p["ah"], 1)
    return None

def ah_of(p):
    if p.get("ah"):
        return float(p["ah"])
    if p.get("wh") and volts(p):
        return p["wh"] / volts(p)
    return None

def segment(p):
    if p["type"] == "rack-battery":
        return "rack"
    if p["type"] == "bare-battery":
        v = volts(p)
        if v and v >= 44: return "48v"
        if v and 11 <= v <= 14.5: return "12v"
    return None

def title_has(p, *words):
    t = p["title"].lower()
    return any(w in t for w in words)

# ---------- formatting ----------
def money(x): return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"
def ppw(p): return p["price_per_wh"]
def cap_label(p):
    a = ah_of(p)
    if a: return f"{a:,.0f}Ah · {p['wh']:,.0f}Wh"
    return f"{p['wh']:,.0f}Wh"

CSS = """
:root{--ink:#16202a;--mut:#5b6b7a;--line:#d9e1e8;--acc:#0b6e4f;--bg:#f7f9fa;--warn:#8a5a00;--warnbg:#fff4d6}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fff}
header.site{border-bottom:1px solid var(--line);background:var(--bg)}
header.site .in{max-width:1080px;margin:0 auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.brand{font-weight:700;font-size:17px;color:var(--ink);text-decoration:none}
nav a{color:var(--mut);text-decoration:none;margin-left:14px;font-size:14px}
nav a:hover{color:var(--acc)}
main{max-width:1080px;margin:0 auto;padding:20px 16px 10px}
h1{font-size:27px;line-height:1.2;margin:4px 0 8px}
h2{font-size:20px;margin:26px 0 8px}
h3{font-size:16px;margin:16px 0 6px}
.lede{font-size:16.5px;color:#2c3e50;max-width:75ch}
.updated{font-size:13px;color:var(--mut)}
.disclosure{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px;margin:14px 0}
#stale{display:none;background:var(--warnbg);color:var(--warn);border:1px solid #ecd28f;border-radius:8px;padding:10px 12px;font-size:14px;margin:10px 0}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}
.stat{border:1px solid var(--line);border-radius:8px;padding:10px 14px;min-width:150px;background:#fff}
.stat b{display:block;font-size:19px;color:var(--acc)}
.stat span{font-size:12.5px;color:var(--mut)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.card h3{margin:0 0 4px;font-size:15px}
.card p{margin:4px 0;font-size:13.5px;color:#2c3e50}
.card .big{font-size:18px;font-weight:700;color:var(--acc)}
table{width:100%;border-collapse:collapse;font-size:14px;margin:10px 0}
th,td{padding:8px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:var(--bg);white-space:nowrap;cursor:pointer;user-select:none}
th:hover{color:var(--acc)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.ppw{font-weight:700;color:var(--acc)}
.was{color:var(--mut);text-decoration:line-through;font-size:12px}
.oos{color:#b03a2e;font-size:12px}
a.buy{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:13px;white-space:nowrap}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.controls input,.controls select{padding:8px 10px;border:1px solid var(--line);border-radius:6px;font-size:14px}
.controls input{flex:1;min-width:200px}
.faq h3{margin:14px 0 2px}
.faq p{margin:2px 0 8px;max-width:78ch}
ul.links{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
ul.links li{border:1px solid var(--line);border-radius:8px;padding:10px 12px}
ul.links a{font-weight:600;color:var(--acc);text-decoration:none}
ul.links p{margin:3px 0 0;font-size:13px;color:var(--mut)}
footer{max-width:1080px;margin:0 auto;padding:16px;color:var(--mut);font-size:13px;border-top:1px solid var(--line)}
footer a{color:var(--acc)}
.prose{max-width:78ch}
.prose li{margin:4px 0}
@media(max-width:760px){table{font-size:13px}th,td{padding:6px 5px}h1{font-size:22px}}
"""

JS = """
<script>
(function(){
  var f=document.getElementById('fetched');
  if(f){var age=(Date.now()-new Date(f.dataset.ts).getTime())/36e5;
    if(age>72){document.getElementById('stale').style.display='block';
      document.querySelectorAll('.pricedata').forEach(function(e){e.style.display='none';});
      document.querySelectorAll('.checkonly').forEach(function(e){e.style.display='';});}}
  var q=document.getElementById('q'), brand=document.getElementById('brandf');
  function filt(){var s=(q?q.value:'').toLowerCase(), b=brand?brand.value:'';
    document.querySelectorAll('tbody tr').forEach(function(r){
      var ok=(!s||r.textContent.toLowerCase().indexOf(s)>=0)&&(!b||r.dataset.brand===b);
      r.style.display=ok?'':'none';});}
  if(q)q.addEventListener('input',filt); if(brand)brand.addEventListener('change',filt);
  document.querySelectorAll('th[data-k]').forEach(function(th){
    th.addEventListener('click',function(){
      var tb=th.closest('table').querySelector('tbody'),k=th.dataset.k,num=th.dataset.n==='1',dir=th.dataset.d==='a'?-1:1;
      th.dataset.d=dir===1?'a':'d';
      var rows=[].slice.call(tb.querySelectorAll('tr'));
      rows.sort(function(a,b){var x=a.children[k].dataset.v||a.children[k].textContent,y=b.children[k].dataset.v||b.children[k].textContent;
        return (num?parseFloat(x)-parseFloat(y):x.localeCompare(y))*dir;});
      rows.forEach(function(r){tb.appendChild(r);});});});
})();
</script>
"""

def esc(s): return html.escape(str(s), quote=True)

def table_html(rows, show_brand_filter=False, tid="t"):
    brands = sorted({p["brand"] for p in rows})
    ctrl = ""
    if show_brand_filter:
        opts = "".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in brands)
        ctrl = (f'<div class="controls"><input id="q" type="search" placeholder="Search products, e.g. 100Ah, Bluetooth, golf cart">'
                f'<select id="brandf"><option value="">All brands</option>{opts}</select></div>')
    trs = []
    for p in rows:
        was = f' <span class="was">{money(p["compare_at"])}</span>' if p.get("compare_at") and p["compare_at"] > p["price"] else ""
        avail = "" if p.get("available", True) else ' <span class="oos">check stock</span>'
        a = ah_of(p)
        trs.append(
            f'<tr data-brand="{esc(p["brand"])}">'
            f'<td data-v="{esc(p["title"])}"><a href="{esc(p["url"])}" rel="nofollow sponsored noopener" target="_blank">{esc(p["title"])}</a>{avail}</td>'
            f'<td data-v="{esc(p["brand"])}">{esc(p["brand"])}</td>'
            f'<td class="num" data-v="{a or 0}">{cap_label(p)}</td>'
            f'<td class="num pricedata" data-v="{p["price"]}">{money(p["price"])}{was}</td>'
            f'<td class="num ppw pricedata" data-v="{ppw(p)}">${ppw(p):.3f}</td>'
            f'<td class="num pricedata" data-v="{ppw(p)*1000}">${ppw(p)*1000:,.0f}</td>'
            f'<td><a class="buy" href="{esc(p["url"])}" rel="nofollow sponsored noopener" target="_blank">View deal</a>'
            f'<span class="checkonly" style="display:none"><a class="buy" href="{esc(p["url"])}" rel="nofollow sponsored noopener" target="_blank">Check price</a></span></td></tr>')
    return (ctrl + f'<div style="overflow-x:auto"><table id="{tid}"><thead><tr>'
            '<th data-k="0">Product</th><th data-k="1">Brand</th><th data-k="2" data-n="1" class="num">Capacity</th>'
            '<th data-k="3" data-n="1" class="num">Price</th><th data-k="4" data-n="1" class="num">$/Wh</th>'
            '<th data-k="5" data-n="1" class="num">$/kWh</th><th></th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')

def stats_html(rows):
    prices = [p["price"] for p in rows]; ppws = [ppw(p) for p in rows]
    cheap = min(rows, key=ppw)
    return ('<div class="stats">'
            f'<div class="stat"><b>{len(rows)}</b><span>batteries tracked</span></div>'
            f'<div class="stat"><b>${min(ppws):.3f}/Wh</b><span>lowest price per Wh ({esc(cheap["brand"])})</span></div>'
            f'<div class="stat"><b>${statistics.median(ppws):.3f}/Wh</b><span>median price per Wh</span></div>'
            f'<div class="stat"><b>{money(min(prices))}–{money(max(prices))}</b><span>price range</span></div></div>')

def faq_html(faqs):
    items = "".join(f'<h3>{esc(q)}</h3><p>{a}</p>' for q, a in faqs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faqs]}
    return f'<section class="faq"><h2>Frequently asked questions</h2>{items}</section><script type="application/ld+json">{json.dumps(ld)}</script>'


# Affiliate-network site-verification meta tags (homepage only), keyed by domain.
VERIFY_META = {
    "48vlifepo4battery.com": "<meta name='impact-site-verification' value='ec050c2d-1e9d-48e1-a271-857624705cd2'>",
    "12vlifepo4battery.com": "<meta name='impact-site-verification' value='09d7df7a-711d-4ada-bc8b-67df34ab4b5a'>",
    "serverrackbatteries.com": "<meta name='impact-site-verification' value='63ba17d3-02ec-4189-ad44-68c1b729f522'>",
}


# ---------- page shell ----------
def page(site, path, title, desc, body, extra_head=""):
    verify = VERIFY_META.get(site["domain"], "") if path == "/" else ""
    nav = "".join(f'<a href="/{c["slug"]}/">{esc(c["nav"])}</a>' for c in site["clusters"][:5])
    sisters = " · ".join(
        f'<a href="https://{d}/">{esc(n)}</a>' for d, n in SISTER_LINKS if d != site["domain"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="https://{site['domain']}{path}">
<style>{CSS}</style>
{verify}
{extra_head}
</head>
<body>
<header class="site"><div class="in">
<a class="brand" href="/">{esc(site['name'])}</a>
<nav>{nav}<a href="/about/">About &amp; method</a></nav>
</div></header>
<main>
{body}
</main>
<footer>
<p><b>How prices are gathered:</b> automatically from the manufacturers' own online stores, refreshed several times a day. We compute price per watt-hour from each battery's rated capacity. We never invent ratings or discounts — a struck-through price appears only when the maker's own store lists one. Full method on the <a href="/about/">about page</a>.</p>
<p><b>Affiliate disclosure:</b> some outbound links on this site are affiliate links. If you buy through them we may earn a commission at no extra cost to you. Prices shown come from the makers' stores, not from affiliate feeds.</p>
<p>Sister trackers: {sisters}</p>
</footer>
{JS}
</body>
</html>"""

SISTER_LINKS = [
    ("48vlifepo4battery.com", "48V LiFePO4 Battery prices"),
    ("12vlifepo4battery.com", "12V LiFePO4 Battery prices"),
    ("serverrackbatteries.com", "Server Rack Batteries prices"),
]

DISCLOSURE = ('<div class="disclosure">Prices below come from the manufacturers\' own stores and were last refreshed '
              '<span id="fetched" data-ts="{ts}">{date}</span>. We rank by price per watt-hour ($/Wh) — the fairest way '
              'to compare batteries of different sizes. Listings are data, not reviews: we have not hands-on tested these batteries.</div>'
              '<div id="stale">These prices are more than 72 hours old, so we have hidden the numbers — click through to the maker\'s store for the current price.</div>')

def itemlist_ld(rows, site):
    items = []
    for i, p in enumerate(rows[:20], 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "Product", "name": p["title"], "brand": {"@type": "Brand", "name": p["brand"]},
            "offers": {"@type": "Offer", "url": p["url"], "priceCurrency": "USD", "price": p["price"],
                       "availability": "https://schema.org/InStock" if p.get("available", True) else "https://schema.org/OutOfStock"}}})
    ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}
    return f'<script type="application/ld+json">{json.dumps(ld)}</script>'

def cluster_cards(site):
    lis = "".join(f'<li><a href="/{c["slug"]}/">{esc(c["h1"])}</a><p>{esc(c["blurb"])}</p></li>' for c in site["clusters"])
    return f'<h2>Browse by need</h2><ul class="links">{lis}</ul>'

# ---------- guide / comparison / blog pages (content_guides.py) ----------
def resolve_rows(spec, pool):
    """Guide table filter: None | FILTERS key | 'brand:A+B' | 'brand:A+B@filterkey'."""
    if not spec:
        return []
    rows = list(pool)
    if "@" in spec:
        spec, fk = spec.split("@", 1)
        rows = FILTERS[fk](rows)
    if spec.startswith("brand:"):
        brands = {b.strip() for b in spec[len("brand:"):].split("+")}
        rows = [p for p in rows if p["brand"] in brands]
    elif spec in FILTERS:
        rows = FILTERS[spec](rows)
    return sorted(rows, key=ppw)

def guide_ctx(rows, pool, date_str):
    base = rows if rows else pool
    ppws = [ppw(p) for p in base]; prices = [p["price"] for p in base]
    cheap = min(base, key=ppw)
    ctx = {"n": len(base), "minppw": f"{min(ppws):.3f}", "medppw": f"{statistics.median(ppws):.3f}",
           "maxppw": f"{max(ppws):.3f}", "minprice": money(min(prices)), "maxprice": money(max(prices)),
           "date": date_str, "cheap_title": esc(cheap["title"]), "cheap_brand": esc(cheap["brand"]),
           "cheap_price": money(cheap["price"]), "cheap_ppw": f"{ppw(cheap):.3f}",
           "cheap_cap": cap_label(cheap),
           "low5k": money(min(ppws) * 5120), "med5k": money(statistics.median(ppws) * 5120),
           "low10k": money(min(ppws) * 10240), "med10k": money(statistics.median(ppws) * 10240)}
    for b in sorted({p["brand"] for p in base}):
        brows = [p for p in base if p["brand"] == b]
        bk = re.sub(r"[^a-z0-9]+", "_", b.lower()).strip("_")
        bcheap = min(brows, key=lambda p: p["price"])
        ctx[f"{bk}_n"] = len(brows)
        ctx[f"{bk}_min_price"] = money(bcheap["price"])
        ctx[f"{bk}_min_ppw"] = f"{ppw(bcheap):.3f}"
        ctx[f"{bk}_cheap_title"] = esc(bcheap["title"])
    return ctx

def fmt(s, ctx):
    try:
        return s.format(**ctx)
    except (KeyError, IndexError, ValueError):
        return s

def guide_cards(site):
    gs = GUIDES.get(site["domain"], [])
    if not gs:
        return ""
    lis = "".join(f'<li><a href="/{g["slug"]}/">{esc(g["h1"])}</a><p>{esc(g["blurb"])}</p></li>' for g in gs)
    return f'<h2>Guides &amp; explainers</h2><ul class="links">{lis}</ul>'

def top_picks(rows):
    cheap = min(rows, key=ppw)
    under = [p for p in rows if p["price"] <= 1000]
    best_value_small = min(under, key=ppw) if under else cheap
    big = [p for p in rows if p["wh"] >= 5000]
    premium = max(big, key=lambda p: p["price"]) if big else max(rows, key=lambda p: p["price"])
    def card(label, p, why):
        return (f'<div class="card"><h3>{esc(label)}</h3><p><b>{esc(p["title"])}</b></p>'
                f'<p class="big pricedata">${ppw(p):.3f}/Wh · {money(p["price"])}</p>'
                f'<p>{esc(why)}</p><p><a class="buy" href="{esc(p["url"])}" rel="nofollow sponsored noopener" target="_blank">View deal</a></p></div>')
    return ('<h2>Top picks by the numbers</h2><div class="cards">'
            + card("Lowest $/Wh overall", cheap, f'{cap_label(cheap)} from {cheap["brand"]}. The cheapest stored energy in this category right now.')
            + card("Lowest $/Wh under $1,000", best_value_small, f'{cap_label(best_value_small)} from {best_value_small["brand"]}. Best cost per watt-hour without crossing four figures.')
            + card("Biggest capacity tracked", premium, f'{cap_label(premium)} from {premium["brand"]}. For large banks and whole-home builds.')
            + '</div>')


# ---------- content: FAQs (factual, no invented claims) ----------
FAQ_48V = [
    ("What is the cheapest 48V LiFePO4 battery per watt-hour?",
     "It changes as maker prices move — the table above is refreshed several times a day and sorted by $/Wh, so the top row is always the current answer. As a rule, large 100Ah (5.12kWh) rack and floor batteries from value brands cluster near the bottom of the $/Wh range, while small marine/golf batteries cost more per watt-hour."),
    ("Is a 48V LiFePO4 battery really 51.2V?",
     "Yes. A '48V' LiFePO4 battery is built from 16 cells in series at 3.2V nominal each, giving 51.2V nominal and a full-charge voltage of about 58.4V. It is the direct lithium replacement class for 48V lead-acid systems and pairs with 48V inverters."),
    ("Can I put 48V LiFePO4 batteries in parallel?",
     "Most 48V LiFePO4 batteries support parallel connection (commonly up to 4–16 units, depending on the model) to add capacity. Series connection is usually NOT supported on 48V packs. Always match brand, model and age, and check the product page for the exact limit before wiring."),
    ("What charger does a 48V LiFePO4 battery need?",
     "A LiFePO4-profile charger or inverter-charger set to a 58.4V absorption voltage for a 51.2V pack, with no equalization stage. Many solar inverter-chargers have a lithium profile built in."),
    ("48V server rack vs regular 48V battery — what's the difference?",
     "Server rack batteries are 48V (51.2V) packs in a standard 19-inch rack-mount case (usually 3U–4U) with built-in communications (CAN/RS485) for inverter pairing. Electrically they do the same job as a floor or wall 48V battery; the rack format just stacks neatly and scales. We track them on our sister site, <a href=\"https://serverrackbatteries.com/\">serverrackbatteries.com</a>."),
]
FAQ_12V = [
    ("What is the cheapest 12V LiFePO4 battery per watt-hour?",
     "The table above is refreshed several times a day and ranked by $/Wh, so the top row is the live answer. In general the big 280–314Ah batteries deliver the lowest $/Wh, while compact 50–100Ah batteries cost more per watt-hour but weigh far less."),
    ("Is a 12V LiFePO4 battery really 12.8V?",
     "Yes. Four 3.2V LiFePO4 cells in series give 12.8V nominal and about 14.6V fully charged — a drop-in match for 12V lead-acid systems in RVs, boats and solar setups."),
    ("Can I connect 12V LiFePO4 batteries in series and parallel?",
     "Most models support up to 4 in series (for 24V/48V systems) and multiple in parallel, but limits vary by brand and model — some budget packs are parallel-only. Match brand, model and purchase date, and confirm the limit on the product page before wiring."),
    ("Will my existing lead-acid charger work?",
     "Often yes for a basic charge, but a LiFePO4-profile charger (14.2–14.6V absorption, no equalization or desulfation) gets a fuller charge and longer life. Avoid chargers that run automatic equalization."),
    ("How long will a 12V 100Ah LiFePO4 battery run my gear?",
     "A 100Ah pack stores 1,280Wh. Divide by your load: a 100W fridge draw runs roughly 10–12 hours accounting for inverter losses, a 50W fan about a day. LiFePO4 can safely use 80–100% of its rated capacity, unlike lead-acid's ~50%."),
]
FAQ_RACK = [
    ("What is a server rack battery?",
     "A server rack battery is a LiFePO4 battery built into a standard 19-inch rack-mount case (typically 3U or 4U tall), almost always 48V/51.2V and 100Ah (5.12kWh) per module. Modules stack in a rack cabinet and connect in parallel to build banks from 5kWh to 100kWh+, with CAN/RS485 communication to hybrid inverters."),
    ("How much does a server rack battery cost per kWh?",
     "The live table above tracks it: divide any row's price by its kWh, or use the $/kWh column. Value-brand 100Ah modules have recently clustered around $170–$230 per kWh, while premium brands with longer warranties run higher."),
    ("How many server rack batteries do I need for 10kWh?",
     "Two standard 5.12kWh (48V 100Ah) modules in parallel give 10.24kWh. For a typical home backup target of 20kWh, plan on four modules. Check the model's parallel limit (commonly 16–64 units) and your inverter's supported battery list before buying."),
    ("Do server rack batteries work with my inverter?",
     "Most speak CAN and RS485 and publish compatibility lists covering Growatt, Deye, Sol-Ark, Victron, Luxpower, Schneider and others. Closed-loop communication (battery talks to inverter) needs a matched protocol; without it, the inverter can still run on voltage-based settings. Confirm your exact inverter model on the product page."),
    ("Server rack vs wall-mounted battery — which is better?",
     "Electrically they are the same 51.2V LiFePO4 storage. Rack modules are usually cheaper per kWh and scale one 5.12kWh step at a time; wall-mounted units look cleaner and save floor space but cost more per kWh. We track wall and floor 48V batteries on our sister site, <a href=\"https://48vlifepo4battery.com/\">48vlifepo4battery.com</a>."),
]

ABOUT_BODY = """
<h1>About this tracker</h1>
<div class="prose">
<p>This site exists for one reason: batteries are sold by amp-hours and brand stories, but the fair way to compare them is <b>price per watt-hour ($/Wh)</b> — what each unit of stored energy actually costs. A $449 battery with 4,019Wh ($0.112/Wh) is cheaper energy than a $300 battery with 1,280Wh ($0.234/Wh), even though the sticker says otherwise.</p>
<h2>Method</h2>
<ul>
<li>Prices are collected automatically from the manufacturers' own online stores, several times a day.</li>
<li>Capacity comes from each product's rated voltage × amp-hours (or the maker's stated watt-hours). Where a feed is ambiguous, the listing is excluded rather than guessed.</li>
<li>$/Wh = price ÷ watt-hours. $/kWh is the same number × 1,000.</li>
<li>We do not hands-on test batteries, and we never publish invented ratings, invented discounts or fake "was" prices. A struck-through price appears only when the maker's own store lists one.</li>
<li>If a price feed is more than 72 hours old, this site hides the numbers rather than show you stale prices.</li>
</ul>
<h2>Affiliate disclosure</h2>
<p>Some outbound links are affiliate links: if you buy through them, the site may earn a commission at no extra cost to you. That is how the tracker pays for itself. Rankings are computed from price data only — no brand can pay for placement, and the sort order is the same math for everyone.</p>
<h2>Corrections</h2>
<p>Spot a wrong capacity or a dead link? The data refreshes several times a day, so most errors fix themselves on the next pass. Persistent errors usually trace back to the maker's own product feed.</p>
</div>
"""


# ---------- cluster definitions ----------
def C(slug, nav, h1, blurb, filt, intro, title=None):
    return {"slug": slug, "nav": nav, "h1": h1, "blurb": blurb, "filter": filt,
            "intro": intro, "title": title or h1}

FILTERS = {
    "all": lambda rows: rows,
    "ah5_60": lambda rows: [p for p in rows if ah_of(p) and 5 <= ah_of(p) <= 60],
    "ah90_330": lambda rows: [p for p in rows if ah_of(p) and 90 <= ah_of(p) <= 330],
    "ah90_115": lambda rows: [p for p in rows if ah_of(p) and 90 <= ah_of(p) <= 115],
    "ah180_230": lambda rows: [p for p in rows if ah_of(p) and 180 <= ah_of(p) <= 235],
    "ah280_330": lambda rows: [p for p in rows if ah_of(p) and 280 <= ah_of(p) <= 330],
    "wh4800_5600": lambda rows: [p for p in rows if 4800 <= p["wh"] <= 5600],
    "golf": lambda rows: [p for p in rows if title_has(p, "golf")],
    "rack": lambda rows: [p for p in rows if p["type"] == "rack-battery"],
    "solar_kw": lambda rows: [p for p in rows if title_has(p, "solar", "off-grid", "off grid", "home energy", "energy storage")],
    "rv": lambda rows: [p for p in rows if title_has(p, "rv", "caravan", "camper", "motorhome")],
    "marine": lambda rows: [p for p in rows if title_has(p, "marine", "trolling", "boat", "kayak", "fish")],
    "top15": lambda rows: rows[:15],
}

SITES = [
    {
        "domain": "48vlifepo4battery.com", "name": "48V LiFePO4 Battery",
        "phrase": "48V LiFePO4 battery", "display": "48V LiFePO4 Battery", "pool": ["48v", "rack"], "faqs": FAQ_48V,
        "lede": "Every {phrase} from the major makers' own stores, ranked by the only number that makes batteries comparable: <b>price per watt-hour</b>. Right now {n} models are tracked — the cheapest stored energy costs <b>${minppw}/Wh</b> and the median is ${medppw}/Wh. Prices refreshed {date}.",
        "clusters": [
            C("48v-100ah-lifepo4-battery", "100Ah", "48V 100Ah LiFePO4 Batteries",
              "The standard 5.12kWh building block — every 100Ah model compared by $/Wh.",
              "ah90_115",
              ["The 48V 100Ah (5.12kWh) battery is the standard brick of home solar storage: one module runs a meaningful slice of a house, and modules parallel upward from there. Because every model stores the same 5,120Wh, this is the purest price fight in the category — the table below is the whole story, sorted by $/Wh.",
               "Watch the fine print when comparing: some 100Ah models are rack-mount with inverter communications, others are simple floor batteries for golf carts and off-grid cabins. Same energy, different jobs."]),
            C("golf-cart-batteries", "Golf cart", "48V LiFePO4 Golf Cart Batteries",
              "Drop-in 48V lithium conversions for golf carts, ranked by $/Wh.",
              "golf",
              ["A 48V golf cart lithium conversion replaces six or eight lead-acid batteries with one pack that weighs a third as much and charges in a few hours. The models below are the 48V LiFePO4 packs marketed for golf carts, ranked by price per watt-hour.",
               "Check your cart's controller and charger before ordering: most conversions need a LiFePO4-profile 58.4V charger, and the pack's continuous discharge rating must cover your controller's draw on hills."]),
            C("solar-storage-batteries", "Solar storage", "48V LiFePO4 Batteries for Solar Storage",
              "48V batteries sold for solar and off-grid home storage, compared on $/Wh.",
              "solar_kw",
              ["For home solar, 48V is the working voltage: it pairs with the mainstream hybrid inverters and keeps cable runs thin. The batteries below are the 48V LiFePO4 models the makers sell for solar and off-grid storage, ranked by $/Wh.",
               "Sizing rule of thumb: one 5.12kWh module covers lights, fridge, internet and a few outlets overnight. Most homes land between 10kWh (2 modules) and 20kWh (4 modules) for real backup."]),
            C("server-rack-batteries", "Server rack", "48V Server Rack Batteries",
              "Rack-mount 48V modules — the format that usually wins on $/Wh.",
              "rack",
              ["Server rack batteries are 48V (51.2V) LiFePO4 modules in a 19-inch rack case with inverter communications built in. They are frequently the cheapest way to buy a watt-hour in the whole 48V category, which is why they get their own tracker: <a href=\"https://serverrackbatteries.com/\">serverrackbatteries.com</a> follows every rack module we can source, with sizing and inverter guides.",
               "The rack modules currently in this catalog are below; the dedicated rack tracker carries the full set plus bank-sizing guides."]),
            C("home-battery-backup", "Home backup", "48V LiFePO4 for Home Battery Backup",
              "Building a home backup bank from 48V batteries — costs by the kWh.",
              "all",
              ["A home backup bank is just 48V batteries plus an inverter. Built from the modules below, backup costs whatever the $/kWh column says — recently far less per kWh than an all-in-one power station of the same capacity, at the price of wiring it yourself or hiring an installer.",
               "Start from the loads you refuse to lose (fridge, lights, internet, a mini-split), add up their watts, and multiply by the hours of backup you want. That watt-hour target divided by 5,120Wh is your module count."]),
            C("how-to-choose", "How to choose", "How to Choose a 48V LiFePO4 Battery",
              "The five checks that matter: $/Wh, BMS, comms, parallel limits, warranty.",
              "top15",
              ["<b>1. Compare $/Wh, not sticker price.</b> Capacity differs wildly between models; price per watt-hour is the honest unit. <b>2. Match the form factor to the job</b> — rack modules for inverter systems, sealed packs for carts and marine use. <b>3. Check inverter communications</b> (CAN/RS485) if you want closed-loop charging. <b>4. Confirm parallel limits</b> before planning a big bank. <b>5. Read the warranty in years and cycles</b>, and prefer brands with a US support presence.",
               "The 15 cheapest-by-$/Wh 48V batteries right now are below — for most buyers the right answer is on this list."]),
        ],
    },
    {
        "domain": "12vlifepo4battery.com", "name": "12V LiFePO4 Battery",
        "phrase": "12V LiFePO4 battery", "display": "12V LiFePO4 Battery", "pool": ["12v"], "faqs": FAQ_12V,
        "lede": "Every {phrase} from the major makers' own stores, ranked by <b>price per watt-hour</b> — the fair way to compare a 100Ah pack against a 314Ah one. {n} models tracked; cheapest stored energy is <b>${minppw}/Wh</b>, median ${medppw}/Wh. Prices refreshed {date}.",
        "clusters": [
            C("12v-100ah-lifepo4-battery", "100Ah", "12V 100Ah LiFePO4 Batteries",
              "The most popular size on the market — every 100Ah model by $/Wh.",
              "ah90_115",
              ["The 12V 100Ah (1,280Wh) battery is the default upgrade for RVs, boats and small solar systems — one battery replaces a pair of lead-acids at half the weight and twice the usable capacity. Every model below stores the same energy, so $/Wh is a pure price comparison.",
               "Differences that matter beyond price: low-temperature charge protection (essential for winter camping), Bluetooth monitoring, and whether the BMS allows series wiring for 24V/48V systems."]),
            C("12v-200ah-lifepo4-battery", "200Ah", "12V 200Ah LiFePO4 Batteries",
              "Double-capacity 200Ah-class packs — usually cheaper per Wh than 100Ah.",
              "ah180_230",
              ["A 200Ah-class 12V battery stores about 2.56–2.94kWh in one case — fewer cables and BMS units than two 100Ah packs, and usually a lower $/Wh. This class (200Ah, 230Ah) is the sweet spot for vans, larger RVs and cabin solar.",
               "Mind the weight and the BMS discharge rating: a single 200Ah pack's continuous output may be lower than two paralleled 100Ah packs, which matters for big inverters."]),
            C("12v-314ah-lifepo4-battery", "314Ah", "12V 314Ah LiFePO4 Batteries",
              "The $/Wh leaders: 314Ah packs storing 4kWh in a single case.",
              "ah280_230" if False else "ah280_330",
              ["The 314Ah class is where 12V stored energy gets cheapest: roughly 4,019Wh in one battery, routinely the lowest $/Wh in the entire 12V catalog. If your space fits the larger case, this is the value play for off-grid and big RV banks.",
               "One caution: a single 314Ah battery is a single point of failure and a heavy lift (around 60–70 lb). For mission-critical setups, two smaller packs in parallel add redundancy."]),
            C("rv-batteries", "RV", "12V LiFePO4 Batteries for RVs",
              "Batteries marketed for RV and camper use, ranked by $/Wh.",
              "rv",
              ["For RV house power, LiFePO4 wins on usable capacity (nearly 100% vs ~50% for lead-acid), weight, and charge speed from solar or a converter. The packs below are the ones makers sell specifically for RV use, ranked by $/Wh.",
               "Before you buy: confirm your converter/charger has a lithium profile (or budget for one), and get low-temperature protection if you camp below freezing — charging a frozen LiFePO4 battery damages it."]),
            C("marine-trolling-motor-batteries", "Marine", "12V LiFePO4 Trolling Motor & Marine Batteries",
              "Lightweight 12V packs for trolling motors and boats, by $/Wh.",
              "marine",
              ["On the water, weight is range. A 12V 100Ah LiFePO4 weighs about 24 lb against 60+ lb for lead-acid, and holds voltage flat through the discharge — your trolling motor pulls the same at 20% charge as at 90%. The marine-marketed packs below are ranked by $/Wh.",
               "Look for an IP-rated case and a BMS whose continuous rating covers your motor's max draw (a 55 lb-thrust motor pulls roughly 50A at full throttle)."]),
            C("how-to-choose", "How to choose", "How to Choose a 12V LiFePO4 Battery",
              "Size, BMS, low-temp protection and $/Wh — the checks that matter.",
              "top15",
              ["<b>1. Start with $/Wh.</b> Sticker prices mislead because capacities differ; cost per watt-hour is the comparison. <b>2. Size from your loads:</b> watt-hours = watts × hours; a 100Ah pack holds 1,280Wh. <b>3. Low-temp protection</b> is non-negotiable if the battery will ever charge below freezing. <b>4. Check series/parallel limits</b> if you may expand later. <b>5. Bluetooth monitoring</b> is genuinely useful — state-of-charge guessing is the top complaint with cheap packs.",
               "The 15 cheapest-by-$/Wh 12V batteries right now:"]),
        ],
    },
    {
        "domain": "serverrackbatteries.com", "name": "Server Rack Batteries",
        "phrase": "server rack batteries", "display": "Server Rack Batteries", "pool": ["rack"], "faqs": FAQ_RACK,
        "lede": "Every {phrase} module we can source from the makers' own stores, ranked by <b>price per watt-hour</b>. Rack modules are usually the cheapest way to buy lithium storage — currently <b>${minppw}/Wh</b> at the low end across {n} tracked modules. Prices refreshed {date}.",
        "clusters": [
            C("48v-100ah-server-rack-battery", "100Ah rack", "48V 100Ah Server Rack Batteries",
              "The standard 5.12kWh rack module — every brand compared by $/Wh.",
              "all",
              ["The 48V 100Ah rack module (5.12kWh, 3U or 4U) is the atom of modern home storage: every major brand sells one, they all store identical energy, and they parallel into banks of 10–100kWh+. That makes $/Wh a pure price fight — the table below is the fight, live.",
               "Beyond price, compare cycle-life ratings, the inverter compatibility list, and whether the BMS supports closed-loop communication with your inverter brand."]),
            C("home-energy-storage", "Home storage", "Server Rack Batteries for Home Energy Storage",
              "Building a home battery bank from rack modules — real costs per kWh.",
              "all",
              ["Rack modules are how solar installers build home storage without the all-in-one markup: a cabinet, an inverter, and as many 5.12kWh modules as the house needs. The $/kWh column in the table is your storage cost before inverter and install — compare it against any packaged home battery quote.",
               "A common path: start with 2 modules (10.24kWh) for essentials backup, add modules yearly. Because modules parallel, the bank grows without replacing anything."]),
            C("10kwh-battery-bank", "10kWh bank", "Building a 10kWh Battery Bank from Server Rack Modules",
              "Two modules, 10.24kWh — what it costs at today's prices.",
              "all",
              ["Ten kWh is the most common home backup target, and with rack modules it is a two-module build: 2 × 5.12kWh = 10.24kWh. At the prices in the table, the batteries alone land near the $/kWh figure shown — typically well under a packaged 10kWh wall battery.",
               "Budget beyond the modules: a rack cabinet or wall bracket, a compatible hybrid inverter, and heavy-gauge interconnect cables. The modules' parallel limit (often 16+) leaves room to grow to 20kWh later.",
               "Starting smaller? The first step of the ladder is a single 5.12kWh module — our 48V sister site prices the <a href=\"https://48vlifepo4battery.com/5kwh-battery/\">5kWh battery class</a> and the full 5 → 10 → 20kWh ladder from the same live data."]),
            C("inverter-compatibility", "Inverter pairing", "Server Rack Battery Inverter Compatibility",
              "CAN/RS485 closed-loop pairing with Growatt, Deye, Sol-Ark, Victron and more.",
              "all",
              ["Nearly every rack module ships with CAN and RS485 ports and a published inverter compatibility list — Growatt, Deye, Sol-Ark, Luxpower, Victron, Schneider, SMA and Voltronic-based brands recur across brands. Closed-loop mode lets the battery's BMS set charge parameters directly; it is worth having, but every module also runs fine on voltage-based settings with any 48V inverter-charger.",
               "Before ordering, find your exact inverter model on the module maker's compatibility list (linked from each product page) and confirm the communication cable is included or available."]),
            C("how-many-server-rack-batteries", "Sizing guide", "How Many Server Rack Batteries Do You Need?",
              "Sizing a rack bank: loads, hours and module counts, with today's costs.",
              "all",
              ["Work backwards from loads. List what must stay on (fridge ~150W, lights ~100W, internet ~20W, furnace blower ~400W), multiply total watts by the hours of backup you want, and divide by 5,120Wh per module. Example: 670W × 10 hours ≈ 6.7kWh → 2 modules with headroom.",
               "Then sanity-check against daily solar production if you have panels: a bank much larger than a day's surplus rarely fills. The table below prices your module options at today's $/Wh."]),
        ],
    },
]


# ---------- build ----------
def build():
    data = json.loads(DATA.read_text())
    fetched = data["fetched_at"]
    dt = datetime.fromisoformat(fetched.replace("Z", "+00:00")).astimezone(timezone.utc)
    date_str = dt.strftime("%B %d, %Y")
    prods = [p for p in data["products"] if p.get("available", True) or True]
    # Merge browser-collected products from stores the fetcher cannot reach
    # (config/manual_products.json), deduped by URL, feed data wins.
    manual_path = ROOT / "config" / "manual_products.json"
    if manual_path.exists():
        seen = {p["url"] for p in prods}
        for mp in json.loads(manual_path.read_text()).get("products", []):
            if mp["url"] not in seen:
                prods.append(mp)
                seen.add(mp["url"])
    pools = {"48v": [], "12v": [], "rack": []}
    for p in prods:
        s = segment(p)
        if s in pools:
            pools[s].append(p)
    for k in pools:
        pools[k].sort(key=ppw)

    summary = {}
    for site in SITES:
        pool = []
        for key in site["pool"]:
            pool.extend(pools[key])
        pool = sorted({p["url"]: p for p in pool}.values(), key=ppw)
        root = OUT / site["domain"]
        root.mkdir(parents=True, exist_ok=True)
        urls = ["/"]
        ppws = [ppw(p) for p in pool]
        lede = site["lede"].format(phrase=site["phrase"], n=len(pool),
                                   minppw=f"{min(ppws):.3f}", medppw=f"{statistics.median(ppws):.3f}",
                                   date=date_str)
        body = (f'<h1>{esc(site["display"])} — Prices per Watt-Hour, Compared Live</h1>'
                f'<p class="lede">{lede}</p>'
                + DISCLOSURE.format(ts=fetched, date=date_str)
                + stats_html(pool)
                + top_picks(pool)
                + f'<h2>All {esc(site["phrase"])} prices, ranked by $/Wh</h2>'
                + table_html(pool, show_brand_filter=True)
                + cluster_cards(site)
                + guide_cards(site)
                + faq_html(site["faqs"]))
        (root / "index.html").write_text(page(
            site, "/", f'{site["display"]} Prices Compared by $/Wh — Live Price Tracker',
            f'Compare {len(pool)} {site["phrase"]} models by price per watt-hour. Prices from the makers\' own stores, refreshed {date_str}.',
            body, extra_head=itemlist_ld(pool, site)))
        # cluster pages
        for c in site["clusters"]:
            sub = FILTERS[c["filter"]](pool)
            sub = sorted(sub, key=ppw)[:30]
            if not sub:
                sub = pool[:10]
            urls.append(f'/{c["slug"]}/')
            paras = "".join(f'<p>{t}</p>' for t in c["intro"])
            sib = [o for o in site["clusters"] if o["slug"] != c["slug"]][:3]
            sib_html = "".join(f'<li><a href="/{o["slug"]}/">{esc(o["h1"])}</a><p>{esc(o["blurb"])}</p></li>' for o in sib)
            cbody = (f'<h1>{esc(c["h1"])}</h1>'
                     f'<p class="lede">{esc(c["blurb"])}</p>'
                     + DISCLOSURE.format(ts=fetched, date=date_str)
                     + stats_html(sub)
                     + f'<h2>Prices, ranked by $/Wh</h2>' + table_html(sub)
                     + f'<div class="prose">{paras}</div>'
                     + f'<h2>Keep comparing</h2><ul class="links"><li><a href="/">All {esc(site["phrase"])} prices</a><p>The full live table, every model ranked by $/Wh.</p></li>{sib_html}</ul>'
                     + faq_html(site["faqs"][:3]))
            d = root / c["slug"]; d.mkdir(exist_ok=True)
            (d / "index.html").write_text(page(
                site, f'/{c["slug"]}/', f'{c["h1"]} — Prices by $/Wh',
                f'{c["blurb"]} Prices from the makers\' own stores, refreshed {date_str}.', cbody))
        # guide / comparison / blog pages (content_guides.py)
        guides = GUIDES.get(site["domain"], [])
        by_slug = {c["slug"]: c for c in site["clusters"]}
        for g in guides:
            by_slug[g["slug"]] = g
        for g in guides:
            rows = resolve_rows(g.get("filter"), pool)[:40]
            ctx = guide_ctx(resolve_rows(g.get("ctx_filter") or g.get("filter"), pool), pool, date_str)
            parts = [f'<h1>{esc(g["h1"])}</h1>',
                     f'<p class="lede">{fmt(g["lede"], ctx)}</p>',
                     DISCLOSURE.format(ts=fetched, date=date_str)]
            if rows and g.get("stats", True):
                parts.append(stats_html(rows))
            for head, blocks in g.get("sections", []):
                parts.append(f'<h2>{esc(head)}</h2>')
                for b in blocks:
                    parts.append(fmt(b, ctx))
            if rows:
                parts.append(f'<h2>{esc(g.get("table_heading") or "Prices, ranked by $/Wh")}</h2>')
                parts.append(table_html(rows))
            rel = [f'<li><a href="/">All {esc(site["phrase"])} prices</a><p>The full live table, every model ranked by $/Wh.</p></li>']
            for slug in g.get("related", [])[:3]:
                o = by_slug.get(slug)
                if o:
                    rel.append(f'<li><a href="/{slug}/">{esc(o["h1"])}</a><p>{esc(o["blurb"])}</p></li>')
            parts.append(f'<h2>Keep comparing</h2><ul class="links">{"".join(rel)}</ul>')
            gfaqs = g.get("faqs") or site["faqs"][:3]
            parts.append(faq_html([(q, fmt(a, ctx)) for q, a in gfaqs]))
            urls.append(f'/{g["slug"]}/')
            gd = root / g["slug"]; gd.mkdir(exist_ok=True)
            (gd / "index.html").write_text(page(
                site, f'/{g["slug"]}/', fmt(g["title"], ctx), fmt(g["desc"], ctx),
                "".join(parts), extra_head=itemlist_ld(rows, site) if rows else ""))
        # about
        urls.append("/about/")
        adir = root / "about"; adir.mkdir(exist_ok=True)
        (adir / "index.html").write_text(page(site, "/about/", f'About & method — {site["name"]}',
                                              "How this tracker gathers prices and computes price per watt-hour.", ABOUT_BODY))
        # sitemap + robots
        sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for u in urls:
            sm.append(f'<url><loc>https://{site["domain"]}{u}</loc><lastmod>{dt.strftime("%Y-%m-%d")}</lastmod></url>')
        sm.append('</urlset>')
        (root / "sitemap.xml").write_text("\n".join(sm))
        (root / "robots.txt").write_text(
            "User-agent: *\nAllow: /\n"
            "User-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\n"
            "User-agent: ChatGPT-User\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\n"
            "User-agent: PerplexityBot\nAllow: /\nUser-agent: Bingbot\nAllow: /\n"
            f"Sitemap: https://{site['domain']}/sitemap.xml\n")
        summary[site["domain"]] = {"pages": len(urls), "products": len(pool)}
        print(f'[build] {site["domain"]}: {len(urls)} pages, {len(pool)} products in pool')
    return summary

if __name__ == "__main__":
    build()

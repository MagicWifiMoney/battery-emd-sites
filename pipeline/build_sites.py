#!/usr/bin/env python3
"""
build_sites.py — render the four EMD sites from data/products.json.

Sites (each standalone, no redirects, cross-linked):
  48vlifepo4battery.com   — 48V bare + rack batteries
  12vlifepo4battery.com   — 12V bare batteries
  24vlifepo4battery.com   — 24V bare batteries
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
import json, re, html, statistics, hashlib, shutil
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
        # 24V guard: a row whose voltage comes ONLY from title text (no
        # rated voltage and no rated Ah in the feed) is not classifiable —
        # e.g. LiTime's RV conversion-kit listing, whose variants span
        # 12V/24V systems under one shared URL and whose "Wh" is a
        # kWh/day usage figure, not rated storage.
        if v and 22 <= v <= 28 and not (p.get("voltage") is None and p.get("ah") is None):
            return "24v"
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
        plink = PROD_URL.get((segment(p), p["url"]))
        if plink:
            title_cell = f'<a href="{esc(plink)}">{esc(p["title"])}</a>'
        else:
            title_cell = (f'<a href="{esc(p["url"])}" rel="nofollow sponsored noopener" '
                          f'target="_blank">{esc(p["title"])}</a>')
        trs.append(
            f'<tr data-brand="{esc(p["brand"])}">'
            f'<td data-v="{esc(p["title"])}">{title_cell}{avail}</td>'
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


# Site-verification meta tags (homepage only), keyed by domain: Impact
# affiliate network, Google Search Console, and Bing Webmaster Tools
# (the Bing msvalidate.01 code is account-wide, identical on every site).
BING_VERIFY = "<meta name='msvalidate.01' content='2FA47358EA1D4A7E3DF926ACEF53F410'>"
VERIFY_META = {
    "48vlifepo4battery.com": "<meta name='impact-site-verification' value='ec050c2d-1e9d-48e1-a271-857624705cd2'>"
        "<meta name='google-site-verification' content='tbW4-K0LffGFfy0K6yYDgyJc1MuJYpSJqktIZnji4HE'>" + BING_VERIFY,
    "12vlifepo4battery.com": "<meta name='impact-site-verification' value='09d7df7a-711d-4ada-bc8b-67df34ab4b5a'>"
        "<meta name='google-site-verification' content='TXRvIcGdrLCX9GsI012j_PXULUWzMRIMcpJZBBI_ZTE'>" + BING_VERIFY,
    "serverrackbatteries.com": "<meta name='impact-site-verification' value='63ba17d3-02ec-4189-ad44-68c1b729f522'>"
        "<meta name='google-site-verification' content='uLL1hkMpkzoAYLMgg5EKA_RplqdXOVGaw5r3fQCXyfY'>" + BING_VERIFY,
    "24vlifepo4battery.com": "<meta name='impact-site-verification' value='900cf588-76ca-4add-8122-f692fb2d1e15'>"
        "<meta name='google-site-verification' content='zMEySrHVfidP_xfgtt7h7DzB0QWHIrFbInLrlCms_Qs'>" + BING_VERIFY,
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
    ("24vlifepo4battery.com", "24V LiFePO4 Battery prices"),
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
FAQ_24V = [
    ("What is the cheapest 24V LiFePO4 battery per watt-hour?",
     "The table above is refreshed several times a day and ranked by $/Wh, so the top row is the live answer. In this category the 100Ah class (2,560Wh) usually holds the best $/Wh, while compact 50–60Ah trolling-motor packs cost more per watt-hour for their smaller, lighter cases."),
    ("Is a 24V LiFePO4 battery really 25.6V?",
     "Yes. Eight 3.2V LiFePO4 cells in series give 25.6V nominal and about 29.2V fully charged — the direct lithium replacement class for 24V lead-acid systems in boats, trucks, RVs and small solar setups."),
    ("24V native battery or two 12V batteries in series — which is better?",
     "A native 24V battery is one case, one BMS and one warranty, and it can never drift out of balance with a twin. Two 12V batteries in series give you two BMS units that must stay balanced (a battery balancer helps) but let you reuse packs you already own and split the weight. Our <a href=\"/series-vs-native-24v/\">series vs native 24V guide</a> walks through the trade-offs."),
    ("What charger does a 24V LiFePO4 battery need?",
     "A LiFePO4-profile charger set to about 29.2V absorption for a 25.6V pack, with no equalization stage. A 12V charger cannot charge a 24V battery; if you run two 12V packs in series, charge the bank with a 24V charger or charge each battery separately."),
    ("How long will a 24V 100Ah battery run a trolling motor?",
     "A 24V 100Ah pack stores 2,560Wh. A 70–80 lb-thrust 24V trolling motor draws roughly 40–55A at full throttle, so expect around 2 hours flat-out and much longer at cruising speeds — most anglers get a full day. LiFePO4 holds voltage flat through the discharge, so thrust does not fade the way it does on lead-acid."),
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
    "ah220_240": lambda rows: [p for p in rows if ah_of(p) and 220 <= ah_of(p) <= 240],
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
        "domain": "24vlifepo4battery.com", "name": "24V LiFePO4 Battery",
        "phrase": "24V LiFePO4 battery", "display": "24V LiFePO4 Battery", "pool": ["24v"], "faqs": FAQ_24V,
        "lede": "Every {phrase} from the major makers' own stores, ranked by <b>price per watt-hour</b> — the honest way to compare a compact 50Ah trolling pack against a 230Ah bank battery. {n} models tracked; cheapest stored energy is <b>${minppw}/Wh</b>, median ${medppw}/Wh. Prices refreshed {date}.",
        "clusters": [
            C("24v-100ah-lifepo4-battery", "100Ah", "24V 100Ah LiFePO4 Batteries",
              "The workhorse size: 2,560Wh for trolling motors, RVs and small solar — every 100Ah model by $/Wh.",
              "ah90_115",
              ["The 24V 100Ah battery (25.6V × 100Ah = 2,560Wh) is where 24V systems get serious: enough energy for a full day on a 24V trolling motor, a weekend of RV house loads, or a small off-grid solar bank — in one case with one BMS. Every model below stores the same 2,560Wh, so the $/Wh column is a pure price fight.",
               "What separates the rows beyond price: Bluetooth monitoring, self-heating for cold mornings on the water, low-temperature charge cut-off, and case format — the Group 31 drop-ins fit standard marine trays, the plain cases do not always. Multi-packs appear in this table at their bundle price; compare their $/Wh against the single units before assuming the bundle wins."]),
            C("24v-230ah-lifepo4-battery", "230Ah", "24V 230Ah LiFePO4 Batteries",
              "5,888Wh in one Group 8D case — the big-bank option, compared by $/Wh.",
              "ah220_240",
              ["A 24V 230Ah battery stores 5,888Wh — as much energy as a 48V 100Ah rack module — in a single Group 8D case. It is the one-box answer for trucks, larger RVs and off-grid cabins that would otherwise wire two 100Ah packs in parallel, and one BMS means nothing to balance.",
               "The trade-offs are honest ones: an 8D lithium pack is still a heavy two-hand lift, and a single battery is a single point of failure where paralleled 100Ah units degrade gracefully. The heated variants in the table add self-heating for winter use; check each row's availability, as the heated models sell out first."]),
            C("trolling-motor-batteries", "Trolling motor", "24V LiFePO4 Trolling Motor Batteries",
              "Lightweight 24V packs for 70–112 lb-thrust trolling motors, ranked by $/Wh.",
              "marine",
              ["A 24V trolling motor is the classic reason a 24V battery exists. Lithium changes the day on the water twice over: a 24V 100Ah LiFePO4 weighs roughly a third of the two lead-acids it replaces, and it holds voltage flat to empty, so the thrust you get at 90% charge is the thrust you get at 20%. The packs below are the ones makers sell for trolling and marine use, ranked by $/Wh.",
               "Size by thrust: 70–80 lb motors draw about 40–55A at full throttle (a 50–60Ah pack covers a morning; 100Ah covers a day), and 112 lb motors want the 100Ah class. Confirm the BMS continuous rating covers your motor's max draw, and prefer low-temperature protection if you fish early-season cold water."]),
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


# ---------- phase 2: product pages, facet hubs, deals ----------
# Spec: research/product-pages-spec-2026-11-21.md (verdicts binding).
HISTORY_PATH = ROOT / "data" / "price_history.json"
PROD_URL = {}   # (segment, catalog url) -> absolute product-page url.
SLUG_OF = {}    # (segment, catalog url) -> slug on its home site.
# Keyed by segment as well as URL: maker feeds emit variant rows that share
# one listing URL across voltage classes (e.g. one LiTime listing selling
# 12V and 24V variants), and each variant's canonical page lives on its own
# home site.
HOME_DOMAIN = {"rack": "serverrackbatteries.com",
               "48v": "48vlifepo4battery.com",
               "12v": "12vlifepo4battery.com",
               "24v": "24vlifepo4battery.com"}
DOMAIN_SEG = {v: k for k, v in HOME_DOMAIN.items()}
# Wave rollout: sites whose product pages / facet hubs / deals render.
PHASE2_SITES = {"serverrackbatteries.com", "12vlifepo4battery.com",
                "48vlifepo4battery.com", "24vlifepo4battery.com"}

def _has(t, *ws):
    return any(w in t for w in ws)

# Slug tokens, applied in this whitelist order (spec section 1).
TOKEN_RULES = [
    ("heated", lambda p, t: _has(t, "heated", "self-heating", "self heating", "liheat")),
    ("bluetooth", lambda p, t: "bluetooth" in t),
    ("wifi", lambda p, t: _has(t, "wifi", "wi-fi")),
    ("wall", lambda p, t: _has(t, "wall-mounted", "wall mounted", "wall-mount")),
    ("rack", lambda p, t: p["type"] == "rack-battery" or "rack" in t),
    ("trolling", lambda p, t: "trolling" in t),
    ("rv", lambda p, t: re.search(r"\brv\b", t) is not None),
    ("golf", lambda p, t: "golf" in t),
    ("marine", lambda p, t: "marine" in t),
    ("low-temp", lambda p, t: _has(t, "low-temp", "low temp")),
    ("smart", lambda p, t: "smart" in t),
    ("8d", lambda p, t: re.search(r"\b8d\b", t) is not None),
]

def class_int(p):
    v = volts(p)
    if v is None:
        return None
    for nominal, ci in ((12.8, 12), (25.6, 24), (38.4, 36), (51.2, 48)):
        if abs(v - nominal) < 1.5:
            return ci
    return int(round(v))

def brand_slug(b):
    return re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")

def descriptive_slug(p):
    a = ah_of(p)
    ci = class_int(p)
    if a is None or ci is None:
        return None
    head = [brand_slug(p["brand"]), f"{ci}v", f"{int(round(a))}ah"]
    t = p["title"].lower()
    toks = [name for name, fn in TOKEN_RULES if fn(p, t)][:3]
    while toks and len("-".join(head + toks)) > 63:
        toks.pop()
    return "-".join(head + toks)

def assign_slugs(home_pool):
    """{catalog url: slug} for one URL-deduped home pool. Colliding
    descriptive slugs get a -<sha1(url)[:6]> suffix on every member."""
    groups = {}
    for p in home_pool:
        s = descriptive_slug(p)
        if s:
            groups.setdefault(s, []).append(p)
    out = {}
    for s, rows in groups.items():
        if len(rows) == 1:
            out[rows[0]["url"]] = s
        else:
            for p in rows:
                h = hashlib.sha1(p["url"].encode()).hexdigest()[:6]
                out[p["url"]] = f"{s}-{h}"
    return out

# Price-position classes (spec section 1): home pool x Ah band.
AH_BANDS = [("60Ah and under", lambda a: a <= 60),
            ("90-115Ah", lambda a: 90 <= a <= 115),
            ("180-235Ah", lambda a: 180 <= a <= 235),
            ("280-330Ah", lambda a: 280 <= a <= 330)]

def class_context(p, home_pool):
    a = ah_of(p)
    rows, label = None, "all tracked models on this site"
    if a is not None:
        for lab, fn in AH_BANDS:
            if fn(a):
                rows = [q for q in home_pool
                        if ah_of(q) is not None and fn(ah_of(q))]
                label = lab
                break
    if not rows:
        rows = list(home_pool)
    rows = sorted(rows, key=ppw)
    rank = next(i for i, q in enumerate(rows) if q["url"] == p["url"]) + 1
    med = statistics.median(ppw(q) for q in rows)
    return {"rows": rows, "rank": rank, "n": len(rows), "label": label,
            "median": med, "cheap": rows[0]}

WH_METHOD_NOTES = {
    "v-times-ah": "Capacity computed from the maker's rated volts x amp-hours.",
    "variant-ah-x-title-v": "Capacity computed from the maker's rated volts x amp-hours for this variant.",
    "explicit-wh": "Capacity as stated in watt-hours in the maker's own listing.",
    "stated-kwh": "Capacity as stated in kilowatt-hours in the maker's own listing.",
    "body-wh-before-capacity-label": "Capacity as stated in watt-hours in the maker's own listing.",
    "explicit-wh-variant-bundle-sum": "Capacity is the sum of the bundled components' stated watt-hours in the maker's listing.",
    "body-mode-wh": "Capacity taken from the watt-hour figure the maker's listing states most consistently.",
    "override-curated": "Capacity verified against the maker's published specification for this model.",
}

def product_ld(p, site, slug):
    a = ah_of(p)
    ah_val = None
    if a is not None:
        ah_val = int(a) if float(a).is_integer() else round(a, 1)
    props = [{"@type": "PropertyValue", "name": "Capacity",
              "value": p["wh"], "unitText": "Wh"}]
    if ah_val is not None:
        props.append({"@type": "PropertyValue", "name": "Amp-hours",
                      "value": ah_val, "unitText": "Ah"})
    if volts(p) is not None:
        props.append({"@type": "PropertyValue", "name": "Nominal voltage",
                      "value": volts(p), "unitText": "V"})
    props.append({"@type": "PropertyValue", "name": "Price per watt-hour",
                  "value": ppw(p), "unitText": "USD/Wh"})
    ld = {"@context": "https://schema.org", "@type": "Product",
          "name": p["title"],
          "brand": {"@type": "Brand", "name": p["brand"]},
          "url": f"https://{site['domain']}/product/{slug}/",
          "additionalProperty": props,
          "offers": {"@type": "Offer", "url": p["url"],
                     "priceCurrency": "USD", "price": p["price"],
                     "availability": ("https://schema.org/InStock" if p.get("available", True)
                                      else "https://schema.org/OutOfStock"),
                     "seller": {"@type": "Organization",
                                "name": f"{p['brand']} (maker's store)"}}}
    return f'<script type="application/ld+json">{json.dumps(ld)}</script>'

def mini_table(rows, self_p):
    trs = []
    for q in rows:
        mark = ' <b style="color:var(--acc)">— this battery</b>' if q["url"] == self_p["url"] else ""
        link = PROD_URL.get((segment(q), q["url"]))
        name = (f'<a href="{esc(link)}">{esc(q["title"])}</a>' if link
                else esc(q["title"]))
        trs.append(f'<tr><td>{name}{mark}</td>'
                   f'<td class="num pricedata" data-v="{q["price"]}">{money(q["price"])}</td>'
                   f'<td class="num ppw pricedata" data-v="{ppw(q)}">${ppw(q):.3f}</td></tr>')
    return ('<div style="overflow-x:auto"><table><thead><tr><th>Product</th>'
            '<th class="num">Price</th><th class="num">$/Wh</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table></div>')

def capacity_link(site, pool, p, by_slug):
    """Most specific existing cluster/guide page (slug contains 'ah') whose
    table contains this product — the product's capacity-class parent."""
    cands = []
    pages = [(c["slug"], FILTERS[c["filter"]](pool)) for c in site["clusters"]]
    pages += [(g["slug"], resolve_rows(g.get("filter"), pool))
              for g in GUIDES.get(site["domain"], [])]
    for slug, rows in pages:
        if "ah" not in slug or not rows:
            continue
        if any(q["url"] == p["url"] for q in rows):
            cands.append((len(rows), slug))
    if not cands:
        return None
    cands.sort()
    return cands[0][1]

# Facet hubs (spec section 3 verdicts). Hub renders only at >=3 rows.
PRICE_BANDS = {
    "12vlifepo4battery.com": [(0, 500, "Under $500", "under-500"),
                              (500, 1000, "$500 to $1,000", "500-to-1000"),
                              (1000, None, "$1,000 and up", "over-1000")],
    "48vlifepo4battery.com": [(0, 1000, "Under $1,000", "under-1000"),
                              (1000, 2000, "$1,000 to $2,000", "1000-to-2000"),
                              (2000, None, "$2,000 and up", "over-2000")],
    "serverrackbatteries.com": [(500, 1000, "$500 to $1,000", "500-to-1000"),
                                (1000, 2000, "$1,000 to $2,000", "1000-to-2000"),
                                (2000, None, "$2,000 and up", "over-2000")],
    # 24V pool prices run $350-$2,088 (19 SKUs, 2026-11-21 pull): bands
    # split 5 / 6 / 8 rows.
    "24vlifepo4battery.com": [(0, 500, "Under $500", "under-500"),
                              (500, 1000, "$500 to $1,000", "500-to-1000"),
                              (1000, None, "$1,000 and up", "over-1000")],
}
HEATED_TEST = lambda p: title_has(p, "heated", "self-heating", "self heating", "liheat")

def plural_display(site):
    d = site["display"]
    return d[:-1] + "ies" if d.endswith("Battery") else d

def facet_hubs(site, pool):
    hubs = []
    pd = plural_display(site)
    counts = {}
    for p in pool:
        counts[p["brand"]] = counts.get(p["brand"], 0) + 1
    for b in sorted(counts):
        if counts[b] >= 3:
            hubs.append({"slug": f"brand/{brand_slug(b)}", "kind": "brand", "key": b,
                         "h1": f"{b} {pd}",
                         "blurb": f"Every {b} model in this tracker, ranked by $/Wh.",
                         "rows": sorted([p for p in pool if p["brand"] == b], key=ppw)})
    for lo, hi, label, slug in PRICE_BANDS[site["domain"]]:
        rows = sorted([p for p in pool
                       if p["price"] >= lo and (hi is None or p["price"] < hi)], key=ppw)
        if len(rows) >= 3:
            hubs.append({"slug": slug, "kind": "price", "key": label,
                         "h1": f"{pd} — {label}",
                         "blurb": f"Tracked models priced {label.lower()}, ranked by $/Wh.",
                         "rows": rows})
    rows = sorted(FILTERS["ah5_60"](pool), key=ppw)
    if len(rows) >= 3:
        hubs.append({"slug": "compact-batteries", "kind": "capacity", "key": "5-60Ah",
                     "h1": f"Compact {pd} (5-60Ah)",
                     "blurb": "Small 5-60Ah packs for portable and space-tight jobs, ranked by $/Wh.",
                     "rows": rows})
    rows = sorted([p for p in pool if HEATED_TEST(p)], key=ppw)
    if len(rows) >= 3:
        hubs.append({"slug": "heated-batteries", "kind": "heated", "key": "heated",
                     "h1": f"Heated {pd}",
                     "blurb": "Models whose maker listing names self-heating, ranked by $/Wh.",
                     "rows": rows})
    rows = sorted([p for p in pool if title_has(p, "bluetooth")], key=ppw)
    if len(rows) >= 3:
        hubs.append({"slug": "bluetooth-batteries", "kind": "bluetooth", "key": "bluetooth",
                     "h1": f"{pd} with Bluetooth",
                     "blurb": "Models whose maker listing names Bluetooth monitoring, ranked by $/Wh.",
                     "rows": rows})
    if site["domain"] == "12vlifepo4battery.com":
        rows = sorted([p for p in pool if title_has(p, "group")], key=ppw)
        if len(rows) >= 4:
            hubs.append({"slug": "group-size-batteries", "kind": "group", "key": "group",
                         "h1": "12V LiFePO4 Batteries by Group Size",
                         "blurb": "Drop-in group-size cases (Group 24, 27, 31, 8D and similar), ranked by $/Wh.",
                         "rows": rows})
    return hubs

def hub_prose(site, hub):
    rows = hub["rows"]
    n = len(rows)
    cheap = rows[0]
    ppws = [ppw(p) for p in rows]
    med = statistics.median(ppws)
    if hub["kind"] == "brand":
        return (f"<p>{esc(hub['key'])} lists {n} models in this tracker's {esc(site['phrase'])} pool, "
                f"from {money(min(p['price'] for p in rows))} to {money(max(p['price'] for p in rows))}. "
                f"The cheapest {esc(hub['key'])} stored energy right now is the {esc(cheap['title'])} "
                f"at ${ppw(cheap):.3f}/Wh; the brand's median is ${med:.3f}/Wh. "
                f"Every model below is ranked by $/Wh, the same order as the main table — "
                f"no placement is paid for.</p>")
    if hub["kind"] == "price":
        medwh = statistics.median(p["wh"] for p in rows)
        return (f"<p>{n} tracked models are priced {esc(hub['key'].lower())} right now. In this band the "
                f"median battery stores {medwh:,.0f}Wh and the cheapest stored energy is "
                f"${min(ppws):.3f}/Wh ({esc(cheap['brand'])}); the band median is ${med:.3f}/Wh. "
                f"A lower sticker in this band is not automatically better value — the $/Wh column "
                f"is the comparison that matters.</p>")
    if hub["kind"] == "capacity":
        return (f"<p>Compact 5-60Ah packs trade a higher $/Wh for portability: trolling motors, fish "
                f"finders, portable power and tight battery boxes. {n} models are tracked here; the "
                f"cheapest stored energy is ${min(ppws):.3f}/Wh ({esc(cheap['brand'])}), the median "
                f"${med:.3f}/Wh. If your space allows a bigger case, the 100Ah class on the main table "
                f"usually stores energy for less.</p>")
    if hub["kind"] == "heated":
        return (f"<p>This hub is built from listing titles: it collects the {n} models whose maker "
                f"listing names self-heating (\"heated\", \"self-heating\" or \"LiHeat\" in the title). "
                f"Low-temperature charge protection — a cutoff that blocks charging below freezing, "
                f"not a heater — does not count here. We have not tested any heating function; the "
                f"maker's own page (linked from each row) describes how each model implements it.</p>")
    if hub["kind"] == "bluetooth":
        return (f"<p>This hub is built from listing titles: it collects the {n} models whose maker "
                f"listing names Bluetooth monitoring. State-of-charge guessing is the top complaint "
                f"with budget packs, so an app-readable BMS is a real feature — but we have not tested "
                f"any of these apps; check the maker's page for what its monitoring actually shows.</p>")
    if hub["kind"] == "group":
        return (f"<p>Group-size cases are built to drop into an existing lead-acid battery tray or box "
                f"(Group 24, 27, 31, 8D and similar). This hub is built from listing titles — the "
                f"{n} models whose maker listing names a group size — ranked by $/Wh. Measure your "
                f"tray before ordering; group sizes are close but not identical across brands.</p>")
    return ""

def facet_cards(hubs):
    if not hubs:
        return ""
    lis = "".join(f'<li><a href="/{h["slug"]}/">{esc(h["h1"])}</a><p>{esc(h["blurb"])}</p></li>'
                  for h in hubs)
    return f'<h2>Browse by brand, size &amp; price</h2><ul class="links">{lis}</ul>'

# Deals (spec section 4): launch gate >=24 snapshots spanning >=7 days.
def _parse_ts(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def load_snapshots():
    try:
        h = json.loads(HISTORY_PATH.read_text())
        snaps = [s for s in h.get("snapshots", []) if s.get("ts") and s.get("prices")]
        return sorted(snaps, key=lambda s: s["ts"])
    except Exception:
        return []

def deals_info(pool):
    """(gate_open, baseline_snapshot, drops, snapshots). Baseline = oldest
    snapshot at least 6 days older than the newest one."""
    snaps = load_snapshots()
    if not snaps:
        return False, None, [], snaps
    from datetime import timedelta
    latest = _parse_ts(snaps[-1]["ts"])
    span_days = (latest - _parse_ts(snaps[0]["ts"])).total_seconds() / 86400
    if len(snaps) < 24 or span_days < 7:
        return False, None, [], snaps
    cutoff = latest - timedelta(days=6)
    eligible = [s for s in snaps if _parse_ts(s["ts"]) <= cutoff]
    if not eligible:
        return False, None, [], snaps
    base = eligible[0]
    drops = []
    for p in pool:
        old = base["prices"].get(p["url"])
        if old and p.get("available", True):
            drop = old - p["price"]
            if drop >= 25 and drop >= 0.05 * old:
                drops.append({"p": p, "old": old, "drop": drop,
                              "pct": drop / old * 100,
                              "old_ppw": old / p["wh"]})
    drops.sort(key=lambda d: -d["pct"])
    return True, base, drops, snaps

def deals_body(site, pool, fetched, date_str):
    gate, base, drops, snaps = deals_info(pool)
    if not gate:
        if snaps:
            from datetime import timedelta as _td
            first = _parse_ts(snaps[0]["ts"])
            last = _parse_ts(snaps[-1]["ts"])
            span = (last - first).total_seconds() / 86400
            status = (f"Price tracking began {first.strftime('%B %d, %Y')}. So far "
                      f"{len(snaps)} snapshot{'s' if len(snaps) != 1 else ''} "
                      f"span {span:.1f} days.")
            eta = (first + _td(days=7)).strftime("%B %d, %Y")
        else:
            status = "Price tracking has just been switched on; no snapshots exist yet."
            eta = "about a week after tracking starts"
        body = (f'<h1>{esc(site["display"])} Price Drops — Tracker warming up</h1>'
                f'<p class="lede">This page will rank the biggest price drops in the makers\' own '
                f'stores over a rolling ~7-day window, by percentage and by $/Wh. It publishes its '
                f'first edition once at least 7 days and 24 snapshots of price history exist — '
                f'we would rather show no drops than invent them.</p>'
                + DISCLOSURE.format(ts=fetched, date=date_str)
                + f'<div class="prose"><p>{esc(status)}</p>'
                f'<h2>How drops will be measured</h2>'
                f'<p>Each refresh of this tracker stores a price snapshot. A model qualifies for '
                f'this page when the same listing is available now and its price has fallen at least '
                f'5% and at least $25 against the oldest snapshot at least 6 days old. Rankings are '
                f'by percentage drop; the table will show the old and new prices and the $/Wh then '
                f'and now, with the snapshot dates. A few hand-tracked models (for example Vatrer) '
                f'have no snapshot history and will never appear here.</p>'
                f'<p>Until the first edition lands (expected around {esc(eta)} plus a few days), the '
                f'<a href="/">live price table</a> is the current picture.</p></div>')
        return body, False
    base_date = _parse_ts(base["ts"]).strftime("%B %d, %Y")
    if drops:
        trs = []
        for d in drops:
            p = d["p"]
            link = PROD_URL.get((segment(p), p["url"]))
            name = (f'<a href="{esc(link)}">{esc(p["title"])}</a>' if link else esc(p["title"]))
            trs.append(f'<tr><td>{name}</td>'
                       f'<td class="num pricedata">{money(d["old"])}</td>'
                       f'<td class="num pricedata">{money(p["price"])}</td>'
                       f'<td class="num pricedata">${d["old_ppw"]:.3f}</td>'
                       f'<td class="num ppw pricedata">${ppw(p):.3f}</td>'
                       f'<td class="num pricedata">-{d["pct"]:.0f}%</td></tr>')
        table = ('<div style="overflow-x:auto"><table><thead><tr><th>Product</th>'
                 '<th class="num">Price then</th><th class="num">Price now</th>'
                 '<th class="num">$/Wh then</th><th class="num">$/Wh now</th>'
                 '<th class="num">Drop</th></tr></thead>'
                 f'<tbody>{"".join(trs)}</tbody></table></div>')
    else:
        table = ('<p>No tracked model currently qualifies — no listing in this pool has fallen '
                 '5% and $25 or more against the baseline snapshot. That is a result too: '
                 'prices in this category are holding.</p>')
    body = (f'<h1>{esc(site["display"])} Price Drops — Biggest Falls in $/Wh</h1>'
            f'<p class="lede">The biggest price drops in the makers\' own stores since '
            f'{esc(base_date)}, ranked by percentage. A model qualifies at a drop of at least 5% '
            f'and $25, still listed as available. Prices refreshed {esc(date_str)}.</p>'
            + DISCLOSURE.format(ts=fetched, date=date_str)
            + table
            + '<div class="prose"><h2>Method</h2>'
              '<p>Drops are measured against the oldest price snapshot at least 6 days old — the '
              'maker\'s own store price then versus now. A struck-through "was" price elsewhere on '
              'this site is the maker\'s list price, a different thing; this page only reports '
              'actual price movement we recorded. A few hand-tracked models (for example Vatrer) '
              'have no snapshot history and never appear here.</p></div>')
    return body, True


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
    pools = {"48v": [], "12v": [], "rack": [], "24v": []}
    for p in prods:
        s = segment(p)
        if s in pools:
            pools[s].append(p)
    for k in pools:
        pools[k].sort(key=ppw)

    # Phase 2: home pools, URL-deduped with the same dict semantics as the
    # site pools below (so a product page shows the same row its tables do),
    # plus slug assignment for the enabled waves.
    home_pools = {}
    for seg, dom in HOME_DOMAIN.items():
        hp = sorted({p["url"]: p for p in pools[seg]}.values(), key=ppw)
        home_pools[seg] = hp
        if dom in PHASE2_SITES:
            for url, slug in assign_slugs(hp).items():
                SLUG_OF[(seg, url)] = slug
                PROD_URL[(seg, url)] = f"https://{dom}/product/{slug}/"

    summary = {}
    for site in SITES:
        pool = []
        for key in site["pool"]:
            pool.extend(pools[key])
        pool = sorted({p["url"]: p for p in pool}.values(), key=ppw)
        p2 = site["domain"] in PHASE2_SITES
        hubs = facet_hubs(site, pool) if p2 else []
        dgate = deals_info(pool)[0] if p2 else False
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
                + facet_cards(hubs)
                + ('<h2>Price drops</h2><ul class="links"><li><a href="/deals/">Biggest price drops this week</a>'
                   '<p>Models down at least 5% and $25 against the baseline snapshot, ranked by drop.</p></li></ul>'
                   if dgate else "")
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
        # phase 2: clear the dynamic page trees so products/hubs that left
        # the catalog lose their pages on this build (spec section 2).
        if p2:
            shutil.rmtree(root / "product", ignore_errors=True)
            shutil.rmtree(root / "brand", ignore_errors=True)
        # phase 2: facet hubs
        for h in hubs:
            urls.append(f'/{h["slug"]}/')
            rows = h["rows"]
            ppws_h = [ppw(p) for p in rows]
            lede_h = (f'{esc(h["blurb"])} {len(rows)} models tracked — cheapest stored energy '
                      f'<b>${min(ppws_h):.3f}/Wh</b>, median ${statistics.median(ppws_h):.3f}/Wh. '
                      f'Prices refreshed {date_str}.')
            sib = [o for o in hubs if o["slug"] != h["slug"]][:4]
            sib_html = "".join(f'<li><a href="/{o["slug"]}/">{esc(o["h1"])}</a><p>{esc(o["blurb"])}</p></li>' for o in sib)
            hbody = (f'<h1>{esc(h["h1"])}</h1>'
                     f'<p class="lede">{lede_h}</p>'
                     + DISCLOSURE.format(ts=fetched, date=date_str)
                     + stats_html(rows)
                     + f'<h2>Prices, ranked by $/Wh</h2>' + table_html(rows)
                     + f'<div class="prose">{hub_prose(site, h)}</div>'
                     + f'<h2>Keep comparing</h2><ul class="links"><li><a href="/">All {esc(site["phrase"])} prices</a><p>The full live table, every model ranked by $/Wh.</p></li>{sib_html}</ul>'
                     + faq_html(site["faqs"][:3]))
            hd = root
            for part in h["slug"].split("/"):
                hd = hd / part
            hd.mkdir(parents=True, exist_ok=True)
            (hd / "index.html").write_text(page(
                site, f'/{h["slug"]}/', f'{h["h1"]} — Prices by $/Wh',
                f'{h["blurb"]} Prices from the makers\' own stores, refreshed {date_str}.',
                hbody, extra_head=itemlist_ld(rows, site)))
        # phase 2: product pages (home site only — one canonical page each)
        if p2:
            hp = home_pools[DOMAIN_SEG[site["domain"]]]
            by_slug_all = {c["slug"]: c for c in site["clusters"]}
            for g in GUIDES.get(site["domain"], []):
                by_slug_all[g["slug"]] = g
            for p in hp:
                slug = SLUG_OF.get((DOMAIN_SEG[site["domain"]], p["url"]))
                if not slug:
                    continue
                urls.append(f"/product/{slug}/")
                cc = class_context(p, hp)
                rows_c, rank, med = cc["rows"], cc["rank"], cc["median"]
                myppw = ppw(p)
                if rank == 1:
                    pos = (f"It ranks #1 of {cc['n']} in the {cc['label']} class by price per "
                           f"watt-hour — the cheapest stored energy in its class right now.")
                elif myppw <= med:
                    pos = (f"It ranks #{rank} of {cc['n']} in the {cc['label']} class by $/Wh, "
                           f"below the class median of ${med:.3f}/Wh.")
                else:
                    pos = (f"It ranks #{rank} of {cc['n']} in the {cc['label']} class by $/Wh; "
                           f"the class median is ${med:.3f}/Wh, so on price per watt-hour this "
                           f"is a premium pick in its class.")
                lede_p = (f"This {esc(cap_label(p))} LiFePO4 battery from {esc(p['brand'])} is "
                          f"listed at {money(p['price'])} in the maker's own store — "
                          f"${myppw:.3f}/Wh (${myppw*1000:,.0f}/kWh). {pos} "
                          f"Prices refreshed {date_str}.")
                pct = (myppw - med) / med * 100 if med else 0
                if rank == 1:
                    rankline = (f"<p>Cheapest in its class: this model itself. The class median is "
                                f"${med:.3f}/Wh — {abs(pct):.0f}% above this model's $/Wh.</p>")
                else:
                    cheap = cc["cheap"]
                    rankline = (f"<p>Cheapest in class: <a href=\"{esc(PROD_URL.get((segment(cheap), cheap['url']), cheap['url']))}\">"
                                f"{esc(cheap['title'])}</a> at ${ppw(cheap):.3f}/Wh ({money(cheap['price'])}). "
                                f"This model sits {abs(pct):.0f}% {'below' if pct < 0 else 'above'} "
                                f"the class median of ${med:.3f}/Wh.</p>")
                lo = max(0, rank - 4)
                hi = min(len(rows_c), rank + 3)
                rel = [f'<li><a href="/">All {esc(site["phrase"])} prices</a><p>The full live table, every model ranked by $/Wh.</p></li>']
                cap_slug = capacity_link(site, pool, p, by_slug_all)
                if cap_slug and cap_slug in by_slug_all:
                    o = by_slug_all[cap_slug]
                    rel.append(f'<li><a href="/{cap_slug}/">{esc(o["h1"])}</a><p>{esc(o["blurb"])}</p></li>')
                for h in hubs:
                    if any(q["url"] == p["url"] for q in h["rows"]):
                        rel.append(f'<li><a href="/{h["slug"]}/">{esc(h["h1"])}</a><p>{esc(h["blurb"])}</p></li>')
                avail_txt = ("Listed as available at the maker's store." if p.get("available", True)
                             else "Not currently listed as available at the maker's store — check the maker's page for stock.")
                note = WH_METHOD_NOTES.get(p.get("wh_method"),
                                           "Capacity from the maker's own listing.")
                store_host = re.sub(r"^https?://", "", p.get("source_store", "")).rstrip("/")
                v = volts(p)
                cap_detail = f"{p['wh']:,.0f}Wh" + (f" at {v}V nominal" if v else "")
                pbody = (f'<h1>{esc(p["title"])}</h1>'
                         f'<p class="lede">{lede_p}</p>'
                         + DISCLOSURE.format(ts=fetched, date=date_str)
                         + '<div class="stats">'
                         + f'<div class="stat"><b class="pricedata">{money(p["price"])}</b><span>price at the maker\'s store</span></div>'
                         + f'<div class="stat"><b class="pricedata">${myppw:.3f}/Wh</b><span>price per watt-hour</span></div>'
                         + f'<div class="stat"><b class="pricedata">${myppw*1000:,.0f}/kWh</b><span>price per kilowatt-hour</span></div>'
                         + f'<div class="stat"><b>{esc(cap_label(p))}</b><span>rated capacity</span></div></div>'
                         + (f'<p class="pricedata">Maker\'s list price: <span class="was">{money(p["compare_at"])}</span> — a struck-through price appears only when the maker\'s own store lists one.</p>'
                            if p.get("compare_at") and p["compare_at"] > p["price"] else "")
                         + f'<p><a class="buy" href="{esc(p["url"])}" rel="nofollow sponsored noopener" target="_blank">View at {esc(p["brand"])}\'s store</a></p>'
                         + f'<h2>Where it ranks in its class</h2>{rankline}'
                         + mini_table(rows_c[lo:hi], p)
                         + '<h2>Details from the maker\'s listing</h2><div class="prose">'
                         + f'<p><b>Capacity:</b> {esc(cap_label(p))} ({cap_detail}). {esc(note)}</p>'
                         + f'<p><b>Availability:</b> {avail_txt}</p>'
                         + f'<p><b>Seller:</b> {esc(p["brand"])}\'s own store ({esc(store_host)}). The buy link above goes to the maker\'s product page.</p></div>'
                         + f'<h2>Keep comparing</h2><ul class="links">{"".join(rel)}</ul>'
                         + faq_html(site["faqs"][:2]))
                pd = root / "product" / slug
                pd.mkdir(parents=True, exist_ok=True)
                (pd / "index.html").write_text(page(
                    site, f"/product/{slug}/", f'{p["title"]} — Price & $/Wh',
                    f'{p["title"]}: {money(p["price"])} at the maker\'s store, ${myppw:.3f}/Wh for {cap_label(p)}. Ranked #{rank} of {cc["n"]} in its class by $/Wh, refreshed {date_str}.',
                    pbody, extra_head=product_ld(p, site, slug)))
        # phase 2: deals page — rendered in tracking state until the
        # history gate passes; joins the sitemap only once it is live.
        if p2:
            dbody, dopen = deals_body(site, pool, fetched, date_str)
            dd = root / "deals"
            dd.mkdir(exist_ok=True)
            (dd / "index.html").write_text(page(
                site, "/deals/", f'{site["display"]} Price Drops — Biggest $/Wh Falls',
                f'The biggest recorded price drops on {site["phrase"]} models in the makers\' own stores, ranked by percentage and $/Wh.',
                dbody))
            if dopen:
                urls.append("/deals/")
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
        # Google Search Console HTML-file verification (account-level token,
        # same file on every site; the meta-tag method in VERIFY_META is the
        # backup). Must stay in place to remain verified.
        (root / "google389f2fc75ee6ba5c.html").write_text(
            "google-site-verification: google389f2fc75ee6ba5c.html")
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

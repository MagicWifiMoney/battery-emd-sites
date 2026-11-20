#!/usr/bin/env python3
"""
build_site.py — render dist/index.html from data/products.json.

Single self-contained static page: no CDN, no external assets, inline CSS/JS.
Stage A compliance wiring:
  * Maker-store prices only (no numeric Amazon prices anywhere).
  * "Check price on Amazon" = plain Amazon search link, NO affiliate tag.
  * Header shows the fetched_at timestamp next to the prices.
  * FRESHNESS GUARD: if fetched_at is older than 48h when a visitor loads
    the page, client JS hides every numeric price / $/Wh and shows
    "Check price" instead, plus a stale-data banner.
Affiliate swap point: affiliateUrl() in the page JS — today it returns the
plain maker product URL; after Awin/Impact approval it is the ONE place
where network deep-links get generated.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "products.json"
OUT = ROOT / "dist" / "index.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Battery $/Wh — LiFePO4 &amp; Power Station Prices per Watt-Hour (Prototype)</title>
<meta name="description" content="Compare LiFePO4 batteries, server-rack batteries and portable power stations by price per watt-hour, using prices from the makers' own stores.">
<style>
  :root{--ink:#16202a;--mut:#5b6b7a;--line:#d9e1e8;--acc:#0b6e4f;--bg:#f7f9fa;--warn:#8a5a00;--warnbg:#fff4d6}
  *{box-sizing:border-box}
  body{margin:0;font:15px/1.45 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:#fff}
  header{padding:22px 16px 10px;max-width:1180px;margin:0 auto}
  h1{font-size:26px;margin:0 0 4px}
  .sub{color:var(--mut);margin:0 0 8px}
  .updated{font-size:13px;color:var(--mut)}
  .disclosure{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px;max-width:1180px;margin:10px auto}
  #stale{display:none;background:var(--warnbg);color:var(--warn);border:1px solid #ecd28f;border-radius:8px;padding:10px 12px;font-size:14px;max-width:1180px;margin:10px auto}
  .wrap{max-width:1180px;margin:0 auto;padding:0 16px 30px}
  .controls{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
  .controls input,.controls select{padding:8px 10px;border:1px solid var(--line);border-radius:6px;font-size:14px}
  .controls input{flex:1;min-width:200px}
  .stats{font-size:13px;color:var(--mut);margin:6px 0 10px}
  table{width:100%;border-collapse:collapse;font-size:14px}
  th,td{padding:8px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
  th{cursor:pointer;user-select:none;background:var(--bg);position:sticky;top:0;white-space:nowrap}
  th:hover{color:var(--acc)}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
  .ppw{font-weight:700;color:var(--acc)}
  .was{color:var(--mut);text-decoration:line-through;font-size:12px}
  .oos{color:#b03a2e;font-size:12px}
  .in{color:var(--acc);font-size:12px}
  a.buy{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:13px;white-space:nowrap}
  a.amz{display:inline-block;border:1px solid var(--line);color:var(--ink);text-decoration:none;padding:5px 9px;border-radius:6px;font-size:12px;margin-top:4px;white-space:nowrap}
  footer{max-width:1180px;margin:0 auto;padding:14px 16px 34px;color:var(--mut);font-size:13px;border-top:1px solid var(--line)}
  @media(max-width:760px){table{font-size:13px} th,td{padding:6px 5px} h1{font-size:21px}}
</style>
</head>
<body>
<header>
  <h1>Battery Prices per Watt-Hour</h1>
  <p class="sub">LiFePO4 batteries, server-rack batteries and portable power stations, sorted by $/Wh — the diskprices model, for stored energy.</p>
  <p class="updated">Prices updated <strong id="fetched">__FETCHED_AT__</strong> · __COUNT__ products from the makers' own stores</p>
</header>
<div class="disclosure">Prices come from the makers' own stores and change often — the price at the store when you buy is the price that applies. <strong>As an Amazon Associate I earn from qualifying purchases.</strong> Amazon prices are not shown here; use the “Check price on Amazon” button to see today's Amazon price.</div>
<div id="stale">These prices are more than 48 hours old, so numeric prices are hidden. Use the store buttons to see current prices.</div>
<div class="wrap">
  <div class="controls">
    <input id="q" type="search" placeholder="Search products, e.g. 100Ah, DELTA, server rack…">
    <select id="ftype"><option value="">All types</option><option value="station">Power stations</option><option value="bare-battery">Bare batteries</option><option value="rack-battery">Server-rack batteries</option><option value="expansion">Expansion batteries</option></select>
    <select id="fbrand"><option value="">All brands</option></select>
    <select id="unit"><option value="wh">$/Wh</option><option value="kwh">$/kWh</option></select>
    <select id="favail"><option value="">Any availability</option><option value="1">In stock only</option></select>
  </div>
  <p class="stats" id="stats"></p>
  <table id="t">
    <thead><tr>
      <th data-k="title">Product</th><th data-k="brand">Brand</th><th data-k="type">Type</th>
      <th class="num" data-k="wh">Wh</th><th class="num" data-k="price">Price</th>
      <th class="num" data-k="price_per_wh" id="ppwhead">$/Wh</th>
      <th>Availability</th><th>Buy</th>
    </tr></thead>
    <tbody id="rows"></tbody>
  </table>
</div>
<footer>
  Pre-launch prototype — no domain yet, not a live store. Prices are a snapshot from maker stores (see update time above) and are hidden automatically when the snapshot is more than 48 hours old. Capacity is the maker's stated watt-hours, or nominal LiFePO4 voltage × amp-hours (12V class = 12.8V, 24V = 25.6V, 48V = 51.2V) where a maker only states Ah.
</footer>
<script>
const DATA = __DATA_JSON__;
const FETCHED_AT = "__FETCHED_AT__";
/* AFFILIATE_URL_PLACEHOLDER: today this returns the plain maker product URL.
   After Awin/Impact approval, generate the network deep link HERE (one place
   only), e.g. return "https://www.awin1.com/awclick.php?...&ued=" + encodeURIComponent(p.url); */
function affiliateUrl(p){ return p.url; }
function amazonSearchUrl(p){ return "https://www.amazon.com/s?k=" + encodeURIComponent(p.brand + " " + p.title); }
const stale = (Date.now() - new Date(FETCHED_AT).getTime()) > 48*3600*1000;
if (stale) document.getElementById('stale').style.display = 'block';
let sortK = 'price_per_wh', sortDir = 1, unit = 'wh';
const brands = [...new Set(DATA.map(p=>p.brand))].sort();
const fb = document.getElementById('fbrand');
brands.forEach(b=>{ const o=document.createElement('option'); o.value=b; o.textContent=b; fb.appendChild(o); });
function money(n){ return "$" + n.toLocaleString('en-US',{minimumFractionDigits:2, maximumFractionDigits:2}); }
function render(){
  const q = document.getElementById('q').value.toLowerCase();
  const ft = document.getElementById('ftype').value;
  const fbr = fb.value;
  const fa = document.getElementById('favail').value;
  document.getElementById('ppwhead').textContent = unit==='wh' ? '$/Wh' : '$/kWh';
  let rows = DATA.filter(p =>
    (!q || (p.title+' '+p.brand+' '+p.type).toLowerCase().includes(q)) &&
    (!ft || p.type===ft) && (!fbr || p.brand===fbr) && (!fa || p.available));
  rows.sort((a,b)=>{ const x=a[sortK], y=b[sortK];
    return (typeof x==='string' ? x.localeCompare(y) : x-y) * sortDir; });
  document.getElementById('stats').textContent = rows.length + " of " + DATA.length + " products shown" + (stale ? " · prices hidden (stale snapshot)" : "");
  document.getElementById('rows').innerHTML = rows.map(p=>{
    const pp = unit==='wh' ? "$"+p.price_per_wh.toFixed(3) : "$"+(p.price_per_wh*1000).toFixed(0);
    const priceCell = stale ? "Check price" :
      money(p.price) + (p.compare_at && p.compare_at>p.price ? ' <span class="was">'+money(p.compare_at)+'</span>' : '');
    const ppwCell = stale ? "—" : pp;
    return "<tr><td>"+p.title+"</td><td>"+p.brand+"</td><td>"+p.type+"</td>"+
      "<td class='num'>"+p.wh.toLocaleString()+"</td>"+
      "<td class='num'>"+priceCell+"</td>"+
      "<td class='num ppw'>"+ppwCell+"</td>"+
      "<td>"+(p.available ? "<span class='in'>In stock</span>" : "<span class='oos'>Out of stock</span>")+"</td>"+
      "<td><a class='buy' href='"+affiliateUrl(p)+"' rel='nofollow sponsored' target='_blank'>Buy at "+p.brand+"</a><br>"+
      "<a class='amz' href='"+amazonSearchUrl(p)+"' rel='nofollow sponsored' target='_blank'>Check price on Amazon</a></td></tr>";
  }).join('');
}
document.querySelectorAll('th[data-k]').forEach(th=> th.addEventListener('click', ()=>{
  const k = th.dataset.k; if (sortK===k) sortDir*=-1; else { sortK=k; sortDir=1; } render();
}));
['q','ftype','fbrand','favail'].forEach(id=> document.getElementById(id).addEventListener('input', render));
document.getElementById('unit').addEventListener('change', e=>{ unit=e.target.value; render(); });
render();
</script>
</body>
</html>
"""


def main():
    data = json.loads(DATA.read_text())
    products = data["products"]
    fetched = data["fetched_at"]
    html = (TEMPLATE
            .replace("__FETCHED_AT__", fetched)
            .replace("__COUNT__", str(len(products)))
            .replace("__DATA_JSON__", json.dumps(products)))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print(f"[built] {OUT} ({len(html)} bytes, {len(products)} products, fetched_at={fetched})")


if __name__ == "__main__":
    main()

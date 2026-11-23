# Battery EMD Sites — $/Wh LiFePO4 Price Comparison (LIVE)

**Status: LIVE since 2026-11-20/21.** This repo builds and operates four
live exact-match comparison sites. It is no longer a pre-launch pipeline —
the Stage A document further down is the 2026-11-19 pre-launch plan the
sites grew from, kept as history.

| Site | Focus | Vercel project |
|---|---|---|
| https://48vlifepo4battery.com | 48V LiFePO4 (flagship) | `48vlifepo4battery` |
| https://12vlifepo4battery.com | 12V LiFePO4 | `12vlifepo4battery` |
| https://serverrackbatteries.com | Server-rack batteries | `serverrackbatteries` |
| https://24vlifepo4battery.com | 24V LiFePO4 (added 2026-11-21) | `24vlifepo4battery` |

- **Layout:** one folder per site under `sites/<domain>/`; the pipeline
  (`pipeline/fetch_prices.py` → `pipeline/build_sites.py`) polls maker
  Shopify stores, computes $/Wh, and renders every site from
  `data/products.json`.
- **Deploy:** each Vercel project above is git-connected to this repo;
  pushing to `main` deploys. A GitHub Actions workflow also refreshes
  prices on a schedule and commits the new snapshot back (runs at $0
  inside the free Actions allowance).
- **Programs:** affiliate/discovery programs (Impact, Awin, Directory.stack,
  GSC/Bing) are documented in [PROGRAMS.md](PROGRAMS.md); the detailed
  application log is [AFFILIATE-APPLICATIONS.md](AFFILIATE-APPLICATIONS.md).

---

# History — Stage A pre-launch pipeline (2026-11-19, superseded)

_The document below is the original Stage A plan, written before any domain
was bought. Its "pre-launch, NO domain, no deployment" framing no longer
applies; it is preserved unchanged as the record of how the sites were
built._

# Stage A Pipeline — $/Wh Battery Comparison Site (pre-launch, NO domain)

A local, runnable pipeline that polls maker stores' own prices, computes
price-per-watt-hour for LiFePO4 batteries and portable power stations, and
renders a diskprices-style static comparison page. Built 2026-11-19 from the
research in `../research/` (self-sustaining-plan + price-data-stack).
**No domain, no deployment, no signups, no spend** — this folder is ready to
drop into a GitHub repo when Jay says go (domain/launch is the LAST step).

## Architecture

```
config/stores.json            which maker stores to poll (endpoint-tested)
config/capacity_overrides.json curated Wh for models whose catalog omits it
pipeline/fetch_prices.py      Shopify /products.json -> data/products.json
pipeline/build_site.py        data/products.json -> dist/index.html
data/products.json            latest snapshot (committed by the workflow)
data/fetch_log.json           per-store counts / skips / errors per run
dist/index.html               single self-contained page (no CDN, no assets)
.github/workflows/refresh.yml cron 17 past 03/09/15/21 UTC: fetch + build +
                              commit snapshot back (deploy step commented out)
```

Data flow: maker Shopify catalog → relevance filter → capacity (Wh)
extraction → sanity guards → $/Wh → static page with client-side
search/filter/sort, a 48-hour freshness guard, and Stage A compliance
(maker prices only; Amazon appears only as a no-price "Check price on
Amazon" search button with **no affiliate tag**).

## Run it locally

```bash
cd stage-a
python3 pipeline/fetch_prices.py   # writes data/products.json + fetch_log.json
python3 pipeline/build_site.py     # writes dist/index.html
# open dist/index.html in any browser
```

Python 3 stdlib only — no pip installs, no dependencies.

## Store endpoint test results (one low-volume GET each, 2026-11-19)

| Store | /products.json | Result |
|---|---|---|
| EcoFlow — ecoflow.com | ✅ works | 200 JSON, 250/page, paginated (319 raw). us.ecoflow.com returns byte-identical data — disabled as duplicate. |
| Jackery — jackery.com | ✅ works | 200 JSON, 200 products total. |
| LiTime — litime.com | ✅ works | 200 JSON, 250/page, paginated (252 raw). |
| Eco-Worthy — eco-worthy.com | ✅ works | 200 JSON, 53 products total. |
| Renogy — renogy.com | ✅ works | 200 JSON, 250/page, paginated (276 raw). Broad catalog — strict relevance filter required. |
| BLUETTI — bluettipower.com | ✅ works via shop domain | Main domain is a Hydrogen storefront (HTML, no JSON), but its Shopify shop domain **checkout.bluettipower.com** serves real `/products.json` (436 raw) — discovered 2026-11-19 via a Firecrawl scrape (page CDN host) and verified by direct JSON test. Fetcher polls the checkout domain (`base_url`); product links use `display_base_url` (main domain), a fetcher option added for this store. |
| Anker SOLIX — ankersolix.com / anker.com | ❌ 404 | Not exposed; page prices are JS-loaded and local Firecrawl (no JS rendering on this VM) could not extract a trustworthy price either. Fallback: Impact/Awin/Rakuten catalog feed. |

## Latest run (2026-11-20T03:11Z, verified by inspection)

- **447 products**: EcoFlow 66, BLUETTI 164, Jackery 59, LiTime 100, Eco-Worthy 12, Renogy 58
- BLUETTI shape: 141 stations (their catalog is kit-heavy — station+battery/solar
  kits are kept by design, with bundle Wh summed, same as EcoFlow/Jackery kits),
  20 expansion, 3 bare batteries (their B-series). BLUETTI median $0.683/Wh.
  87 BLUETTI products skipped as unparsed (complex bundle titles, logged).
- Cross-check: BLUETTI AC180 feed price $549 / 1,152Wh = $0.477/Wh matches the
  $549 found independently by Firecrawl page scrape the same evening.
- By type (all stores, previous run): 168 bare batteries, 101 power stations, 12 expansion batteries, 2 server-rack batteries
- Median $/Wh: bare **$0.267**, rack **$0.192**, expansion **$0.452**, stations **$0.618**
- Cheapest overall: Eco-Worthy 12V 314Ah at $449 / 4,019Wh = **$0.112/Wh**
- Skipped as irrelevant: 669 (panels, chargers, apparel, accessories, AGM/lead-acid, bundles)
- Skipped as unparsed (no trustworthy capacity): 30 — every one logged with
  samples in `data/fetch_log.json`
- $/Wh math spot-checked by hand on 15 rows (top + random): **15/15 exact**

## How capacity (Wh) is derived

Priority: explicit Wh in title → variant-Ah × title-voltage (LiFePO4 nominal:
12V class = 12.8V, 24V = 25.6V, 48V = 51.2V) → title V×Ah → body-copy
signals (labelled values / most-mentioned value, expansion totals filtered)
→ curated overrides (`config/capacity_overrides.json`, flagged
`wh_method: "override-curated"` in the output). Sanity guards drop Wh
outside 50–20,000, price outside $20–$15,000, $/Wh outside 0.05–3.00.
Every row carries its `wh_method` so any number can be audited.

## The affiliate deep-link swap (later)

Today every Buy button links to the plain maker product page. In
`pipeline/build_site.py`'s generated page there is exactly **one** marked
function:

```js
/* AFFILIATE_URL_PLACEHOLDER */
function affiliateUrl(p){ return p.url; }
```

After Awin/Impact approval, that function is the only place that changes —
it will wrap `p.url` in the network deep-link (e.g. Awin
`awclick.php?gid=…&ued=<urlencoded p.url>`). No other code moves.

## Jay-only steps remaining (from research plan §5 — none block Stage A)

1. **Amazon Associates** — tax interview + bank details (account setup);
   later, Creators API registration (owner-only; PA-API 5 is deprecated and
   the Creators API needs 10 qualifying sales in the trailing 30 days).
2. **Awin** — W-9 upload. One account unlocks EcoFlow, BLUETTI, Jackery,
   Redodo, Dakota Lithium, Eco-Worthy (and the BLUETTI/Anker catalog feeds
   that replace the two stores whose /products.json doesn't work).
3. **Impact** — tax doc approval before payouts (BLUETTI, Jackery,
   Eco-Worthy, Walmart, Home Depot, Best Buy).
4. **Domains — DONE 2026-11-20**: 48vlifepo4battery.com,
   12vlifepo4battery.com and serverrackbatteries.com bought on Vercel
   ($12.03 each); the three Vercel projects are git-connected to this repo
   (each with its `sites/<domain>` root directory), so pushes auto-deploy.
   `.github/workflows/refresh.yml` re-fetches prices and rebuilds every
   6 hours; the repo is public, so Actions runs are free.

## Known limitations (honest list)

- **Anker SOLIX is missing** until network catalog feeds exist (its store
  doesn't expose Shopify JSON and its prices are JS-loaded — see endpoint
  table). BLUETTI was missing until 2026-11-19; it now comes from its
  Shopify shop domain (see endpoint table). One known BLUETTI wart: a
  "(Discontinued)" AC180T listing is still in their feed and kept.
- Stores dual-list some SKUs under different titles; dedupe is conservative
  (exact core-name + Wh + price), so a few near-duplicate rows remain
  (mostly LiTime application variants — Truck/RV/Marine — which are real
  separate listings, and some Renogy/Jackery dual listings).
- Body-copy capacity parsing is heuristic; 32 rows currently rely on the
  curated overrides and 16 on body-mode. Overrides should be re-verified
  against maker spec pages whenever the catalog is onboarded/extended.
- Server-rack coverage is thin (2 rows): most rack products are sold as
  48V batteries without "server rack" in the title, or as cabinets (excluded).
- Prices are maker-store list prices at fetch time; the page hides all
  numeric prices automatically once the snapshot is >48h old.

— Wally, 2026-11-19

## EMD sites (added 2026-11-20)
Three standalone sites are generated by `pipeline/build_sites.py` into `sites/<domain>/`
and deployed to Vercel projects of the same name (team giebz), git-sourced from
this repo (rootDirectory = sites/<domain>):
- 48vlifepo4battery.com — 48V bare + rack pool
- 12vlifepo4battery.com — 12V bare pool
- serverrackbatteries.com — rack pool
Refresh loop: fetch_prices.py -> build_sites.py -> commit+push -> Vercel redeploys.

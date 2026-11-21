#!/usr/bin/env python3
"""
fetch_prices.py — Stage A price fetcher for the $/Wh battery comparison site.

Stdlib only (urllib). Polls each enabled maker store's public Shopify
/products.json endpoint, filters to battery-relevant products, extracts
capacity in watt-hours, computes $/Wh, and writes:
  data/products.json   (the catalog snapshot the site generator renders)
  data/fetch_log.json  (per-store counts, skips, errors — for inspection)

Capacity (Wh) extraction, in priority order (v2 — order matters; v1 let
body copy override the title and produced wrong Wh on ~15% of rows):
  1. Explicit Wh/kWh in the variant title or product title ("1024Wh", "2kWh").
     If a variant title bundles components with "+", all explicit Wh
     mentions in it are SUMMED (station + extra battery kits).
  2. Voltage x Ah: from variant/title patterns ("12V 100Ah", "100Ah 12V"),
     or variant Ah combined with the title's voltage. LiFePO4 nominal
     voltages are used when a voltage CLASS is stated: 12V -> 12.8V,
     24V -> 25.6V, 36V -> 38.4V, 48V -> 51.2V (3.2V/cell nominal; using
     12.0V would understate Wh ~6%). A stated decimal nominal is used as-is.
     Multi-pack variants (variant title says "2 Pack", "*2") multiply the
     single-unit Wh by the pack quantity.
  3. Body copy: a Wh value next to a capacity/energy label, skipping values
     introduced by "expandable / up to / max" (system-max marketing numbers).
  4. Body mode: the most frequently mentioned Wh value in body copy
     (expandable-max sentences removed first); ties break to the smallest.
  Otherwise the product is skipped and logged as unparsed.

Scope: lithium (LiFePO4/LFP) products only. AGM / GEL / lead-acid rows are
excluded — different chemistry, not comparable on this table. Chargers,
controllers, shunts, monitors, panels-alone, accessories and full solar
system bundles are excluded as irrelevant.

Variants: if a product's variants encode different capacities (Ah/Wh in the
variant title), each distinct-capacity variant becomes its own row with that
variant's price. Otherwise one row per product at its lowest variant price
(available variants preferred).

Politeness: one sequential pass, paginated, with the configured User-Agent.
Maker ToS note: price/title/URL facts only; no copy or images are stored.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "stores.json"
OVERRIDES_PATH = ROOT / "config" / "capacity_overrides.json"
OUT_PRODUCTS = ROOT / "data" / "products.json"
OUT_LOG = ROOT / "data" / "fetch_log.json"
OUT_HISTORY = ROOT / "data" / "price_history.json"
HISTORY_KEEP_DAYS = 35


def _load_overrides():
    try:
        raw = json.loads(OVERRIDES_PATH.read_text())["overrides"]
    except Exception:
        return []
    # Longest (most specific) title match wins.
    return sorted(raw, key=lambda o: -len(o["title_contains"]))


OVERRIDES = _load_overrides()


def find_override(brand: str, title: str, variant_title: str = ""):
    # Check the variant title too: some dual-listings name the model only
    # there ("Jackery Solar Generator 1000 v2 — Explorer 1000 v2 ...").
    texts = [re.sub(r"\s+", " ", (title or "").lower()),
             re.sub(r"\s+", " ", (variant_title or "").lower())]
    for o in OVERRIDES:
        if o["brand"] == brand and any(o["title_contains"] in t for t in texts):
            return o["wh"]
    return None

MAX_PAGES = 12          # safety cap per store (250/page -> 3000 products)
PAGE_LIMIT = 250
TIMEOUT = 40

# Sanity guards (drops are logged, never silent)
WH_MIN, WH_MAX = 50, 20000
PRICE_MIN, PRICE_MAX = 20.0, 15000.0
PPW_MIN, PPW_MAX = 0.05, 3.00

NOMINAL_LFP = {12: 12.8, 24: 25.6, 36: 38.4, 48: 51.2}

# ---------------------------------------------------------------- text utils
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def clean_text(html: str) -> str:
    if not html:
        return ""
    return WS_RE.sub(" ", TAG_RE.sub(" ", html)).strip()


def to_float(s):
    try:
        return float(str(s).replace(",", ""))
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------- capacity extraction
WH_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(kwh|wh)\b", re.I)
WH_BODY_RE = re.compile(
    r"(?:battery\s+capacity|capacity|energy|usable\s+capacity)[^0-9]{0,40}?"
    r"(\d[\d,]*(?:\.\d+)?)\s*(kwh|wh)\b", re.I)
VAH_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*v(?:olt)?s?\b[^0-9]{0,12}?(\d+(?:\.\d+)?)\s*ah\b", re.I)
AHV_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*ah\b[^0-9]{0,12}?(\d+(?:\.\d+)?)\s*v(?:olt)?s?\b", re.I)
AH_ONLY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*ah\b", re.I)
V_ONLY_RE = re.compile(r"(\d+(?:\.\d+)?)\s*v(?:olt)?s?\b", re.I)
EXPAND_WORDS = ("expand", "up to", "max ", "maximum", "total")


def _wh_val(num, unit):
    v = to_float(num)
    if v is None:
        return None
    return v * 1000.0 if unit.lower() == "kwh" else v


def wh_first(text):
    m = WH_RE.search(text or "")
    return _wh_val(m.group(1), m.group(2)) if m else None


def wh_sum(text):
    vals = [_wh_val(n, u) for n, u in WH_RE.findall(text or "")]
    vals = [v for v in vals if v]
    return sum(vals) if vals else None


def nominal_voltage(v: float):
    if v in (12.8, 25.6, 38.4, 51.2):
        return v
    return NOMINAL_LFP.get(int(round(v)), v)


def pack_qty(variant_title: str):
    """Multi-pack quantity stated in a VARIANT title ('2 Pack', '*2', 'x2')."""
    t = variant_title or ""
    m = re.search(r"(\d+)\s*[- ]?packs?\b", t, re.I)
    if m and int(m.group(1)) >= 2:
        return int(m.group(1))
    # Asterisk form only ("*2"). A bare "x2" is NOT used: variant titles like
    # "9.6 kWh (4x2.4kWh)" are multiplication expressions, not pack counts —
    # v2 inspection caught qty=2 misfiring on exactly that and doubling Wh.
    m = re.search(r"\*\s*(\d+)\b", t)
    if m and int(m.group(1)) >= 2:
        return int(m.group(1))
    return 1


def parse_capacity(title, body_text, variant_title=""):
    """Return (wh, voltage, ah, method) or (None, voltage, ah, reason)."""
    # 1. Explicit Wh in variant / title (sum when a bundle variant uses '+')
    if variant_title and "+" in variant_title:
        s = wh_sum(variant_title)
        if s:
            return s, None, None, "explicit-wh-variant-bundle-sum"
    for text in (variant_title, title):
        if text:
            wh = wh_first(text)
            if wh:
                return wh, None, None, "explicit-wh"
    # 2. Voltage x Ah. The VARIANT's Ah wins over the title's first capacity:
    # titles like "12V 100Ah/200Ah ..." list both sizes, and v3 inspection
    # caught the 200Ah variant row priced against the 100Ah capacity.
    ah = None
    if variant_title:
        m = AH_ONLY_RE.search(variant_title)
        if m:
            ah = to_float(m.group(1))
    if ah:
        mv = V_ONLY_RE.search(variant_title or "") or V_ONLY_RE.search(title or "")
        if mv:
            v = to_float(mv.group(1))
            if v:
                nv = nominal_voltage(v)
                return nv * ah, nv, ah, "variant-ah-x-title-v"
    for text in (variant_title, title):
        if not text:
            continue
        for rx in (VAH_RE, AHV_RE):
            m = rx.search(text)
            if m:
                a, b = to_float(m.group(1)), to_float(m.group(2))
                v, ah2 = (a, b) if rx is VAH_RE else (b, a)
                if v and ah2:
                    nv = nominal_voltage(v)
                    return nv * ah2, nv, ah2, "v-times-ah"
    if not ah and title:
        m = AH_ONLY_RE.search(title)
        if m:
            ah = to_float(m.group(1))
    if ah:
        m = V_ONLY_RE.search(title or "")
        if m:
            v = to_float(m.group(1))
            if v:
                nv = nominal_voltage(v)
                return nv * ah, nv, ah, "variant-ah-x-title-v"
    # 3+4. Body copy. Strongest signal: a value immediately followed by
    # "Wh capacity / Wh battery" ("a 2048Wh capacity that can be expanded
    # to 12kWh" — the expanded total follows the expand word, the base
    # capacity precedes the label). Otherwise combine label-first values
    # and the mention-mode, filtering every mention whose own preceding
    # context carries expand/up-to/max words, and take the smallest
    # candidate: base capacity is always <= any system-max total.
    if body_text:
        def _clean(m, start):
            window = body_text[max(0, start - 45):start].lower()
            return not any(w in window for w in EXPAND_WORDS)

        before_label = []
        for m in re.finditer(
                r"(\d[\d,]*(?:\.\d+)?)\s*(kwh|wh)\s+(?:capacity|battery)\b",
                body_text, re.I):
            if _clean(m, m.start()):
                wh = _wh_val(m.group(1), m.group(2))
                if wh and WH_MIN <= wh <= WH_MAX:
                    before_label.append(wh)
        if before_label:
            return min(before_label), None, None, "body-wh-before-capacity-label"
        candidates = []
        for m in WH_BODY_RE.finditer(body_text):
            if _clean(m, m.start()):
                wh = _wh_val(m.group(1), m.group(2))
                if wh and WH_MIN <= wh <= WH_MAX:
                    candidates.append(wh)
        vals = []
        for m in WH_RE.finditer(body_text):
            if _clean(m, m.start()):
                wh = _wh_val(m.group(1), m.group(2))
                if wh and WH_MIN <= wh <= WH_MAX:
                    vals.append(wh)
        if vals:
            counts = Counter(vals)
            repeated = [v for v, c in counts.items() if c >= 2]
            if repeated:
                # Expansion totals (2x, 3x base) are marketed hard and can
                # out-mention the base capacity — v4 caught DELTA 2 Max at
                # its 6,144Wh expanded max instead of 2,048Wh base. The
                # smallest REPEATED value is the base: expansion tiers are
                # multiples of it and each tier is named once or twice,
                # while the base recurs across specs/features/FAQ copy.
                candidates.append(min(repeated))
            else:
                top = max(counts.values())
                candidates.append(min(v for v, c in counts.items() if c == top))
        if candidates:
            return min(candidates), None, None, "body-mode-wh"
    return None, None, ah, "no-capacity-found"


# ------------------------------------------------------------- relevance
# Absolute exclusions (title-level): not the product this table compares.
ABSOLUTE_EXCLUDE_RE = [re.compile(p, re.I) for p in [
    r"\bagm\b", r"\bgel battery\b", r"lead[- ]acid", r"flooded battery",
    r"\bcharger\b", r"charge controller", r"battery shunt", r"monitoring screen",
    r"\baccessories\b", r"compatible accessories", r"solar panel",
    r"complete .*solar kit", r"solar kit\b", r"cabin solution", r"\bbundle\b",
    r"hybrid home backup", r"storage system", r"heated (vest|jacket|gloves)",
    r"coffee cup", r"gift card", r"smart generator", r"dual fuel generator",
]]
# Soft exclusions: dropped unless the title itself signals station/battery.
SOFT_EXCLUDE_RE = [re.compile(p, re.I) for p in [
    r"\bcable\b", r"\badapter\b", r"\bmount", r"\bbracket\b", r"\bmug\b",
    r"carrying (case|bag)", r"\bbackpack\b", r"\btrolley\b", r"\bfuse\b",
    r"\bcover\b", r"protection plan", r"\bshirt\b", r"\bhat\b", r"water pump",
    r"air conditioner", r"\bfridge\b", r"refrigerator",
]]
REFURB_RE = re.compile(r"refurbished|renewed|like new|open box|certified refurb", re.I)
# Accessory head-nouns: a product whose title names an accessory and does
# NOT itself claim to be a power station / generator / battery is an
# accessory even when its title name-drops a station model ("RIVER 2
# Waterproof Bag", "DELTA Pro Ultra Transfer Switch") — v5 caught both
# inheriting the station's capacity via overrides.
ACCESSORY_NOUN_RE = re.compile(
    r"waterproof bag|\bbag\b|pegboard|transfer switch|\bstand\b|organizer|"
    r"hard case|dust cover|wall mount|\bcart\b|wheel kit|solar panel|"
    r"\bcable\b|\badapter\b", re.I)
HEAD_NOUN_RE = re.compile(r"power station|solar generator|\bbattery\b", re.I)
STATION_RE = re.compile(
    r"portable power station|power station|solar generator|explorer\s?\d|"
    r"delta\s?(pro|max|2|3)|river\s?(2|3)|homepower|ac\d{2,3}\b|elite\s?\d|"
    r"solix\s?[cf]\d|apex\s?\d", re.I)
RACK_RE = re.compile(r"server rack|rackmount|rack-mounted|rack battery", re.I)
EXPANSION_RE = re.compile(
    r"extra battery|expansion battery|additional battery|expansion pack|"
    r"smart extra|battery expansion", re.I)
BARE_RE = re.compile(
    r"lifepo4|lithium iron|lithium battery|deep cycle|lithium-ion battery|"
    r"lfp battery|\d+\s*ah\b.*\bbattery\b|\bbattery\b.*\d+\s*ah\b", re.I)


def classify(title: str, blob: str):
    """Return product type or None / 'REFURB' if not relevant."""
    t = title.lower()
    if REFURB_RE.search(t):
        return "REFURB"
    if ACCESSORY_NOUN_RE.search(title) and not HEAD_NOUN_RE.search(title):
        return None
    for rx in ABSOLUTE_EXCLUDE_RE:
        if rx.search(t):
            # A power station sold WITH a panel is still a station.
            if rx.pattern == r"solar panel" and STATION_RE.search(title):
                pass
            else:
                return None
    for rx in SOFT_EXCLUDE_RE:
        if rx.search(t) and not (STATION_RE.search(title) or BARE_RE.search(title)):
            return None
    if RACK_RE.search(blob):
        return "rack-battery"
    if EXPANSION_RE.search(blob):
        return "expansion"
    if STATION_RE.search(title):
        return "station"
    if BARE_RE.search(blob):
        return "bare-battery"
    if STATION_RE.search(blob):
        return "station"
    return None


# ------------------------------------------------------------------- fetch
def fetch_json(url: str, ua: str):
    req = urllib.request.Request(url, headers={"User-Agent": ua,
                                                "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def variant_capacity_hint(variant_title: str):
    if not variant_title or variant_title.strip().lower() == "default title":
        return None
    wh = wh_first(variant_title)
    if wh:
        return ("wh", wh)
    m = AH_ONLY_RE.search(variant_title)
    if m:
        ah = to_float(m.group(1))
        if ah:
            return ("ah", ah)
    return None


def process_store(store_cfg, ua):
    base = store_cfg["base_url"].rstrip("/")
    display_base = store_cfg.get("display_base_url", base).rstrip("/")
    brand = store_cfg["brand"]
    log = {"store": brand, "base_url": base, "enabled": True, "pages": 0,
           "raw_products": 0, "kept": 0, "skipped_irrelevant": 0,
           "skipped_refurb": 0, "skipped_unparsed": 0, "dropped_guard": 0,
           "errors": [], "unparsed_samples": [], "guard_samples": []}
    products = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{base}/products.json?limit={PAGE_LIMIT}&page={page}"
        try:
            data = fetch_json(url, ua)
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as e:
            log["errors"].append(f"page {page}: {type(e).__name__}: {e}")
            break
        batch = data.get("products", []) if isinstance(data, dict) else []
        log["pages"] += 1
        log["raw_products"] += len(batch)
        for p in batch:
            products.extend(process_product(p, brand, display_base, log))
        if len(batch) < PAGE_LIMIT:
            break
    log["kept"] = len(products)
    return products, log


def process_product(p, brand, base, log):
    title = (p.get("title") or "").strip()
    handle = p.get("handle") or ""
    url = f"{base}/products/{handle}" if handle else base
    blob = " ".join([title, p.get("product_type") or "",
                     " ".join(p.get("tags") or [])])
    body_text = clean_text(p.get("body_html") or "")[:6000]

    ptype = classify(title, blob)
    if ptype == "REFURB":
        log["skipped_refurb"] += 1
        return []
    if ptype is None:
        log["skipped_irrelevant"] += 1
        return []

    variants = [v for v in (p.get("variants") or []) if to_float(v.get("price"))]
    if not variants:
        log["skipped_unparsed"] += 1
        log["unparsed_samples"].append(f"{title} :: no priced variants")
        return []

    hints = {}
    for v in variants:
        h = variant_capacity_hint(v.get("title") or "")
        if h:
            hints[h] = v
    rows = []
    if len(hints) >= 2:
        by_cap = {}
        for v in variants:
            h = variant_capacity_hint(v.get("title") or "")
            if h and (h not in by_cap or
                      to_float(v["price"]) < to_float(by_cap[h]["price"])):
                by_cap[h] = v
        for (kind, cap), v in sorted(by_cap.items()):
            rows.append(make_row(brand, title, v.get("title") or "",
                                 ptype, body_text, v, url, log))
    else:
        avail = [v for v in variants if v.get("available")]
        pool = avail if avail else variants
        v = min(pool, key=lambda x: to_float(x["price"]))
        rows.append(make_row(brand, title, v.get("title") or "",
                             ptype, body_text, v, url, log))
    return [r for r in rows if r]


def make_row(brand, title, variant_title, ptype, body_text, variant, url, log):
    wh, volt, ah, method = parse_capacity(title, body_text, variant_title)
    # Curated overrides rescue models whose catalog never states capacity,
    # and replace ALL body-derived values (body copy mixes base capacity
    # with expansion totals and cross-sell specs) — never explicit title
    # or V x Ah values, which come from the product's own name.
    if not wh or method.startswith("body") or method == "explicit-wh-body-labelled":
        ow = find_override(brand, title, variant_title)
        if ow and ow != wh:
            wh, volt, ah, method = float(ow), None, None, "override-curated"
    if wh:
        qty = pack_qty(variant_title)
        # Multiply only when capacity came from a single-unit signal and the
        # variant title itself declares a multi-pack (not bundle-sum rows).
        if qty > 1 and method in ("explicit-wh", "v-times-ah",
                                  "variant-ah-x-title-v"):
            wh = wh * qty
    if not wh:
        # Bundle variant whose capacity would have to come from body copy:
        # pairing is unreliable — skip honestly rather than guess.
        log["skipped_unparsed"] += 1
        if len(log["unparsed_samples"]) < 20:
            log["unparsed_samples"].append(f"{title} :: no Wh/Ah capacity parsed")
        return None
    price = to_float(variant.get("price"))
    compare_at = to_float(variant.get("compare_at_price"))
    ppw = price / wh if price else None
    if not (WH_MIN <= wh <= WH_MAX and price and PRICE_MIN <= price <= PRICE_MAX
            and ppw and PPW_MIN <= ppw <= PPW_MAX):
        log["dropped_guard"] += 1
        if len(log["guard_samples"]) < 15:
            log["guard_samples"].append(
                f"{title} :: wh={wh} price={price} ppw={ppw and round(ppw,3)} via {method}")
        return None
    display_title = title
    vt = (variant_title or "").strip()
    if vt and vt.lower() != "default title" and vt not in title:
        display_title = f"{title} — {vt}"
    return {
        "brand": brand,
        "title": display_title,
        "type": ptype,
        "wh": int(round(wh)),
        "voltage": volt,
        "ah": ah,
        "price": round(price, 2),
        "compare_at": round(compare_at, 2) if compare_at else None,
        "available": bool(variant.get("available")),
        "price_per_wh": round(ppw, 3),
        "url": url,
        "source_store": url.split("/products/")[0],
        "image": None,
        "wh_method": method,
    }


def normalize_title(t: str, brand: str) -> str:
    """Core product name for dedupe: strips brand/sales prefixes and a
    variant suffix that merely repeats the base title."""
    s = re.sub(r"\s+", " ", t.lower()).strip()
    if " — " in s:
        base, suffix = s.split(" — ", 1)
        if suffix.strip() and (suffix.strip() in base or base in suffix.strip()):
            s = base
    s = s.replace(brand.lower(), " ")
    # Category filler and colour words are not model discriminators; stores
    # dual-list the same unit as "...Power Station X" and "Solar Generator X".
    for filler in ("portable power station", "solar generator", "power station",
                   "jackery", "ecoflow", "litime", "renogy", "eco worthy",
                   "black", "white", "grey", "gray"):
        s = s.replace(filler, " ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def append_price_snapshot(fetched_at: str, rows: list) -> None:
    """Append one compact price snapshot to data/price_history.json and
    prune snapshots older than HISTORY_KEEP_DAYS. Keyed by product URL
    (the catalog's identity). Price only; $/Wh is recomputed at build.
    A corrupt/unreadable history file is replaced, never fatal."""
    try:
        hist = json.loads(OUT_HISTORY.read_text())
        if not isinstance(hist, dict) or hist.get("v") != 1:
            hist = {"v": 1, "snapshots": []}
    except Exception:
        hist = {"v": 1, "snapshots": []}
    snaps = [s for s in hist.get("snapshots", [])
             if isinstance(s, dict) and s.get("ts") and s.get("prices")]
    snaps.append({"ts": fetched_at,
                  "prices": {r["url"]: r["price"] for r in rows}})
    cutoff = (datetime.now(timezone.utc)
              - timedelta(days=HISTORY_KEEP_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    snaps = [s for s in snaps if s["ts"] >= cutoff]
    snaps.sort(key=lambda s: s["ts"])
    OUT_HISTORY.write_text(json.dumps({"v": 1, "snapshots": snaps},
                                      separators=(",", ":")))
    print(f"[history] {len(snaps)} snapshots -> {OUT_HISTORY}",
          file=sys.stderr)


def main():
    cfg = json.loads(CONFIG_PATH.read_text())
    ua = cfg.get("user_agent", "BatteryPerWh-Prototype/0.1")
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    all_products, store_logs = [], []
    for store in cfg["stores"]:
        if not store.get("enabled"):
            store_logs.append({"store": store["brand"],
                               "base_url": store["base_url"], "enabled": False,
                               "note": store.get("endpoint_test", ""),
                               "kept": 0})
            continue
        print(f"[fetch] {store['brand']} …", file=sys.stderr)
        products, log = process_store(store, ua)
        all_products.extend(products)
        store_logs.append(log)
        print(f"        raw={log['raw_products']} kept={log['kept']} "
              f"unparsed={log['skipped_unparsed']} "
              f"irrelevant={log['skipped_irrelevant']} "
              f"errors={len(log['errors'])}", file=sys.stderr)

    # Dedupe: exact rows, then same core product at same Wh+price listed
    # multiple times by a store (keep the shortest/cleanest title).
    seen, deduped = set(), []
    for r in sorted(all_products, key=lambda x: (x["price_per_wh"], len(x["title"]))):
        key = (r["brand"], normalize_title(r["title"], r["brand"]),
               r["wh"], r["price"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)
    deduped.sort(key=lambda x: x["price_per_wh"])

    out = {"fetched_at": fetched_at,
           "stores": [{"store": s["store"], "enabled": s["enabled"],
                       "kept": s.get("kept", 0)} for s in store_logs],
           "products": deduped}
    OUT_PRODUCTS.parent.mkdir(parents=True, exist_ok=True)
    OUT_PRODUCTS.write_text(json.dumps(out, indent=2))
    append_price_snapshot(fetched_at, deduped)
    OUT_LOG.write_text(json.dumps(
        {"fetched_at": fetched_at, "total_kept": len(deduped),
         "stores": store_logs}, indent=2))
    print(f"[done] {len(deduped)} products -> {OUT_PRODUCTS}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

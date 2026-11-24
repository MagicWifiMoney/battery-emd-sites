"""Refresh hand-tracked Vatrer prices from the Awin product feed.

Vatrer's store sits behind a bot wall, so its four rack models live in
config/manual_products.json as browser pulls. Once Vatrer joined Awin
(2026-11-21, product feed = Yes) the feed became the automation path.

Reads the feed download URL from the AWIN_VATRER_FEED_URL environment
variable (a GitHub Actions secret: the URL embeds the Awin API key and this
repo is PUBLIC, so it must never be committed). With no URL set, or on any
error, it changes nothing and exits 0: the manual prices stay in place.

Matching: a feed row updates a manual product when its merchant_deep_link
has the same /products/<handle> path. Only price, compare_at, available and
price_per_wh change; capacity, titles and URLs never come from the feed.

Python 3 stdlib only.
"""
import csv
import gzip
import io
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "config" / "manual_products.json"
PRICE_COLS = ("search_price", "store_price", "display_price")
RRP_COLS = ("rrp_price", "product_price_old", "base_price")
LINK_COLS = ("merchant_deep_link", "merchant_product_url", "aw_deep_link")
STOCK_COLS = ("in_stock", "stock_status", "is_for_sale")


def _path(url):
    return urlparse(url or "").path.rstrip("/").lower()


def _num(s):
    try:
        v = float(str(s).replace("$", "").replace(",", "").strip())
        return v if v > 0 else None
    except (TypeError, ValueError):
        return None


def _first(row, cols):
    for c in cols:
        if row.get(c):
            return row[c]
    return None


def fetch_rows(url):
    req = urllib.request.Request(url, headers={"User-Agent": "BatteryPerWh/1.0"})
    raw = urllib.request.urlopen(req, timeout=60).read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))


def main():
    url = os.environ.get("AWIN_VATRER_FEED_URL", "").strip()
    if not url:
        print("[awin] AWIN_VATRER_FEED_URL not set - keeping manual Vatrer prices",
              file=sys.stderr)
        return 0
    try:
        rows = fetch_rows(url)
    except Exception as e:  # never break the refresh over the feed
        print(f"[awin] feed fetch failed ({type(e).__name__}) - keeping manual prices",
              file=sys.stderr)
        return 0
    feed = {}
    for r in rows:
        link = _first(r, LINK_COLS)
        if link and "/products/" in link:
            feed[_path(link)] = r
    cfg = json.loads(MANUAL.read_text())
    updated = 0
    for p in cfg.get("products", []):
        if p.get("brand") != "Vatrer":
            continue
        r = feed.get(_path(p["url"]))
        if not r:
            continue
        price = _num(_first(r, PRICE_COLS))
        if not price or not p.get("wh"):
            continue
        ppw = round(price / p["wh"], 3)
        if not (0.05 <= ppw <= 2.0):  # same spirit as the fetcher's sanity guards
            continue
        p["price"] = round(price, 2)
        rrp = _num(_first(r, RRP_COLS))
        p["compare_at"] = round(rrp, 2) if rrp and rrp > price else None
        stock = str(_first(r, STOCK_COLS) or "1").strip().lower()
        p["available"] = stock not in ("0", "false", "no", "out of stock")
        p["price_per_wh"] = ppw
        updated += 1
    if updated:
        cfg["collected_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cfg["source"] = "awin-feed"
        MANUAL.write_text(json.dumps(cfg, separators=(",", ":")))
    print(f"[awin] {len(rows)} feed rows, {updated} Vatrer products updated",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

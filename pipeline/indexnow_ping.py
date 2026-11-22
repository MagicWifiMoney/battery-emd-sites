#!/usr/bin/env python3
"""indexnow_ping.py — submit the build's changed URLs to IndexNow.

Reads indexnow-changed.json (written by build_sites.py: only pages whose
content actually changed, fetch timestamp normalized out) and POSTs each
site's URL list to api.indexnow.org, which fans out to Bing, Yandex and
other participants. Run AFTER the new build is deployed — pinging tells
engines to re-crawl, so the live pages must already serve the new content.

Usage: python3 pipeline/indexnow_ping.py [--dry-run]
"""
import json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    dry = "--dry-run" in sys.argv
    payload = json.loads((ROOT / "indexnow-changed.json").read_text())
    key = payload["key"]
    for domain, urls in payload["sites"].items():
        if not urls:
            print(f"[indexnow] {domain}: no changed URLs")
            continue
        body = json.dumps({
            "host": domain,
            "key": key,
            "keyLocation": f"https://{domain}/{key}.txt",
            "urlList": urls[:10000],
        }).encode()
        print(f"[indexnow] {domain}: {len(urls)} changed URLs")
        if dry:
            continue
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow", data=body,
            headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"[indexnow] {domain}: HTTP {r.status}")
        except Exception as e:
            print(f"[indexnow] {domain}: FAILED {e}")


if __name__ == "__main__":
    main()

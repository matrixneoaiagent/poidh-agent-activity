#!/usr/bin/env python3
"""Pull POIDH public indexer tables (read-only) and cache raw JSON.

Usage: python3 collect_indexer.py
Writes data/indexer_<table>_<chain>.json  + data/collect_meta.json
"""
import json, os, time, urllib.request, urllib.error, datetime

BASE = "https://indexer.poidh.xyz/api/v1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)
CHAINS = [8453, 42161, 1]
TABLES = ["bounties", "claims", "transactions"]


def get(url, tries=5):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "poidh-agent-research/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            if a == tries - 1:
                raise
            time.sleep(1.5 * (a + 1))


def paginate(table, chain):
    rows, off = [], 0
    while True:
        url = f"{BASE}/{table}?chainId={chain}&limit=100&offset={off}"
        page = get(url)
        if not isinstance(page, list) or not page:
            break
        rows.extend(page)
        if len(page) < 100:
            break
        off += 100
        time.sleep(0.15)
    return rows


meta = {"fetched_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "source": BASE,
        "endpoints": {}}
for chain in CHAINS:
    for t in TABLES:
        rows = paginate(t, chain)
        path = os.path.join(OUT, f"indexer_{t}_{chain}.json")
        json.dump(rows, open(path, "w"), indent=None)
        meta["endpoints"][f"{t}_{chain}"] = {"url": f"{BASE}/{t}?chainId={chain}&limit=100&offset=0..N",
                                             "rows": len(rows), "file": os.path.basename(path)}
        print(chain, t, len(rows), flush=True)

json.dump(meta, open(os.path.join(OUT, "collect_meta.json"), "w"), indent=2)
print("done")

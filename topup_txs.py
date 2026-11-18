#!/usr/bin/env python3
"""Top-up: 25 txs per call (mainnet.base.org enforces 25 req/s), 1.1s spacing.
Merges into data/tx_extra.json, keyed by tx hash."""
import json, os, time, urllib.request, random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RPC = "https://mainnet.base.org"
CH = 25

txs = json.load(open(os.path.join(DATA, "indexer_transactions_8453.json")))
hashes = list(dict.fromkeys(t["tx"] for t in txs))
extra = json.load(open(os.path.join(DATA, "tx_extra.json")))
missing = [h for h in hashes if h not in extra]
print("to fetch", len(missing), flush=True)


def call(payload):
    req = urllib.request.Request(RPC, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "curl/8.5.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


todo = missing
for i in range(0, len(todo), CH):
    chunk = [h for h in todo[i:i+CH] if h not in extra]
    if not chunk:
        continue
    payload = [{"jsonrpc": "2.0", "id": j, "method": "eth_getTransactionByHash", "params": [h]}
               for j, h in enumerate(chunk)]
    for attempt in range(6):
        try:
            res = call(payload)
            got = {r["id"]: r["result"] for r in res if isinstance(r, dict) and isinstance(r.get("result"), dict)}
            for j, h in enumerate(chunk):
                if j in got:
                    extra[h] = got[j]
            if got:
                json.dump(extra, open(os.path.join(DATA, "tx_extra.json"), "w"))
            break
        except Exception as e:
            print("retry", i, attempt, type(e).__name__, e, flush=True)
            time.sleep(2 + random.random() * 2)
    time.sleep(1.1)
    if i % 500 == 0:
        print("at", i, "have", len(extra), flush=True)

json.dump(extra, open(os.path.join(DATA, "tx_extra.json"), "w"))
missing = [h for h in hashes if h not in extra]
print("have", len(extra), "missing", len(missing), flush=True)
json.dump(missing, open(os.path.join(DATA, "tx_missing.json"), "w"), indent=1)

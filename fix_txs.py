#!/usr/bin/env python3
"""Top-up pass: refetch any eth_getTransactionByHash slot that is missing,
null or errored. Small batches (20), spaced out, several public RPCs.
Merges results into data/tx_map.json keyed by tx hash (raw tx objects).
"""
import json, glob, os, time, random, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RPCS = ["https://mainnet.base.org", "https://base.drpc.org",
        "https://1rpc.io/base", "https://base-rpc.publicnode.com"]

txs = json.load(open(os.path.join(DATA, "indexer_transactions_8453.json")))
hashes = list(dict.fromkeys(t["tx"] for t in txs))
need = []
for i in range(0, len(hashes), 100):
    p = os.path.join(DATA, f"tx_batch_{i//100:03d}.json")
    d = json.load(open(p))
    got = {}
    for r in d["response"]:
        if isinstance(r, dict) and isinstance(r.get("result"), dict):
            got[r["id"]] = r["result"]
    for j, h in enumerate(hashes[i:i+100]):
        if j not in got:
            need.append(h)
print("missing", len(need), flush=True)


def call(rpc, payload):
    req = urllib.request.Request(rpc, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "curl/8.5.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


out_path = os.path.join(DATA, "tx_extra.json")
extra = json.load(open(out_path)) if os.path.exists(out_path) else {}
CH = 20
rpc_i = 0
for i in range(0, len(need), CH):
    chunk = [h for h in need[i:i+CH] if h not in extra]
    if not chunk:
        continue
    payload = [{"jsonrpc": "2.0", "id": j, "method": "eth_getTransactionByHash", "params": [h]}
               for j, h in enumerate(chunk)]
    for attempt in range(10):
        rpc = RPCS[rpc_i % len(RPCS)]
        rpc_i += 1
        try:
            res = call(rpc, payload)
            got = {r["id"]: r["result"] for r in res
                   if isinstance(r, dict) and isinstance(r.get("result"), dict)}
            for j, h in enumerate(chunk):
                if j in got:
                    extra[h] = got[j]
            json.dump(extra, open(out_path, "w"))
            if len(got) < len(chunk):
                print(f"partial {len(got)}/{len(chunk)} via {rpc}", flush=True)
            break
        except Exception as e:
            print("retry", i, attempt, rpc, type(e).__name__, e, flush=True)
            time.sleep(1.5 + random.random() * 2)
    time.sleep(0.25)

print("tx_extra has", len(extra), "of", len(hashes), flush=True)
missing = [h for h in hashes if h not in extra]
print("still missing", len(missing), flush=True)
json.dump(missing, open(os.path.join(DATA, "tx_missing.json"), "w"), indent=1)

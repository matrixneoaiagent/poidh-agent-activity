#!/usr/bin/env python3
"""Fetch raw Base transactions for every POIDH 'claim created' tx (read-only).

Reads data/indexer_transactions_8453.json, batches eth_getTransactionByHash
(100 per JSON-RPC batch) against public Base RPCs, caches each batch as
data/tx_batch_<n>.json. Resumable.
"""
import json, os, time, urllib.request, random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RPCS = ["https://mainnet.base.org", "https://base-rpc.publicnode.com",
        "https://base.llamarpc.com", "https://1rpc.io/base"]

txs = json.load(open(os.path.join(DATA, "indexer_transactions_8453.json")))
claims = [t for t in txs if t["action"] == "claim created"]
hashes = [t["tx"] for t in txs]
hashes = list(dict.fromkeys([t["tx"] for t in txs]))  # every indexed tx
print("indexed txs to fetch:", len(hashes), flush=True)

CHUNK = 100
batches = [hashes[i:i + CHUNK] for i in range(0, len(hashes), CHUNK)]


def call(rpc, payload):
    req = urllib.request.Request(rpc, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "curl/8.5.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


ok = 0
for i, chunk in enumerate(batches):
    path = os.path.join(DATA, f"tx_batch_{i:03d}.json")
    if os.path.exists(path):
        ok += 1
        continue
    payload = [{"jsonrpc": "2.0", "id": j, "method": "eth_getTransactionByHash", "params": [h]}
               for j, h in enumerate(chunk)]
    for attempt in range(12):
        rpc = RPCS[attempt % len(RPCS)]
        try:
            res = call(rpc, payload)
            if not isinstance(res, list) or len(res) != len(chunk):
                raise RuntimeError("bad batch shape")
            # a null result is legal (tx unseen by that node) but resend once if all null
            if all(r.get("result") is None for r in res):
                raise RuntimeError("all null")
            json.dump({"rpc": rpc, "payload_ids": chunk, "response": res}, open(path, "w"))
            ok += 1
            break
        except Exception as e:
            print(f"batch {i} attempt {attempt} {rpc} {type(e).__name__} {e}", flush=True)
            time.sleep(1.0 + random.random() * 2)
    else:
        print("FAILED batch", i, flush=True)
    if i % 20 == 0:
        print("progress", i, "/", len(batches), flush=True)

print("batches cached:", ok, "/", len(batches))

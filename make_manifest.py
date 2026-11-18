#!/usr/bin/env python3
"""Emit data/MANIFEST.md: file, size, rows (for JSON arrays / CSV), sha256."""
import csv, glob, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
lines = ["# Data manifest", "",
         "Everything under `data/` is read-only output of the scripts in the parent directory.",
         "`tx_batch_*.json` (142 files, ~61 MB) is the raw JSON-RPC cache and can be deleted +",
         "re-fetched with `collect_txs.py`; `tx_extra.json` holds the same transactions merged.",
         "", "| file | bytes | rows | sha256 (first 16) |", "|---|---|---|---|"]
total = 0
for p in sorted(glob.glob(os.path.join(D, "*"))):
    name = os.path.basename(p)
    if name == "MANIFEST.md":
        continue
    size = os.path.getsize(p)
    total += size
    rows = ""
    if name.endswith(".json"):
        try:
            d = json.load(open(p))
            if isinstance(d, list):
                rows = len(d)
            elif isinstance(d, dict):
                rows = f"{len(d)} keys"
        except Exception:
            rows = "-"
    elif name.endswith(".csv"):
        rows = sum(1 for _ in csv.reader(open(p, newline=""))) - 1
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    lines.append(f"| {name} | {size:,} | {rows} | `{h}` |")
lines += ["", f"Total {total/1e6:.1f} MB across {len(glob.glob(os.path.join(D,'*')))-1} files.",
          "", "## Key files", "",
          "| file | what it is |", "|---|---|",
          "| `indexer_claims_8453.json` | all 9,748 Base claims incl. full description text |",
          "| `indexer_transactions_8453.json` | 14,376 indexed Base actions with timestamps + tx hashes |",
          "| `tx_extra.json` | 14,158 raw Base tx objects keyed by hash |",
          "| `claims_tx.csv` | the join: 9,709 claims x tx fields x text |",
          "| `detectors.csv` | the 4,431 claims in scope with D1/D2/D3 flags and capture pattern |",
          "| `final_tables.json` | main table, four sensitivities, wallet-level table |",
          "| `hand_audit_sample.csv` | 42 sampled claims with my verdicts and notes |",
          "| `QUERIES.md` | every endpoint, parameter and snapshot time |"]
open(os.path.join(D, "MANIFEST.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines[:12]))
print("...")

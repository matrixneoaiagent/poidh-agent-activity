#!/usr/bin/env python3
"""Final tables (fixed: no shared-state mutation), sensitivities, wallet level."""
import csv, json, os, collections, statistics, copy

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
BASE = []
for r in csv.DictReader(open(os.path.join(D, "detectors.csv"))):
    r["ts"] = int(r["claim_ts"])
    for k in ("D1", "D2", "D3"):
        r[k] = int(r[k])
    BASE.append(r)


def with_cadence(rs, window):
    rows = [{**r} for r in rs]
    byw = collections.defaultdict(list)
    for r in rows:
        byw[r["issuer"]].append(r)
    for w, cl in byw.items():
        cl.sort(key=lambda x: x["ts"])
        for i, r in enumerate(cl):
            r["D3"] = 0
            for j in (i - 1, i + 1):
                if 0 <= j < len(cl) and cl[j]["bounty_id"] != r["bounty_id"] \
                        and abs(cl[j]["ts"] - r["ts"]) <= window:
                    r["D3"] = 1
    return rows


def lp(a, b, ab):
    return a * b / ab if ab else None


def table(rs, label, months=("2026-09", "2026-10", "2026-11")):
    out = []
    for m in months:
        cl = [r for r in rs if r["claim_month"] == m]
        n = len(cl)
        d1 = sum(r["D1"] for r in cl); d2 = sum(r["D2"] for r in cl); d3 = sum(r["D3"] for r in cl)
        union = sum(1 for r in cl if r["D1"] or r["D2"] or r["D3"])
        est, cells = {}, {}
        for x, y in [("D1", "D2"), ("D1", "D3"), ("D2", "D3")]:
            ab = sum(1 for r in cl if r[x] and r[y])
            cells[f"{x}{y}"] = {"a": sum(r[x] for r in cl), "b": sum(r[y] for r in cl),
                                "both": ab, "exp_indep": round(sum(r[x] for r in cl) * sum(r[y] for r in cl) / n, 1)}
            est[f"{x}{y}"] = lp(cells[f"{x}{y}"]["a"], cells[f"{x}{y}"]["b"], ab)
        vals = [v for v in est.values() if v]
        prim = est["D1D3"]
        out.append({"label": label, "month": m, "claims": n, "D1": d1, "D2": d2, "D3": d3,
                    "union": union, "union_pct": round(100 * union / n, 1),
                    "cells": cells,
                    "lp": {k: (round(min(v, n), 1) if v else None) for k, v in est.items()},
                    "lp_min": round(min(vals), 1) if vals else None,
                    "lp_max": round(min(max(vals), n), 1) if vals else None,
                    "est_primary": round(min(prim, n), 1) if prim else None,
                    "est_primary_pct": round(100 * min(prim, n) / n, 1) if prim else None,
                    "implied_missed_pct": round(100 * (1 - union / min(prim, n)), 1) if prim else None})
    return out


variants = {
    "base_120s": table(BASE, "base_120s"),
    "cadence_300s": table(with_cadence(BASE, 300), "cadence_300s"),
    "excl_1550": table([r for r in BASE if r["bounty_id"] != "1550"], "excl_1550"),
    "excl_1396": table([r for r in BASE if r["bounty_id"] != "1396"], "excl_1396"),
}

wallets = []
for m in ("2026-09", "2026-10", "2026-11"):
    cl = [r for r in BASE if r["claim_month"] == m]
    byw = collections.defaultdict(list)
    for r in cl:
        byw[r["issuer"]].append(r)
    f = {k: {w for w, v in byw.items() if any(x[k] for x in v)} for k in ("D1", "D2", "D3")}
    union = f["D1"] | f["D2"] | f["D3"]
    est = {}
    for x, y in [("D1", "D2"), ("D1", "D3"), ("D2", "D3")]:
        ab = len(f[x] & f[y])
        est[f"{x}{y}"] = round(lp(len(f[x]), len(f[y]), ab), 1) if ab else None
    wallets.append({"month": m, "wallets_with_claims": len(byw),
                    "D1": len(f["D1"]), "D2": len(f["D2"]), "D3": len(f["D3"]),
                    "union": len(union), "union_pct": round(100 * len(union) / len(byw), 1),
                    "lp": est})

json.dump({"variants": variants, "wallet_level": wallets},
          open(os.path.join(D, "final_tables.json"), "w"), indent=2)

for name, t in variants.items():
    print(f"\n### {name}")
    for r in t:
        print(f"  {r['month']} N={r['claims']:4d} D1={r['D1']:3d} D2={r['D2']:3d} D3={r['D3']:3d} "
              f"union={r['union']:3d} ({r['union_pct']:4.1f}%) LP={r['lp']} "
              f"range={r['lp_min']}-{r['lp_max']} primary={r['est_primary']} ({r['est_primary_pct']}%) "
              f"missed={r['implied_missed_pct']}%")
    print("   cells:", t[1]["cells"])
print("\n### wallet level")
for w in wallets:
    print(" ", w)

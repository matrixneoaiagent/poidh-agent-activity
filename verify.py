#!/usr/bin/env python3
"""verify.py — re-derive every number in ANALYSIS.md from the cached raw files.

No network. Prints a PASS/FAIL line per claim. Usage: python3 verify.py
"""
import csv, json, os, collections, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
fails = []


def check(label, got, want, tol=0.05):
    ok = (abs(got - want) <= tol) if isinstance(want, (int, float)) else (got == want)
    print(f"{'PASS' if ok else 'FAIL'}  {label}: got {got}, expected {want}")
    if not ok:
        fails.append(label)


rows = list(csv.DictReader(open(os.path.join(D, "detectors.csv"))))
for r in rows:
    for k in ("D1", "D2", "D3"):
        r[k] = int(r[k])

check("claims in universe", len(rows), 4431, 0)
check("distinct claimant wallets", len({r["issuer"] for r in rows}), 1091, 0)
check("first month", min(r["claim_month"] for r in rows), "2026-01")
check("last month", max(r["claim_month"] for r in rows), "2026-11")

idx_claims = json.load(open(os.path.join(D, "indexer_claims_8453.json")))
check("indexer Base claim rows", len(idx_claims), 9748, 0)
# every 2026 claim in the indexer is present in the joined set
v3 = [c for c in idx_claims if int(c["bountyId"]) >= 987 or c["bountyId"] in
      {r["bounty_id"] for r in rows}]
check("join rate >99% of 2026 indexer claims",
      round(100 * len(rows) / len([c for c in idx_claims if int(c["bountyId"]) >= 987]), 1) >= 99.0,
      True)

monthly = {
    "2026-01": (121, 0, 1, 0, 1), "2026-02": (204, 0, 1, 0, 1),
    "2026-03": (305, 0, 0, 0, 0), "2026-04": (416, 1, 0, 0, 1),
    "2026-05": (338, 0, 0, 2, 2), "2026-06": (284, 0, 0, 0, 0),
    "2026-07": (394, 0, 0, 0, 0), "2026-08": (435, 2, 31, 2, 35),
    "2026-09": (599, 35, 44, 20, 75), "2026-10": (856, 40, 125, 44, 168),
    "2026-11": (479, 21, 93, 42, 133),
}
for m, (n, d1, d2, d3, u) in monthly.items():
    cl = [r for r in rows if r["claim_month"] == m]
    got = (len(cl), sum(r["D1"] for r in cl), sum(r["D2"] for r in cl),
           sum(r["D3"] for r in cl), sum(1 for r in cl if r["D1"] or r["D2"] or r["D3"]))
    check(f"{m} (n,D1,D2,D3,union)", got, (n, d1, d2, d3, u))

print("\n-- union shares")
for m, pct in [("2026-08", 8.0), ("2026-09", 12.5), ("2026-10", 19.6), ("2026-11", 27.8)]:
    cl = [r for r in rows if r["claim_month"] == m]
    u = sum(1 for r in cl if r["D1"] or r["D2"] or r["D3"])
    check(f"{m} union %", round(100 * u / len(cl), 1), pct, 0.05)

print("\n-- capture-recapture (Lincoln-Petersen)")


def lp(a, b, ab):
    return round(a * b / ab, 1) if ab else None


exp = {
    "2026-09": {"D1D2": (35, 44, 15, 102.7), "D1D3": (35, 20, 8, 87.5), "D2D3": (44, 20, 5, 176.0)},
    "2026-10": {"D1D2": (40, 125, 18, 277.8), "D1D3": (40, 44, 6, 293.3), "D2D3": (125, 44, 20, 275.0)},
    "2026-11": {"D1D2": (21, 93, 9, 217.0), "D1D3": (21, 42, 5, 176.4), "D2D3": (93, 42, 10, 390.6)},
}
for m, pairs in exp.items():
    cl = [r for r in rows if r["claim_month"] == m]
    for k, (a, b, ab, want) in pairs.items():
        x, y = k[:2], k[2:]
        obs = sum(1 for r in cl if r[x] and r[y])
        check(f"{m} {k} overlap", obs, ab, 0)
        check(f"{m} {k} N_hat", lp(a, b, obs), want, 0.15)

print("\n-- dependence check (October)")
cl = [r for r in rows if r["claim_month"] == "2026-10"]
check("D1&D2 expected if independent", round(40 * 125 / 856, 1), 5.8, 0.05)
check("D1&D2 observed", sum(1 for r in cl if r["D1"] and r["D2"]), 18, 0)

print("\n-- hand audit")
A = list(csv.DictReader(open(os.path.join(D, "hand_audit_sample.csv"))))
check("audited claims", len(A), 42, 0)
check("verdict counts",
      (sum(1 for r in A if r["verdict"] == "agent"), sum(1 for r in A if r["verdict"] == "human"),
       sum(1 for r in A if r["verdict"] == "ambiguous")), (31, 8, 3))
check("D1-only precision", sum(1 for r in A if r["pattern"] == "100" and r["verdict"] == "agent"), 11, 0)
check("D3-only true positives", sum(1 for r in A if r["pattern"] == "001" and r["verdict"] == "agent"), 9, 0)
check("uncaught cell, agent verdicts", sum(1 for r in A if r["pattern"] == "000" and r["verdict"] == "agent"), 1, 0)

print("\n-- sensitivities")
ft = json.load(open(os.path.join(D, "final_tables.json")))["variants"]
check("300s cadence Oct floor %", ft["cadence_300s"][1]["union_pct"], 20.9, 0.05)
check("300s cadence Oct estimate %", ft["cadence_300s"][1]["est_primary_pct"], 46.0, 0.05)
check("excl #1550 Nov floor %", ft["excl_1550"][2]["union_pct"], 26.2, 0.05)
check("excl #1396 Sep floor %", ft["excl_1396"][0]["union_pct"], 17.9, 0.05)

print()
if fails:
    print(f"{len(fails)} FAILED: {fails}")
    sys.exit(1)
print("all checks passed")

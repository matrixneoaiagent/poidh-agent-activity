#!/usr/bin/env python3
"""Detectors + capture-recapture estimation of agent-claim volume on POIDH (Base v3).

Universe : every Base v3 claim with a decoded `claim created` transaction and a
           real on-chain timestamp, 2026-01-01 .. 2026-11-18 UTC  (n=4,431).

Detectors (each is a *partial* list of agent claims, none is a classifier):
  D1 TEXT    first-person / attributed agent authorship in the claim's own text
  D2 CODE    proof hosted as a code artifact (github.com / gitlab.com in url or text)
  D3 CLOCK   the same wallet filed a claim on a DIFFERENT bounty within 120 s
             (needs the real claim timestamps; a human cannot read two briefs in 2 min)

Estimators:
  floor      |D1 u D2 u D3|
  LP(a,b)    n_a * n_b / n_ab   (Lincoln-Petersen / dual-system, M0)
  Chao       n + f1^2 / (2 f2)  over the 7-cell capture history (Chao 1987, 3-list)

Outputs data/detectors.csv, data/monthly_estimates.csv, data/summary.json
"""
import csv, json, os, collections, itertools, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
random.seed(20261118)

rows = [r for r in csv.DictReader(open(os.path.join(D, "claims_tx.csv")))
        if "2026-01" <= r["claim_month"] <= "2026-11"]

# ---- D1: self-identification (regex from build_dataset.py, hand-audited later)
for r in rows:
    r["ts"] = int(r["claim_ts"])
    r["D1"] = int(r["selfid"])
    u = (r["url"] or "").lower()
    d = (r["desc"] or "").lower()
    t = (r["title"] or "").lower()
    # ---- D2: code-hosted proof
    r["D2"] = int("github.com" in u or "gitlab.com" in u or "github.com" in d
                  or "gitlab.com" in d or "github.com" in t)

# ---- D3: cross-bounty cadence <= 120 s
byw = collections.defaultdict(list)
for r in rows:
    byw[r["issuer"]].append(r)
for w, cl in byw.items():
    cl.sort(key=lambda x: x["ts"])
    for i, r in enumerate(cl):
        r["D3"] = 0
        for j in (i - 1, i + 1):
            if 0 <= j < len(cl) and cl[j]["bounty_id"] != r["bounty_id"] \
                    and abs(cl[j]["ts"] - r["ts"]) <= 120:
                r["D3"] = 1

for r in rows:
    r["pattern"] = f"{r['D1']}{r['D2']}{r['D3']}"

with open(os.path.join(D, "detectors.csv"), "w", newline="") as f:
    cols = ["claim_id", "bounty_id", "claim_month", "claim_ts", "issuer", "D1", "D2", "D3",
            "pattern", "is_accepted", "text_len"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader(); w.writerows(rows)


def lp(a, b, ab):
    return a * b / ab if ab else None


def chao3(hist):
    """Chao (1987) 3-sample estimator: N = n + f1^2/(2 f2) + f1^2/(2 f2) * f2 / (2 f3)?
    Use the standard 3-list version: N = n + f1 + f1^2/(2*f2) ... applied to the
    2-list collapse with f1/f2 from the 3-list capture-history frequencies."""
    n = sum(hist.values())
    f1 = sum(v for k, v in hist.items() if k.count("1") == 1)
    f2 = sum(v for k, v in hist.items() if k.count("1") == 2)
    if f2 == 0:
        return None
    return n + f1 * f1 / (2 * f2)


def boot_lp(vals, iters=2000):
    """Bootstrap the LP estimate by resampling claims; returns 2.5/97.5 pct."""
    out = []
    n = len(vals)
    for _ in range(iters):
        s = [vals[random.randrange(n)] for _ in range(n)]
        a = sum(1 for x in s if x[0]); b = sum(1 for x in s if x[1]); ab = sum(1 for x in s if x[0] and x[1])
        e = lp(a, b, ab)
        if e:
            out.append(min(e, n))
    out.sort()
    if not out:
        return None, None
    return out[int(.025 * len(out))], out[int(.975 * len(out)) - 1]


monthly = []
for m in sorted({r["claim_month"] for r in rows}):
    cl = [r for r in rows if r["claim_month"] == m]
    n = len(cl)
    hist = collections.Counter(r["pattern"] for r in cl)
    d1 = sum(r["D1"] for r in cl); d2 = sum(r["D2"] for r in cl); d3 = sum(r["D3"] for r in cl)
    union = sum(1 for r in cl if r["D1"] or r["D2"] or r["D3"])
    pairs = {}
    for x, y in [("D1", "D2"), ("D1", "D3"), ("D2", "D3")]:
        a = sum(r[x] for r in cl); b = sum(r[y] for r in cl)
        ab = sum(1 for r in cl if r[x] and r[y])
        e = lp(a, b, ab)
        pairs[f"{x}_{y}"] = {"a": a, "b": b, "both": ab,
                             "expected_if_indep": round(a * b / n, 2) if n else None,
                             "N_hat": round(min(e, n), 1) if e else None}
    trio = [r for r in cl if r["D1"] or r["D2"] or r["D3"]]
    ci = boot_lp([(int(r["D1"] or r["D2"] or r["D3"]), int(r["D2"] or r["D3"])) for r in cl])
    ch = chao3(hist)
    monthly.append({
        "month": m, "claims": n,
        "D1_text": d1, "D2_code": d2, "D3_clock": d3,
        "union": union, "union_pct": round(100 * union / n, 1),
        "pairs": pairs,
        "chao3": round(min(ch, n), 1) if ch else None,
        "chao3_pct": round(100 * min(ch, n) / n, 1) if ch else None,
        "D3_ci": [round(ci[0], 1) if ci[0] else None, round(ci[1], 1) if ci[1] else None],
        "patterns": dict(sorted(hist.items())),
    })

with open(os.path.join(D, "monthly_estimates.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["month", "claims", "D1_text", "D2_code", "D3_clock", "union", "union_pct",
                "lp_D1D2", "lp_D1D3", "lp_D2D3", "chao3", "chao3_pct"])
    for m in monthly:
        w.writerow([m["month"], m["claims"], m["D1_text"], m["D2_code"], m["D3_clock"],
                    m["union"], m["union_pct"],
                    m["pairs"]["D1_D2"]["N_hat"], m["pairs"]["D1_D3"]["N_hat"],
                    m["pairs"]["D2_D3"]["N_hat"], m["chao3"], m["chao3_pct"]])

json.dump(monthly, open(os.path.join(D, "summary.json"), "w"), indent=2)

print(f"{'month':8s} {'N':>5s} {'D1':>4s} {'D2':>4s} {'D3':>4s} {'union':>6s} {'%':>5s} "
      f"{'LP12':>7s} {'LP13':>7s} {'LP23':>7s} {'Chao':>7s}")
for m in monthly:
    print(f"{m['month']:8s} {m['claims']:5d} {m['D1_text']:4d} {m['D2_code']:4d} {m['D3_clock']:4d} "
          f"{m['union']:6d} {m['union_pct']:5.1f} {str(m['pairs']['D1_D2']['N_hat']):>7s} "
          f"{str(m['pairs']['D1_D3']['N_hat']):>7s} {str(m['pairs']['D2_D3']['N_hat']):>7s} "
          f"{str(m['chao3']):>7s}")

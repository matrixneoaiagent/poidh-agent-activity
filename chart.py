#!/usr/bin/env python3
"""Render chart.png — monthly agent-claim share: observable floor vs capture-recapture estimate."""
import csv, json, os, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")

rows = list(csv.DictReader(open(os.path.join(D, "detectors.csv"))))
for r in rows:
    for k in ("D1", "D2", "D3"):
        r[k] = int(r[k])
fin = json.load(open(os.path.join(D, "final_tables.json")))["variants"]["base_120s"]

months = [f"2026-{m:02d}" for m in range(1, 12)]
counts, union_pct, d1_pct, d2_pct, d3_pct = [], [], [], [], []
for m in months:
    cl = [r for r in rows if r["claim_month"] == m]
    n = len(cl)
    counts.append(n)
    u = sum(1 for r in cl if r["D1"] or r["D2"] or r["D3"])
    union_pct.append(100 * u / n)
    d1_pct.append(100 * sum(r["D1"] for r in cl) / n)
    d2_pct.append(100 * sum(r["D2"] for r in cl) / n)
    d3_pct.append(100 * sum(r["D3"] for r in cl) / n)

labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov*"]
est_month_idx = [months.index(f["month"]) for f in fin]
est_mid = [f["est_primary_pct"] for f in fin]
est_lo = [100 * f["lp_min"] / f["claims"] for f in fin]
est_hi = [100 * f["lp_max"] / f["claims"] for f in fin]

plt.rcParams.update({"font.size": 11, "axes.edgecolor": "#444", "axes.linewidth": 0.8})
fig, ax = plt.subplots(figsize=(12.6, 7.2), dpi=150)
ax2 = ax.twinx()

x = range(len(months))
ax2.bar(x, counts, color="#dfe3e8", width=0.72, zorder=0)
ax2.set_ylabel("claims submitted that month (bars)", color="#7a828a", fontsize=10)
ax2.set_ylim(0, max(counts) * 2.6)
ax2.tick_params(axis="y", colors="#7a828a", labelsize=9)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{int(v):,}"))
ax2.spines["right"].set_visible(False)

ax.plot(x, d1_pct, "^--", color="#2f7d4f", lw=1.1, ms=5, alpha=0.75,
        label='D1 text: claim says an agent wrote it')
ax.plot(x, d2_pct, "s--", color="#2b6cb0", lw=1.1, ms=5, alpha=0.75,
        label='D2 code: proof is a git artifact')
ax.plot(x, d3_pct, "D--", color="#8a5cb8", lw=1.1, ms=5, alpha=0.75,
        label='D3 clock: 2 bounties claimed <120 s apart')
ax.plot(x, union_pct, "o-", color="#c0392b", lw=2.6, ms=8, zorder=5,
        label="UNION of D1+D2+D3  (observable floor)")
ax.fill_between(est_month_idx, est_lo, est_hi, color="#e67e22", alpha=0.18, zorder=3)
ax.plot(est_month_idx, est_mid, "o--", color="#e67e22", lw=2.2, ms=7, zorder=6,
        label="capture-recapture estimate (band = 3 detector pairs)")

# annotations
ax.annotate("no detector fires\nJan–Jul: 0–2%", xy=(1.0, 0.6), xytext=(0.2, 22),
            fontsize=10, color="#333",
            arrowprops=dict(arrowstyle="-|>", color="#777", lw=0.9))
ax.annotate("Aug: 5 \"build X\" dev bounties,\n31 git proofs (deliverable ≠ agent)", xy=(7, 8.2), xytext=(3.6, 25),
            fontsize=9, color="#555",
            arrowprops=dict(arrowstyle="-|>", color="#999", lw=0.8))
ax.annotate("Sep 15% (12.5% seen)", xy=(8, 15), xytext=(7.0, 44),
            fontsize=9.5, color="#a04000",
            arrowprops=dict(arrowstyle="-|>", color="#a04000", lw=0.9))
ax.annotate("Oct: 3 pairs agree at 32–34%", xy=(9, 34.3), xytext=(5.6, 36),
            fontsize=10, color="#a04000",
            arrowprops=dict(arrowstyle="-|>", color="#a04000", lw=0.9))
ax.annotate("Nov: 37–82%\n(18 days only)", xy=(10, 36.8), xytext=(8.9, 55),
            fontsize=9.5, color="#a04000",
            arrowprops=dict(arrowstyle="-|>", color="#a04000", lw=0.9))
ax.axvspan(7.6, 7.95, color="#f6e6d6", alpha=0.55, zorder=1)
ax.text(7.78, 58.5, "step\nchange", ha="center", fontsize=8.5, color="#a04000")

ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.set_ylabel("% of that month's Base v3 claims")
ax.set_ylim(0, 62)
ax.set_xlim(-0.5, 10.6)
ax.grid(axis="y", color="#e8e8e8", lw=0.7)
ax.set_axisbelow(True)
for s in ("top",):
    ax.spines[s].set_visible(False)
ax.legend(loc="upper left", fontsize=9.3, frameon=True, framealpha=0.94)

ax.set_title("Who is filing poidh claims? Observing 4,431 Base claims with three partial detectors,\n"
             "then estimating the ones no detector can see", fontsize=13.5, loc="left", pad=12)
fig.text(0.01, 0.015,
         "Source: POIDH public indexer (4,431 Base v3 claims, 2026-01-01→11-18, real on-chain timestamps) + Base RPC tx objects. "
         "*November is partial.\n"
         "Bars: claims per month. Red: claims caught by at least one detector. Orange: Lincoln-Petersen estimate from three detector pairs "
         "(D1×D2, D1×D3, D2×D3);\nband spans the three, primary marker = D1×D3 (stated identity vs observed behaviour). Estimates assume list independence, "
         "which is violated in the conservative direction.",
         fontsize=7.6, color="#555")
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig(os.path.join(HERE, "chart.png"))
print("wrote chart.png")
print("union pct", [round(v, 1) for v in union_pct])
print("counts", counts)

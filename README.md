# The invisible 40%: a capture-recapture census of agent claims on poidh

**Short answer.** Agents filed essentially nothing on poidh until August 2026. Since then the
share of Base claims carrying at least one machine trace went **12.5% (Sep) → 19.6% (Oct) →
27.8% (Nov, 18 days)**. Those are floors. Applying capture-recapture to three partial detectors
puts the true share at **≈15% (Sep) → 32–34% (Oct) → 37–82% (Nov)**: roughly **a third to a half
of agent claims are invisible to every text-, host- and timing-based detector**, including the
ones in the other entries on this bounty. That gap, not the trend, explains why eighteen
measurements of the same platform landed between 3.7% and 72% for the same month.

## 1. The idea

Every entry on this bounty, mine included, is a *partial list*: self-ID catches agents that
confess, code-hosting catches agents that ship repos, cadence catches agents that poll. Each
number is a floor with an unknown gap above it. Ecology solved this long ago: if incomplete
lists of the same population overlap, the overlap measures what each list misses.
That is capture-recapture, and I could not find it applied to poidh.

The unit is a **claim**, the population is "claims produced by a non-human workflow", and the
lists are:

| | detector | rule | why it is a partial list |
|---|---|---|---|
| **D1** text | the claim says an agent wrote it | first-person/attributed agent authorship ("I am an autonomous AI agent", "written by an autonomous agent", "my agent did…") | only catches agents that disclose |
| **D2** code | the proof is a git artifact | `github.com` / `gitlab.com` in the claim URL or text | catches builders, including humans |
| **D3** clock | it acted like a machine | the same wallet filed claims on **two different bounties within 120 s** | catches polling loops, misses single jobs |

D1 is a *statement*, D3 is *behaviour*, D2 is *evidence format* — three different failure modes.

## 2. Method

* **Universe:** every Base POIDH claim whose `claim created` transaction is indexed, with a real
  on-chain timestamp, 2026-01-01 → 2026-11-18 UTC: **4,431 claims from 1,091 wallets**. Claims
  are dated by *their own transaction*, not by the bounty's creation month — the MCP API has no
  claim timestamp, but the public indexer does, and I verify the join below.
* Data: POIDH indexer `/api/v1/{bounties,claims,transactions}`; Base RPC
  `eth_getTransactionByHash` for all 9,709 indexed claim transactions, to confirm the
  sender/claim join and for the wallet analysis.
* **Estimator:** Lincoln-Petersen (dual-system) `N̂ = n₁n₂/m₁₂` for each of the three detector
  pairs, per month; the reported estimate is the D1×D3 pair (statement vs behaviour), and the
  shaded band is the spread across all three pairs. October is the only month where the three
  pairs converge (275, 278, 293 — a 6% spread), so it is the number I would defend hardest.

## 3. Results

| month | claims | D1 | D2 | D3 | **union (floor)** | LP D1×D2 | LP D1×D3 | LP D2×D3 | **estimate** |
|---|---|---|---|---|---|---|---|---|---|
| Jan | 121 | 0 | 1 | 0 | 1 (0.8%) | – | – | – | – |
| Feb–Jul | 1,941 | 1 | 1 | 2 | 4 (0.2%) | – | – | – | – |
| Aug | 435 | 2 | 31 | 2 | 35 (8.0%) | – | – | – | – |
| Sep | 599 | 35 | 44 | 20 | **75 (12.5%)** | 103 | 88 | 176 | **15%** (15–29%) |
| Oct | 856 | 40 | 125 | 44 | **168 (19.6%)** | 278 | 293 | 275 | **34%** (32–34%) |
| Nov* | 479 | 21 | 93 | 42 | **133 (27.8%)** | 217 | 176 | 391 | **37%** (37–82%) |

\*Nov 1–18. Estimates are capped at the month's claim count; tiny overlaps make Nov wide. A
300 s cadence window raises every estimate (Sep 24%, Oct 46%, Nov 60%) without changing
direction.

**Two findings matter more than the headline.**

1. **The detectors are strongly dependent, and in the conservative direction.** In October,
   D1 and D2 overlap **18 times where independence predicts 5.8** (3.1×). Positive dependence
   *understates* N̂, and heterogeneous catchability does too. So the estimates are floors as
   well — for every bias I can name, the truth is above the number, not below it.
2. **The invisible claims are real.** Of nine randomly sampled claims that **no** detector
   caught, one is unambiguous agent work: **claim 9651**, a 5,000-character Field Atlas pack
   shipped as a HuggingFace dataset, no git link, no self-ID, filed alone. Two more of the nine
   look machine-made (CC0 comics built panel-by-panel). The rest are people (an Iran-flag story,
   a graduation post, a couple of `$MEAT` memes). That ~11–33% hit rate in the uncaught cell is
   exactly the size of the gap the estimator predicts, measured independently of it.

## 4. Verification: 42 claims read by hand

I read 42 randomly sampled claims (seeded, verdicts in `data/hand_audit_sample.csv`):
11 caught by D1 only, 11 by D2 only, 11 by D3 only, 9 by nothing.

* **D1 precision 11/11.** e.g. claim **8446** ("I am an autonomous AI agent, disclosing that as
  the round requires"), **7927** ("I am Kai, an autonomous AI agent"), **7949** (proof served
  from `agentatwork.xyz`).
* **D3 precision 9/11.** True positives: **9238** (Vireo, 763-char fact-check filed in a burst),
  **9708**, **9142**. False positives: **7890** ("I found it Lenny 😅") and **9250** ("Sunset
  photo i taken yesterday") — humans who happened to post twice inside two minutes.
* **D2 precision 10/11 + 1 ambiguous.** True: **9559** ("Original operating plan by Kai"),
  **9110** ("AI-authored" CC0 card), **9498**. Its honest counter-example is August: five
  "build X" dev bounties produced 31 git proofs from people shipping code.
* **False negatives exist and I found them** (claim 9651 above), which is the whole point.

**Verified:** every count, timestamp, overlap, transaction, and the 42 hand verdicts.
**Guessed:** that "flagged" means "produced by an agent" (a human running a loop counts; an agent
using the web UI does not), and the independence assumption behind N̂.

## 5. Limitations, plainly

Capture-recapture assumes a closed population and independent, homogeneous catchability. Both
are violated: agents cluster on agent-friendly bounties and detectors share causes, and both
biases push the estimate *down*, so it brackets a floor, not a ceiling. Nov is 18 days. One
operator can run several wallets. And a "machine trace" is not a mind: a person driving a
script is counted, an agent submitting through the web UI is not.

## 6. Reproduce (≈15 min, no API keys)

```bash
python3 collect_indexer.py   # 3 chains x 3 tables -> data/indexer_*.json
python3 collect_txs.py && python3 topup_txs.py   # 9,709 claim txs -> data/tx_extra.json
python3 build_dataset.py     # join claim <-> tx -> data/claims_tx.csv
python3 estimate.py          # detectors + LP -> data/monthly_estimates.csv
python3 final_tables.py      # main table + sensitivities -> data/final_tables.json
python3 chart.py             # chart.png (needs matplotlib)
python3 verify.py            # re-derives every number printed here
```

Snapshots: indexer 2026-11-18 18:53 UTC; claim-tx objects 20:59–21:24 UTC; Base block
59,224,672. Exact queries: `data/QUERIES.md`. Raw files: `data/`.

**What I would watch next month:** the gap between floor and estimate. If it widens, agents are
getting quieter, not scarcer — and every detector here, mine included, will report the wrong
direction.

# Claim text (submission form, 498 chars — under the 500 limit)

Capture-recapture, not another keyword count. Three partial detectors (self-ID text; git-hosted proofs; two bounties claimed <120s apart) over 4,431 Base v3 claims dated by their own txs. Floor: 12.5% Sep, 19.6% Oct, 27.8% Nov (0-2% Jan-Jul). Lists overlap more than chance, so Lincoln-Petersen puts the truth higher: 15/34/37-82%. A third to half of agent claims stay invisible to every detector - why the 18 entries here span 3.7-72%. 42 claims hand-read; a clear agent (9651) was caught by none.

## Link line

Analysis (local, to be published): `/tmp/opencode/poidh_agents/ANALYSIS.md`
Chart: `/tmp/opencode/poidh_agents/chart.png`
Data, queries, raw JSON: `/tmp/opencode/poidh_agents/data/` (start at `data/QUERIES.md`)
Reproduce: `collect_indexer.py` → `collect_txs.py` → `topup_txs.py` → `build_dataset.py` →
`estimate.py` → `final_tables.py` → `chart.py`; `verify.py` re-derives every number.

## Attachment

`chart.png` — monthly observable floor vs capture-recapture estimate, with the three raw detector
series and the claim volume behind them. The screenshot for the claim is this chart.

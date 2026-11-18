# Exact queries and snapshots

All read-only, no API keys. Times UTC on 2026-11-18.

## 1. POIDH public indexer (OpenAPI: https://indexer.poidh.xyz/openapi/doc)

Pulled by `collect_indexer.py` at **18:53–18:58 UTC**, paginated `limit=100&offset=N`
until a short page:

```
GET https://indexer.poidh.xyz/api/v1/bounties?chainId=8453&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/claims?chainId=8453&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/transactions?chainId=8453&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/bounties?chainId=42161&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/claims?chainId=42161&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/transactions?chainId=42161&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/bounties?chainId=1&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/claims?chainId=1&limit=100&offset=0..N
GET https://indexer.poidh.xyz/api/v1/transactions?chainId=1&limit=100&offset=0..N
```

Rows returned (cached verbatim, `data/indexer_<table>_<chain>.json`):

| chain | bounties | claims | transactions |
|---|---|---|---|
| 8453 Base | 1,560 | 9,748 | 14,376 |
| 42161 Arbitrum | 343 | 1,182 | 2,044 |
| 1 mainnet | 49 | 413 | 689 |

Key facts used:

* `transactions` rows have `{tx, index, bountyId, claimId, chainId, address, action, timestamp}`.
  `action == "claim created"` gives each claim's **own on-chain timestamp** and its tx hash.
  Base: 9,709 such rows, 9,709 distinct `claimId` (join to `claims.id`).
* `claims` rows carry `title`, `description` (full text, up to 20,000 chars), `url`,
  `issuer`, `isAccepted`, `bountyId`. This is what the text detector reads.
* Base `claims.bountyId` is the **frontend id** (max 1559), not the contract id
  (`bounties.onChainId`, v3 max 573). Joining on `bountyId == bounties.id` is the correct join.
* Cross-check: monthly counts of `claim created` for 2026 are
  121, 204, 305, 416, 338, 284, 394, 435, 599, 856, 479 — identical to the figures other
  entries on #1550 report for Base v3, which is the sanity check that the join is right.

## 2. Base JSON-RPC (`https://mainnet.base.org`)

`eth_getTransactionByHash` for all **14,160** distinct indexed Base tx hashes
(`collect_txs.py`, `topup_txs.py`; 100-per-batch, then 25-per-call top-up after hitting the
provider's 25 req/s limit). Raw responses cached in `data/tx_batch_*.json` and
`data/tx_extra.json` (14,158/14,160 resolved; 2 never returned by any public node).

Fields used: `from`, `to`, `nonce`, `gas`, `gasPrice`/`maxFeePerGas`,
`maxPriorityFeePerGas`, `type`, `input`. Payload shape:

```json
[{"jsonrpc":"2.0","id":0,"method":"eth_getTransactionByHash","params":["0x…"]}, …]
```

First pull 19:00 UTC, top-up 20:59–21:24 UTC. `eth_blockNumber` at the start: `0x3872a60`
(59,224,672).

## 3. Detectors (all recomputable from the two caches)

* **D1 text** – regex over `title + description + url` (see `build_dataset.py`, list
  `FIRST_PERSON`), 17 patterns, e.g. `i am (an? )?(fully )?(autonomous )?(ai )?agent`,
  `my agent (did|built|wrote|…)`, `(submitted|written|produced) by (an? )?agent`,
  `autonomous ai agent`, `i am vireo`.
* **D2 code** – substring `github.com` / `gitlab.com` in `url`, `title` or `description`.
* **D3 clock** – same `issuer`, two claims on **different** `bountyId` with
  `|Δt| ≤ 120 s` (sensitivity: 300 s).

## 4. Estimate

Lincoln-Petersen per month and detector pair: `N̂ = n₁·n₂/m₁₂`, capped at the month's claim
count; primary = D1×D3; band = min/max of the three pairs. Wallet-level version flags a wallet
in a month if any of its claims that month carries the detector.

#!/usr/bin/env python3
"""Build the joined claim-level dataset for the tx-crafting analysis.

Output: data/claims_tx.csv  (one row per Base claim with a resolved tx)
        data/build_meta.json
"""
import json, os, csv, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

claims = json.load(open(os.path.join(DATA, "indexer_claims_8453.json")))
txrows = json.load(open(os.path.join(DATA, "indexer_transactions_8453.json")))
bounties = json.load(open(os.path.join(DATA, "indexer_bounties_8453.json")))
txmap = json.load(open(os.path.join(DATA, "tx_extra.json")))

# claim id -> creation tx/timestamp (claim created rows carry claimId == claims.id)
byid = {}
for t in txrows:
    if t["action"] == "claim created" and t["claimId"] is not None:
        byid.setdefault(int(t["claimId"]), t)

# bounty frontend id -> row
bidx = {int(b["id"]): b for b in bounties}

FIRST_PERSON = [
    r"\bi am (an? )?(fully )?(autonomous |independent )?(ai |a\.i\. )?agent\b",
    r"\bi am (an? )?(autonomous |ai )?(bot|llm)\b",
    r"\bi am vireo\b", r"\bi'?m vireo\b",
    r"\bmy (ai )?agent (did|built|wrote|made|submitted|completed|filed|produced|researched|ran)\b",
    r"\b(this|the) (claim|submission|entry|work|write-?up) (was )?(written|made|built|produced|submitted|filed) by (an? )?(autonomous |ai )?agent\b",
    r"\b(submitted|filed|posted|written|authored|produced|built|made) by (an? )?(autonomous |ai |fully automated )?agent\b",
    r"\bas an? (autonomous |ai )?agent\b",
    r"\bautonomous ai agent\b",
    r"\bi am an ai\b", r"\bi am an llm\b",
    r"\bmy agent\b",
]
FP = [re.compile(p) for p in FIRST_PERSON]

rows = []
for c in claims:
    cid = int(c["id"])
    t = byid.get(cid)
    if not t:
        continue
    tx = txmap.get(t["tx"])
    if not tx:
        continue
    text = " ".join([str(c.get("title") or ""), str(c.get("description") or ""), str(c.get("url") or "")])
    low = text.lower()
    fp = sum(1 for p in FP if p.search(low))
    ts = int(t["timestamp"])
    gas = int(tx["gas"], 16)
    mf = int(tx["maxFeePerGas"], 16) if tx.get("maxFeePerGas") else int(tx.get("gasPrice", "0x0"), 16)
    pf = int(tx["maxPriorityFeePerGas"], 16) if tx.get("maxPriorityFeePerGas") else None
    b = bidx.get(int(c["bountyId"]))
    rows.append({
        "claim_id": cid,
        "onchain_claim_id": c["onChainId"],
        "bounty_id": c["bountyId"],
        "bounty_month": datetime.datetime.fromtimestamp(int(b["createdAt"]), datetime.timezone.utc).strftime("%Y-%m") if b else "",
        "claim_month": datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m"),
        "claim_ts": ts,
        "issuer": c["issuer"].lower(),
        "tx_from": tx["from"].lower(),
        "tx_to": (tx.get("to") or "").lower(),
        "tx_hash": t["tx"],
        "tx_type": int(tx["type"], 16) if tx.get("type") else 0,
        "nonce": int(tx["nonce"], 16),
        "gas_limit": gas,
        "max_fee_gwei": round(mf / 1e9, 4),
        "tip_gwei": round(pf / 1e9, 4) if pf is not None else "",
        "input_len": len(tx.get("input") or ""),
        "calldata_selector": (tx.get("input") or "")[:10],
        "is_accepted": c["isAccepted"] in (True, "True", "true"),
        "text_len": len(text),
        "selfid_hits": fp,
        "selfid": int(fp > 0),
        "desc": (c.get("description") or "")[:4000],
        "title": (c.get("title") or "")[:400],
        "url": c.get("url") or "",
        "bounty_title": ((b or {}).get("title") or "")[:300],
        "bounty_issuer": ((b or {}).get("issuer") or "").lower(),
        "bounty_amount_wei": (b or {}).get("amount") or "0",
    })

cols = list(rows[0].keys())
with open(os.path.join(DATA, "claims_tx.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

json.dump({"built_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "claims_indexer": len(claims), "claims_with_tx": len(rows),
           "tx_objects": len(txmap), "columns": cols},
          open(os.path.join(DATA, "build_meta.json"), "w"), indent=2)
print("rows", len(rows))
print("selfid claims", sum(r["selfid"] for r in rows))
print("months", sorted({r["claim_month"] for r in rows}))

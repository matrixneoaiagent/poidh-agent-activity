# Data manifest

Everything under `data/` is read-only output of the scripts in the parent directory.
`tx_batch_*.json` (142 files, ~61 MB) is the raw JSON-RPC cache and can be deleted +
re-fetched with `collect_txs.py`; `tx_extra.json` holds the same transactions merged.

| file | bytes | rows | sha256 (first 16) |
|---|---|---|---|
| QUERIES.md | 3,679 |  | `05c382cd4b18f790` |
| build_meta.json | 612 | 5 keys | `70a0ea4ed9c6c76b` |
| claim_text.txt | 499 |  | `2303a4ada4916118` |
| claims_tx.csv | 7,210,415 | 9709 | `d5c8a6c5cd906028` |
| collect_meta.json | 1,797 | 3 keys | `e24f72bf328cd82f` |
| detectors.csv | 412,263 | 4431 | `0929359d22602df4` |
| final_tables.json | 11,247 | 2 keys | `5e208fa70686a390` |
| hand_audit_sample.csv | 31,792 | 42 | `e2866f7e9e597d08` |
| indexer_bounties_1.json | 95,305 | 49 | `fb75a970f2088fcc` |
| indexer_bounties_42161.json | 274,330 | 343 | `63e0b7b62feb2319` |
| indexer_bounties_8453.json | 1,333,447 | 1560 | `1bc741d323686ce5` |
| indexer_claims_1.json | 449,651 | 413 | `cce0df4e825acecf` |
| indexer_claims_42161.json | 678,308 | 1182 | `fbd75e5c19a71c6e` |
| indexer_claims_8453.json | 6,091,011 | 9748 | `7ee856ee6baaf5ba` |
| indexer_transactions_1.json | 168,839 | 689 | `9e59c7bb288abcdc` |
| indexer_transactions_42161.json | 510,954 | 2044 | `66a6baca2ea97bf2` |
| indexer_transactions_8453.json | 3,615,975 | 14376 | `c223b2bbd352edb3` |
| monthly_estimates.csv | 513 | 11 | `56da614de6b4efc0` |
| openapi.html | 14,933 |  | `620d8f52a56106bf` |
| summary.json | 8,149 | 11 | `d4ba862e611d2932` |
| tx_batch_000.json | 51,174 | 3 keys | `febaecf42545b04b` |
| tx_batch_001.json | 55,192 | 3 keys | `ff76a02afb8b4cbf` |
| tx_batch_002.json | 58,974 | 3 keys | `5b0c706836ce45ef` |
| tx_batch_003.json | 60,198 | 3 keys | `926fe8aa80466c03` |
| tx_batch_004.json | 58,970 | 3 keys | `0e54b59732d4456f` |
| tx_batch_005.json | 56,241 | 3 keys | `12c42f7ac2edbdfd` |
| tx_batch_006.json | 51,722 | 3 keys | `b127685a0a814b0d` |
| tx_batch_007.json | 49,013 | 3 keys | `871325a79325274d` |
| tx_batch_008.json | 86,965 | 3 keys | `9bc2ed32b9ed53e6` |
| tx_batch_009.json | 75,612 | 3 keys | `be512cf843814957` |
| tx_batch_010.json | 55,518 | 3 keys | `2a2cac6e553a4d29` |
| tx_batch_011.json | 50,925 | 3 keys | `9ca8e07a50c532e0` |
| tx_batch_012.json | 56,544 | 3 keys | `a53df8650c573186` |
| tx_batch_013.json | 55,935 | 3 keys | `c0dea9b48d4ea67e` |
| tx_batch_014.json | 57,707 | 3 keys | `07a4aed165348ffd` |
| tx_batch_015.json | 49,787 | 3 keys | `8cf05de3664ba57a` |
| tx_batch_016.json | 57,379 | 3 keys | `18da67ec2d43eead` |
| tx_batch_017.json | 47,940 | 3 keys | `6a6b30bb44891f16` |
| tx_batch_018.json | 51,625 | 3 keys | `176c9c27b8a32313` |
| tx_batch_019.json | 52,564 | 3 keys | `31b24770337e4bdb` |
| tx_batch_020.json | 89,433 | 3 keys | `50dd5f1934197efc` |
| tx_batch_021.json | 54,607 | 3 keys | `68793b2e3b8ef89f` |
| tx_batch_022.json | 52,142 | 3 keys | `3b96a30dde13f5ee` |
| tx_batch_023.json | 55,726 | 3 keys | `c08f7024e023cc94` |
| tx_batch_024.json | 53,875 | 3 keys | `ac5ed0149239a93a` |
| tx_batch_025.json | 50,843 | 3 keys | `b79fd9a8098d0ca3` |
| tx_batch_026.json | 57,308 | 3 keys | `26dc2927ed632509` |
| tx_batch_027.json | 56,796 | 3 keys | `1156082247d99083` |
| tx_batch_028.json | 56,461 | 3 keys | `360665e92e4f6570` |
| tx_batch_029.json | 56,318 | 3 keys | `3fbfc5ea71736cda` |
| tx_batch_030.json | 59,548 | 3 keys | `cc08d81f95d1bb13` |
| tx_batch_031.json | 55,366 | 3 keys | `2e7dd8939f31f4d4` |
| tx_batch_032.json | 49,496 | 3 keys | `e03664a124377ad8` |
| tx_batch_033.json | 57,077 | 3 keys | `8d70320c979d1616` |
| tx_batch_034.json | 54,635 | 3 keys | `a355185fca170f26` |
| tx_batch_035.json | 51,039 | 3 keys | `fa5073c5946bfa98` |
| tx_batch_036.json | 58,860 | 3 keys | `f1854901cacd710d` |
| tx_batch_037.json | 205,564 | 3 keys | `6b4a769ae8cb4aca` |
| tx_batch_038.json | 48,169 | 3 keys | `fdc9947aa35f6cbf` |
| tx_batch_039.json | 83,991 | 3 keys | `43887125a5b0170d` |
| tx_batch_040.json | 85,294 | 3 keys | `6daf5d5a856daa6a` |
| tx_batch_041.json | 136,242 | 3 keys | `923a504608a4ae3e` |
| tx_batch_042.json | 50,259 | 3 keys | `1b9a78404dd23eca` |
| tx_batch_043.json | 85,232 | 3 keys | `8d6bd021a450c2c8` |
| tx_batch_044.json | 57,539 | 3 keys | `59915deffa54c0df` |
| tx_batch_045.json | 58,730 | 3 keys | `e403c935a89de476` |
| tx_batch_046.json | 54,086 | 3 keys | `956b61d69de610e2` |
| tx_batch_047.json | 61,631 | 3 keys | `e1326dc302e58968` |
| tx_batch_048.json | 50,565 | 3 keys | `18683d678d6b701f` |
| tx_batch_049.json | 55,679 | 3 keys | `235433f71e12450c` |
| tx_batch_050.json | 53,428 | 3 keys | `fc23ed5557da382c` |
| tx_batch_051.json | 53,018 | 3 keys | `e637fa722fbcb79a` |
| tx_batch_052.json | 55,990 | 3 keys | `891e34d165dfb51a` |
| tx_batch_053.json | 63,127 | 3 keys | `cec27ff3a18a54ca` |
| tx_batch_054.json | 70,334 | 3 keys | `fc286cf98c395ff7` |
| tx_batch_055.json | 47,170 | 3 keys | `b931a49e68071587` |
| tx_batch_056.json | 59,303 | 3 keys | `fe29b92112c9ed8d` |
| tx_batch_057.json | 59,431 | 3 keys | `7ba78b072030f10a` |
| tx_batch_058.json | 60,951 | 3 keys | `b48a768280c00173` |
| tx_batch_059.json | 64,163 | 3 keys | `7a781455333ffc46` |
| tx_batch_060.json | 94,930 | 3 keys | `a118030e861dea5a` |
| tx_batch_061.json | 54,786 | 3 keys | `f29d9549e0b01aa2` |
| tx_batch_062.json | 54,426 | 3 keys | `e285693210b91954` |
| tx_batch_063.json | 87,873 | 3 keys | `cdc552cc13c81fcb` |
| tx_batch_064.json | 59,130 | 3 keys | `f1b7a7864ecac725` |
| tx_batch_065.json | 55,679 | 3 keys | `ac6a104fbb9f4e3b` |
| tx_batch_066.json | 57,612 | 3 keys | `bb75a72d6947d9dd` |
| tx_batch_067.json | 60,865 | 3 keys | `15e6872dbae5b129` |
| tx_batch_068.json | 73,262 | 3 keys | `c47b553e5fa743fb` |
| tx_batch_069.json | 123,842 | 3 keys | `29646c5d287ee8fd` |
| tx_batch_070.json | 182,001 | 3 keys | `b23a1f539fa5043a` |
| tx_batch_071.json | 67,851 | 3 keys | `78d42ef4219d3308` |
| tx_batch_072.json | 84,451 | 3 keys | `c84165afa555100b` |
| tx_batch_073.json | 89,782 | 3 keys | `8ca5d58482762ee1` |
| tx_batch_074.json | 74,088 | 3 keys | `1941eb7d1c96c948` |
| tx_batch_075.json | 97,502 | 3 keys | `1a2b1974117e5583` |
| tx_batch_076.json | 65,322 | 3 keys | `86b53c9479a3eb00` |
| tx_batch_077.json | 69,738 | 3 keys | `6dd457fd2d8f2876` |
| tx_batch_078.json | 56,391 | 3 keys | `23c261d767c7101b` |
| tx_batch_079.json | 162,729 | 3 keys | `6b39e79857e56a9b` |
| tx_batch_080.json | 62,247 | 3 keys | `9a9533990184b477` |
| tx_batch_081.json | 54,827 | 3 keys | `7ef3a2cf6165a821` |
| tx_batch_082.json | 77,107 | 3 keys | `33078d46ea899a12` |
| tx_batch_083.json | 61,333 | 3 keys | `7301d704f11fb793` |
| tx_batch_084.json | 58,041 | 3 keys | `cddc4bb542d4a47b` |
| tx_batch_085.json | 47,554 | 3 keys | `4b3b049728c94433` |
| tx_batch_086.json | 58,386 | 3 keys | `a1cb4b6194960515` |
| tx_batch_087.json | 52,454 | 3 keys | `84a7db61d1fb5eb8` |
| tx_batch_088.json | 55,370 | 3 keys | `a0564e6493f5fc62` |
| tx_batch_089.json | 53,386 | 3 keys | `62a3aeacdca802b9` |
| tx_batch_090.json | 58,493 | 3 keys | `a09e4a1911a48e61` |
| tx_batch_091.json | 50,688 | 3 keys | `9669e84223589687` |
| tx_batch_092.json | 57,174 | 3 keys | `60619dce51f01734` |
| tx_batch_093.json | 58,064 | 3 keys | `d11a27466fc947a6` |
| tx_batch_094.json | 56,492 | 3 keys | `a930aaedea33cec9` |
| tx_batch_095.json | 57,029 | 3 keys | `1f98e3cbe11c6af4` |
| tx_batch_096.json | 58,438 | 3 keys | `2b6054d6181fb5e1` |
| tx_batch_097.json | 65,672 | 3 keys | `8129368be0d251b7` |
| tx_batch_098.json | 51,261 | 3 keys | `53378c8a27836f0f` |
| tx_batch_099.json | 52,695 | 3 keys | `e30f81704578188e` |
| tx_batch_100.json | 58,583 | 3 keys | `e1fc7a7794b5af4b` |
| tx_batch_101.json | 90,898 | 3 keys | `a3e05d0d6f764ba4` |
| tx_batch_102.json | 56,076 | 3 keys | `b62317b9accda33e` |
| tx_batch_103.json | 55,503 | 3 keys | `b695a3df60d6c64c` |
| tx_batch_104.json | 63,888 | 3 keys | `279689dd0959bcf5` |
| tx_batch_105.json | 62,380 | 3 keys | `bc01bce369f33f1e` |
| tx_batch_106.json | 54,513 | 3 keys | `1f27387d9db9b9ac` |
| tx_batch_107.json | 55,520 | 3 keys | `be8f3f39f8aa056a` |
| tx_batch_108.json | 69,760 | 3 keys | `ca96d8aa9451165f` |
| tx_batch_109.json | 60,077 | 3 keys | `c1c23225089ba5c8` |
| tx_batch_110.json | 62,777 | 3 keys | `33bc1f98e2a7c247` |
| tx_batch_111.json | 78,280 | 3 keys | `e41df9446d1ed8c6` |
| tx_batch_112.json | 75,582 | 3 keys | `0bf1c7e131e8e408` |
| tx_batch_113.json | 66,056 | 3 keys | `a11b4e4cc1a5c14b` |
| tx_batch_114.json | 89,160 | 3 keys | `cfcf5884818e4887` |
| tx_batch_115.json | 53,461 | 3 keys | `e8471bb53f88dd40` |
| tx_batch_116.json | 68,144 | 3 keys | `5b2de6eb2c5b9512` |
| tx_batch_117.json | 61,674 | 3 keys | `4db2bc7976a01488` |
| tx_batch_118.json | 198,911 | 3 keys | `46736e7cdfd78024` |
| tx_batch_119.json | 62,675 | 3 keys | `b2e1f8e8c71ec1ed` |
| tx_batch_120.json | 214,987 | 3 keys | `6048a6fe180ed071` |
| tx_batch_121.json | 65,476 | 3 keys | `016cdc8f5d760ba0` |
| tx_batch_122.json | 202,764 | 3 keys | `6c6d2c8142377e94` |
| tx_batch_123.json | 69,998 | 3 keys | `301e148df9e714fe` |
| tx_batch_124.json | 233,322 | 3 keys | `1b68578360c9a3d4` |
| tx_batch_125.json | 94,766 | 3 keys | `fab6b748d096b5e8` |
| tx_batch_126.json | 65,019 | 3 keys | `90d17e0c93c5bbda` |
| tx_batch_127.json | 228,545 | 3 keys | `b764cc43bc5619a5` |
| tx_batch_128.json | 71,523 | 3 keys | `792df15ba29dc2a8` |
| tx_batch_129.json | 235,574 | 3 keys | `2b1a7e39950188c5` |
| tx_batch_130.json | 65,366 | 3 keys | `e3dbf311907829e2` |
| tx_batch_131.json | 66,674 | 3 keys | `ee496b520b8e527c` |
| tx_batch_132.json | 356,000 | 3 keys | `4627c2ae5d7986c2` |
| tx_batch_133.json | 152,410 | 3 keys | `244043874d36eff1` |
| tx_batch_134.json | 146,001 | 3 keys | `8637d4ffd1822df8` |
| tx_batch_135.json | 306,843 | 3 keys | `ea8e9b6d72bd1234` |
| tx_batch_136.json | 105,525 | 3 keys | `62b0654342a3b2d5` |
| tx_batch_137.json | 115,521 | 3 keys | `3cbf633409ddcc41` |
| tx_batch_138.json | 387,440 | 3 keys | `76bc645e50e33477` |
| tx_batch_139.json | 118,180 | 3 keys | `9c1ade0b604c8f3c` |
| tx_batch_140.json | 128,840 | 3 keys | `9f938a849330f4df` |
| tx_batch_141.json | 242,177 | 3 keys | `3ccac052b9d233dc` |
| tx_extra.json | 30,144,569 | 14158 keys | `44c32f56ad372dd4` |
| tx_missing.json | 144 | 2 | `b2b602e726d6ad96` |

Total 62.7 MB across 164 files.

## Key files

| file | what it is |
|---|---|
| `indexer_claims_8453.json` | all 9,748 Base claims incl. full description text |
| `indexer_transactions_8453.json` | 14,376 indexed Base actions with timestamps + tx hashes |
| `tx_extra.json` | 14,158 raw Base tx objects keyed by hash |
| `claims_tx.csv` | the join: 9,709 claims x tx fields x text |
| `detectors.csv` | the 4,431 claims in scope with D1/D2/D3 flags and capture pattern |
| `final_tables.json` | main table, four sensitivities, wallet-level table |
| `hand_audit_sample.csv` | 42 sampled claims with my verdicts and notes |
| `QUERIES.md` | every endpoint, parameter and snapshot time |

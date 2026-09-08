# Case report: USDT activity triage

## Assessment

A fixed public Ethereum window supports a 15-address, 15-event neighborhood around `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5`. A same-amount two-step sequence is observable, alongside tiny incoming transfers and an address-suffix similarity. These are investigative leads, not findings of illicit conduct. No identity or exchange attribution is made.

## Scope and selection

- Ethereum mainnet (chain ID 1), canonical USDT contract `0xdac17f958d2ee523a2206206994597c13d831ec7`; six decimals checked by `eth_call`.
- Blocks 25,929,879–25,929,958, 80 blocks; 7,640 decoded USDT events. Capture: 2026-09-08T03:46:12.438028+00:00.
- Provider: https://rpc.mevblocker.io. End block was returned under the node's finalized tag. Raw headers supply UTC timestamps.
- Among addresses with 6–12 distinct counterparties and both incoming and outgoing positive USDT in the window, choose the most counterparties, then lexicographic address. This is a deliberately manageable activity sample, not a representative or risk-ranked sample.
- Two-hop incoming/outgoing neighborhood, maximum 24 addresses. Actual: 15 addresses, 12 direct counterparties and two additional second-hop addresses; no candidates omitted by the address cap. Second-hop nodes were not expanded further. Other tokens and activity outside this window are excluded.

## Observations

The seed has nine incoming and three outgoing USDT events. Incoming amounts total 57.754041 USDT and outgoing amounts total 4120.912839 USDT within this window. These are window totals, not balances or net economic gains. Seven incoming events are below 0.001 USDT; the threshold is descriptive and is not a risk score.

### Candidate sequence

1. At 2026-09-08 03:13:35 UTC, the seed sends **353.912839 USDT** to `0x5417fde7d1a1ddfd2effbccb002bf0a38327e546`. Transaction `0xc848acf88934686e53a87db8690c7ef867feddd36947f1d5f3e0b486615cb715`, log 44, block 25,929,884.
2. At 03:16:23 UTC, that recipient sends **353.912839 USDT** to `0x18e296053cbdf986196903e889b7dca7a73882f6`. Transaction `0x4076778f5d8c4eade1a000df84bdff20c66f1c758891ded634fea6633ec1d501`, log 23, block 25,929,898.

The 168-second separation, shared intermediary, and equal amount support a candidate onward-transfer hypothesis. They do **not** prove the identical funds were forwarded: prior balances and other activity may explain it. Both successful receipts were queried through a second endpoint, `https://eth-mainnet.public.blastapi.io`, and their USDT event fields match the primary logs. Shared upstream infrastructure cannot be excluded.

### Tiny transfers and address similarity

The actual recipient above ends in `27e546`. Another address, `0x5446ad65110d5f352aee34538ff0bff72827e546`, shares that six-character suffix and sends 0.000353 USDT to the seed at 03:18:23 UTC (transaction `0x45acfc6268faefe2652a905bfbd5b274660094417cc306a1659aaea1057f0968`, log 450). The latter address had received 0.000353 USDT from `0x7d9f4ca54131e588fc1fe577973b55fb11231e76` at 03:16:11 UTC.

**Hypothesis:** this could warrant investigating transaction-history contamination or address imitation. **Alternatives:** unrelated transfers, automated distribution, or coincidence. This short sample does not establish intent, control, a deceived user, or loss. Never identify counterparties from a truncated address alone.

## Recommended next steps

1. Expand the time window around the candidate sequence and obtain starting balances, receipts, transaction input, and caller details. Separate token-event participants from transaction signers.
2. Check whether tiny transfers and address similarities repeat systematically; compare full addresses and retain disconfirming examples.
3. If a legitimate case supplies exchange attribution, document the source and seek authorized account records through appropriate channels. Public-chain activity alone cannot establish account ownership or USD conversion inside an exchange.

## Evidence and reproducibility

`data/raw/` contains normalized JSON request/response records. `data/manifest.json` includes SHA-256 digests, collection parameters, selection rule, and provenance. Run `python3 verify.py` to check cached evidence and the two corroborating receipts; run the tests with `python3 -m unittest discover -s tests -v`.

Checksums are local integrity controls, not cryptographic chain inclusion proofs. The providers' completeness and correctness remain assumptions. UTC times are block timestamps. The graph shows relationships, not a mechanically proven path of funds. The following table is generated from the cached events, in on-chain order.

## Event register

| UTC | USDT | Sender → recipient | Transaction hash | Log |
|---|---:|---|---|---:|
| 2026-09-08T03:13:35+00:00 | 353.912839 | `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` → `0x5417fde7d1a1ddfd2effbccb002bf0a38327e546` | `0xc848acf88934686e53a87db8690c7ef867feddd36947f1d5f3e0b486615cb715` | 44 |
| 2026-09-08T03:13:35+00:00 | 24.004309 | `0x35193481e18de1c8d50912539a7c43d31877213c` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0xf2139ef4a79165230a5b740711cf58479dcb3f65391362c66bdc0d9f588508fa` | 140 |
| 2026-09-08T03:14:23+00:00 | 0.000436 | `0x7d9f4ca54131e588fc1fe577973b55fb11231e76` → `0x98c762ad6a2ee18e8e95300d38ffe49c725f0fbf` | `0x68facc3436c784b99aeb1612fedba55b357845d734caf3d444ced08ee64e672a` | 329 |
| 2026-09-08T03:16:11+00:00 | 0.000353 | `0x7d9f4ca54131e588fc1fe577973b55fb11231e76` → `0x5446ad65110d5f352aee34538ff0bff72827e546` | `0xb1319e22494757e3a71966add94e924fe7a7b04dbf04574f0144e26d94afc075` | 174 |
| 2026-09-08T03:16:23+00:00 | 353.912839 | `0x5417fde7d1a1ddfd2effbccb002bf0a38327e546` → `0x18e296053cbdf986196903e889b7dca7a73882f6` | `0x4076778f5d8c4eade1a000df84bdff20c66f1c758891ded634fea6633ec1d501` | 23 |
| 2026-09-08T03:16:35+00:00 | 1779 | `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` → `0x85276d777f24be1eade37645a55d06aae2563255` | `0xa962723cd3c1c3c6679e1abf6c89428e8cf9f245294a6c08881e521b6af937a8` | 10 |
| 2026-09-08T03:18:23+00:00 | 0.000353 | `0x5446ad65110d5f352aee34538ff0bff72827e546` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x45acfc6268faefe2652a905bfbd5b274660094417cc306a1659aaea1057f0968` | 450 |
| 2026-09-08T03:19:11+00:00 | 0.000131 | `0xbc5de343d414592eaa8a41c96adfde1e3a15f097` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x4ddd56763b0b6c4738459a26d4c27092934917633548f8db2d50e252a6606294` | 443 |
| 2026-09-08T03:19:47+00:00 | 0.000206 | `0xc79f864456c49f528aa257e4d4d2543f314df825` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x18b0dcd7eb5b40e5b4d0a188854ca9da2ad1c5df111310aaffb32e1c398bfd9d` | 450 |
| 2026-09-08T03:21:11+00:00 | 1988 | `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` → `0xd7e3f598f401a0c509706266b1431cfa21ee6cb0` | `0xe0308d8a2b10609d8f04c0765119de7e16d9dddc9b02724b9f83ed90ae73a997` | 9 |
| 2026-09-08T03:24:11+00:00 | 0.000356 | `0x0d56c067edb519fb2da180dcd190f9196246858d` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0xc2d4e989ad1b0a9cad8eaef38d4ebd67c0b4ab69835429daf69179fd61413e4e` | 103 |
| 2026-09-08T03:24:35+00:00 | 0.0005 | `0x592320a34bd19c1c67a1669fcff7ed0072bd4f84` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x13e91c8fb1a3037afa11ac9c08c1fa854028c7aef982c34cc562833712b3e625` | 346 |
| 2026-09-08T03:24:35+00:00 | 0.00075 | `0xe61370efe14c513aff32f4b675208d646ef74250` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x06dc7fbb43c8fc10a335fec2474196772e83fcc6c80a03719bcbd36262a22cc0` | 347 |
| 2026-09-08T03:24:47+00:00 | 33.747 | `0xf4403eeb521751243fcd08e0dd332c90a0e513be` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0xf7a975cd8eda62f5f2e33e5258dbdf1330c7717571ebb19a5901504d37addd29` | 170 |
| 2026-09-08T03:26:47+00:00 | 0.000436 | `0x98c762ad6a2ee18e8e95300d38ffe49c725f0fbf` → `0x1d6d074c711ec1a4d79456eaf7822c8e6c1801e5` | `0x66e5c6bc03a6884a9e3a0741a9b25aaf2031b664ec7d0df681f5d0cc1532910e` | 396 |

# USDT Investigator — Original Saved Case

**[Open the original demo](https://brandon-usdt-investigator.brandon-d-candela.chatgpt.site/)**

This repository contains the original fixed 15-address investigation work sample.

A small Python investigation dashboard using **real Ethereum node data**, with a saved case that runs offline without an API key. Built as an entry-level blockchain investigator portfolio exercise. No paid service, wallet, or credentials required.

## Start in two minutes

Install Python 3.10+ from [python.org](https://www.python.org/downloads/) if needed. Download or clone this project, open Terminal in the project folder, then run:

```sh
python3 app.py
```

On Windows use `py app.py`. Open **http://127.0.0.1:8000** in your browser. Keep Terminal open; Ctrl+C stops the server. If port 8000 is busy, run `python3 app.py --port 8001` and open port 8001. No `pip install` is needed.

On the original Mac, double-click `Launch.command`. It also finds the bundled Codex Python when Apple's default Python is unavailable. The portable command above works for reviewers with Python installed.

## What to inspect

1. Read scope and findings, including the fixed block window.
2. Click the gold seed or another graph node to filter recorded events.
3. Click a transaction button for full addresses, hash, log index, raw integer amount, and block hash.
4. Export the visible CSV or complete case JSON.
5. Read [CASE_REPORT.md](CASE_REPORT.md) for a short analyst assessment and the candidate two-step transfer sequence.

**Saved case:** 7,640 USDT Transfer events across blocks 25,929,879–25,929,958. The selected two-hop neighborhood contains 15 addresses and 15 events. This is a public activity triage exercise, not an allegation of a crime or a known hack investigation.

## Method

- Query chain ID, a finalized block, canonical USDT `Transfer` logs in four non-overlapping 20-block chunks, block headers, and token `decimals()` from an Ethereum JSON-RPC node.
- Decode indexed sender/recipient topics and the uint256 amount ourselves. Store amounts as exact base-unit integers and decimal strings (never floats).
- Select a manageable seed deterministically: among addresses with 6–12 distinct peers and both positive incoming/outgoing transfers, choose the highest peer count, then lexicographic address. This criterion was chosen during case development to keep the review manageable, rather than as an unbiased sampling procedure.
- Traverse incoming and outgoing relationships for at most two hops, at most 24 addresses, lexicographic tie-break. Exclude zero-value events and the zero address from expansion. Display all positive events whose endpoints are selected. The graph is **not** a temporal funds-flow algorithm.
- Order evidence by block, transaction index, and log index. Keep event IDs as transaction hash plus log index because one transaction can emit multiple events.
- Verify file SHA-256 hashes and event block hashes against saved blocks before serving the case.

The raw cache includes all fetched window events, including addresses outside the displayed neighborhood. No explorer tracing, risk scores, ownership labels, or proprietary attribution are used. Explorer links are optional manual lookups only.

## Reproduce and test

```sh
python3 -m unittest discover -s tests -v
python3 verify.py
```

Offline reproduction regenerates the case from saved responses every time the dashboard starts. `data/manifest.json` records parameters, seed selection, source, retrieval time, and SHA-256 digests. `data/raw/*.json` preserves each request, parsed JSON response, and capture time. Formatting is normalized JSON, not original HTTP bytes.

To collect a fresh case into a separate directory:

```sh
ETH_RPC_URL=https://rpc.mevblocker.io python3 collect.py --blocks 80 --output fresh-data
```

To attempt the exact saved block window, add `--end-block 25929958`. Public nodes may restrict historical requests, rate-limit, or change availability; offline replay remains available. The collector fails on RPC errors rather than silently accepting partial results. A window with no suitable seed fails and needs a different window. The dashboard reads `data/`; inspect and validate a newly collected dataset before substituting it. Do not commit credential-bearing RPC URLs.

## Files

- `app.py`: loopback-only HTTP server, standard library.
- `investigator.py`: decoder, bounded neighborhood, evidence loader.
- `collect.py`: optional public JSON-RPC collection.
- `verify.py`: offline evidence and receipt checks.
- `static/index.html`: dependency-free dashboard; no CDN or external fonts.
- `data/raw/`: raw node request/response records.
- `CASE_REPORT.md`: observations, hypotheses, evidence references, limits.
- `tests/`: decoding, bounds, ordering, and saved-case tests.

## Limits and honest presentation

An address is not a person. Matching amounts and sequential transfers do not prove identical funds. This window does not establish full wallet history or starting balances. USDT amounts are token units, not proof of USD redemption. A public chain cannot show fiat conversion or internal exchange account activity. No address is attributed to Coinbase, Binance, or any individual.

A node response is trusted input: local checksums detect changes against the local manifest but do not authenticate the manifest, independently verify consensus, or prove log inclusion. Receipt checks from a second provider add corroboration, not cryptographic proof. Block timestamps are block times, not precise real-world action times. Provider completeness is assumed, not proven.

This project was built with AI assistance. Before using it in an application, run it, understand the report and code, and describe accurately what you can explain and maintain. Suggested portfolio wording: “Built an AI-assisted Python work sample that decodes raw USDT logs, explores a bounded address graph, and documents evidence and investigative limitations.”

## Technical references

- [Ethereum JSON-RPC](https://ethereum.org/developers/docs/apis/json-rpc/)
- [ERC-20 event specification](https://eips.ethereum.org/EIPS/eip-20)
- [Tether supported contracts](https://tether.to/en/supported-protocols/)

MIT license for project code; public node evidence is included for reproducibility.

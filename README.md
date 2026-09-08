# Trace Desk — USDT investigator work sample

**[Original saved-case demo](https://brandon-usdt-investigator.brandon-d-candela.chatgpt.site/)** — instant 15-address example.

**[Live AML review workspace](https://brandon-usdt-workspace.brandon-d-candela.chatgpt.site/)** — query an address, expand counterparties, and export your assessment. No login or wallet connection required.

An AML review workspace with a Python evidence pipeline and a dependency-free JavaScript interface. Start with the verified saved example or query a new Ethereum address, expand observed counterparties, record your assessment, and export a handoff report. Built with AI assistance as an entry-level investigator portfolio project.

## Version 2: repeatable review workflow

1. Enter a nonzero Ethereum address and UTC start/end times. Maximum two hours; choose an end at least 20 minutes in the past. The default is a recent 30-minute window ending 30 minutes ago.
2. Collect incoming and outgoing USDT activity. Dates are converted to block boundaries using node block timestamps; start is inclusive and end exclusive. Only finalized data is accepted.
3. Inspect the graph and transaction evidence. Live queries start with the subject address only. Expand an observed counterparty in the same window, up to five queried addresses total. The graph displays up to 25 addresses, while the table and exports retain all fetched events.
4. Consider equal-amount sequential pairs as leads, not proof of identical funds. The heuristic shows at most 20 pairs within 30 minutes; it does not perform taint accounting or attribute ownership.
5. Record observations, alternative explanations, missing evidence, and a review disposition. Export a Markdown case summary or a JSON case bundle containing raw node responses and notes.

Notes live only in the current tab's memory and survive case switching only while that tab stays open. Refreshing or closing loses them: export before leaving. Notes are never sent to the node or a hosted database. The queried address is sent directly from the browser to `https://rpc.mevblocker.io`. Use public/example data for portfolio demonstrations.

Live collection has strict limits: 700 blocks, 1,000 combined events, five queried addresses, and 180 RPC requests per address. Each request times out after 20 seconds; Cancel stops the current query. Failed, cancelled, or over-budget queries never replace the currently displayed case. An empty successful response is labeled as an empty scope, not clearance. Public-node access can fail or restrict historical queries; the saved example is always available without RPC access.

No paid provider, API key, or wallet connection is required. Use a current browser supporting JavaScript modules, BigInt, and AbortSignal.timeout/any. This is a bounded review work sample, not a production compliance system, complete historical index, or replacement for KYC and internal records.

## Start in two minutes

Install Python 3.10+ from [python.org](https://www.python.org/downloads/) if needed. Download or clone this project, open Terminal in the project folder, then run:

```sh
python3 app.py
```

On Windows use `py app.py`. Open **http://127.0.0.1:8000** in your browser. Keep Terminal open; Ctrl+C stops the server. If port 8000 is busy, run `python3 app.py --port 8001` and open port 8001. No `pip install` is needed. The local dashboard also serves the live-query JavaScript modules; new queries require internet access.

On the original Mac, double-click `Launch.command`. It also finds the bundled Codex Python when Apple's default Python is unavailable. The portable command above works for reviewers with Python installed.

## What to inspect

1. Read scope and findings, including the fixed block window.
2. Click the gold seed or another graph node to filter recorded events.
3. Click a transaction button for full addresses, hash, log index, raw integer amount, and block hash.
4. Export the visible CSV or complete case JSON.
5. Read [CASE_REPORT.md](CASE_REPORT.md) for a short analyst assessment and the candidate two-step transfer sequence.

**Saved case:** 7,640 USDT Transfer events across blocks 25,929,879–25,929,958. The selected two-hop neighborhood contains 15 addresses and 15 events. This is a public activity triage exercise, not an allegation of a crime or a known hack investigation.

## Saved example methodology

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
node --test tests/test_workspace.mjs tests/test_aml.mjs tests/test_casefile.mjs
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
- `static/index.html` and `ui.mjs`: guided review interface and in-tab notes.
- `static/live.mjs`: browser-to-node bounded collection and raw provenance.
- `static/core.mjs`: exact decoding, de-duplication, merge bounds, sequence leads, CSV/report exports.
- `build_demo.py`: verifies the Python saved case and copies the static workspace to `dist/`.
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

## Validation of version 2

Python tests cover the saved evidence pipeline. Node tests cover exact large token amounts, Python/JavaScript parity, malformed logs, UTC boundaries, duplicate/conflicting events, provider failures, cancellation, empty scopes, report evidence and counterparty expansion constraints. A real node query of the example subject from 2026-09-08 03:12 to 03:29 UTC returned its 12 direct events; expanding the intermediary reproduced the candidate 353.912839 USDT sequence. Provider availability is not guaranteed by this one successful check.

Build for static hosting with `python3 build_demo.py`. The published app performs new queries directly in the browser; Python prepares and verifies the saved sample. No claim is made that the live browser collector executes Python on the hosting service.

## AML review features

The live workspace now includes an AML-specific review layer:

- Evidence-linked descriptive indicators: equal-amount sequences, three or more incoming/outgoing counterparties, very small incoming transfers, and transfers above an optional analyst-entered expectation. These are heuristics, not risk scores, regulatory thresholds or findings of suspicious activity.
- A subject counterparty ledger, ranked by observed incoming plus outgoing USDT, with direct access to supporting events.
- A case profile with review trigger, expected activity and the source of that analyst-supplied context. No identity or customer profile is inferred from blockchain data.
- Per-indicator analyst assessment and reasoning. Expanding the case resets indicator assessments to Unreviewed because the evidence set changed; entered reasoning remains available for revision.
- Pinned transaction evidence and a five-item review checklist. Documentation readiness is not compliance approval. Exports remain available for incomplete drafts.
- A handoff report that includes context, disposition rationale, checklist state, indicator limitations and evidence IDs, analyst responses, and pinned transactions.

Notes, context and assessments remain in the current tab only. Export before closing or refreshing. The tool does not file SARs, screen sanctions, establish beneficial ownership or make compliance decisions. All indicators describe only returned evidence within the selected scope.

## Save and reopen cases

Use **Save portable case file** to download a JSON file with the current evidence, notes, context, per-indicator reviews, pinned transactions and checklist. Use **Open case file** to resume it later. Files stay in the browser; there is no upload or automatic server storage. Save before closing. A browser leave-page warning is requested when notes have not been exported, but browser settings can suppress it.

Versioned files contain a SHA-256 checksum of the payload. On import, the tool checks the checksum, Ethereum/USDT scope, event identifiers, exact amounts, block bounds and note/evidence references. This detects accidental file changes; anyone who edits the file can recalculate the checksum, so it does not prove authenticity or chain inclusion. Imported data is explicitly marked as not reverified against a node and cannot be expanded directly. Start a fresh query to collect new evidence.

Older case JSON and evidence bundles remain importable, with a no-checksum notice. Unsupported files, oversized files (over 20 MB), bad event amounts and dangling pinned references are rejected before replacing the displayed case. The saved example's full raw evidence remains available in this repository; case exports include raw responses only when present in that case.

## QC review workflow

After documenting the case and completing the checklist, enter an analyst reference and submit a snapshot for QC. Each submission preserves its scope, decoded events, pinned evidence, indicator assessments and narrative. Reviewers can attach categorized findings to a transaction or the overall conclusion, record a decision rationale, and return the submission for correction or complete QC. Analysts respond to findings and submit revised drafts as a new round. Changes to the current evidence or assessment invalidate its match with the reviewed submission; prior outcomes stay attached to their original snapshot.

Use **Save portable case file** to hand the evidence, notes and QC history to another person. **Open case file** restores that history; the export checksum detects changes but is not authentication. The summary includes review decisions and findings, and each full submission can also be downloaded separately for inspection. Up to 20 rounds and 100 findings per round are supported within the existing 20 MB file limit.

This is a file-based workflow prototype, not an authenticated case-management system. Names and timestamps are self-reported/browser-generated. It does not enforce reviewer independence, permissions or a tamperproof audit trail. QC completion is a documentation outcome, not a clearance determination.

QC regression tests: `node --test tests/test_qc.mjs`.

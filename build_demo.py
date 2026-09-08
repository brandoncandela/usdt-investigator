"""Build the public demo from verified saved evidence; no live RPC needed."""
import json
from investigator import ROOT, load_case
from verify import verify
verify()
out=ROOT/'dist';out.mkdir(exist_ok=True)
case=load_case()
(out/'case.json').write_text(json.dumps(case,indent=2)+'\n')
html=(ROOT/'static/index.html').read_text().replace("fetch('/api/case')", "fetch('./case.json')")
html=html.replace('Loading and verifying evidence checksums…','Loading saved case…')
html=html.replace('<h1>Follow the evidence. Bound the claim.</h1>','<h1>USDT investigation demo</h1>')
html=html.replace('A reproducible USDT activity review built from raw Ethereum event logs. Explore a selected address and its counterparties, inspect each transfer, and see where the evidence stops.','Brandon Candela · AML investigation work sample. Explore 15 addresses from a saved public Ethereum case. No installation or wallet connection required.')
html=html.replace('</div>\n<div id="status">','<p><a href="https://github.com/brandoncandela/usdt-investigator/blob/main/CASE_REPORT.md" target="_blank" rel="noopener noreferrer">Read the investigation report ↗</a> · <a href="https://github.com/brandoncandela/usdt-investigator" target="_blank" rel="noopener noreferrer">Source code &amp; raw evidence ↗</a></p></div>\n<div id="status">')
html=html.replace('Raw JSON-RPC requests and responses are saved in','This demo uses a fixed saved case, not live monitoring or arbitrary-wallet tracing. Evidence checks run when the demo is built; your browser loads the resulting case. Raw JSON-RPC requests and responses are saved in the GitHub repository under')
html=html.replace('<title>Trace Desk | USDT investigation</title>','<title>Brandon Candela | USDT investigation demo</title><meta name="description" content="Explore a reproducible 15-address USDT investigation with transaction evidence, a relationship graph, and an analyst report.">')
html=html.replace('main{max-width:1400px;margin:auto;padding:32px 4vw}','main{max-width:1400px;margin:auto;padding:20px 4vw}').replace('font-size:9','font-size:12')
html=html.replace('<div id="status">','<noscript>This interactive demo requires JavaScript. You can still read the <a href="https://github.com/brandoncandela/usdt-investigator/blob/main/CASE_REPORT.md">case report on GitHub</a>.</noscript><div id="status">')
(out/'index.html').write_text(html)
assert json.loads((out/'case.json').read_text())==case
assert '/api/case' not in html
print('Built public demo: 15 addresses, 15 events, verified cached evidence.')

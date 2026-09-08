"""Exact ERC-20 decoding and bounded graph exploration; Python standard library only."""
import json
import hashlib
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
CONTRACT = '0xdac17f958d2ee523a2206206994597c13d831ec7'
TRANSFER = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
ZERO = '0x' + '0' * 40

def decode(log):
    if log.get('removed', False):
        raise ValueError('Removed log')
    if log['address'].lower() != CONTRACT or len(log['topics']) != 3 or log['topics'][0].lower() != TRANSFER:
        raise ValueError('Not a canonical USDT Transfer event')
    for word in log['topics'][1:]:
        if len(word) != 66 or int(word[2:26], 16) != 0:
            raise ValueError('Invalid indexed address')
        int(word[2:], 16)
    if len(log['data']) != 66:
        raise ValueError('Invalid uint256')
    units = int(log['data'], 16)
    return dict(id=log['transactionHash'] + ':' + str(int(log['logIndex'], 16)),
                tx=log['transactionHash'], block=int(log['blockNumber'], 16),
                block_hash=log['blockHash'], tx_index=int(log['transactionIndex'], 16),
                log_index=int(log['logIndex'], 16), source='0x'+log['topics'][1][-40:].lower(),
                target='0x'+log['topics'][2][-40:].lower(), units=str(units),
                amount=(str(units // 10**6) + '.' + str(units % 10**6).zfill(6)).rstrip('0').rstrip('.'))

def explore(events, seed, hops=2, max_addresses=24):
    """Undirected neighborhood, NOT temporal flow or ownership clustering."""
    seed = seed.lower()
    nodes = {seed: 0}
    frontier = [seed]
    candidates_omitted = set()
    for depth in range(1, hops+1):
        candidates = set()
        for e in events:
            if int(e['units']) == 0 or ZERO in (e['source'], e['target']):
                continue
            if e['source'] in frontier: candidates.add(e['target'])
            if e['target'] in frontier: candidates.add(e['source'])
        candidates -= nodes.keys()
        # Stable lexicographic tie-break; not amount/risk ranking.
        chosen = sorted(candidates)[:max(0, max_addresses-len(nodes))]
        candidates_omitted.update(candidates-set(chosen))
        nodes.update({a: depth for a in chosen})
        frontier = chosen
        if not frontier: break
    edges = [e for e in events if e['source'] in nodes and e['target'] in nodes and int(e['units']) > 0]
    return nodes, edges, sorted(candidates_omitted-set(nodes))

def load_case():
    manifest = json.loads((ROOT/'data/manifest.json').read_text())
    for name, digest in manifest['sha256'].items():
        if hashlib.sha256((ROOT/'data/raw'/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Evidence checksum mismatch: '+name)
    records = [json.loads(p.read_text()) for p in sorted((ROOT/'data/raw').glob('*.json'))]
    logs, blocks = [], {}
    for r in records:
        method = r['request']['method']; result = r['response'].get('result')
        if method == 'eth_getLogs': logs.extend(result)
        if method == 'eth_getBlockByNumber' and result:
            blocks[int(result['number'],16)] = result
    events = {}
    for log in logs:
        e = decode(log)
        block = blocks[e['block']]
        if block['hash'] != e['block_hash']: raise ValueError('Block hash mismatch')
        e['timestamp'] = datetime.fromtimestamp(int(block['timestamp'],16),timezone.utc).isoformat()
        if e['id'] in events and events[e['id']] != e: raise ValueError('Conflicting event')
        events[e['id']] = e
    ordered = sorted(events.values(),key=lambda e:(e['block'],e['tx_index'],e['log_index']))
    nodes, edges, omitted = explore(ordered, manifest['seed'], manifest['hops'],manifest['max_addresses'])
    return dict(manifest=manifest,nodes=[dict(address=a,depth=d) for a,d in nodes.items()],
                events=edges,window_event_count=len(ordered),omitted_addresses=omitted)

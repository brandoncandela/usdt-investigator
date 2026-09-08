"""Offline integrity and selected receipt corroboration checks."""
import json
from investigator import load_case, ROOT, decode, CONTRACT, TRANSFER

def verify():
    c=load_case(); events={e['id']:e for e in c['events']};checked=0
    for p in (ROOT/'data/raw').glob('corroboration-receipt-*.json'):
        r=json.loads(p.read_text())['response']['result']
        assert r['status']=='0x1', 'Receipt reverted'
        for log in r['logs']:
            if log['address'].lower()!=CONTRACT or log['topics'][0].lower()!=TRANSFER:continue
            e=decode(log)
            if e['id'] in events:
                assert all(events[e['id']][k]==v for k,v in e.items()), 'Receipt/log mismatch'
                checked+=1
    assert checked>=2, 'Missing candidate-sequence receipt evidence'
    print(f"Verified checksums, block hashes, {c['window_event_count']} decoded events, {len(c['nodes'])} case addresses, and {checked} corroborated receipt events.")
if __name__=='__main__':verify()

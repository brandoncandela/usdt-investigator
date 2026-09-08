"""Collect fixed-window Ethereum node evidence. Never uses explorer APIs."""
import argparse, json, hashlib, time, urllib.request, os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from investigator import CONTRACT, TRANSFER, decode, ROOT

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--end-block',type=int,help='Defaults to node finalized block')
parser.add_argument('--blocks',type=int,default=80)
parser.add_argument('--output',type=Path,default=ROOT/'data')
args=parser.parse_args()
if not 1 <= args.blocks <= 200: parser.error('--blocks must be 1..200')
if (args.output/'manifest.json').exists(): parser.error('Output already contains a case; choose a new --output directory')
raw=args.output/'raw'; raw.mkdir(parents=True,exist_ok=True)
endpoint=os.environ.get('ETH_RPC_URL','https://ethereum-rpc.publicnode.com')

def rpc(method,params,name):
    request={'jsonrpc':'2.0','id':1,'method':method,'params':params}
    for attempt in range(4):
        try:
            req=urllib.request.Request(endpoint,data=json.dumps(request).encode(),headers={'Content-Type':'application/json','User-Agent':'USDT-investigator/1.0'})
            with urllib.request.urlopen(req,timeout=40) as response: body=json.loads(response.read())
            if 'error' in body: raise RuntimeError(str(body['error']))
            if body.get('result') is None: raise RuntimeError('Null RPC response')
            record={'retrieved_at':datetime.now(timezone.utc).isoformat(),'request':request,'response':body}
            (raw/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
            return body['result']
        except Exception:
            if attempt==3: raise
            time.sleep(1+attempt)

chain=rpc('eth_chainId',[],'chain')
if chain != '0x1': raise RuntimeError('Expected Ethereum mainnet')
finalized=rpc('eth_getBlockByNumber',['finalized',False],'finalized')
end=args.end_block if args.end_block is not None else int(finalized['number'],16)
if end > int(finalized['number'],16): raise RuntimeError('Window must end at or before finalized block')
start=end-args.blocks+1
logs=[]
for lo in range(start,end+1,20):
    hi=min(lo+19,end)
    logs.extend(rpc('eth_getLogs',[{'address':CONTRACT,'fromBlock':hex(lo),'toBlock':hex(hi),'topics':[TRANSFER]}],f'logs-{lo}-{hi}'))
    print('Collected blocks',lo,hi,flush=True)
events=[decode(x) for x in logs]
# Selection is explicit: most distinct peers (6–12) among addresses seen sending AND receiving.
peers={}; directions={}
for e in events:
    if int(e['units'])==0: continue
    for a,b,d in [(e['source'],e['target'],'out'),(e['target'],e['source'],'in')]:
        peers.setdefault(a,set()).add(b); directions.setdefault(a,set()).add(d)
candidates=[a for a in peers if len(directions[a])==2 and 6 <= len(peers[a]) <= 12 and int(a,16)!=0]
if not candidates: raise RuntimeError('No bidirectional candidate in this window')
seed=sorted(candidates,key=lambda a:(-len(peers[a]),a))[0]
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(lambda n:rpc('eth_getBlockByNumber',[hex(n),False],f'block-{n}'),sorted({e['block'] for e in events})))
# Verify decimals at this fixed block: 0x313ce567 is decimals().
decimals=rpc('eth_call',[{'to':CONTRACT,'data':'0x313ce567'},hex(end)],'decimals')
if int(decimals,16)!=6: raise RuntimeError('Unexpected decimals')
manifest=dict(title='USDT activity triage • public Ethereum case',chain_id=1,contract=CONTRACT,decimals=6,
    from_block=start,to_block=end,seed=seed,hops=2,max_addresses=24,
    selection='Among addresses with 6–12 distinct counterparties and both incoming and outgoing positive USDT in the window, choose the most counterparties, then lexicographic address.',
    endpoint='https://ethereum-rpc.publicnode.com' if endpoint=='https://ethereum-rpc.publicnode.com' else 'https://rpc.mevblocker.io' if endpoint=='https://rpc.mevblocker.io' else 'User-supplied RPC endpoint (credentials omitted)',
    captured_at=datetime.now(timezone.utc).isoformat(),sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(raw.glob('*.json'))})
(args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Saved',len(events),'events; seed',seed)

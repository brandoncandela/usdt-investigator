import {address,amount,ZERO} from './core.mjs';
import {CHECKS} from './aml.mjs';
export const MAX_FILE_BYTES=20*1024*1024;
const string=(v,max=20000)=>{if(v===undefined)return '';if(typeof v!=='string'||v.length>max)throw Error('Case file contains an invalid or oversized text field.');return v};
const integer=n=>Number.isSafeInteger(n)&&n>=0;
const addr=a=>typeof a==='string'&&/^0x[0-9a-f]{40}$/.test(a);
const hash=a=>typeof a==='string'&&/^0x[0-9a-fA-F]{64}$/.test(a);
async function digest(payload){const bytes=new TextEncoder().encode(JSON.stringify(payload));return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('')}
export async function makeCaseFile(c,n){const payload={case:c,analyst_notes:n};if(new TextEncoder().encode(JSON.stringify(payload)).length>MAX_FILE_BYTES-1000)throw Error('Case exceeds the 20 MB portable-file limit. Export a narrower case.');return {format:'trace-desk-case',version:1,exported_at:new Date().toISOString(),payload,sha256:await digest(payload)}}
export async function openCaseFile(text){
 if(new TextEncoder().encode(text).length>MAX_FILE_BYTES)throw Error('Case files must be 20 MB or smaller.');
 let file;try{file=JSON.parse(text)}catch{throw Error('This is not a valid JSON case file.');}
 let payload=file,integrity='Legacy file: no export checksum available.';
 if(file?.format!==undefined){if(file.format!=='trace-desk-case'||file.version!==1||!file.payload)throw Error('Unsupported case file version.');if(await digest(file.payload)!==file.sha256)throw Error('Case checksum mismatch. The file may have changed since export.');payload=file.payload;integrity='Export checksum matches. This detects file changes, not authenticity or blockchain inclusion.';}
 const c=payload?.case||payload,n=payload?.analyst_notes||{},m=c?.manifest;
 if(!m||m.chain_id!==1||m.contract!=='0xdac17f958d2ee523a2206206994597c13d831ec7'||m.decimals!==6)throw Error('Expected an Ethereum mainnet USDT case.');
 const seed=address(m.seed);if(!integer(m.from_block)||!integer(m.to_block)||m.to_block<m.from_block)throw Error('Invalid case block window.');
 if(!Array.isArray(c.events)||c.events.length>1000)throw Error('A case may contain at most 1,000 events.');
 const ids=new Set();const events=c.events.map(e=>{if(!e||!hash(e.tx)||!hash(e.block_hash)||!addr(e.source)||!addr(e.target)||!integer(e.block)||!integer(e.tx_index)||!integer(e.log_index)||e.block<m.from_block||e.block>m.to_block)throw Error('Malformed event or event outside case scope.');if(typeof e.units!=='string'||!/^\d{1,78}$/.test(e.units)||BigInt(e.units)>=2n**256n||e.amount!==amount(e.units))throw Error('Event amount does not match raw token units.');if(e.id!==e.tx+':'+e.log_index||ids.has(e.id))throw Error('Invalid or duplicate event ID.');ids.add(e.id);if(typeof e.timestamp!=='string'||!Number.isFinite(Date.parse(e.timestamp)))throw Error('Invalid event timestamp.');return {id:e.id,tx:e.tx,block_hash:e.block_hash,source:e.source,target:e.target,block:e.block,tx_index:e.tx_index,log_index:e.log_index,units:e.units,amount:e.amount,timestamp:new Date(e.timestamp).toISOString()}}).sort((a,b)=>a.block-b.block||a.tx_index-b.tx_index||a.log_index-b.log_index);
 const notes={};for(const k of ['observations','alternatives','next','caseTitle','trigger','expectedActivity','contextSource','rationale','expectedMax'])notes[k]=string(n[k]);
 const dispositions=['Unreviewed','Further information needed','Recommend escalation for review','No escalation proposed within reviewed scope'];notes.disposition=n.disposition||'Unreviewed';if(!dispositions.includes(notes.disposition))throw Error('Invalid review disposition.');
 if(n.pinned!==undefined&&(!Array.isArray(n.pinned)||n.pinned.some(id=>!ids.has(id))))throw Error('Pinned evidence does not exist in this case.');notes.pinned=[...new Set(n.pinned||[])];
 if(n.checks!==undefined&&(!Array.isArray(n.checks)||n.checks.some(id=>!CHECKS.some(([k])=>k===id))))throw Error('Invalid checklist item.');notes.checks=[...new Set(n.checks||[])];
 notes.indicatorReviews={};for(const k of ['sequence','incoming-peers','outgoing-peers','tiny','expected'])if(n.indicatorReviews?.[k]){const r=n.indicatorReviews[k];if(!['Unreviewed','Needs further information','Potential concern for escalation','Explained within reviewed scope'].includes(r.status))throw Error('Invalid indicator assessment.');notes.indicatorReviews[k]={status:r.status,reason:string(r.reason)}}
 if(c.raw!==undefined&&!Array.isArray(c.raw))throw Error('Invalid raw-evidence collection.');
 const peers=[...new Set(events.flatMap(e=>[e.source,e.target]))].filter(a=>a!==seed&&a!==ZERO).sort();
 const loaded={mode:'Imported case · not reverified against a node',manifest:{seed,chain_id:1,contract:m.contract,decimals:6,from_block:m.from_block,to_block:m.to_block,endpoint:string(m.endpoint,500),captured_at:string(m.captured_at,100),hops:2,max_addresses:25,selection:'Opened from an analyst-supplied case file.'},events,nodes:[{address:seed,depth:0},...peers.slice(0,24).map(a=>({address:a,depth:events.some(e=>(e.source===seed&&e.target===a)||(e.target===seed&&e.source===a))?1:2}))],omitted_addresses:peers.slice(24),window_event_count:events.length,coverage:'Imported events only. Original claimed coverage: '+string(c.coverage||'Saved neighborhood; source completeness not independently verified.',5000),raw:c.raw||[],import_info:{opened_at:new Date().toISOString(),integrity,warning:'Event shape, amounts and references checked locally. Raw responses and blockchain authenticity have not been independently verified. Imported cases cannot be expanded; start a new node query to obtain fresh evidence.'}};
 return {case:loaded,analyst_notes:notes};
}

import {findings,csv,report,mergeReview,ZERO} from './core.mjs';
import {collect} from './live.mjs';

const $=id=>document.getElementById(id),short=a=>a.slice(0,8)+'…'+a.slice(-6);let data,visible=[],selected='',controller=null;const notesByCase=new Map();
const key=c=>c.manifest.seed+':'+c.manifest.from_block+':'+c.manifest.to_block;
const readNotes=()=>Object.fromEntries(['observations','alternatives','next','disposition'].map(k=>[k,$(k).value]));

function node(tag,text,cls){let n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n}
function download(name,text,type){const url=URL.createObjectURL(new Blob([text],{type}));let a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
function render(){const q=$('search').value.trim().toLowerCase();visible=data.events.filter(e=>(!selected||e.source===selected||e.target===selected)&&(!q||[e.source,e.target,e.tx].some(v=>v.includes(q))));$('rows').replaceChildren();$('count').textContent=visible.length+' recorded events'+(selected?' involving '+selected:'');for(const e of visible){let row=document.createElement('tr');for(const value of [e.timestamp.replace('T',' ').replace('+00:00','')+' / '+e.block,short(e.source),short(e.target),e.amount])row.append(node('td',value));row.children[1].title=e.source;row.children[2].title=e.target;let td=document.createElement('td'),b=node('button',short(e.tx)+' / '+e.log_index);b.onclick=()=>{$('detail').replaceChildren(node('p','Transaction: '+e.tx,'mono'),node('p','Event ID: '+e.id,'mono'),node('p','Block hash: '+e.block_hash,'mono'),node('p','Sender: '+e.source,'mono'),node('p','Recipient: '+e.target,'mono'),node('p','Raw token units: '+e.units+' / 1,000,000 = '+e.amount+' USDT'));let link=node('a','Optional independent explorer lookup ↗');link.href='https://etherscan.io/tx/'+e.tx;link.target='_blank';link.rel='noopener noreferrer';$('detail').append(link)};td.append(b);row.append(td);$('rows').append(row)}}
function graph(){const ns='http://www.w3.org/2000/svg',svg=$('graph');function el(t,attrs){let n=document.createElementNS(ns,t);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);return n}const defs=el('defs',{}),marker=el('marker',{id:'arrow',viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:5,markerHeight:5,orient:'auto-start-reverse'});marker.append(el('path',{d:'M 0 0 L 10 5 L 0 10 z',fill:'#6f8bab'}));defs.append(marker);svg.append(defs);let positions={};data.nodes.forEach((n,i)=>{const a=2*Math.PI*(i-1)/Math.max(1,data.nodes.length-1);positions[n.address]=i===0?[350,210]:[350+285*Math.cos(a),210+165*Math.sin(a)]});let pairs=new Set;for(const e of data.events){let key=e.source+e.target;if(pairs.has(key))continue;pairs.add(key);let[a,b]=[positions[e.source],positions[e.target]];if(!a||!b)continue;let dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy);if(!len)continue;svg.append(el('line',{x1:a[0]+dx/len*12,y1:a[1]+dy/len*12,x2:b[0]-dx/len*15,y2:b[1]-dy/len*15,stroke:'#516d8b','stroke-opacity':.5,'marker-end':'url(#arrow)'}))}data.nodes.forEach((n,i)=>{let[x,y]=positions[n.address],g=el('g',{class:'node',tabindex:0,role:'button','aria-label':'Filter '+n.address});g.append(el('circle',{cx:x,cy:y,r:i===0?14:9,fill:i===0?'#f4be70':n.depth===1?'#83dec2':'#8b9ee9'}));let title=el('title',{});title.textContent=n.address+' · hop '+n.depth;g.append(title);let label=el('text',{x,y:y+24,'text-anchor':'middle',fill:'#bccde1','font-size':12});label.textContent=short(n.address);g.append(label);g.onclick=()=>{selected=n.address;render()};g.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();g.onclick()}};svg.append(g)})}
function showCase(d){
 if(data)notesByCase.set(key(data),readNotes());data=d;selected='';$('search').value='';
 for(const id of ['cards','graph','findings','provenance','sequences','peer'])$(id).replaceChildren();
 $('detail').textContent='Select a transaction for full evidence details.';
 for(const k of ['observations','alternatives','next','disposition'])$(k).value=notesByCase.get(key(d))?.[k]|| (k==='disposition'?'Unreviewed':'');
 const m=d.manifest,f=findings(d.events,m.seed);$('mode').textContent=d.mode||'Saved training case';$('status').textContent=d.events.length?'Case ready. Review coverage before drawing conclusions.':'No USDT events returned within this window. This does not establish absence of activity outside the scope.';$('content').hidden=false;
 for(const [label,value]of [['Case addresses',d.nodes.length],['Returned events',d.events.length],['Incoming USDT',f.in_total],['Outgoing USDT',f.out_total]]){let c=node('div','','card');c.append(node('span',label,'label'),node('strong',value));$('cards').append(c)}
 for(const text of ['Seed: '+m.seed,'Bounds: blocks '+m.from_block+'–'+m.to_block+'. '+(d.coverage||'Saved two-hop neighborhood from an 80-block window containing '+d.window_event_count+' decoded USDT events. Graph and table show the selected neighborhood only.'),'Graph: '+d.nodes.length+' addresses; '+d.omitted_addresses.length+' encountered addresses omitted from graph.','Observed: '+f.incoming+' incoming and '+f.outgoing+' outgoing events involving the seed. Self-transfers excluded from these totals.','Observed: '+f.tiny+' incoming transfers below 0.001 USDT. This descriptive threshold is not a risk score.'])$('findings').append(node('p',text,'muted'));
 for(const seq of f.sequences){const b=node('button',seq.amount+' USDT · '+seq.seconds+' seconds apart');b.onclick=()=>{$('search').value=d.events.find(e=>e.id===seq.first).target;selected='';render();$('evidence').scrollIntoView({behavior:'smooth'})};$('sequences').append(b)}
 if(!f.sequences.length)$('sequences').append(node('p','No equal-amount sequential pairs found in the returned events within 30 minutes. This does not rule out pass-through activity.','muted'));
 $('provenance').append(node('p','Provider: '+m.endpoint+' · Captured: '+m.captured_at),node('p','Contract: '+m.contract+' · Decimals: '+m.decimals,'mono'));
 const peers=[...new Set(d.events.flatMap(e=>[e.source,e.target]))].filter(a=>a!==ZERO&&!(d.queried_addresses||[]).includes(a)).sort();
 for(const a of peers){const o=node('option',a);o.value=a;$('peer').append(o)}
 $('expand').disabled=!d.queried_addresses||d.queried_addresses.length>=5||!peers.length;$('peer').disabled=$('expand').disabled;
 $('expansion').textContent=d.queried_addresses?'Queried addresses: '+d.queried_addresses.length+'/5. Expand one counterparty at a time within the same UTC window. Unqueried peers are not cleared.':'Counterparty expansion is available after a new address query. The saved case already includes its bounded two-hop neighborhood.';
 graph();render();
}
async function saved(){if(controller)controller.abort();try{const r=await fetch('./case.json');if(!r.ok)throw Error('Saved case unavailable.');showCase(await r.json())}catch(e){$('status').textContent=e.message}}
$('loadsaved').onclick=saved;
async function runReview(seed,start,end,expand=false){
 if(controller)return;controller=new AbortController();for(const id of ['run','loadsaved','expand'])$(id).disabled=true;$('cancel').disabled=false;
 try{let d=await collect({seed,start,end,signal:controller.signal,onProgress:msg=>$('status').textContent=msg+' · current case unchanged'});
 if(expand)d=mergeReview(data,d);
 showCase(d)
 }catch(err){$('status').textContent='Query not loaded: '+err.message+' The previous case remains displayed.'}
 finally{controller=null;$('run').disabled=false;$('cancel').disabled=true;$('loadsaved').disabled=false;$('expand').disabled=!data?.queried_addresses||data.queried_addresses.length>=5||!$('peer').options.length}
}
$('intake').onsubmit=e=>{e.preventDefault();runReview($('seed').value,$('start').value+'Z',$('end').value+'Z')};
$('expand').onclick=()=>runReview($('peer').value,data.start,data.end,true);
$('cancel').onclick=()=>controller?.abort();
$('report').onclick=()=>download('investigation-review.md',report(data,readNotes()),'text/markdown');
$('bundle').onclick=()=>download('case-evidence.json',JSON.stringify({case:data,analyst_notes:readNotes()},null,2),'application/json');
const end=new Date(Date.now()-30*60000);end.setUTCSeconds(0,0);$('end').value=end.toISOString().slice(0,16);$('start').value=new Date(end.getTime()-30*60000).toISOString().slice(0,16);
saved();
$('search').oninput=render;$('reset').onclick=()=>{selected='';$('search').value='';render()};$('json').onclick=()=>download('case.json',JSON.stringify(data,null,2),'application/json');$('csv').onclick=()=>{let keys=['timestamp','block','tx','log_index','source','target','amount','units'];download('transfers.csv',[keys.join(','),...visible.map(e=>keys.map(k=>'"'+String(e[k]).replaceAll('"','""')+'"').join(','))].join('\n'),'text/csv')};

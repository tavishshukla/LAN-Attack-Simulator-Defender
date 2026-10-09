const $=id=>document.getElementById(id);
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
async function get(path){const r=await fetch(path);return r.json();}
function render(data,incidents,events,rules){
  $("cards").innerHTML=Object.entries(data.counts).map(([k,v])=>'<div class="card"><div class="label">'+esc(k)+'</div><div class="value">'+esc(v)+'</div></div>').join("");
  $("severity").innerHTML=Object.entries(data.severity).map(([k,v])=>'<div class="severity-row"><span class="'+k.toLowerCase()+'">'+esc(k)+'</span><b>'+esc(v)+'</b></div>').join("")||'<span class="muted">No alerts yet</span>';
  $("rules").innerHTML=Object.entries(rules).map(([k,v])=>'<div class="rule-row"><span>'+esc(k.replaceAll("_"," "))+'</span><span class="muted">'+esc(v.threshold)+' / '+esc(v.window_seconds)+'s / '+esc(v.severity)+'</span></div>').join("");
  $("incidents").innerHTML=incidents.map(i=>'<tr><td class="'+esc(i.severity).toLowerCase()+'">'+esc(i.severity)+'</td><td>'+esc(i.type)+'</td><td>'+esc(i.source)+'</td><td>'+esc(i.status)+'</td><td>'+esc(i.response||"pending")+'</td></tr>').join("")||'<tr><td colspan="5" class="muted">No incidents yet</td></tr>';
  $("events").innerHTML=events.map(e=>'<div class="event"><span class="muted">'+esc(e.timestamp)+'</span> '+esc(e.event_type)+' '+esc(e.source)+' → '+esc(e.destination)+' <span class="muted">'+esc(e.metadata)+'</span></div>').join("");
}
async function refresh(){const [s,i,e,r]=await Promise.all([get("/api/summary"),get("/api/incidents"),get("/api/events"),get("/api/rules")]);render(s,i,e,r);}
$("run").onclick=async()=>{ $("run").disabled=true;$("run").textContent="Running…";try{await fetch("/api/lab/run",{method:"POST"});await refresh();}finally{$("run").disabled=false;$("run").textContent="Run Safe Lab Simulation";}};
refresh();setInterval(refresh,3000);

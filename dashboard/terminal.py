from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
console=Console()
def live_event(e):
 console.print(f"[dim]EVENT[/dim] {e.event_type:<18} source={e.source:<15} port={e.port or '-'}")
def show_alert(a):
 console.print(Panel(f"[bold]{a.severity.value}[/bold]  {a.rule_id}\n{a.description}\nSource: {a.source}",title="SECURITY ALERT",border_style="red"))
def dashboard_snapshot(db):
 counts,sevs=db.stats()
 layout=Layout()
 layout.split_column(Layout(name="header",size=3),Layout(name="body"))
 layout["body"].split_row(Layout(name="stats",ratio=1),Layout(name="incidents",ratio=2))
 layout["header"].update(Panel("LAN DEFENDER  |  SECURITY OPERATIONS CENTER",style="bold"))
 st=Table();st.add_column("Metric");st.add_column("Count")
 for k,v in counts.items():st.add_row(k.title(),str(v))
 for r in sevs:st.add_row(f"Alerts: {r['severity']}",str(r['n']))
 layout["stats"].update(Panel(st,title="Telemetry"))
 it=Table();it.add_column("Severity");it.add_column("Rule");it.add_column("Source");it.add_column("Status");it.add_column("Response")
 for r in db.incidents()[:8]:it.add_row(r["severity"],r["type"],r["source"],r["status"],r["response"] or "-")
 layout["incidents"].update(Panel(it,title="Recent Incidents"))
 return layout
def show_stats(db):
 console.print(dashboard_snapshot(db))
def show_incidents(db):
 t=Table(title="Recent Incidents")
 for c in ["Severity","Rule","Source","Status","Response"]:t.add_column(c)
 for r in db.incidents():t.add_row(r["severity"],r["type"],r["source"],r["status"],r["response"] or "-")
 console.print(t)

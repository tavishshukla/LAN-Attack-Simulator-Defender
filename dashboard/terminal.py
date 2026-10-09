from rich.console import Console
from rich.table import Table
from rich.panel import Panel
console=Console()
def live_event(e): console.print(f'[dim][SIM][/dim] {e.event_type} source={e.source} port={e.port or "-"}')
def show_alert(a): console.print(Panel(f'[bold]{a.severity.value}[/bold] {a.rule_id}\n{a.description}\nSource: {a.source}',title='SECURITY ALERT',border_style='red'))
def show_stats(db):
 counts,sevs=db.stats(); t=Table(title='LAN DEFENDER STATISTICS'); t.add_column('Metric'); t.add_column('Count')
 for k,v in counts.items(): t.add_row(k.title(),str(v))
 for r in sevs: t.add_row(f'Alerts ({r["severity"]})',str(r['n']))
 console.print(t)
def show_incidents(db):
 t=Table(title='Recent Incidents')
 for c in ['Severity','Rule','Source','Status','Response']: t.add_column(c)
 for r in db.incidents(): t.add_row(r['severity'],r['type'],r['source'],r['status'],r['response'] or '-')
 console.print(t)

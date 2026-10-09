import sqlite3,json
from pathlib import Path
class Database:
 def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
 def _conn(self):
  c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
 def initialize(self):
  with self._conn() as c: c.executescript('CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY,timestamp TEXT,event_type TEXT,source TEXT,destination TEXT,port INTEGER,protocol TEXT,metadata TEXT,simulation_id TEXT); CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY,timestamp TEXT,rule_id TEXT,title TEXT,description TEXT,source TEXT,destination TEXT,severity TEXT,related_events TEXT,response_status TEXT); CREATE TABLE IF NOT EXISTS incidents(incident_id TEXT PRIMARY KEY,alert_id TEXT,timestamp TEXT,severity TEXT,source TEXT,type TEXT,status TEXT,response TEXT,notes TEXT);')
 def insert_event(self,e):
  with self._conn() as c: c.execute('INSERT OR REPLACE INTO events VALUES(?,?,?,?,?,?,?,?,?)',(e.event_id,e.timestamp.isoformat(),e.event_type,e.source,e.destination,e.port,e.protocol,json.dumps(e.metadata),e.simulation_id))
 def insert_alert(self,a):
  with self._conn() as c: c.execute('INSERT OR REPLACE INTO alerts VALUES(?,?,?,?,?,?,?,?,?,?)',(a.alert_id,a.timestamp.isoformat(),a.rule_id,a.title,a.description,a.source,a.destination,a.severity.value,json.dumps(a.related_events),'DETECTED'))
 def insert_incident(self,a):
  import uuid
  with self._conn() as c: c.execute('INSERT INTO incidents VALUES(?,?,?,?,?,?,?,?,?)',(str(uuid.uuid4()),a.alert_id,a.timestamp.isoformat(),a.severity.value,a.source,a.rule_id,'OPEN','',a.description))
 def update_incident_response(self,alert_id,response):
  with self._conn() as c: c.execute('UPDATE incidents SET response=? WHERE alert_id=?',(response,alert_id))
 def stats(self):
  with self._conn() as c: return {k:c.execute(f'SELECT COUNT(*) FROM {k}').fetchone()[0] for k in ['events','alerts','incidents']},c.execute('SELECT severity,COUNT(*) n FROM alerts GROUP BY severity').fetchall()
 def incidents(self):
  with self._conn() as c: return c.execute('SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 25').fetchall()
 def recent_events(self,limit=30):
  with self._conn() as c: return c.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ?',(limit,)).fetchall()

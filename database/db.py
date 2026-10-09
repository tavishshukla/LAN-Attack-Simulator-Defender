import sqlite3,json
from pathlib import Path
class Database:
 def __init__(self,path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
 def _conn(self):
  c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
 def initialize(self):
  with self._conn() as c: c.executescript('CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY,timestamp TEXT,event_type TEXT,source TEXT,destination TEXT,port INTEGER,protocol TEXT,metadata TEXT,simulation_id TEXT); CREATE TABLE IF NOT EXISTS alerts(alert_id TEXT PRIMARY KEY,timestamp TEXT,rule_id TEXT,title TEXT,description TEXT,source TEXT,destination TEXT,severity TEXT,related_events TEXT,response_status TEXT); CREATE TABLE IF NOT EXISTS incidents(incident_id TEXT PRIMARY KEY,alert_id TEXT,timestamp TEXT,severity TEXT,source TEXT,type TEXT,status TEXT,response TEXT,notes TEXT); CREATE TABLE IF NOT EXISTS siem_events(record_id INTEGER,channel TEXT,event_id INTEGER,timestamp TEXT,computer TEXT,source TEXT,message TEXT,level TEXT,data TEXT,PRIMARY KEY(channel,record_id)); CREATE TABLE IF NOT EXISTS siem_alerts(id INTEGER PRIMARY KEY AUTOINCREMENT,record_id INTEGER,channel TEXT,event_id INTEGER,timestamp TEXT,rule TEXT,severity TEXT,description TEXT);')
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
 def insert_siem_event(self,e):
  with self._conn() as c: c.execute('INSERT OR IGNORE INTO siem_events VALUES(?,?,?,?,?,?,?,?,?)',(e["record_id"],e["channel"],e["event_id"],e["timestamp"],e["computer"],e["source"],e["message"],e["level"],json.dumps(e["data"])))
 def insert_siem_alert(self,e):
  with self._conn() as c: c.execute('INSERT INTO siem_alerts(record_id,channel,event_id,timestamp,rule,severity,description) VALUES(?,?,?,?,?,?,?)',(e["record_id"],e["channel"],e["event_id"],e["timestamp"],e["rule"],e["severity"],e["description"]))
 def siem_alerts(self,limit=30):
  with self._conn() as c: return c.execute('SELECT * FROM siem_alerts ORDER BY id DESC LIMIT ?',(limit,)).fetchall()
 def siem_events(self,limit=50):
  with self._conn() as c: return c.execute('SELECT * FROM siem_events ORDER BY timestamp DESC LIMIT ?',(limit,)).fetchall()
 def recent_events(self,limit=30):
  with self._conn() as c: return c.execute('SELECT * FROM events ORDER BY timestamp DESC LIMIT ?',(limit,)).fetchall()
 def health(self):
  with self._conn() as c:
   return {"path":str(self.path),"events":c.execute("SELECT COUNT(*) FROM events").fetchone()[0],"alerts":c.execute("SELECT COUNT(*) FROM alerts").fetchone()[0],"incidents":c.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]}

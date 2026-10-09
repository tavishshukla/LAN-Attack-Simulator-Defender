from collections import defaultdict,deque
from datetime import timedelta
from .alerts import Alert
from .severity import Severity
class Rule:
 def __init__(self,key,threshold,window,severity):self.key,self.threshold,self.window,self.severity=key,threshold,window,Severity(severity)
class DetectionRules:
 def __init__(self,cfg):
  self.rules={"port_scan":Rule("PORT_SCAN_01",cfg["port_scan"]["threshold"],cfg["port_scan"]["window_seconds"],cfg["port_scan"]["severity"]),"connection_burst":Rule("CONNECTION_BURST_01",cfg["connection_burst"]["threshold"],cfg["connection_burst"]["window_seconds"],cfg["connection_burst"]["severity"]),"failed_login":Rule("FAILED_LOGIN_01",cfg["failed_login"]["threshold"],cfg["failed_login"]["window_seconds"],cfg["failed_login"]["severity"]),"http_burst":Rule("HTTP_BURST_01",cfg["http_burst"]["threshold"],cfg["http_burst"]["window_seconds"],cfg["http_burst"]["severity"])};self.events=defaultdict(deque);self.triggered=set()
 def check(self,event):
  q=self.events[event.source];q.append(event);now=event.timestamp;max_window=max(r.window for r in self.rules.values())
  while q and now-q[0].timestamp>timedelta(seconds=max_window):q.popleft()
  types={"port_scan":"PORT_CONNECTION","connection_burst":"CONNECTION","failed_login":"LOGIN_FAILURE","http_burst":"HTTP_REQUEST"};out=[]
  for name,r in self.rules.items():
   ev=[x for x in q if x.event_type==types[name] and now-x.timestamp<=timedelta(seconds=r.window)];metric=len({x.port for x in ev}) if name=="port_scan" else len(ev);sig=(r.key,event.source)
   if metric>=r.threshold and sig not in self.triggered:
    self.triggered.add(sig);out.append(Alert(r.key,r.key.replace("_"," ").title(),f"Threshold {r.threshold} exceeded ({metric}).",event.source,event.destination,r.severity,[x.event_id for x in ev]))
  return out

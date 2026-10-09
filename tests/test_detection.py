from datetime import datetime,timezone,timedelta
from core.events import Event
from defender.detector import Detector
def cfg():
 return {'port_scan':{'threshold':3,'window_seconds':5,'severity':'HIGH'},'connection_burst':{'threshold':99,'window_seconds':5,'severity':'MEDIUM'},'failed_login':{'threshold':2,'window_seconds':30,'severity':'HIGH'},'http_burst':{'threshold':99,'window_seconds':10,'severity':'MEDIUM'}}
def test_port_scan_detects():
 d=Detector(cfg()); t=datetime.now(timezone.utc); alerts=[]
 for i,p in enumerate([20,21,22]): alerts += d.process(Event('PORT_CONNECTION',port=p,timestamp=t+timedelta(seconds=i)))
 assert alerts[0].rule_id=='PORT_SCAN_01'
def test_failed_login_detects():
 d=Detector(cfg()); t=datetime.now(timezone.utc); alerts=[]
 for i in range(2): alerts += d.process(Event('LOGIN_FAILURE',timestamp=t+timedelta(seconds=i)))
 assert any(a.rule_id=='FAILED_LOGIN_01' for a in alerts)

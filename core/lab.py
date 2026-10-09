from time import sleep
from defender.detector import Detector
from defender.response import ResponseEngine
from dashboard.terminal import live_event,show_alert
from simulator.port_scan import PortScanSimulator
from simulator.connection_burst import ConnectionBurstSimulator
from simulator.failed_login import FailedLoginSimulator
from simulator.http_burst import HttpBurstSimulator
def run_lab(cfg,db):
 detector=Detector(cfg["detection"]);response=ResponseEngine();print("\n=== LAN DEFENDER | CYBERSECURITY LAB ===\n")
 for sim in [PortScanSimulator(),ConnectionBurstSimulator(),FailedLoginSimulator(),HttpBurstSimulator()]:
  print(f"[SIM] {sim.name}")
  for event in sim.generate():
   db.insert_event(event);live_event(event)
   for alert in detector.process(event):
    db.insert_alert(alert);db.insert_incident(alert);show_alert(alert);action=response.respond(alert);db.update_incident_response(alert.alert_id,action);print(f"[RESP] {action}")
   sleep(.01)
 print("\nLab complete. Run stats to inspect results.\n")

import argparse, json
from pathlib import Path
from core.config import load_config
from core.lab import run_lab
from database.db import Database
from dashboard.terminal import show_stats, show_incidents
from simulator.port_scan import PortScanSimulator
from simulator.connection_burst import ConnectionBurstSimulator
from simulator.failed_login import FailedLoginSimulator
from simulator.http_burst import HttpBurstSimulator

ROOT=Path(__file__).parent

def main():
 p=argparse.ArgumentParser(description="LAN Attack Simulator + Defender")
 p.add_argument("command",choices=["lab","simulator","defender","monitor","siem","incidents","stats","config","web"])
 a=p.parse_args()
 cfg=load_config(ROOT/"config/config.json")
 db=Database(ROOT/"data/lab.db")
 db.initialize()

 if a.command=="lab":
  run_lab(cfg,db)
 elif a.command=="simulator":
  sims=[PortScanSimulator(),ConnectionBurstSimulator(),FailedLoginSimulator(),HttpBurstSimulator()]
  for i,s in enumerate(sims,1):print(f"{i}. {s.name}")
  c=input("Select simulation (1-4, a=all): ").strip().lower()
  selected=sims if c=="a" else [sims[int(c)-1]]
  for s in selected:
   for e in s.generate():
    db.insert_event(e);print(f"[SIM] {e.event_type}: {e.metadata}")
 elif a.command in ("defender","monitor"):
  from monitor.engine import run_monitor
  run_monitor(cfg,db)
 elif a.command=="siem":
  from siem.engine import SIEM
  SIEM(db).run()
 elif a.command=="incidents":
  show_incidents(db)
 elif a.command=="stats":
  show_stats(db)
 elif a.command=="web":
  from webapp.app import create_app
  create_app().run(host="127.0.0.1",port=5000,debug=False)
 else:
  print(json.dumps(cfg,indent=2))

if __name__=="__main__":
 main()

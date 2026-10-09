import uuid
from datetime import datetime,timezone,timedelta
from core.events import Event
from .base import Simulator
class PortScanSimulator(Simulator):
 name="Port Scan Simulation"
 def generate(self):
  sid=str(uuid.uuid4());start=datetime.now(timezone.utc)
  for i,p in enumerate([20,21,22,23,25,53,80,110,139,443,445,8080]):yield Event("PORT_CONNECTION",port=p,metadata={"simulated":True},simulation_id=sid,timestamp=start+timedelta(milliseconds=i*100))

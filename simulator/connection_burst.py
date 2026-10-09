import uuid
from datetime import datetime,timezone,timedelta
from core.events import Event
from .base import Simulator
class ConnectionBurstSimulator(Simulator):
 name="Connection Burst Simulation"
 def generate(self):
  sid=str(uuid.uuid4());start=datetime.now(timezone.utc)
  for i in range(35):yield Event("CONNECTION",port=8000+i%3,metadata={"simulated":True},simulation_id=sid,timestamp=start+timedelta(milliseconds=i*100))

import uuid
from datetime import datetime,timezone,timedelta
from core.events import Event
from .base import Simulator
class HttpBurstSimulator(Simulator):
 name="HTTP Request Burst Simulation"
 def generate(self):
  sid=str(uuid.uuid4());start=datetime.now(timezone.utc)
  for i in range(55):yield Event("HTTP_REQUEST",protocol="HTTP",port=8080,metadata={"method":"GET","path":"/login","simulated":True},simulation_id=sid,timestamp=start+timedelta(milliseconds=i*100))

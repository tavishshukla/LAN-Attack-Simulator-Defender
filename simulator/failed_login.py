import uuid
from datetime import datetime,timezone,timedelta
from core.events import Event
from .base import Simulator
class FailedLoginSimulator(Simulator):
 name="Failed Login Simulation"
 def generate(self):
  sid=str(uuid.uuid4());start=datetime.now(timezone.utc)
  for i in range(7):yield Event("LOGIN_FAILURE",protocol="AUTH",metadata={"username":"admin","simulated":True},simulation_id=sid,timestamp=start+timedelta(seconds=i))

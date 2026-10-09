from dataclasses import dataclass,field
from datetime import datetime,timezone
import uuid
@dataclass
class Event:
 event_type:str;source:str="127.0.0.1";destination:str="127.0.0.1";port:int|None=None;protocol:str="TCP";metadata:dict=field(default_factory=dict);simulation_id:str="";timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc));event_id:str=field(default_factory=lambda:str(uuid.uuid4()))

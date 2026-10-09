from dataclasses import dataclass,field
from datetime import datetime,timezone
import uuid
from .severity import Severity
@dataclass
class Alert:
 rule_id:str;title:str;description:str;source:str;destination:str;severity:Severity;related_events:list[str]=field(default_factory=list);timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc));alert_id:str=field(default_factory=lambda:str(uuid.uuid4()))

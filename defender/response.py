class ResponseEngine:
 def __init__(self):self.blocked=set();self.suspicious=set()
 def respond(self,alert):self.suspicious.add(alert.source);self.blocked.add(alert.source);return "SIMULATED_BLOCK"

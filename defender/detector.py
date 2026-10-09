from .rules import DetectionRules
class Detector:
 def __init__(self,cfg):self.rules=DetectionRules(cfg)
 def process(self,event):return self.rules.check(event)

import json
from pathlib import Path
def load_config(path:Path)->dict:
 with path.open(encoding="utf-8") as f:return json.load(f)

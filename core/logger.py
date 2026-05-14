import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("logs/agent.jsonl")
LOG_FILE.parent.mkdir(exist_ok=True)

def log_event(event: dict):
    event["timestamp"] = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
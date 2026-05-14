import json
from pathlib import Path
from datetime import datetime

PROV_PATH = Path("memory/provenance.jsonl")
PROV_PATH.parent.mkdir(exist_ok=True)

def record_execution(record: dict):
    record["timestamp"] = datetime.now().isoformat()
    with open(PROV_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")

def get_recent_failures(limit=10):
    if not PROV_PATH.exists():
        return []
    failures = []
    with open(PROV_PATH) as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("final_status") != "success":
                failures.append(rec)
                if len(failures) >= limit:
                    break
    return failures

def get_tool_statistics():
    stats = {}
    if not PROV_PATH.exists():
        return stats
    with open(PROV_PATH) as f:
        for line in f:
            rec = json.loads(line)
            for step in rec.get("trace", []):
                tool = step.get("tool")
                status = step.get("status")
                if tool not in stats:
                    stats[tool] = {"success": 0, "failed": 0, "partial": 0}
                if status in stats[tool]:
                    stats[tool][status] += 1
    return stats
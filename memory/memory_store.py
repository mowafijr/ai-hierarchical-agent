import json
from pathlib import Path

MEMORY_PATH = Path("memory/memory.json")

def load_memory():
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH) as f:
            return json.load(f)
    return {"user_preferences": {}}

def save_memory(memory):
    MEMORY_PATH.parent.mkdir(exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def remember_fact(key: str, value: str, memory: dict) -> str:
    memory["user_preferences"][key] = value
    save_memory(memory)
    return f"Remembered {key} = {value}"
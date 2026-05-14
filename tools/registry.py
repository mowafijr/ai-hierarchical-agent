from tools.time_tool import get_time
from tools.file_tool import read_file
from tools.notes_tool import save_note, list_notes
from tools.calculator_tool import safe_eval

TOOLS = {
    "get_time": {"func": get_time, "schema": {"required": []}, "description": "Current time"},
    "read_file": {"func": read_file, "schema": {"required": ["path"]}, "description": "Read file"},
    "save_note": {"func": save_note, "schema": {"required": ["title", "content"]}, "description": "Save note"},
    "list_notes": {"func": list_notes, "schema": {"required": []}, "description": "List notes"},
    "calculate": {"func": safe_eval, "schema": {"required": ["expression"]}, "description": "Calculate"}
}

def get_tool_schemas():
    return "\n".join(f"- {name}: {info['description']} (args: {info['schema'].get('required', [])})" for name, info in TOOLS.items())
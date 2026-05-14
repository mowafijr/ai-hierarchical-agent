def evaluate_step_success(tool_name: str, args: dict, result: str) -> str:
    if result.startswith(("Unknown tool:", "Missing argument:", "Tool error:", "File not found:")):
        return "failed"

    if tool_name == "read_file":
        if len(result.strip()) > 0 and not result.startswith("Error"):
            return "success"
        return "failed" if result.startswith("Error") else "partial"

    if tool_name == "calculate":
        if "=" in result and not result.startswith("Calculation error"):
            return "success"
        return "failed"

    if tool_name == "save_note":
        return "success" if result.startswith("Note saved:") else "failed"

    if tool_name in ("list_notes", "get_time"):
        return "success"

    return "success" if result and not result.startswith("Error") else "partial"
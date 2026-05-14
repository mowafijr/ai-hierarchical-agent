def evaluate_goal(user_input: str, trace: list) -> dict:
    if not trace:
        return {"status": "failed", "reason": "No execution steps."}
    successful = [t for t in trace if t.get("status") == "success"]
    failed = [t for t in trace if t.get("status") == "failed"]
    if not successful:
        return {"status": "failed", "reason": "No steps succeeded."}
    if failed:
        return {"status": "partial", "reason": "Some steps failed."}
    return {"status": "success", "reason": "All steps succeeded."}
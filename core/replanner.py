import json

class Replanner:
    def __init__(self, llm_client, tool_schemas: str):
        self.llm = llm_client
        self.tool_schemas = tool_schemas

    def replan_subgoal(self, subgoal: dict, failed_step: dict, error_msg: str, memory_facts: dict):
        system_prompt = f"""
You are a surgical replanner.

A step inside a subgoal failed. Revise ONLY the steps of this subgoal.

Original subgoal:
{json.dumps(subgoal, indent=2)}

Failed step:
{json.dumps(failed_step, indent=2)}

Error:
{error_msg}

Available tools:
{self.tool_schemas}

Memory:
{json.dumps(memory_facts)}

RULES:
- Do NOT change the subgoal name or intent.
- Output a new list of steps (same format) for this subgoal.
- You may adjust order, tool names, or arguments.
- Output ONLY valid JSON: [{{"action": "...", "input": {{...}}, "goal": "..."}}]
"""
        try:
            raw = self.llm.chat([{"role": "system", "content": system_prompt}], temperature=0.2, max_tokens=600)
            raw = raw.strip().replace("```json", "").replace("```", "").strip()
            new_steps = json.loads(raw)
            return new_steps if isinstance(new_steps, list) else []
        except Exception as e:
            return []
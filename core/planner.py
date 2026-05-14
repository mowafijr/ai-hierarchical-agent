import json
import jsonschema

# Schema for validating planner output
PLAN_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["subgoal", "steps"],
        "properties": {
            "subgoal": {"type": "string"},
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["action", "input"],
                    "properties": {
                        "action": {"type": "string"},
                        "input": {"type": "object"},
                        "goal": {"type": "string"},
                        "response": {"type": "string"}
                    }
                }
            }
        }
    }
}

class Planner:
    def __init__(self, llm_client, tool_schemas: str):
        self.llm = llm_client
        self.tool_schemas = tool_schemas

    def create_plan(self, user_input: str, memory_facts: dict):
        system_prompt = f"""
You are a subgoal decomposition planner.

Break the user request into SUBGOALS.
Each subgoal contains ordered steps.

OUTPUT STRICT JSON ONLY:

[
  {{
    "subgoal": "string describing intent",
    "steps": [
      {{
        "action": "tool_name OR respond",
        "input": {{...}},
        "goal": "what this step achieves",
        "response": "final answer"   // only for respond action
      }}
    ]
  }}
]

RULES:
- Subgoals represent meaningful phases (gather, analyze, compute, respond).
- Steps inside a subgoal must be minimal and executable.
- Only final subgoal should contain a "respond" step.
- For "respond" steps, include "response" field with the final answer.
- Do NOT over-decompose.
- Output ONLY valid JSON.

TOOLS:
{self.tool_schemas}

Memory:
{json.dumps(memory_facts or {{}})}
"""
        messages = [
            {{"role": "system", "content": system_prompt}},
            {{"role": "user", "content": user_input}}
        ]
        try:
            raw = self.llm.chat(messages, temperature=0.2, max_tokens=700)
            raw = raw.strip().replace("```json", "").replace("```", "").strip()
            plan = json.loads(raw)
            
            # Validate against schema
            try:
                jsonschema.validate(instance=plan, schema=PLAN_SCHEMA)
            except jsonschema.ValidationError as e:
                print(f"Plan validation error: {e.message}")
                return []
            
            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"Planner error: {e}")
            return []
import unittest
import json
from core.planner import PLAN_SCHEMA
import jsonschema

class TestPlannerSchema(unittest.TestCase):
    def test_valid_plan(self):
        valid_plan = [
            {
                "subgoal": "Gather information",
                "steps": [
                    {
                        "action": "get_time",
                        "input": {},
                        "goal": "Get current time"
                    },
                    {
                        "action": "respond",
                        "input": {},
                        "goal": "Provide response",
                        "response": "The current time is..."
                    }
                ]
            }
        ]
        # Should not raise
        jsonschema.validate(instance=valid_plan, schema=PLAN_SCHEMA)

    def test_invalid_plan_missing_subgoal(self):
        invalid_plan = [
            {
                "steps": []
            }
        ]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_plan, schema=PLAN_SCHEMA)

    def test_invalid_plan_missing_steps(self):
        invalid_plan = [
            {
                "subgoal": "Test"
            }
        ]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_plan, schema=PLAN_SCHEMA)

    def test_invalid_plan_missing_action(self):
        invalid_plan = [
            {
                "subgoal": "Test",
                "steps": [
                    {
                        "input": {}
                    }
                ]
            }
        ]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance=invalid_plan, schema=PLAN_SCHEMA)

if __name__ == "__main__":
    unittest.main()
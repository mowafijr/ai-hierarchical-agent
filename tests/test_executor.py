import unittest
from core.executor import Executor
from tools.calculator_tool import safe_eval
from tools.time_tool import get_time

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.tools = {
            "calculate": {"func": safe_eval, "schema": {"required": ["expression"]}},
            "get_time": {"func": get_time, "schema": {"required": []}}
        }
        self.executor = Executor(self.tools)

    def test_execute_calculate(self):
        result = self.executor.run("calculate", {"expression": "2 + 2"})
        self.assertIn("=", result)
        self.assertIn("4", result)

    def test_execute_get_time(self):
        result = self.executor.run("get_time", {})
        self.assertIn(":", result)  # Time contains colons

    def test_unknown_tool(self):
        result = self.executor.run("unknown_tool", {})
        self.assertIn("Unknown tool", result)

    def test_missing_argument(self):
        result = self.executor.run("calculate", {})
        self.assertIn("Missing argument", result)

if __name__ == "__main__":
    unittest.main()
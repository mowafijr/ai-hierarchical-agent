import unittest
from core.evaluator import evaluate_step_success
from core.goal_evaluator import evaluate_goal

class TestEvaluator(unittest.TestCase):
    def test_success_calculate(self):
        result = "2 + 2 = 4"
        status = evaluate_step_success("calculate", {}, result)
        self.assertEqual(status, "success")

    def test_failure_unknown_tool(self):
        result = "Unknown tool: foo"
        status = evaluate_step_success("foo", {}, result)
        self.assertEqual(status, "failed")

    def test_success_save_note(self):
        result = "Note saved: /path/to/note.txt"
        status = evaluate_step_success("save_note", {}, result)
        self.assertEqual(status, "success")

    def test_goal_evaluation_all_success(self):
        trace = [
            {"tool": "calculate", "status": "success"},
            {"tool": "get_time", "status": "success"}
        ]
        goal_result = evaluate_goal("test", trace)
        self.assertEqual(goal_result["status"], "success")

    def test_goal_evaluation_partial(self):
        trace = [
            {"tool": "calculate", "status": "success"},
            {"tool": "unknown", "status": "failed"}
        ]
        goal_result = evaluate_goal("test", trace)
        self.assertEqual(goal_result["status"], "partial")

    def test_goal_evaluation_empty_trace(self):
        goal_result = evaluate_goal("test", [])
        self.assertEqual(goal_result["status"], "failed")

if __name__ == "__main__":
    unittest.main()
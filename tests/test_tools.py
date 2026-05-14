import unittest
from tools.calculator_tool import safe_eval
from tools.time_tool import get_time

class TestCalculatorTool(unittest.TestCase):
    def test_addition(self):
        result = safe_eval("2 + 3")
        self.assertIn("5", result)

    def test_multiplication(self):
        result = safe_eval("4 * 5")
        self.assertIn("20", result)

    def test_complex_expression(self):
        result = safe_eval("(2 + 3) * 4")
        self.assertIn("20", result)

    def test_invalid_expression(self):
        result = safe_eval("invalid()")
        self.assertIn("Calculation error", result)

class TestTimeTool(unittest.TestCase):
    def test_get_time_format(self):
        result = get_time()
        # Should be in format YYYY-MM-DD HH:MM:SS
        parts = result.split(" ")
        self.assertEqual(len(parts), 2)
        self.assertEqual(len(parts[0].split("-")), 3)  # Date
        self.assertEqual(len(parts[1].split(":")), 3)  # Time

if __name__ == "__main__":
    unittest.main()
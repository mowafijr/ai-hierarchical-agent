import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def safe_eval(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode='eval')
        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op = OPERATORS.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
                return op(left, right)
            if isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                op = OPERATORS.get(type(node.op))
                if op is None:
                    raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
                return op(operand)
            raise ValueError(f"Unsupported expression: {type(node).__name__}")
        result = _eval(tree.body)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {e}"
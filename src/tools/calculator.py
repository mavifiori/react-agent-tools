from typing import Union

from langchain_core.tools import tool
import ast, operator

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

def safe_eval(node:ast.expr) -> Union[int, float]:
    if isinstance(node, ast.Constant):  
        return node.value
    if isinstance(node, ast.BinOp): 
        op = type(node.op)

        if op not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op.__name__}")
        left = safe_eval(node.left)
        right = safe_eval(node.right)

        if op == ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return SAFE_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -safe_eval(node.operand)
    raise ValueError("Unsupported expression")

@tool
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression and returns the exact result.
    Use whenever the user asks an arithmetic calculation question."""""
    try:
        tree = ast.parse(expression, mode="eval")
        result = safe_eval(tree.body)
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        else:
            return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
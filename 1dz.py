from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import re
import operator

app = FastAPI()

class Expression(BaseModel):
    expr: str

class Operation(BaseModel):
    a: float
    b: float
    op: str

current_expression = ""

def evaluate_simple_expression(a: float, b: float, op: str) -> float:
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    if op not in operations:
        raise ValueError(f"Неподдерживаемая операция: {op}")
    return operations[op](a, b)

def evaluate_complex_expression(expr: str) -> float:
    expr = expr.replace(" ", "")
    
    if not is_balanced(expr):
        raise ValueError("Несбалансированные скобки в выражении")
    
    while '(' in expr or ')' in expr:
        expr = evaluate_parentheses(expr)
    
    return evaluate_simple_expression_without_parentheses(expr)

def is_balanced(expr: str) -> bool:
    count = 0
    for char in expr:
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
            if count < 0:
                return False
    return count == 0

def evaluate_parentheses(expr: str) -> str:
    start = end = -1
    for i, char in enumerate(expr):
        if char == '(':
            start = i
        elif char == ')':
            end = i
            break
    
    if start == -1 or end == -1:
        return expr
    
    inner_expr = expr[start+1:end]
    result = evaluate_simple_expression_without_parentheses(inner_expr)
    
    return expr[:start] + str(result) + expr[end+1:]

def evaluate_simple_expression_without_parentheses(expr: str) -> float:
    expr = process_operations(expr, ['*', '/'])
    expr = process_operations(expr, ['+', '-'])
    return float(expr)

def process_operations(expr: str, ops: list) -> str:
    pattern = r'(-?\d+\.?\d*)([' + re.escape(''.join(ops)) + r'])(-?\d+\.?\d*)'
    while True:
        match = re.search(pattern, expr)
        if not match:
            break
        a = float(match.group(1))
        op = match.group(2)
        b = float(match.group(3))
        result = evaluate_simple_expression(a, b, op)
        expr = expr[:match.start()] + str(result) + expr[match.end():]
    return expr

@app.post("/set_expression/")
async def set_expression(expression: Expression):
    global current_expression
    current_expression = expression.expr
    return {"message": "Выражение установлено", "expression": current_expression}

@app.get("/get_expression/")
async def get_expression():
    return {"current_expression": current_expression}

@app.post("/calculate/")
async def calculate():
    if not current_expression:
        return {"error": "Выражение не установлено"}
    try:
        result = evaluate_complex_expression(current_expression)
        return {"result": result, "expression": current_expression}
    except Exception as e:
        return {"error": str(e)}

@app.post("/simple_operation/")
async def simple_operation(operation: Operation):
    try:
        result = evaluate_simple_expression(operation.a, operation.b, operation.op)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/add_to_expression/")
async def add_to_expression(operation: Operation):
    global current_expression
    try:
        part = f"({operation.a}{operation.op}{operation.b})"
        if current_expression:
            current_expression += f"+{part}"
        else:
            current_expression = part
        return {"message": "Часть выражения добавлена", "current_expression": current_expression}
    except Exception as e:
        return {"error": str(e)}

def solve(a, b, op):
    try:
        a = int(a)
        b = int(b)
    except:
        return {"error": "invalid operands"}

    if "add" == op:
        return {"result": a + b}
    if "mult" == op:
        return {"result": a * b}
    if "diff" == op:
        return {"result": a - b}
    if "sub" == op:
        if b == 0:
            return {"error": "division by zero"}
        return {"result": a / b}
    return {"error": "unknown operation"}

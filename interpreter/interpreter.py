from . import ValueType, RuntimeVal, NumberVal, NullVal
from . import BinaryExpr
from . import NodeType, Statement, Program


def evaluate_program(program: Program) -> RuntimeVal:
    lastEvaluated: RuntimeVal = NullVal()
    for statement in program.body:
        lastEvaluated = evaluate(statement)
    return lastEvaluated


def evaluate(astNode: Statement) -> RuntimeVal:
    match astNode.get_type():
        case 'NumericLiteral':
            return NumberVal(value=astNode.value)

        case 'NullLiteral':
            return NullVal()

        case 'BinaryExpr':
            return evaluate_binary_expression(astNode)

        case 'Program':
            return evaluate_program(astNode)

        case _:
            print(astNode.get_type())
            raise TypeError('Invalid AST node type')


def evaluate_binary_expression(binop: BinaryExpr) -> RuntimeVal:
    left_side: RuntimeVal = evaluate(binop.left)
    right_side: RuntimeVal = evaluate(binop.right)

    if left_side.get_type() == 'NUMBER' and right_side.get_type() == 'NUMBER':
        return eval_numeric_binop(left_side, right_side, binop.operator)

    return NullVal()


def eval_numeric_binop(left: NullVal, right: NullVal, operator: str) -> RuntimeVal:
    result = 0
    match operator:
        case '+':
            result = left.value + right.value
        case '-':
            result = left.value - right.value
        case '*':
            result = left.value * right.value
        case '/':
            result = left.value / right.value
        case 'MOD':
            result = left.value % right.value
        case 'DIV':
            result = left.value // right.value
        case _:
            pass

    return NumberVal(result)

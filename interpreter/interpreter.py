from . import ValueType, RuntimeVal, NumberVal, NullVal
from . import BinaryExpr, Identifier
from . import NodeType, Statement, Program
from . import Environment
from . import MK_NULL


def evaluate_program(program: Program, env: Environment) -> RuntimeVal:
    last_evaluated: RuntimeVal = MK_NULL
    for statement in program.body:
        last_evaluated = evaluate(statement, env)
    return last_evaluated


def evaluate(astNode: Statement, env: Environment) -> RuntimeVal:
    match astNode.get_type():
        case 'NumericLiteral':
            return NumberVal(value=astNode.value)

        case 'BinaryExpr':
            return evaluate_binary_expression(astNode, env)

        case 'Program':
            return evaluate_program(astNode, env)

        case 'Identifier':
            return evaluate_identifier(astNode, env)

        case _:
            raise TypeError('Invalid AST node type ' + astNode.get_type())


def evaluate_binary_expression(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    left_side: RuntimeVal = evaluate(binop.left, env)
    right_side: RuntimeVal = evaluate(binop.right, env)

    if left_side.get_type() == 'NUMBER' and right_side.get_type() == 'NUMBER':
        return eval_numeric_binop(left_side, right_side, binop.operator)

    return MK_NULL()


def eval_numeric_binop(left: NumberVal, right: NumberVal, operator: str) -> RuntimeVal:
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


def evaluate_identifier(identifier: Identifier, env: Environment) -> RuntimeVal:
    val = env.get_var(identifier.symbol)
    return val

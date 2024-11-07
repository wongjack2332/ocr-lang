# value types
from . import ValueType, RuntimeVal, NumberVal, NullVal, BoolVal
# Expression types
from . import BinaryExpr, Identifier, AssignmentExpr, UnaryExpr
# statement types
from . import NodeType, Statement, Program
from . import Environment
# value constructors
from . import MK_NULL, MK_BOOL, MK_NUMBER, MK_STRING


def evaluate_program(program: Program, env: Environment) -> RuntimeVal:
    last_evaluated: RuntimeVal = MK_NULL()
    for statement in program.body:
        last_evaluated = evaluate(statement, env)
    return last_evaluated


def evaluate(astNode: Statement, env: Environment) -> RuntimeVal:
    print(astNode.fields())
    match astNode.get_type():
        case 'NumericLiteral':
            return NumberVal(value=astNode.value)

        case 'StringLiteral':
            return MK_STRING(astNode.value)

        case 'BinaryExpr':
            return evaluate_binary_expression(astNode, env)

        case 'Program':
            return evaluate_program(astNode, env)

        case 'Identifier':
            return evaluate_identifier(astNode, env)

        case "AssignmentExpr":
            return evaluate_assignment_expr(astNode, env)

        case "UnaryExpr":
            return evaluate_unary_expression(astNode, env)

        case _:
            raise TypeError('Invalid AST node type ' + astNode.get_type())


def evaluate_assignment_expr(expr: AssignmentExpr, env: Environment) -> RuntimeVal:
    left_side = expr.left
    right_side: RuntimeVal = evaluate(expr.right, env)
    if expr.i_type == "CONST":
        right_side.set_const()

    env.assign_var(left_side, right_side)

    return right_side


def evaluate_binary_expression(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    left_side: RuntimeVal = evaluate(binop.left, env)
    right_side: RuntimeVal = evaluate(binop.right, env)

    if binop.binop_type == 'NUMERIC':
        return eval_numeric_binop(left_side, right_side, binop.operator)
    elif binop.binop_type == 'BOOLEAN':
        return eval_boolean_binop(left_side, right_side, binop.operator)

    return MK_NULL()


def eval_boolean_binop(left: BoolVal, right: BoolVal, operator: str) -> RuntimeVal:
    match operator:
        case 'AND':
            return MK_BOOL(left.value and right.value)

        case 'OR':
            return MK_BOOL(left.value or right.value)

        case _:
            raise RuntimeError(f"unable to parse operator {operator}")


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
            eval_comparison_expression(left, right, operator)

    return NumberVal(result)


def eval_comparison_expression(left, right, operator) -> BoolVal:
    match operator:
        case '<':
            return MK_BOOL(left.value < right.value)
        case '>':
            return MK_BOOL(left.value > right.value)
        case '>=':
            return MK_BOOL(left.value >= right.value)
        case '<=':
            return MK_BOOL(left.value <= right.value)
        case '==':
            return MK_BOOL(left.value == right.value)
        case '!=':
            return MK_BOOL(left.value != right.value)

        case _:
            pass


def evaluate_unary_expression(unop: UnaryExpr, env: Environment) -> RuntimeVal:
    right = evaluate(unop.right, env)
    match unop.operator:
        case 'NOT':
            print(type(right))
            return MK_BOOL(not bool(right))


def evaluate_identifier(identifier: Identifier, env: Environment) -> RuntimeVal:
    val = env.get_var(identifier.symbol)
    return val

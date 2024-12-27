# value types
from re import L
from typing import Any



from . import Block, IfBlock, IfStatement
from . import ValueType, RuntimeVal, NumberVal, NullVal, BoolVal, ListVal
# Expression types
from . import BinaryExpr, Identifier, AssignmentExpr, UnaryExpr, ArrayIndex, MemberExpr, ListExpression
# statement types
from . import NodeType, Statement, Program
from . import Environment
# value constructors
from . import MK_NULL, MK_BOOL, MK_NUMBER, MK_STRING, MK_LIST, is_iterable, is_mutable_iterable



# TODO: create some sort of expected type to prevent passing in wrong types, e.g. functions names into expression evalutions


def evaluate_program(program: Program | Block, env: Environment) -> RuntimeVal:
    last_evaluated: RuntimeVal = MK_NULL()
    for statement in program.body:
        last_evaluated = evaluate(statement, env)
    return last_evaluated


def evaluate(astNode: Statement, env: Environment) -> RuntimeVal:
    match astNode.get_type():
        case 'FuncBlock':
            return evaluate_func_block(astNode, env)
        case 'IfBlock':
            return evaluate_if_block(astNode, env)
        case 'ForBlock':
            return evaluate_for_block(astNode, env)
        
        case 'WhileBlock':
            return evaluate_while_block(astNode, env)
        
        case 'ListExpression':
            return evaluate_list_expression(astNode, env)
        
        case 'FunctionCall':
            return evaluate_function_call(astNode, env)
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
        
        case "ArrayAssignmentExpr":
            return evaluate_assignment_expr(astNode, env)
        
        case "ArrayIndex":
            return evaluate_array_index(astNode, env)

        case "UnaryExpr":
            return evaluate_unary_expression(astNode, env)        
        
        case "MemberExpr":
            return evaluate_member_expr(astNode, env)

        case _:
            raise TypeError('Invalid AST node type ' + astNode.get_type())


def evaluate_func_block(func_block, env: Environment) -> Any:
    env.assign_var(func_block.name, func_block)
    return MK_NULL()

def evaluate_if_block(if_block, env: Environment) -> Any:
    if_block.reset_conditions()

    while True:
        curr_condition = if_block.next_condition()
        if curr_condition is None:
            return MK_NULL()
        if curr_condition.condition is None:
            if_block.reset_conditions()
            return evaluate_program(curr_condition, env)
        if evaluate(curr_condition.condition, env):
            return evaluate_program(curr_condition, env)

def evaluate_for_block(for_block, env: Environment) -> Any:
    evaluate(for_block.initialising_expr, env)
    if isinstance(for_block.step, BinaryExpr):
        for_block.step = evaluate(for_block.step, env)
    while env.get_var(for_block.initialiser).value != for_block.limit.value:
        evaluate_program(for_block, env)
        env.assign_var(for_block.initialiser, MK_NUMBER(env.get_var(for_block.initialiser).value + (for_block.step.value or 1)))
    
    return MK_NULL()


def evaluate_while_block(while_block, env: Environment) -> Any:
    while evaluate(while_block.condition, env):
        evaluate_program(while_block, env)

    return MK_NULL()
    


def evaluate_assignment_expr(expr: AssignmentExpr, env: Environment) -> RuntimeVal:
    left_side = expr.left
    evaluation: RuntimeVal | list[Any] = evaluate(expr.right, env)
    if isinstance(evaluation, RuntimeVal):
        right_side = evaluation
    else:
        right_side = MK_LIST(evaluation)
    if expr.i_type == "CONST":
        right_side.set_const()
        env.assign_var(left_side, right_side)
    elif expr.i_type == "GLOBAL":
        env.assign_global_var(left_side, right_side)
    else:
        env.assign_var(left_side, right_side)

    return right_side


def evaluate_member_expr(expr: MemberExpr, env: Environment) -> RuntimeVal:
    object_ = env.get_var(expr.name)
    method = expr.method
    arguments = evaluate_list_expression(expr.arguments, env)
    if "method_set" in dir(object_):
        method_set = object_.method_set
    else:
        raise TypeError(f"Method set not available for {expr.name}")
    
    if method not in method_set:
        raise NameError(f"Method {method} not found in object {expr.name}")
    
    return method_set[method](*arguments.value)

def evaluate_array_index(expr: ArrayIndex, env: Environment) -> RuntimeVal:
    array = env.get_var(expr.array)
    if not is_iterable(array):
        raise TypeError(f"Name {expr.array} is not an iterable") 

    index = evaluate(expr.index, env)
    if not isinstance(index, NumberVal):
        raise RuntimeError(f"Index {expr.index} is not valid, index={index}")

    if not expr.assign:
        return array.get_index(index.value)
    
    if not is_mutable_iterable(array):
        raise TypeError(f"Name {expr.array} is not a mutable iterable")

    right = evaluate(expr.right, env)
    if isinstance(right, list):
        right = MK_LIST(right)

    array.set_index(index, right)
    return array

def evaluate_function_call(function_call, env: Environment) -> RuntimeVal | None:
    func_name = function_call.name
    func_block = env.get_var(func_name)

    if func_block.get_type() not in ("FuncBlock", "EXT_NAME"):
        raise RuntimeError(f"name {func_name} is not a callable")
    
    arguments: ListVal = evaluate_list_expression(function_call.arguments, env)

    if func_block.get_type() == "EXT_NAME":
        evaluation = func_block.value(*(arguments.value))
        if type(evaluation) == int:
            return MK_NUMBER(evaluation)
        elif type(evaluation) == bool:
            return MK_BOOL(evaluation)
        elif type(evaluation) == str:
            return MK_STRING(evaluation)
        elif evaluation is None:
            return MK_NULL() 
        else:
            return evaluation
        
    evaluation = evaluate_function(func_block, arguments, env)
    return evaluation


def evaluate_function(func_block, arguments, env:Environment):
    parameters = func_block.parameters
    if len(parameters) != arguments.length:
        raise RuntimeError(f"Incorrect amount of arguments, expected {len(parameters)}, got {len(arguments)}")
    
    new_env = Environment(parent=env)
    for param, arg in zip(parameters, arguments.value):
        new_env.assign_var(varname=param, value=arg)
    evaluate_program(func_block, new_env)
    return evaluate(func_block.return_expr, new_env)
#TODO

def evaluate_list_expression(list_expr: ListExpression, env: Environment) -> ListVal:
    return MK_LIST([evaluate(arg, env) for arg in list_expr.elements])


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
            return eval_comparison_expression(left, right, operator)

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

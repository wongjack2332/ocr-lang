from typing import Any, Self

from interpreter.ast import NumericLiteral
from . import NodeType, Statement, Expression, AssignmentExpr


class Block:
    def __init__(self) -> None:
        self.node_type = NodeType('Block')
        self.body = []
    
    def body_append(self, statement: Statement | Self):
        self.body.append(statement)
    
    def fields(self) -> dict:
        return {'type': self.node_type.node_type, 'body': self.body}
    
    def get_type(self) -> str:
        return self.node_type.node_type



class IfStatement(Block):
    def __init__(self, condition) -> None:
        self.condition = condition
        super().__init__()
        self.node_type = NodeType("IfStatement")
    
    def fields(self) -> dict:
        return {'type': self.node_type.node_type, 'condition': self.condition, 'body': self.body}

    def get_type(self) -> str:
        return self.node_type.node_type


class IfBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.node_type = NodeType("IfBlock")
        self.conditions: list[IfStatement] = []
        self.pointer = 0 
    
    def add_condition(self, condition: IfStatement):
        self.conditions.append(condition)

    def next_condition(self) -> IfStatement | None:
        if self.pointer != len(self.conditions):
            condition = self.conditions[self.pointer]
            self.pointer += 1
            return condition
        return None
    
    def reset_conditions(self) -> None:
        self.pointer = 0
    
    def fields(self) -> dict:
        return {'type': self.node_type.node_type, 'conditions': self.conditions}

    def get_type(self) -> str:
        return self.node_type.node_type


class ForBlock(Block):
    def __init__(self, initialiser, limit, step=None) -> None:
        super().__init__()
        self.node_type = NodeType("ForBlock")
        self.initialiser = initialiser
        self.initialising_expr: None | AssignmentExpr = None
        self.limit = limit
        self.step = step or NumericLiteral(value=1)

    def next(self):
        self.initialiser += self.step
        return self.initialiser if self.initialiser < self.limit else None

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'initialiser': self.initialiser,
            'limit': self.limit,
            'step': self.step,
            'body': self.body,
        }
    
    def get_type(self) -> str:
        return self.node_type.node_type


class WhileBlock(Block):
    def __init__(self, condition: Expression) -> None:
        super().__init__()
        self.node_type = NodeType("WhileBlock")
        self.condition = condition
    
    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'condition': self.condition,
            'body': self.body,
        }
    
    def get_type(self) -> str:
        return self.node_type.node_type


class SwitchBlock(Block):
    pass


class CaseBlock(Block):
    pass


class FuncBlock(Block):
    def __init__(self, name: str, parameters: list[str] | None = None, body: list[Statement] | None = None, functype = 'FUNCTION', return_expr: Expression | None = None) -> None:
        """
        functypes: FUNCTION, PROCEDURE
        """

        super().__init__()
        self.node_type = NodeType("FuncBlock")
        self.name = name
        self.parameters: list[str] | None = parameters
        self.functype = functype
        self.return_expr: Expression | None = return_expr
    
    def get_type(self) -> str:
        return self.node_type.node_type
    
    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'name': self.name,
            'parameters': self.parameters,
            'body': self.body,
            'return_expr': self.return_expr
        }
class NodeType:
    """Node in AST"""

    def __init__(self, node_type: str) -> None:
        self.node_type = self.__parse_type(node_type)

    def __parse_type(self, node_type: str) -> str:
        available_types = (
            'Statement',
            'Program',
            'Block',
            'IfBlock',
            'IfStatement',
            'ForBlock',
            'FuncBlock',
            'WhileBlock',
            'NumericLiteral',
            'AssignmentExpr',
            'ArrayAssignmentExpr',
            'ListExpression',
            'FunctionCall',
            'Identifier',
            'ArrayIndex',
            'BinaryExpr',
            'UnaryExpr',
            'MemberExpr',
            'CallExpr',
            'FunctionDeclaration',
            'StringLiteral',
        )

        if node_type in available_types:
            return node_type
        raise ValueError(f'Invalid node type: {node_type}')


class Statement:
    """Statement in AST"""

    def __init__(self) -> None:
        self.node_type = NodeType('Statement')

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class Program(Statement):
    def __init__(self) -> None:
        super().__init__()
        self.node_type = NodeType('Program')
        self.body: list[Statement] = []

    def fields(self) -> dict: 
        return {'type': self.node_type.node_type, 'body': self.body}

    def get_type(self) -> str:
        return 'Program'


class Expression(Statement):
    """Expression in AST"""

    def __init__(self) -> None:
        super().__init__()

    def get_type(self) -> str:
        return self.node_type.node_type


class FunctionCall(Expression):
    def __init__(self, name, arguments) -> None:
        super().__init__()
        self.node_type = NodeType('FunctionCall')
        self.name = name
        self.arguments = arguments
    
    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'name': self.name,
            'arguments': self.arguments
        }

class ListExpression(Expression):
    def __init__(self, elements: list[Expression] | None = None) -> None:
        super().__init__()
        self.node_type = NodeType('ListExpression')
        self.elements = elements or list()
        self.length: int = len(self.elements)
    
    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'elements': self.elements
        }
    
    def get_type(self) -> str:
        return self.node_type.node_type


class AssignmentExpr(Expression):
    """Assignment expression in AST"""

    def __init__(self, left: str, right: Expression, i_type: str = "VAR") -> None:
        super().__init__()
        self.node_type = NodeType("AssignmentExpr")
        self.left: str = left
        self.right: Expression = right
        self.i_type = i_type

    def fields(self) -> dict:
        return {
            "type": self.node_type.node_type,
            "left": self.left,
            "right": self.right
        }

class ArrayAssignmentExpr(Expression):
    """Array Assignment expression in AST"""

    def __init__(self, left: str, length: int = 0, right: ListExpression | None = None, i_type="VAR") -> None:
        super().__init__()
        self.node_type = NodeType("ArrayAssignmentExpr")
        self.left: str = left
        self.length: int = length
        self.i_type: str = i_type
        if right is None:
            self.right: ListExpression = ListExpression(elements=[Identifier(symbol="None")] * length)
        else:
            if right.length != length:
                raise IndexError("Length of array assignment expression does not match length of array")
            self.right: ListExpression = right
        

class MemberExpr(Expression):
    def __init__(self, name: Expression, method: str, arguments: ListExpression, is_attribute = False) -> None:
        super().__init__()
        self.node_type = NodeType('MemberExpr')
        self.name = name
        self.method = method
        self.arguments = arguments
        self.is_attribute = is_attribute
    
    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'name': self.name,
            'method': self.method,
            'arguments': self.arguments,
            'is_attribute': self.is_attribute
        }
    
    def get_type(self) -> str:
        return self.node_type.node_type



class BinaryExpr(Expression):
    """Binary expression in AST"""

    def __init__(
        self,
        left: Expression = None,
        right: Expression = None,
        operator: str = None,
        binop_type: str = "NUMERIC"  # numberic, boolean
    ) -> None:

        super().__init__()
        self.node_type = NodeType('BinaryExpr')
        self.left: Expression = left
        self.right: Expression = right
        self.operator: str = operator
        self.binop_type = binop_type

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'left': self.left,
            'right': self.right,
            'operator': self.operator,
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class UnaryExpr(Expression):
    def __init__(self, operator: str = None, right: Expression = None) -> None:
        super().__init__()
        self.node_type = NodeType('UnaryExpr')
        self.operator: str = operator
        self.right = right

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'operator': self.operator,
            'right': self.right
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class Identifier(Expression):
    """Identifier in AST"""

    def __init__(self, symbol: str | None = None) -> None:
        super().__init__()
        self.node_type = NodeType('Identifier')
        self.symbol: str | None = symbol

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'symbol': self.symbol
        }

    def get_type(self) -> str:
        return self.node_type.node_type

class ArrayIndex(Expression):
    def __init__(self, array: str, index: Expression, right = None, assign=True):
        super().__init__()
        self.node_type = NodeType("ArrayIndex")
        self.array: str = array
        self.index: Expression = index
        self.right = right
        self.assign = assign
    
    def get_type(self) -> str:
        return self.node_type.node_type
    
    def fields(self) -> dict:
        return {
            "type": self.node_type.node_type,
            "array": self.array,
            "index": self.index,
            "right": self.right
        }


class NumericLiteral(Expression):
    """Numeric literal in AST"""

    def __init__(self, value: int = 0) -> None:
        super().__init__()
        self.node_type = NodeType('NumericLiteral')
        self.value: int = value

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'value': self.value
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class StringLiteral(Expression):
    def __init__(self, value: str = '') -> None:
        super().__init__()
        self.node_type = NodeType('StringLiteral')
        self.value: str = value[1:-1]

    def fields(self) -> dict:
        return {
            'type': self.node_type.node_type,
            'value': self.value
        }

    def get_type(self) -> str:
        return self.node_type.node_type

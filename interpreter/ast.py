class NodeType:
    """Node in AST"""

    def __init__(self, node_type: str) -> None:
        self.node_type = self.__parse_type(node_type)

    def __parse_type(self, node_type: str) -> str:
        available_types = (
            'Statement',
            'Program',
            'NumericLiteral',
            'AssignmentExpr',
            'Identifier',
            'BinaryExpr',
            'UnaryExpr',
            'CallExpr',
            'FunctionDeclaration',
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

    def fields(self) -> str:
        return {'type': self.node_type.node_type, 'body': self.body}

    def get_type(self) -> str:
        return 'Program'


class Expression(Statement):
    """Expression in AST"""

    def __init__(self) -> None:
        super().__init__()

    def get_type(self) -> str:
        return self.node_type.node_type


class AssignmentExpr(Expression):
    """Assignment expression in AST"""

    def __init__(self, left: str, right: Expression) -> None:
        super().__init__()
        self.node_type = NodeType("AssignmentExpr")
        self.left: str = left
        self.right: Expression = right

    def fields(self) -> str:
        return {
            "type": self.node_type.node_type,
            "left": self.left,
            "right": self.right
        }


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

    def fields(self) -> str:
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

    def fields(self) -> str:
        return {
            'type': self.node_type.node_type,
            'operator': self.operator,
            'right': self.right
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class Identifier(Expression):
    """Identifier in AST"""

    def __init__(self, symbol: str = None) -> None:
        super().__init__()
        self.node_type = NodeType('Identifier')
        self.symbol: str = symbol

    def fields(self) -> str:
        return {
            'type': self.node_type.node_type,
            'symbol': self.symbol
        }

    def get_type(self) -> str:
        return self.node_type.node_type


class NumericLiteral(Expression):
    """Numeric literal in AST"""

    def __init__(self, value: int = None) -> None:
        super().__init__()
        self.node_type = NodeType('NumericLiteral')
        self.value: int = value

    def fields(self) -> str:
        return {
            'type': self.node_type.node_type,
            'value': self.value
        }

    def get_type(self) -> str:
        return self.node_type.node_type

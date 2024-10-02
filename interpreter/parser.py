from . import Statement, Program, Expression, AssignmentExpr, BinaryExpr, Identifier, NumericLiteral, NodeType
from . import Lexer


class Parser:
    def __init__(self) -> None:
        self.tokens: Lexer = None

    def produce_ast(self, source) -> Program:
        self.tokens = Lexer(source)
        self.tokens.run()
        self.tokens.print_tokens()
        program: Program = Program()

        # parse until the end of file
        while not self.__eof():
            program.body.append(self.__parse_statement())
        # return AstBuilder(program)
        return program

    def at(self) -> dict:
        return self.tokens.tokens[0]

    def look_forward(self) -> dict:
        return self.tokens.tokens[1]

    def expect(self, token_type: str, err: str) -> dict:
        prev = self.next_token()
        if not prev or prev['type'] != token_type:
            raise EOFError(f'{err}, instead found "{prev["value"]}"')

        return prev

    def next_token(self):
        return self.tokens.next_token()

    def __eof(self) -> bool:
        return self.tokens.tokens[0]['type'] == 'EOF'

    def __parse_statement(self) -> Statement:
        # skip to parse expression
        return self.__parse_expression()

    def __parse_expression(self) -> Expression:
        return self.__parse_assignment_expression()

    # orders of precedence
    """
    AssignmentExpr
    MemberExpr
    FunctionCall
    LogicalExpr
    ComparisonExpr
    Additive Expr
    Multiplicative Expr
    Unary Expr
    Primary Expr
    """

    def __parse_assignment_expression(self) -> Expression:
        tk: dict = self.at()
        next_level = self.__parse_logical_expression
        match tk['type']:
            case "NAME":
                identifier = tk['value']
                left = identifier
                if self.look_forward()['type'] == "ASSIGN":
                    self.next_token()
                    assign_operator = self.next_token()
                    right: Expression = next_level()
                    return AssignmentExpr(left=left, right=right)

                return next_level()
            case _:
                return next_level()

    def __parse_logical_expression(self) -> Expression:
        next_level = self.__parse_comparison_expression
        left = next_level()
        while self.at()['type'] == "LOGIC":
            operator = self.next_token()['value']
            right = next_level()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator, binop_type="BOOLEAN")

        return left

    def __parse_comparison_expression(self) -> Expression:
        next_level = self.__parse_additive_expression
        left = next_level()
        while self.at()['type'] == 'COMPARE':
            operator = self.next_token()['value']
            right = next_level()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator)

        return left

    def __parse_additive_expression(self) -> Expression:
        """Additive expression: 10 + 4 - 5"""
        left = self.__parse_multiplicative_expression()
        while self.at()['value'] in ('+', '-'):
            operator = self.next_token()['value']
            right = self.__parse_multiplicative_expression()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator)

        return left

    def __parse_multiplicative_expression(self) -> Expression:
        """Multiplicative expression: 10 * 4 / 5"""
        left = self.__parse_primary_expression()
        while self.at()['value'] in ('/', '*', 'DIV', 'MOD'):
            operator = self.next_token()['value']
            right = self.__parse_primary_expression()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator)

        return left

    def __parse_primary_expression(self) -> Expression:
        tk: dict = self.next_token()

        match tk['type']:
            case 'NAME':
                identifier = Identifier()
                identifier.symbol = tk['value']

                return identifier

            case 'NUMBER':
                numeric_literal = NumericLiteral()
                numeric_literal.value = int(tk['value'])
                return numeric_literal

            case 'LPAREN':
                value = self.__parse_expression()
                self.expect('RPAREN', 'Expected ")"')
                return value

            # case 'NULL':
            #     return NullLiteral()
            case _:
                raise ValueError(f"unexpected token found {tk}")


class AstBuilder:
    """AST builder"""

    def __init__(self, program: Program) -> None:
        self.program = program
        self.ast = self.build()

    def fill(self, statement: Statement):
        fields = statement.fields()
        for k, v in fields.items():
            if isinstance(v, Statement):
                fields[k] = self.fill(v)

            if isinstance(v, list):
                for i, val in enumerate(v):
                    fields[k][i] = self.fill(val)

        return fields

    def build(self):
        self.ast = self.fill(self.program)
        return self.ast

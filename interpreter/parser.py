from . import Statement, Program
from . import Expression, AssignmentExpr, BinaryExpr, UnaryExpr
from . import Identifier, NumericLiteral, StringLiteral
from . import Block, IfStatement, IfBlock, IfBlock, ForBlock, FuncBlock, WhileBlock, SwitchBlock, CaseBlock
from . import Lexer


class Parser:
    def __init__(self) -> None:
        self.tokens: Lexer | None = None

    def produce_ast(self, source) -> Program:
        self.tokens = Lexer(source)
        self.tokens.run()
        self.tokens.print_tokens()
        program: Program = Program()

        # parse until the end of file
        while not self.__eof():
            program.body.append(self.__parse_next())
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
        return self.at()['type'] == 'EOF'

    def __parse_next(self):
        curr_token = self.at()

        match curr_token['type']:
            case 'IF':
                return self.__parse_if_block()
            case _:
                return self.__parse_statement()
    
    def __parse_block(self, block: Block, terminators: tuple[str]):
        while self.at()['type'] not in terminators:
            block.body_append(self.__parse_next())
        
        

    
    def __parse_if_block(self):
        if_block = IfBlock()
        while self.at()['type'] != 'ENDIF':
            curr_type = self.at()['type']
            match curr_type: 
                case 'IF':
                    if_block.add_condition(self.__parse_if_statement(('ELSEIF', 'ENDIF')))
                case 'ELSEIF':
                    if_block.add_condition(self.__parse_if_statement(('ELSEIF', 'ELSE', 'ENDIF')))
                case 'ELSE':
                    if_block.add_condition(self.__parse_else_statement(('ENDIF',)))

                case _:
                    raise SyntaxError('Unable to find terminator of if-statement: missing elseif or endif')
        
        self.next_token() # discard 'ENDIF'
        self.expect("NEWLINE", "Expected newline after endif")
        
        return if_block

    def __parse_statement(self) -> Statement:
        parsed_expression = self.__parse_expression()
        curr_token = self.at()
        match curr_token['type']:
            case 'NEWLINE':
                self.next_token()
                return parsed_expression
            case 'EOF':
                return parsed_expression
        
        raise SyntaxError(f'Expected newline or EOF instead of {curr_token["type"]}: {curr_token["value"]}')
    
    def __parse_if_statement(self, terminators: tuple = ("ELSEIF", "ELSE", "ENDIF")) -> IfStatement:
        self.next_token() # discard 'IF'
        condition = self.__parse_logical_expression()
        self.expect('THEN', 'Expected "then"') # discard 'THEN'
        self.expect('NEWLINE', 'Expected newline after "then"') # discard 'NEWLINE
        if_statement = IfStatement(condition=condition)
        self.__parse_block(if_statement, terminators)
        return if_statement
    
    def __parse_else_statement(self, terminators: tuple = ("ENDIF",)):
        self.next_token() # discard 'ELSE'
        self.expect('NEWLINE', 'Expected newline after "else"') # discard 'NEWLINE
        if_statement = IfStatement(condition=None)
        self.__parse_block(if_statement, terminators)
        return if_statement

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
            case "CONST":
                self.next_token()
                identifier = self.at()['value']
                if self.look_forward()['type'] == "ASSIGN":
                    self.next_token()
                    assign_operator = self.next_token()
                    right: Expression = next_level()
                    return AssignmentExpr(left=identifier, right=right, i_type="CONST")
                else:
                    raise RuntimeError(f"""expected '=' operator, but found {
                                       self.look_forward()['value']}""")
            case "GLOBAL":
                pass
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
        next_level = self.__parse_multiplicative_expression
        left = next_level()
        while self.at()['value'] in ('+', '-'):
            operator = self.next_token()['value']
            right = next_level()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator)

        return left

    def __parse_multiplicative_expression(self) -> Expression:
        """Multiplicative expression: 10 * 4 / 5"""
        next_level = self.__parse_unary_expression
        left = next_level()
        while self.at()['value'] in ('/', '*', 'DIV', 'MOD'):
            operator = self.next_token()['value']
            right = next_level()
            left: BinaryExpr = BinaryExpr(
                left=left, right=right, operator=operator)

        return left

    def __parse_unary_expression(self) -> Expression:
        tk: dict = self.at()
        next_level = self.__parse_primary_expression
        match tk['type']:
            case 'NEG':
                operator = tk['value']
                self.next_token()
                right = next_level()
                return UnaryExpr(operator=operator, right=right)

            case _:
                return next_level()

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

            case 'STRING':
                string_literal = StringLiteral(value=tk['value'])
                return string_literal

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

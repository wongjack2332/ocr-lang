from interpreter.ast import ArrayAssignmentExpr
from . import Statement, Program
from . import Expression, AssignmentExpr, BinaryExpr, UnaryExpr, ListExpression, FunctionCall 
from . import Identifier, NumericLiteral, StringLiteral, ArrayIndex
from . import Block, IfStatement, IfBlock, IfBlock, ForBlock, FuncBlock, WhileBlock, SwitchBlock, CaseBlock
from . import Lexer
from . import ArrayAssignmentExpr


class Parser:
    def __init__(self) -> None:
        self.tokens: Lexer | None = None

    def produce_ast(self, source) -> Program:
        self.tokens = Lexer(source)
        self.tokens.run()
        program: Program = Program()

        # parse until the end of file
        while not self.__eof():
            parsed = self.__parse_next()

            if parsed != -1:
                program.body.append(parsed)
        # return AstBuilder(program)
        return program

    def at(self) -> dict:
        return self.tokens.tokens[0]

    def look_forward(self) -> dict:
        return self.tokens.tokens[1]

    def expect(self, token_type: str, err: str) -> dict:
        prev = self.next_token()
        if not prev or prev['type'] != token_type:
            raise SyntaxError(f'{err}, instead found "{prev["value"]}"')

        return prev

    def next_token(self):
        return self.tokens.next_token()

    def __eof(self) -> bool:
        return self.at()['type'] == 'EOF'

    def new_line_or_eof(self):
        curr = self.at()['type']
        if curr != "EOF":
            if curr != "NEWLINE":
                raise SyntaxError(f'Expected newline or EOF instead of {curr}: {self.at()["value"]}')
            self.next_token()
    def __parse_next(self):
        curr_token = self.at()

        match curr_token['type']:
            case 'IF':
                return self.__parse_if_block()
            case 'FOR':
                return self.__parse_for_block()
            case 'WHILE':
                return self.__parse_while_block()
            case 'FUNCTION':
                return self.__parse_func_block('FUNCTION')
            case 'PROCEDURE':
                return self.__parse_func_block('PROCEDURE')
            case 'NEWLINE':
                self.next_token()
                return -1 # code for: this is nothing
            case _:
                return self.__parse_statement()
    
    def __parse_block(self, block: Block, terminators: tuple[str]):
        while self.at()['type'] not in terminators:
            block.body_append(self.__parse_next())
        
    def __parse_for_block(self) -> ForBlock:
        self.next_token() # discard 'FOR'
        initialiser = self.at()['value']
        initialising_expr = self.__parse_assignment_expression()
        self.expect('TO', 'Expected "to"') # discard 'TO'
        limit = self.__parse_expression()
        for_block = ForBlock(initialiser, limit)
        for_block.initialising_expr = initialising_expr

        if self.at()['type'] == 'STEP':
            self.expect('STEP', 'Expected "step"') # discard 'STEP'
            step = self.__parse_expression()
            for_block.step = step
        self.expect('NEWLINE', 'Expected newline after "for"') # discard 'NEWLINE'
        
        self.__parse_block(for_block, ('NEXT',))
        self.next_token() # discard 'NEXT'
        self.__parse_expression()
        self.new_line_or_eof()
        return for_block
    
    def __parse_while_block(self) -> WhileBlock:
        self.next_token() # discard 'WHILE'
        condition = self.__parse_expression()
        while_block = WhileBlock(condition)
        self.expect('NEWLINE', 'Expected newline after "while"') # discard 'NEWLINE'
        self.__parse_block(while_block, ('ENDWHILE',))
        self.next_token() # discard 'ENDWHILE'
        self.new_line_or_eof()
        return while_block
 
    def __parse_if_block(self):
        if_block = IfBlock()
        while self.at()['type'] != 'ENDIF':
            curr_type = self.at()['type']
            match curr_type: 
                case 'IF':
                    if_block.add_condition(self.__parse_if_statement(('ELSEIF', 'ELSE', 'ENDIF')))
                case 'ELSEIF':
                    if_block.add_condition(self.__parse_if_statement(('ELSEIF', 'ELSE', 'ENDIF')))
                case 'ELSE':
                    if_block.add_condition(self.__parse_else_statement(('ENDIF',)))

                case _:
                    raise SyntaxError('Unable to find terminator of if-statement: missing elseif or endif')
        
        self.next_token() # discard 'ENDIF'
        self.new_line_or_eof()
        
        return if_block
    
    def __parse_func_block(self, functype):
        self.next_token() # discard 'FUNCTION' or 'PROCEDURE'
        name = self.expect('NAME', 'Expected function name')['value']
        self.expect('LPAREN', 'Expected "("') # discard 'LPAREN'
        parameters = self.__parse_parameters()
        print(parameters)
        self.expect('RPAREN', 'Expected ")"') # discard 'RPAREN'
        self.expect('NEWLINE', 'Expected newline after function header') # discard 'NEWLINE'
        func_block = FuncBlock(name=name, parameters = parameters)
        self.__parse_block(func_block, terminators=('END'+functype, 'RETURN'))
        if self.at()['type'] == 'RETURN': # discard "RETURN"
            if functype == "PROCEDURE": # procedure cannot return a value
                raise SyntaxError("Procedure cannot return a value")
            self.next_token()
            return_expr = self.__parse_expression() # parse return expression
            func_block.return_expr = return_expr
            print(self.at())
            if self.at()['type'] == "EOF":
                raise SyntaxError(f'Expected subroutine terminator(end{functype.lower()}), instead unexpected EOF')
            next_token = self.next_token()
        self.expect('END'+functype, 'Expected end'+functype.lower()) # discard 'END'+functype
        self.new_line_or_eof()
            

        return func_block
        

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
        condition = self.__parse_expression()
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

    def __parse_parameters(self) -> list[str]:
        params = []
        while True:
            params.append(self.next_token()['value'])
            if self.at()['type'] == 'RPAREN':
                break
            self.expect('COMMA', 'Expected ","')
            if self.at()['type'] == 'RPAREN':
                break
        
        return params
    def __parse_list_expression(self, terminator: str = 'RPAREN') -> ListExpression:
        elems = []
        while True:
            elems.append(self.__parse_expression())
            if self.at()['type'] == terminator:
                break
            self.expect('COMMA', 'Expected ","')
            if self.at()['type'] == terminator:
                break
        
        list_expr = ListExpression(elements = elems)
        return list_expr

    def __parse_name(self, i_type="VAR"):
        next_level = self.__parse_logical_expression
        tk = self.at()
        match tk['type']:
            case "ARRAY":
                self.next_token() # discard ARRAY
                name = self.expect("NAME", "Expected array name")['value']
                self.expect("LSQBRACE", "Expected '['") # discard LSQBRACE
                index = int(self.expect("NUMBER", "Expected array index")['value'])
                self.expect("RSQBRACE", "Expected ']'") # discard RSQBRACE
                if self.at()['type'] == "ASSIGN":
                    self.expect("ASSIGN", "Expected '='")
                    self.expect("LSQBRACE", "Expected '['") # discard LSQBRACE
                    right = self.__parse_list_expression("RSQBRACE")
                    self.expect("RSQBRACE", "Expected ']'")
                else:
                    right = None
                
                return ArrayAssignmentExpr(left=name, length=index, right=right)

            case _:
                pass
        identifier = tk['value']
        left = identifier
        match self.look_forward()['type']:

            case "ASSIGN":
                self.next_token()
                assign_operator = self.next_token()
                right: Expression = next_level()
                return AssignmentExpr(left=left, right=right, i_type=i_type)
            
            case "LPAREN": # function call
                self.next_token() # discard name
                self.next_token() # discard LPAREN
                args = self.__parse_list_expression(terminator="RPAREN")
                self.next_token() # discard RPAREN
                return FunctionCall(name=left, arguments=args)
            
            case "LSQBRACE": # array access
                self.next_token() # discard NAME
                self.next_token()
                index = next_level()
                self.expect("RSQBRACE", "Expected ']'") # discard RSQBRACE
                curr = self.at()['type']
                assign = False
                right = None
                if curr == "ASSIGN":
                    self.next_token()
                    right = self.__parse_expression()
                    assign = True
                return ArrayIndex(array=left, index=index, right=right, assign=assign)



            case "DOT": # member access
                pass

            case _:
                return next_level()


    def __parse_assignment_expression(self) -> Expression:
        tk: dict = self.at()
        next_level = self.__parse_logical_expression
        match tk['type']:
            case "NAME":
                return self.__parse_name()
            
            case "ARRAY":
                return self.__parse_name()

            case "CONST":
                self.next_token()
                return self.__parse_name(i_type="CONST")
            case "GLOBAL":
                self.next_token()
                return self.__parse_name(i_type="GLOBAL")
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
                if self.at()['type'] == 'LPAREN':
                    self.next_token() # discard LPAREN
                    args = self.__parse_list_expression(terminator="RPAREN")
                    self.next_token() # discard RPAREN
                    return FunctionCall(name=tk['value'], arguments=args)
                    
                identifier = Identifier()
                identifier.symbol = tk['value']

                return identifier

            case 'NUMBER':
                numeric_literal = NumericLiteral()
                numeric_literal.value = int(tk['value'])
                return numeric_literal
            
            case 'OPERATION':
                if tk['value'] == '-':
                    return BinaryExpr(left=NumericLiteral(value=0), operator='-', right=self.__parse_expression())

            case 'STRING':
                string_literal = StringLiteral(value=tk['value'])
                return string_literal

            case 'LPAREN':
                value = self.__parse_expression()
                self.expect('RPAREN', 'Expected ")"')
                return value
            
            case 'LSQBRACE':
                value = self.__parse_list_expression(terminator="RSQBRACE")
                self.expect('RSQBRACE', 'Expected "]"')
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

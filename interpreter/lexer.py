import re as regex


class Lexer:
    def __init__(self, lines: str) -> None:
        self.lines = lines
        self.tokens = []
        self.pos = 0

        self.rules = {
            'IGNORE': r'\s+',
            'NAME': '[a-zA-Z_][a-zA-Z0-9_]*',
            'COMPARE': '==|!=|>|<|>=|<=',
            'COMMENT': r'//',
            'ASSIGN': '=',
            'OPERATION': r'\+|-|\*|\/|\^|MOD|DIV|AND|OR|NOT',
            'NUMBER': r'[+-]?([0-9]*[.])?[0-9]+',
            'STRING': r'\".*?\"|\'.*?\'',
            'LPAREN': r'\(',
            'RPAREN': r'\)',
            'COMMA': r',',
            'LSQBRACE': r'\[',
            'RSQBRACE': r'\]',
            'NEWLINE': r'\\n',
            'DOT': r'\.',
        }

        self.keywords = {
            'const': 'CONST',
            'None': 'NULL',
            'global': 'GLOBAL',
            'array': 'ARRAY',
            'for': 'FOR',
            'to': 'TO',
            'step': 'STEP',
            'next': 'NEXT',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'return': 'RETURN',
            'while': 'WHILE',
            'endwhile': 'ENDWHILE',
            'do': 'DO',
            'until': 'UNTIL',
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'endif': 'ENDIF',
            'elseif': 'ELSEIF',
            'switch': 'SWITCH',
            'case': 'CASE',
            'default': 'DEFAULT',
            'endswitch': 'ENDSWITCH',
            'function': 'FUNCTION',
            'procedure': 'PROCEDURE',
        }

    def run(self) -> None:
        """Run"""
        print('====lexing====')
        print(self.lines)
        while self.pos < len(self.lines):
            self.scan_token()

        self.tokens.append({'type': 'EOF', 'value': '', 'index': self.pos})
        print('====lexed=====')


    def scan_token(self) -> None:
        """Scan token"""
        search_string = self.lines[self.pos:]
        for token_type, value in self.rules.items():
            match = regex.match(value, search_string)
            if match:
                self.pos += match.end()
                match token_type:
                    case 'IGNORE':
                        break
                    case 'NAME':
                        if match.group() in self.keywords:
                            token_type = self.keywords[match.group()]
                    case _:
                        pass
                self.tokens.append({'type': token_type, 'value': match.group(), 'index': self.pos})
                break
        else:
            raise ValueError(f'Invalid token: {search_string[0]}, what are you doing mate')


    def print_tokens(self) -> None:
        """Print tokens"""
        for token in self.tokens:
            print(token)

    def next_token(self):
        """Get next token"""

        return self.tokens.pop(0)


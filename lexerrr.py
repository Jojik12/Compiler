from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):



        self.lexer.add('PRINT', r'print')
        self.lexer.add('FOR', r'for')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('RETURN', r'return')

        self.lexer.add('BREAK', r'break')
        self.lexer.add('TRUE', r'True')
        self.lexer.add('FALSE', r'False')

        self.lexer.add('AND', r'and')
        self.lexer.add('INT', r'int')

        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('LB',r'\{')
        self.lexer.add('RB',r'\}')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('TIMES', r'\*')
        self.lexer.add('EQUALS', r'\=')
        self.lexer.add('LOGIC_EQUAL',r'\==')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('LESS', r'\<')
        self.lexer.add('MORE', r'\>')
        self.lexer.add('CONTINUE', r'continue')
        self.lexer.add('OR', r'or')
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('STRING', r'\".*?\"')
        self.lexer.add('INTEGER', r'\d+')
        self.lexer.add('FLOAT', r'\d+\.\d+')
        self.lexer.add('ID', r'[a-zA-Z_][a-zA-Z0-9_]*')


        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


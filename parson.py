from rply import ParserGenerator
from rply.errors import ParserGeneratorWarning
import warnings
import ast
from ast import *


class Parser():
    def __init__(self, module, builder, printf):
        self.variables = {}
        self.pg = ParserGenerator(

            ['PRINT', 'OPEN_PAREN', 'CLOSE_PAREN', 'STRING','INT',
             'SEMI_COLON', 'PLUS', 'SUB', 'TIMES', 'DIV', 'ID',
             'INTEGER','FLOAT','LESS','MORE','LOGIC_EQUAL','EQUALS','LB','RB','IF','ELSE','WHILE','RETURN'],
            precedence=[("left", ["PLUS", "SUB"]), ("right", ["TIMES", "DIV"])]

        )
        self.module = module
        self.builder = builder
        self.printf = printf
        self.idfstr = 0



    def parse(self):
        @self.pg.production('program : body')
        def program_expression(p):
            print("1====", p[0], "====")
            return p[0]

        @self.pg.production('body : stmts')
        def block(p):
            return p[0]

        @self.pg.production('stmts : stmts stmt')
        def stmts_b(p):
            if p[1] is None:
                return p[0]
            else:
                return p[0] + [p[1]]

        @self.pg.production('stmts : stmt')
        def stmts_stmt(p):
            if p[0] is None:
                return []
            else:
                return [p[0]]

        @self.pg.production('stmt : stmt_print SEMI_COLON')
        @self.pg.production('stmt : stmt_equal SEMI_COLON')
        @self.pg.production('stmt : stmt_if SEMI_COLON')
        @self.pg.production('stmt : stmt_while SEMI_COLON')
        @self.pg.production('stmt : stmt_return SEMI_COLON')
        @self.pg.production('stmt : stmt_pere_assign SEMI_COLON')
        def stmt(p):
            return p[0]

        @self.pg.production('stmt_if : IF OPEN_PAREN expression CLOSE_PAREN LB stmts RB')
        def ifs(p):
            return IfStatement(self.builder, self.module, p[2], p[5], [])

        @self.pg.production('stmt_while : WHILE OPEN_PAREN expression CLOSE_PAREN LB stmts RB')
        def whiles(p):
            return WhileStatement(self.builder, self.module, p[2], p[5])


        @self.pg.production('stmt_print : PRINT OPEN_PAREN expression CLOSE_PAREN')
        def prints(p):
            print("++++3", p)
            self.idfstr += 1
            return Print(self.builder, self.module, self.printf, p[2],self.idfstr)

        @self.pg.production('stmt_equal : INT ID EQUALS expression')
        @self.pg.production('stmt_equal : FLOAT ID EQUALS expression')
        def equals(p):
            print("++++6",p)
            print("++++6.1",type(p[2]))

           # if isinstance(p[2],ast.Integer):
            return Equal(self.builder,self.module,p[1].value,p[3].value)
            #else:
              #  return Equal(self.builder,self.module,p[1].value,p[2])

        @self.pg.production('stmt_return : RETURN expression')
        def ruturn_func(p):
            return ReturnStatement(self.builder, p[1])

        @self.pg.production('stmt_pere_assign : ID EQUALS expression')
        def pere_assign(p):

            if isinstance(p[2], ast.Integer):
                return PereASSIGN(self.builder, self.module, p[0].value, p[2].value)
            else:
                return PereASSIGN(self.builder, self.module, p[0].value, p[2])

        @self.pg.production('expression : expression PLUS expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression TIMES expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression LESS expression')
        @self.pg.production('expression : expression MORE expression')
        @self.pg.production('expression : expression LOGIC_EQUAL expression')
        def expression(p):
            left = p[0]
            right = p[2]
            operator = p[1]
            if operator.gettokentype() == 'TIMES':
                return Times(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'DIV':
                return Div(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'PLUS':
                return Plus(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'SUB':
                return Sub(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LESS':
                return Less(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'MORE':
                return More(self.builder, self.module, left, right)
            elif operator.gettokentype() == 'LOGIC_EQUAL':
                return LogicEqual(self.builder, self.module, left, right)

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def paren_exp(p):
            return p[1]

        @self.pg.production('expression : FLOAT OPEN_PAREN ID CLOSE_PAREN')
        @self.pg.production('expression : INT OPEN_PAREN ID CLOSE_PAREN')
        def typecast(p):
            return Typecast(self.builder, self.module, p[0].value, p[2].value)




        @self.pg.production('expression : INTEGER')
        def integer(p):
            print("++++5 ", p)
            return Integer(self.builder, self.module, p[0].value)

        @self.pg.production('expression : ID')
        def id(p):
            print("++++7 ", p)
            return Id(self.builder, self.module, p[0].value)

        @self.pg.error
        def error_handle(token):
            warnings.filterwarnings("ignore", category=ParserGeneratorWarning)
            raise ValueError(
                "Syntax error at token {0} at line {1}".format(token.gettokentype(), token.source_pos.lineno - 1))

    def get_parser(self):
        warnings.filterwarnings('ignore')

        return self.pg.build()

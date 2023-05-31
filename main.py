from codegen import CodeGen
from lexerrr import Lexer
from parson import Parser

def get_last_element(lst):
    if isinstance(lst, list):
        return get_last_element(lst[-1])
    else:
        return lst

fname = "input.pyf"
with open(fname) as f:
    text_input = f.read()

lexer = Lexer().get_lexer()
try:
    tokens = lexer.lex(text_input)

    # for token in tokens:
    #     print(token)

    codegen = CodeGen()

    module = codegen.module
    builder = codegen.builder
    printf = codegen.printf

    pg = Parser(module, builder, printf)
    pg.parse()
    parser = pg.get_parser()

    # parser.parse(tokens).eval()

    nodes = parser.parse(tokens)
    for node in nodes:
        if type(node) == type(list()):
            item = get_last_element(node)
            item.eval()
        else:
            node.eval()

    codegen.create_ir()
    codegen.save_ir("output.ll")
except Exception as e:
    if hasattr(e, "source_pos"):
        line = e.source_pos.lineno
        print("Parsing Error at line", line)
    else:

        print("Parsing Error:", e)

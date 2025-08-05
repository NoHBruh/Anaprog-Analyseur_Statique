import lexer
from grammar_parser import get_parser
from ast_Visitor import AstVisitor
from symbol_table import *
import pprint
def main():
    with open("program.txt", 'r') as program_file:
        code = program_file.read()

    _lexer = lexer.get_lexer()
    lexer.tokenize(_lexer, code)
    print("-------------------------------------------------------------------------------")
    parser = get_parser()
    ast = parser.parse(code, debug=False)
    pprint.pprint(ast)
    print("-------------------------------------------------------------------------------")
    semantic_analyzer = AstVisitor(sym_table=SymbolTable())
    semantic_analyzer.visit(ast)
    
if __name__ == '__main__':
    main()
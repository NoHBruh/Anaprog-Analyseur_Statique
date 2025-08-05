from worklist import Worklist
from lexer import get_lexer, tokenize
from grammar_parser import get_parser


def main():
    with open("program.txt", 'r') as program_file :
            code = program_file.read()

    _lexer = get_lexer()
    tokenize(_lexer, code)
    print("-------------------------------------------------------------------------------")
    parser = get_parser()
    ast = parser.parse(code, debug=False)
    import pprint
    pprint.pprint(ast)
    
    
    wl = Worklist()
    wl.visit(ast)
    print("-----------------")
    print(" ↓↓↓ ERRORS/WARNINGS BELOW ↓↓↓ ")
    print("\n")
    
    
    wl.warnings.print_warnings()
    
    
if __name__ == '__main__':
    main()


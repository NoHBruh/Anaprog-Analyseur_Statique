import lexer
from grammar_parser import get_parser


def main():
    with open("program.txt", 'r') as program_file:
        code = program_file.read()

    _lexer = lexer.get_lexer()
    lexer.tokenize(_lexer, code)
    print("-------------------------------------------------------------------------------")
    parser = get_parser()
    ast = parser.parse(code, debug=False)
    import pprint
    pprint.pprint(ast)
    
if __name__ == '__main__':
    main()
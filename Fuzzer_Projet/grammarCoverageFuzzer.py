ss_directory = directory = './SyntaxAndSemantics'
from fuzzingbook.GrammarCoverageFuzzer import TrackingGrammarCoverageFuzzer, SimpleGrammarCoverageFuzzer, GrammarCoverageFuzzer, is_valid_grammar
from fuzzerGrammars import SMALL_GRAMMAR, ebnf_small_grammar
import matplotlib.pyplot as plt
import  lexer
from grammar_parser import get_parser
from ast_Visitor import AstVisitor
from  symbol_table import *
import pprint
except_dict = {}
_lexer = lexer.get_lexer()

assert(is_valid_grammar(ebnf_small_grammar))
gcf = TrackingGrammarCoverageFuzzer(ebnf_small_grammar, start_symbol ="<start>", max_nonterminals = 15, log = True)
for i in range(500):
    fuzz = gcf.fuzz()
    lexer.tokenize(_lexer, fuzz)
    print("-------------------------------------------------------------------------------")
    parser = get_parser()
    ast = parser.parse(fuzz, debug=False)
    pprint.pprint(ast)
    print("-------------------------------------------------------------------------")
    semantic_analyzer = AstVisitor(sym_table=SymbolTable())
    try :
        semantic_analyzer.visit(ast)
    except(Exception) as e :
        
        if e not in except_dict.values():
            except_dict[fuzz] = e
        continue
    
print('Here are all the errors/Exceptions encountered :\n')
for _fuzz in except_dict.keys() :
    print(f'Exception/Error : {except_dict[_fuzz]} in program -> {_fuzz}\n')

    
    
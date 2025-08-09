ss_directory = directory = './SyntaxAndSemantics'
from fuzzingbook.GrammarCoverageFuzzer import TrackingGrammarCoverageFuzzer, SimpleGrammarCoverageFuzzer, GrammarCoverageFuzzer, is_valid_grammar, average_length_until_full_coverage
from fuzzerGrammars import SMALL_GRAMMAR, ebnf_small_grammar
import matplotlib.pyplot as plt
import  lexer
from grammar_parser import get_parser
from ast_Visitor import AstVisitor
from  symbol_table import *
from fuzzingbook.Coverage import Coverage
import pprint
from fuzzingbook.WhenToStopFuzzing import population_trace_coverage


except_dict = {}
_lexer = lexer.get_lexer()
lines_covered = {}

def get_lines(cov) :
    lines_covered[i] = cov.coverage()

assert(is_valid_grammar(ebnf_small_grammar))
gcf = TrackingGrammarCoverageFuzzer(ebnf_small_grammar, start_symbol ="<start>", log = False)

for i in range(50) : #len(gcf.max_expansion_coverage() - gcf.expansion_coverage()) > 0
    fuzz = gcf.fuzz()
    lexer.tokenize(_lexer, fuzz)
    print("-------------------------------------------------------------------------------")
    parser = get_parser()
    ast = parser.parse(fuzz, debug=False)
    pprint.pprint(ast)
    semantic_analyzer = AstVisitor(sym_table=SymbolTable())
    try :
        with Coverage() as cov :
            semantic_analyzer.visit(ast)
            get_lines(cov)
    except(Exception) as e :
        if e not in except_dict.values():
            except_dict[fuzz] = e
            get_lines(cov)
        continue
    
print('Here are all the errors/Exceptions encountered :\n')
for _fuzz in except_dict.keys() :
    print(f'Exception/Error : {except_dict[_fuzz]} in program -> {_fuzz}\n')

print(f'Coverage : {lines_covered}')

 # Avrg length : 7026.72  
#print(f'Average length until full coverage : {average_length_until_full_coverage(gcf)}') 
    

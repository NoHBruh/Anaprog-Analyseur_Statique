from fuzzingbook.MutationFuzzer import MutationCoverageFuzzer, FunctionCoverageRunner, population_coverage
import os
import lexer
from grammar_parser import get_parser

directory = './Fuzzer/seed_programs'
seeds = []

def ast_program(program) -> bool :
    _lexer = lexer.get_lexer()
    lexer.tokenize(_lexer, code)
    parser = get_parser()
    result = parser.parse(code, debug=False) 
    if ("function main()") not in program :
        raise ValueError("invalid program")

    return True
ast_runner = FunctionCoverageRunner(ast_program)

for program in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, program)) :
        if program == "program1.txt" :
            with open(os.path.join(directory, program), 'r') as p :
                code = p.read()
                seeds.append(code)
                
_lexer = lexer.get_lexer()
lexer.tokenize(_lexer, code)
parser = get_parser()
ast = parser.parse(code, debug=False)
import pprint
pprint.pprint(ast) 

           

mutation_fuzzer = MutationCoverageFuzzer(seed = [seeds])
mutation_fuzzer.runs(ast_runner, trials = 10000)
all_coverage, cumulative_coverage = population_coverage(mutation_fuzzer.population, ast_program)

print(cumulative_coverage)
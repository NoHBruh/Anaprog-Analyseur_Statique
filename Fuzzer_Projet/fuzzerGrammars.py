from fuzzingbook.Grammars import is_valid_grammar, opts, extend_grammar, Grammar, convert_ebnf_grammar, srange
import pprint
import string
# Small Grammar with array extension, written in a way so that fuzzingbook classes can make use of it 
SMALL_GRAMMAR = {
    '<start>':
        ['<program>'],
    '<program>' : ['<main>'],
    '<main>' : ['function main() {<stmtlist>} <functionlist>'],
    '<functionlist>' : ['<function>*'],
    '<function>' : ['function <identifier> (<paramlist>) {<stmtlist>}'],
    '<paramlist>' : ['<param>', '<param>, <paramlist>'],
    '<param>' : ['<identifier>', '<num>'],
    
    '<stmtlist>' : ['<stmt>*'],
    '<stmt>' : ['<assign_val>', '<assign_func_call>', '<if>', '<while>', '<sequence>', '<returnStmt>', '<array_create>', '<array_assign>'],
    
    '<assign_val>' : ['<identifier> = <expr>;'],
    '<assign_func_call>' : ['<identifier> = call <identifier>(<paramlist>);'],
    '<array_create>' : ['<identifier> = new array(<arithExpr>);'],
    '<array_assign>' : ['<identifier>[<arithExpr>] = <expr>;'],
    
    '<if>' : ['if(<expr>) <stmt> else <stmt>'],
    '<while>' : ['while(<boolExpr>) <sequence>'],
    '<sequence>' : ['{<stmtlist>}'],
    '<returnStmt>' : ['return <expr>;'],
    
    '<expr>' : ['<arithExpr>', '<boolExpr>', '<identifier>[<arithExpr>]'],
    '<arithExpr>' : ['<arithExpr> <op> <arithExpr>', '<noprnd>'],
    '<boolExpr>' : ['<boolExpr> <rop> <boolExpr>', '<boprnd>'],
    '<noprnd>' : ['<var>', '<num>', '<negnum>'],
    '<boprnd>' : ['<var>', 'True', 'False'],
    '<op>' : ['+', '-', '*', '/'],
    '<rop>' : ['<', '>', '==', '!=', '>=', '<=', 'and', 'or'],
    
    '<var>' : ['<identifier>'],
    '<num>' : ['<digit>+'],
    '<negnum>' : ['-<digit>+'],
    
    '<identifier>' : ['<letter><char>*'],
    '<char>' : ['<letter>', '<digit>'],
    '<letter>' : srange(string.ascii_letters),
    '<digit>' : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
}

is_valid_grammar(SMALL_GRAMMAR)

#conversion for (non)optionnal non-terminals (+ / * / ?)
ebnf_small_grammar = convert_ebnf_grammar(SMALL_GRAMMAR)
pprint.pprint(ebnf_small_grammar)
is_valid_grammar(ebnf_small_grammar)
import re # used for RegEx rules declaration using 't_' prefix
from ply import lex

#-----Tokens-----

reserved_words = {
    'if' : 'IF',
    'else' :'ELSE',
    'while' :'WHILE',
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'main' : 'MAIN',
    
    'True' : 'TRUE',
    'False' : 'FALSE',
    
    'new' : 'NEW',
    'array' : 'ARRAY',
    'call' : 'CALL'
}

tokens = [
    'NUMBER',
    'IDENTIFIER',
    'LETTER',
    'DIGIT',
    
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    
    'LT', # <
    'GT', # >
    'LTE', # <=
    'GTE', # >=
    
    'EQUAL', # =
    'NEQUAL', # !=
    'DEQUAL', # ==
    'AND',
    'OR',
    
    'LPAR', # (
    'RPAR', # )
    'LBRACE', # {
    'RBRACE', # }
    'LBRACKET', # [
    'RBRACKET', # ]
    
    'SEMICOLON', # ;
    'COMMA' # ,
] + list(reserved_words.values())

#-----LexerRules-----

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_LETTER  = r'([_A-Za-z])'
t_DIGIT = r'([0-9])'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'  
    t.type = reserved_words.get(t.value, 'IDENTIFIER')  # Checks for reserved words
    return t

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_EQUAL = r'='
t_NEQUAL = r'!='
t_DEQUAL = r'=='
t_AND = r'and'
t_OR = r'or'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','

t_ignore = ' \t'

# Rule for tracking line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    

def get_lexer():
    return lex.lex()

# LEXER output
def tokenize(lexer,data) :
    lexer.input(data)
    
    output = []
    
    while True :
        tok = lexer.token()
        if not tok: 
            break      # No more input
        output.append(tok)
        print(tok)

    return output 
    


    


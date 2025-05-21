import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

DEBUG = True

# -----GrammarRules-----

def p_program(p) :
    '''program : main'''
    p[0] = ('program', p[1])
    
def p_main(p) :
    '''main : FUNCTION MAIN LPAR RPAR LBRACE stmtlist RBRACE functionlist'''
    p[0] = ('main', p[6], p[8])
    
def p_functionlist(p) :
    '''functionlist : function
                    | function functionlist
                    | empty'''
    if len(p) == 2 :
        p[0] = p[1]
    
    else :
        p[0] = [p[1]] + [p[2]]
        

def p_function(p) :
    '''function : FUNCTION IDENTIFIER LPAR  paramlist RPAR LBRACE stmtlist RBRACE'''
    p[0] = ('function', p[2],p[4], p[7])
    
def p_paramlist(p) :
    '''paramlist : param
                 | param COMMA paramlist
                 | empty'''
    if len(p) == 2 and p[1] is not None : #Single parameter paramlist
        p[0] = [p[1]]
        
    if len(p) > 2 : #multiple parameter paramlist
        p[0] = [p[1]] + [p[3]]
        
    else : # empty paramlist
        p[0] = []
    
def p_param(p):
    '''param : IDENTIFIER
             | NUMBER'''
    p[0] = ('var', p[1])
    
def p_stmtlist(p):
    '''stmtlist : stmt
                | stmt stmtlist'''
    if len(p) == 2 :
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + [p[2]]
        
def p_stmt(p):
    '''stmt : assign_val
            | assign_func_call
            | array_create
            | array_assign'''
    p[0] = p[1]

def p_assign_val(p) :
    '''assign_val : IDENTIFIER EQUAL expr SEMICOLON'''
    p[0] = ('assign',p[1], p[3]) 
                #var_name  #var_value

def p_assign_func_call(p):
    '''assign_func_call : IDENTIFIER EQUAL CALL funcCall LPAR paramlist RPAR SEMICOLON'''
    
    var_name = p[1]
    func_name = p[4]
    params = p[6]
    
    p[0] = ('assign_func_call', var_name, func_name, params)
    
    
def p_array_create(p) :
    '''array_create : IDENTIFIER EQUAL NEW ARRAY LPAR arithExpr RPAR SEMICOLON'''
    p[0] = ('array_create', p[1], p[6]) 
    

def p_array_assign(p):   
    '''array_assign : IDENTIFIER LBRACKET arithExpr RBRACKET EQUAL expr SEMICOLON'''
    array_name = p[1]
    index = p[3]
    
    p[0] = ('array_assign', array_name, index, p[6])
    
def p_if(p):
    '''stmt : IF LPAR expr RPAR stmt ELSE stmt'''
    p[0] = ('if', p[3], p[5], p[7])
    
    
def p_while(p) :
    '''stmt : WHILE LPAR expr RPAR stmt'''
    p[0] = ('while', p[3], p[5])

def p_sequence(p):
    '''stmt : LBRACE stmtlist RBRACE'''
    p[0] = ('sequence', p[2])
    
def p_returnStmt(p):
    '''stmt : RETURN expr SEMICOLON'''
    
    p[0] = ('return', p[2])
    
    
# -----ExpressionRules-----
  
def p_expr_func_call(p):
    '''funcCall : IDENTIFIER'''
    p[0] = ('func_call', p[1])    
        
        
def p_arith_expr(p) :
    '''expr : arithExpr'''
    p[0] = p[1]


def p_bool_expr(p) :
    '''expr : boolExpr'''
    p[0] = p[1]
    
    
def p_array_expr(p):
    '''expr : IDENTIFIER LBRACKET arithExpr RBRACKET
            | IDENTIFIER LBRACE RBRACE'''
    if len(p) == 4 :
        p[0] = ('array_expr', p[1], None) #no index
        
    else:
        p[0] = ('array_expr', p[1], p[3]) #with index
    
        
def p_noprnd_var(p) :
    '''noprnd : var'''
    p[0] = p[1]


def p_noprnd_num(p) :
    '''noprnd : NUMBER'''
    p[0] = p[1]
    
    
def p_boprnd_true(p) :
    '''boprnd : TRUE'''
    p[0] = True
   
    
def p_boprnd_false(p) :   
     '''boprnd : FALSE'''
     p[0] = False
     
     
def p_var(p) :
    '''var : IDENTIFIER'''
    p[0] = ('var_name', p[1])
    
    
def p_arithExpr_binOp(p):
    '''arithExpr : arithExpr PLUS arithExpr
                 | arithExpr MINUS arithExpr
                 | arithExpr MULTIPLY arithExpr
                 | arithExpr DIVIDE arithExpr
                 | noprnd'''
    
    if len(p) == 2 :
        p[0] = p[1]
        
    else :
        p[0] = ('arithExpr_binOp', p[1], p[2], p[3])
     
        
def p_boolExpr_binOp(p):
    '''boolExpr : arithExpr LT arithExpr
                | arithExpr GT arithExpr
                | arithExpr LTE arithExpr
                | arithExpr GTE arithExpr
                | arithExpr DEQUAL arithExpr
                | arithExpr NEQUAL arithExpr
                | arithExpr AND arithExpr
                | arithExpr OR arithExpr
                | boprnd'''
    if len(p) == 2:
        p[0] = p[1]
    else :
        p[0] = (p[1], p[2], p[3])   
    
        
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")


def p_empty(p):
    'empty :'
    pass


#-----BuildTheParser-----
def get_parser():
    return yacc.yacc() 

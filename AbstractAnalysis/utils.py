from abstractDomain import AbstractDomain
import operator
ops = { "+": operator.add, "-": operator.sub, '*' : operator.mul, '/' : operator.truediv }
num_to_string = { '+': "sum", '-': 'sub', '*' : 'mult' , '/' : 'div'}
bool_ops_reverse = {'==' : "!=",
                    '!=' : '==',
                    '<' : '>', 
                    '>' : '<', 
                    '>=' : '<=',
                    '<=' : '>='}

abs_integers = {AbstractDomain.POSITIVE, AbstractDomain.NEGATIVE, AbstractDomain.ZERO}

def handle_arithmetic_variables(var1, op, var2) :
    match op:
        case '+' :
            return get_abstract_val_addition(var1, var2)
            
        case '-' :
            return get_abstract_val_substraction(var1, var2)
            
        case '*' :
            return get_abstract_val_multiplication(var1, var2)
            
        case '/' :
            return get_abstract_val_division(var1, var2)
            
def get_abstract_val_addition(var1, var2):
    if var1 not in AbstractDomain and var2 not in AbstractDomain :
        return var1 + var2
    
    elif (var1 == var2 == AbstractDomain.POSITIVE):
        return AbstractDomain.POSITIVE
            
    elif (var1 == var2 == AbstractDomain.ZERO):
        return AbstractDomain.ZERO
            
    elif (var1 == var2 == AbstractDomain.NEGATIVE):
        return AbstractDomain.NEGATIVE
            
    else :
        return AbstractDomain.UNSURE
 
def get_abstract_val_substraction(var1, var2): 
    if var1 not in AbstractDomain and var2 not in AbstractDomain :
        return var1 - var2
    
    elif (var1 == AbstractDomain.POSITIVE and var2 == AbstractDomain.NEGATIVE):
        return AbstractDomain.POSITIVE
            
    elif (var1 == AbstractDomain.NEGATIVE and var2 == AbstractDomain.POSITIVE or var1 == AbstractDomain.NEGATIVE and var2 == AbstractDomain.ZERO):
        return AbstractDomain.NEGATIVE
            
    elif (var1 == AbstractDomain.ZERO == var2 == AbstractDomain.ZERO):
        return AbstractDomain.ZERO
            
    else :
        return AbstractDomain.UNSURE 
    
def get_abstract_val_multiplication(var1, var2):
    if var1 not in AbstractDomain and var2 not in AbstractDomain :
        return var1 * var2
    
    elif (var1  == var2 == AbstractDomain.POSITIVE or var1 == var2 == AbstractDomain.NEGATIVE):
        return AbstractDomain.POSITIVE
    
    elif ((var1 == AbstractDomain.NEGATIVE) != (var2 == AbstractDomain.NEGATIVE)) :
        return AbstractDomain.NEGATIVE
    
    elif (var1 == var2 == AbstractDomain.ZERO):
        return AbstractDomain.ZERO
    
    else :
        return AbstractDomain.UNSURE  
    
def get_abstract_val_division(var1, var2):
    if var1 not in AbstractDomain and var2 not in AbstractDomain :
        return var1 // var2
    
    elif (var1 == var2 == AbstractDomain.POSITIVE or var1 == var2 == AbstractDomain.NEGATIVE) :
        return AbstractDomain.POSITIVE
    
    elif (var1 == AbstractDomain.NEGATIVE != var2 == AbstractDomain.NEGATIVE) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE
         
#//-------------------------\\ 
            
def handle_arithmetic_with_constant_right(var, op, const):
    
    match op :
        case '+' :
            return get_abstract_val_add_const_right(var, const)
            
        case '-' :
            return get_abstract_val_sub_const_right(var, const)
        
        case '*' :
            return get_abstract_val_mult_const_right(var, const)
            
        case '/' :
            return get_abstract_val_div_const_right(var, const)
            
def get_abstract_val_add_const_right(var, const) :
    if var not in AbstractDomain :
        return var + const
    
    if (var == AbstractDomain.POSITIVE and const >= 0) :
        return AbstractDomain.POSITIVE
    
    elif (var == const == AbstractDomain.ZERO) :
        return AbstractDomain.ZERO    
    
    elif(var == AbstractDomain.NEGATIVE and const <= 0):
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE
    
def get_abstract_val_sub_const_right(var, const):
    if var not in AbstractDomain :
        return var - const
    
    if (var == AbstractDomain.POSITIVE and const <= 0) :
        return AbstractDomain.POSITIVE
    
    elif (var == const == AbstractDomain.ZERO) :
        return AbstractDomain.ZERO
    
    elif (var == AbstractDomain.NEGATIVE and const >= 0) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE 
    
def get_abstract_val_mult_const_right(var, const) :
    if var not in AbstractDomain :
        return var * const
    
    if (var == AbstractDomain.POSITIVE and const > 0 or var == AbstractDomain.NEGATIVE and const < 0) :
           return AbstractDomain.POSITIVE
       
    elif (var == AbstractDomain.ZERO or const == 0) :
        return AbstractDomain.ZERO
    
    elif (var == AbstractDomain.POSITIVE and const < 0 or var == AbstractDomain.NEGATIVE and const > 0) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE
    
def get_abstract_val_div_const_right(var, const) :
    if var not in AbstractDomain :
        return var // const
    
    if (var == AbstractDomain.POSITIVE and const > 0 or var == AbstractDomain.NEGATIVE and const < 0) :
        return AbstractDomain.POSITIVE
    
    elif (var == AbstractDomain.ZERO and const != 0) :
        return AbstractDomain.ZERO
    
    elif (var == AbstractDomain.NEGATIVE != (const < 0 and const != 0)) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE
           
#//--------------------------\\ 
           
def handle_arithmetic_with_constant_left(const, op, var) :
    match op :
        case '+' :
            return get_abstract_val_add_const_left(var, const)    
        
        case '-' :
            return get_abstract_val_sub_const_left(var, const)
        
        case '*' :
            return get_abstract_val_mult_const_left(var, const)
        
        case '/' :
            return get_abstract_val_div_const_left(var, const)    
        
def get_abstract_val_add_const_left(var, const):
    return get_abstract_val_add_const_right(var, const)    

def get_abstract_val_sub_const_left(var, const) :
    if var not in AbstractDomain :
        return const - var
    
    if (const > 0 and var == AbstractDomain.NEGATIVE):
        return AbstractDomain.POSITIVE
    
    elif (const == var == AbstractDomain.ZERO) :
        return AbstractDomain.ZERO
    
    elif (const < 0 and var == AbstractDomain.POSITIVE) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE

def get_abstract_val_mult_const_left(var, const) :
    return get_abstract_val_mult_const_right(var, const)

def get_abstract_val_div_const_left(var, const) :
    if var not in AbstractDomain :
        return const // var
    
    if (const > 0 and var == AbstractDomain.POSITIVE or const < 0 and var == AbstractDomain.NEGATIVE) :
        return AbstractDomain.POSITIVE

    elif (const == 0 and var != AbstractDomain.ZERO) :
        return AbstractDomain.ZERO
    
    elif (const < 0 != var == AbstractDomain.NEGATIVE) :
        return AbstractDomain.NEGATIVE
    
    else :
        return AbstractDomain.UNSURE
    
#//--------------------------\\
    
def handle_concrete_val_least_upper_bound(var1, var2):
    if var1 > 0 and var2 > 0 :
        return AbstractDomain.POSITIVE
    
    elif var1 < 0 and var2 < 0 :
        return AbstractDomain.NEGATIVE
    
    elif var1 == var2 == 0  or var1 == -var2:
        return AbstractDomain.ZERO
    
    elif var1 > 0 != var2 > 0 :
        return AbstractDomain.UNSURE
    
def handle_abstract_val_least_upper_bound(var1, var2):
    
    if var1 == AbstractDomain.BOTTOM or var2 == AbstractDomain.BOTTOM :
        return var1 if var1 != AbstractDomain.BOTTOM else var2
    
    elif var1 in abs_integers and var2 in abs_integers  :
        return AbstractDomain.UNSURE if var1 != var2 else var1
    
    elif var1 == AbstractDomain.NOTNUMERIC or var2 == AbstractDomain.NOTNUMERIC :
        return AbstractDomain.TOP
    
    elif var1 == AbstractDomain.UNSURE and var2 in abs_integers or var1 in abs_integers and var2 == AbstractDomain.UNSURE :
        return AbstractDomain.UNSURE
    
    elif var1 == var2 :
        return var1
    
    return AbstractDomain.TOP
        
        
        
        
def handle_var_const_least_upper_bound(var1, var2) :  
    if var1 == AbstractDomain.BOTTOM or var2 == AbstractDomain.BOTTOM: 
        return var1 if var1 != AbstractDomain.BOTTOM else var2 
    
    elif ( var1 in abs_integers and var2 == int(var2) ) or ( var1 == int(var1) and var2 in abs_integers ) :
        return var1 if var1 in abs_integers else var2
    
    elif var1 == AbstractDomain.NOTNUMERIC or var2 == AbstractDomain.NOTNUMERIC :
        return AbstractDomain.TOP
    
    if var1 == AbstractDomain.UNSURE or var2 == AbstractDomain.UNSURE :
        return AbstractDomain.UNSURE
    
    return AbstractDomain.TOP 
    
    
   
    
    
    
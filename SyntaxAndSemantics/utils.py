import operator

bops = {'==' : operator.eq, '!=' : operator.ne, '>=' : operator.ge, '<=' : operator.le, '>' : operator.gt, '<' : operator.lt,
       '&' : operator.and_, '|' : operator.or_}

arith_ops = {"+": operator.add, "-": operator.sub, '*' : operator.mul, '/' : operator.truediv }

def process_arith_binOp(left, operator, right):
    if isinstance(left, tuple) :
       left = left[1]
       
    if isinstance(right, tuple):
        right = right[1]
    try:
        return arith_ops[operator](left, right)
    except (ValueError, ZeroDivisionError) as e:
        print(e)
        return


def process_bool_binOp(left, operator, right) :
    if isinstance(left, tuple) :
         
        left = left[1]
            
    if isinstance(right, tuple):
        
        right = right[1]
    

    
    if (isinstance(left, bool) or isinstance(right, bool)) and operator in {"<", ">", ">=", "<="} :
        return False 
        
    try:
        result = bops[operator](int(left), int(right))
        print(f'Bool operation {operator} between {left} and {right} processed : {result}')
        return bool(result)
    except ValueError:
        print(f'{operator} : unsupported boolean operator')
        return
    
def is_negnumber(node) :
    return node[0] == 'negnumber'
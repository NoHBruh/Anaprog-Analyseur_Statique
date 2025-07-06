import operator

bops = {'==' : operator.eq, '!=' : operator.ne, '>=' : operator.ge, '<=' : operator.le, '>' : operator.gt, '<' : operator.lt,
       'and' : operator.and_, 'or' : operator.or_}

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
        
    try:
        return bops[operator](left, right)
    except ValueError:
        print(f'{operator} unsupported boolean operator')
        return
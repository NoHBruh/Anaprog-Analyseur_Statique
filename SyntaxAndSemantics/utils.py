def process_arith_binOp(left, operator, right):
    if isinstance(left, tuple) :
       left = left[1]
       
    if isinstance(right, tuple):
        right = right[1]
    
    match operator :
        
        case "+" :
            return left + right
        
        case "-" :
            return left - right
        
        case "*" :
            return left * right
                   
        case "/" :
            if right == 0 :
                raise Exception("Dividing by zero is unallowed")    
            return left // right
        
    raise Exception(f'{operator} unsupported arithmetic operator')

def process_bool_binOp(left, operator, right) :
    if isinstance(left, tuple) :
       left = left[1]
       
    if isinstance(right, tuple):
        right = right[1]
        
    match operator :
        
        case "==" :
         return left == right
        
        case "!=" :
         return left != right 
        
        case ">" :
            return left > right
              
        case "<" :
            return left < right 
        
        case ">=" :
            return left >= right
        
        case "<=" :
            return right <= right
        
        case "and" :
            return left and right
            
        case "or" :
            return left or right
    
    raise Exception(f'{operator} unsupported boolean operator')
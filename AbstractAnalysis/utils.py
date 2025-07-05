from abstractDomain import AbstractDomain
def handle_arithmetic_abstract_value(var1, op, var2) :
    match op:
        case '+' :
            if (var1 == AbstractDomain.POSITIVE == var2 == AbstractDomain.POSITIVE):
                return AbstractDomain.POSITIVE
            
            elif (var1 == AbstractDomain.ZERO == var2 == AbstractDomain.ZERO):
                return AbstractDomain.ZERO
            
            elif (var1 == AbstractDomain.NEGATIVE == var2 == AbstractDomain.NEGATIVE):
                return AbstractDomain.NEGATIVE
            
            else :
                return AbstractDomain.UNSURE
            
        case '-' :
            if (var1 == AbstractDomain.POSITIVE and var2 == AbstractDomain.NEGATIVE):
                return AbstractDomain.POSITIVE
            
            elif (var1 == AbstractDomain.NEGATIVE and var2 == AbstractDomain.POSITIVE or var1 == AbstractDomain.NEGATIVE and var2 == AbstractDomain.ZERO):
                return AbstractDomain.NEGATIVE
            
            elif (var1 == AbstractDomain.ZERO == var2 == AbstractDomain.ZERO):
                return AbstractDomain.ZERO
            
            else :
                return AbstractDomain.UNSURE
            
        case '*' :
            if (var1 == AbstractDomain.POSITIVE == var2 == AbstractDomain.POSITIVE or var1 == var2 == AbstractDomain.NEGATIVE):
                return AbstractDomain.POSITIVE
            
            elif (var1 == AbstractDomain.NEGATIVE or var2 == AbstractDomain.NEGATIVE) :
                return AbstractDomain.NEGATIVE
            
            elif (var1 == var2 == AbstractDomain.ZERO):
                return AbstractDomain.ZERO
            
            else :
                return AbstractDomain.UNSURE
            
        case '/' :
            if (var1 == var2 == AbstractDomain.POSITIVE or var1 == var2 == AbstractDomain.NEGATIVE) :
                return AbstractDomain.POSITIVE
            
            elif (var1 == AbstractDomain.NEGATIVE or var2 == AbstractDomain.NEGATIVE) :
                return AbstractDomain.NEGATIVE
            
            else :
                return AbstractDomain.UNSURE
            
            
            
                
                
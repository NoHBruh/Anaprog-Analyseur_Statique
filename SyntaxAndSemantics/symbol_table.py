class SymbolTable :
    def __init__(self): #equivalent of allocate function
        self.scopes = [{}] #list of dictionnaries
        
    def insert(self, symbol, token_type,token_value, **kwargs) : #additional kwargs for array size
        if symbol in self.scopes[-1] : # always checking the inner scope
            raise Exception (f"{symbol} already in scope")
        
        sym = {"Type" :token_type,  "Value" : token_value}
        sym.update(kwargs) #adding extra data when necessary, like tha array size
        self.scopes[-1][symbol] = sym
        
        print(f"Added symbol: {symbol} -> {self.scopes[-1][symbol]}")
     
    def remove(self, symbol):
        current = self.scopes[-1]
        if symbol in current :
            del current[symbol]
        else:
            raise Exception(f"{symbol} has not been declared")
               
        
    def update(self, symbol, value = None, **kwargs) :
        for scope in reversed(self.scopes) :
            if symbol in scope :
                scope[symbol].update({"Value" : value})
                print(f"symbol updated : {symbol} -> {scope[symbol]}")
                return
        raise Exception(f"{symbol} has not been declared")
    
    
    def exist(self, symbol) :
        return any(symbol in scope for scope in reversed(self.scopes))
    
    
    def lookup(self, symbol) :
        for scope in reversed(self.scopes) :
            if symbol in scope :
                return scope[symbol]
        raise Exception(f"{symbol} has not been declared")
    
    
    def new_scope(self) :
        self.scopes.append({})
        
    
    def leave_scope(self) :
        if len(self.scopes) > 1 :
            self.scopes.pop()
        else :
            raise Exception("Cannot leave global scope")
        
    
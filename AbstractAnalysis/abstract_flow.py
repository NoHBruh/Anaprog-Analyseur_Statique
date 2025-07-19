from abstractDomain import AbstractDomain
from utils import handle_arithmetic_variables, handle_arithmetic_with_constant_right, handle_arithmetic_with_constant_left
from utils import handle_concrete_val_least_upper_bound, handle_abstract_val_least_upper_bound, handle_var_const_least_upper_bound

class AbstractEnvironment :
    def __init__(self):
        self.abs_env = {}
        
        
    """Abstract analysis will be made on array access and creation operations.
    These operations need an index that can be a variable or a constant. 
    We thus may pay attention to assignation/update (+ arithmetic) operations  on variables, as they could cause an IndexOutOfBoundsException
      
    FORWARD analysis using visitor pattern
    """
    
    # ------FlowFunctions--------
    
    def constant_assign_flow_function(self, symbol, value):
        """var x = constant c"""
        if value in {True, False} :
            self.abs_env[symbol] = AbstractDomain.NOTNUMERIC
        elif (value < 0):
            self.abs_env[symbol] = -value
            
        elif value == 0 : 
            self.abs_env[symbol] = AbstractDomain.ZERO 
            
        elif value > 0 :
            self.abs_env[symbol] = value
            
        else :
            self.abs_env[symbol] = AbstractDomain.TOP
            
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    
    def variable_assign_flow_function(self, symbol, assigned_variable):
        """ var symbol = var assigned_variable"""
        if assigned_variable not in self.abs_env:
            raise Exception("variable not in abstract environment")
        self.abs_env[symbol] = self.abs_env[assigned_variable]
        print(f"Updated variable '{symbol}' in abstract environment to value of: {assigned_variable}")
        
    
    
    def variable_sum_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 + var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '+', self.abs_env[assigned_variable2])
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def variable_sub_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 - var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '-', self.abs_env[assigned_variable2])    
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
    
    def variable_mult_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 * var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '*', self.abs_env[assigned_variable2])  
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def variable_div_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 / var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '/', self.abs_env[assigned_variable2])  
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
    
    def var_const_sum_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '+' , constant)
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def var_const_sub_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '-' , constant)
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
        
    def var_const_mult_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '*' , constant)
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def var_const_div_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '/' , constant)
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def const_var_sum_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '+' ,self.abs_env[assigned_variable])
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def const_var_sub_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '-' ,self.abs_env[assigned_variable])
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def const_var_mult_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '*' ,self.abs_env[assigned_variable])
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
    def const_var_div_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '/' ,self.abs_env[assigned_variable])
        print(f'added/updated symbol {symbol} with value {self.abs_env[symbol]} in abstract environment')
        
#----------------ApplyingConditions-------------------------        
    def conditions_handler(self, conditions) :
           for cond in conditions :
               match cond:
                   case (oprnd1, op, oprnd2) :
                       if oprnd1 in self.abs_env and oprnd2 in self.abs_env :
                           self.variables_condition_applier(oprnd1, op, oprnd2)
                           
                       elif oprnd1 in self.abs_env and oprnd2 not in self.abs_env :
                           self.var_const_condition_applier(oprnd1, op, oprnd2) 
                        
                       elif oprnd1 not in self.abs_env and oprnd2 in self.abs_env :
                           self.const_var_condition_applier(oprnd1, op, oprnd2) 

        
   
    def variables_condition_applier(self, var1, op, var2) :
        if var1 not in AbstractDomain and var2 not in AbstractDomain :
            value1 = self.abs_env[var1]
            value2 = self.abs_env[var2]
            
            match op :
                
                case '>' :
                    if value1 <= value2 :
                       self.abs_env[var1] = min(value2, value1)
                    
                case '<' :
                    if value1 >= value2 :
                        self.abs_env[var1] = max(value1, value2)
                case '>=' :
                    if value1 < value2 :
                        self.abs_env[var1] = value2 - 1
                    
                case '<=' :
                   if value1 > value2 :
                       self.abs_env[var1] = value1
                    
                case '==' :
                    self.abs_env[var1] = value2
   
    def var_const_condition_applier(self, var, op, const) :
        value = self.abs_env[var]
        match op :
            case '>' :
              if value  not in AbstractDomain and value <= const  or value == AbstractDomain.BOTTOM:
                  self.abs_env[var] = min(value, const)
            
            case '<' :
                if value not in AbstractDomain and value >= const or value == AbstractDomain.TOP :
                    self.abs_env[var] = max(value, const)
                    
            case '>=' :
                if value not in AbstractDomain and value < const or value == AbstractDomain.BOTTOM :
                    self.abs_env[var] = const - 1
                    
            case '<=' :
                if value not in AbstractDomain and value > const or value == AbstractDomain.TOP :
                    self.abs_env[var] = value 
                    
            case '==' :
                self.abs_env[var] = const 
                
            
    def const_var_condition_applier(self, const, op, var) :
        value = self.abs_env[var]    
              
        match op :
            case '>' :
                if value not in AbstractDomain and const <= value or value == AbstractDomain.BOTTOM :
                    self.abs_env[var] = max(const,value)
                
            case '<' :
                if value not in AbstractDomain and const >= value or value == AbstractDomain.BOTTOM :
                    self.abs_env[var] = min(value, const)
                
            case '>=' :
                if value not in AbstractDomain and const < value or value == AbstractDomain.BOTTOM :
                    self.abs_env[var] = value
                
            case '<=' :
                if value not in AbstractDomain and const > value or value == AbstractDomain.BOTTOM :
                    self.abs_env[var] = const - 1
                
            case '==' :
                self.abs_env[var] = value
                    
        
#------------Join_And_Widening_Operations-------------------------

    def join(self ,abs_env1, abs_env2):
        result = None
        
        for var in abs_env1:
            if var in abs_env2 :
                val1 = abs_env1[var]
                val2 = abs_env2[var]
                
                if val1 not in AbstractDomain and val2 not in AbstractDomain and val1 != val2 :
                    result = handle_concrete_val_least_upper_bound(val1, val2)

                elif val1 in AbstractDomain and val2 in AbstractDomain :
                    result = handle_abstract_val_least_upper_bound(val1, val2)
                    
                #only one value is abstract    
                elif val1 in AbstractDomain != val2 in AbstractDomain : 
                    result = handle_var_const_least_upper_bound(val1, val2)
                
                if result != None :
                    self.abs_env[var] = result
                    print(f'join operation done for variable {var} now with abstract value {result}')
                
    
    def while_widening_handler(self, node) :
        _, stmts_list = node
        
        for stmt in stmts_list :
            match stmt :
                case ('assign', var_id, value) :
                    match value :
                        case('arithExpr_binOp', _, op, _ ) :
                            self.widening(var_id, op)
        
    def widening(self, symbol, op) :
        match op:
            case '+' |'*' :
                self.abs_env[symbol] = AbstractDomain.TOP
            
            case '-':
                self.abs_env[symbol] = AbstractDomain.BOTTOM
                
            case '/' :
                self.abs_env[symbol] = AbstractDomain.ZERO
            
            case _:
                return    
            
        print(f' widening done, variable {symbol} now with abstract value {self.abs_env[symbol]}')
from .abstractDomain import AbstractDomain
from utils import handle_arithmetic_variables, handle_arithmetic_with_constant_right, handle_arithmetic_with_constant_left

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
            self.abs_env[symbol] = AbstractDomain.NEGATIVE
            
        else : 
            self.abs_env[symbol] = value  #not abstract value, we can make an easy check on value if used as an array index
        
    
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
        
        
    def variable_sub_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 - var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '-', self.abs_env[assigned_variable2])    
    
    
    def variable_mult_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 * var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '*', self.abs_env[assigned_variable2])  
     
        
    def variable_div_assign_flow_function(self, symbol, assigned_variable1, assigned_variable2):
        """var symbol = var assigned_variable1 / var assigned variable2"""
        
        if (assigned_variable1 not in self.abs_env or assigned_variable2 not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = self.abs_env[symbol] = handle_arithmetic_variables(self.abs_env[assigned_variable1], '/', self.abs_env[assigned_variable2])  
    
    def var_const_sum_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '+' , constant)
        
    def var_const_sub_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '-' , constant)
        
    def var_const_mult_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '*' , constant)
        
        
    def var_const_div_assign_flow_function(self, symbol, assigned_variable, constant) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_right(self.abs_env[assigned_variable], '/' , constant)
      
    def const_var_sum_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '+' ,self.abs_env[assigned_variable])
        
    def const_var_sub_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '-' ,self.abs_env[assigned_variable])
        
    def const_var_mult_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '*' ,self.abs_env[assigned_variable])
        
    def const_var_div_assign_flow_function(self, symbol, constant, assigned_variable) :
        if (assigned_variable not in self.abs_env):
            raise Exception("variable not in abstract environment")   
        
        self.abs_env[symbol] = handle_arithmetic_with_constant_left(constant, '/' ,self.abs_env[assigned_variable])
        
        
#------------Join_And_Widening_Operations-------------------------


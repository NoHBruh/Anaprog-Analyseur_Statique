import utils

class AstVisitor :
    def __init__(self, sym_table):
        self.sym_table = sym_table
        self.call_stack = [] #stack of function calls
        
    def visit(self, node):
        """intermediate visitor for call the right one on the current node
        
        params
        ------
        self : the current visitor
        
        node : the current node of the ast we're at
        
        notes
        -----
        Most visitor functions are formatted using the name given to the nodes in the grammar_parser.py file
        """
        node_type = node[0]
        visitor_name = f"visit_{node_type}"
        visitor = getattr(self, visitor_name, self.default_visitor)
        return visitor(node)    
    
    def default_visitor(self,node) :
        """default visitor for unsupported node types"""
        raise Exception(f"Unsupported node type for {node[0]} node, no visitor found")
    
  #-------------------------------------
  
    
    def visit_program(self, node) :
        _, program_body = node #(p[0] = ('program', p[1])) in grammar_parser.py, p[1] is program body
        main = (program_body[0], program_body[1]) #name and stmtlist
        prog_functions = program_body[2] # functionlist
        
        '''program functions must be analyzed first, as they might be used in main program'''
        print("Visiting program")
        # ----------------Functions analysis----------------

        if prog_functions != [None] : 
            for func in prog_functions :
                print(f' IN LOOP {func}')
                self.visit(func)
            
        # ----------------Main analysis----------------
        self.visit(main)
    
    
    
    #--------------------------------------------
    
    def visit_function(self, node) :
        
        try:
            _, function_id, param_list, stmt_list = node
        except ValueError:
            print(f"Invalid function node : {node}")
            return
        
        if self.sym_table.exist(function_id) :
            raise Exception(f"Function '{function_id}'already exists")
        
        self.sym_table.insert(function_id, token_type="function", token_value =(param_list, stmt_list))
        print(f'visiting fuction {function_id}')
        
    def visit_main(self, node):
        print("Visiting main")
        name, stmt_list = node
        
        if not self.sym_table.exist(name) :
            self.sym_table.insert(name, token_type ="function")
        
        #entering main scope
        self.sym_table.new_scope()
        for stmt in stmt_list :
            self.visit(stmt)
        self.sym_table.leave_scope()
        
    #---------------------------------------------    
        
    def visit_var(self, node) :
        _, var_id = node
        
        if not self.sym_table.exist(var_id) :
            raise Exception(f"Variable '{var_id}' does not exist")
        
        var_value = self.sym_table.lookup(var_id)["Value"]
        print(f'var {var_id} with value {var_value}')
        return var_value
     
    def visit_number(self, node) :
        _, val = node
        return val
        
    def visit_assign(self, node) :
        _, var_id, value = node
        print(f'visiting assign : {var_id} = {value}')
        if isinstance(var_id, tuple) and var_id[0] =='array_access':
            _, array_id, index = var_id
            idx = self.visit(index)
            
            if not self.sym_table.exist(array_id) :
                raise Exception(f'Array {array_id} does not exist')
            
            # updating array
            array_data = self.sym_table.lookup(array_id)
            array_size = array_data["size"]
            
            #Asserting array size was not altered
            if array_data["Type"] != "array":
                raise Exception(f'{array_id} is not an array')
            if not (0<= idx < array_size):
                raise Exception(f'Index {idx} out of bounds with array {array_id} of size {array_size}')
            
            val = self.visit(value)
            array_data["Value"][idx] = val
            prinf(f'Updatined array {array_id} at index {idx} to value {val}')
            return
        
        #Variable assignment
        val = self.visit(value)
        
        if not self.sym_table.exist(var_id):
            if (isinstance(val, list)):
                self.sym_table.insert(var_id, token_type = "array", token_value = val, size = len(val))
            else:
                self.sym_table.insert(var_id, token_type = "variable", token_value = val)
        
        else :
            self.sym_table.update(var_id, token_value = val)
        
        print(f"Added/Updated variable '{var_id}' with value: {val}")
        
    def visit_assign_func_call(self, node):
        _, var_id, _function, _args = node
        
        func_id = _function[1]
        
        if not self.sym_table.exist(func_id):
            raise Exception(f'function {func_id} does not exist')
        
        #------------------------------
        if func_id in self.call_stack:
            raise Exception(f'no recursion allowed, {func_id} already in call stack')
        
        self.call_stack.append(func_id)
        
        try:
            function_data = self.sym_table.lookup(func_id)
            params, body = function_data["Value"]
            
            if len(_args) != len(params) :
                raise Exception(f"Function {func_id} expects {len(params)}, got {len(_args)}")
        
            self.sym_table.new_scope()
            
            for param, _arg in zip(params, _args):
                if isinstance(_arg[1], str):
                    _arg = self.visit(_arg)

                if not self.sym_table.exist(param[1]):
                    self.sym_table.insert(param_[1], token_type="parameter", token_value=_arg)
                else:
                    self.sym_table.update(param[1], token_type="parameter", token_value = _arg)
            
            return_val = None
            
            for stmt in body:
                return_val = self.visit(stmt)
            self.sym_table.leave_scope()
            
            if not self.sym_table.exist(var_id):
                self.sym_table.insert(var_id, token_type="variable", token_value= return_val)
            else:
                self.sym_table.update(var_id, token_value=return_val)
            print(f'added/updated {var_id} with return value {return_val}')
            
        finally:
            self.call_stack.pop()
            
            
    def visit_array_create(self, node) :
        _, array_id, size = node
        
        if isinstance(size, tuple) and size[0] == 'number' :
            array_size = size[1]
        elif isinstance(size, tuple) and size[0] == 'variable':
            size_var = size
            if not self.sym_table.exist(size_var) :
                raise Exception(f'size variable {size_var} does not exist')
            array_size = self.sym_table.lookup(size_var)["Value"]
        
        else:
            raise Exception("Invalid size")
        
        if self.sym_table.exist(array_id) :
            raise Exception(f'Array {array_id} already exists')
            
        self.sym_table.insert(array_id, token_type = "array", size = array_size, token_value = [None] * array_size)
        
        print(f'Array {array_id} of size {array_size} initialized')      
        
        
        
        
    def visit_array_assign(self, node) :
        _, array_id, index, value = node
        if not self.sym_table.exist(array_id):
            raise Exception(f' array {array_id} does not exist')
        
        array_data = self.sym_table.lookup(array_id)
        if array_data["Type"] != "array" :
            raise Exception(f'{array_id} is not an array')

        idx_value = self.visit(index)
        if not (0<= idx_value < array_data["size"]):
            raise Exception(f'Index out of bounds for array {array_id}')
        
        #Assigning values
        val = self.visit(value)
        
        array_data["Value"][idx_value] = val
        
        print(f'Array {array_id} updated at index {idx_value} to value {val}')
        
    def visit_array_expr(self, node) :
        
        _, array_id, index = node
        print(f"Analyzing array access: {array_id}[{index}]")

        
        if not self.sym_table.exist(array_id):
            raise Exception(f"Array {array_id} does not exist")


        array_data = self.sym_table.lookup(array_id)
        if (array_data["Type"] != "array"):
            raise Exception(f'Array {array_id} used as an array but is {array_data["Type"]}')


        print(f"array data  {array_data}")

        array_size = array_data["size"]
        if array_size is None:
            raise Exception(f'Array {array_id} does not have a defined size.')
        
         # Handle the case where no index is provided (t[])
        if index is None:
            print(f"Accessing entire array '{array_id}'")
            return array_data["Value"]  # Return the entire array

        # Resolve the index value
        index = self.visit(index)

        # Check for out-of-bounds access
        if not (0 <= index < array_size):
            raise Exception(f'Index {index} out of bounds for array {array_id} with size {array_size}.')

         # Retrieve the value at the index
        value = array_data["Value"][index]
        if value == None:
            raise Exception(f'No value at index {index} of array {array_id} ')
        print(f'Accessed value at {array_id}[{index}] = {value}')
        return value
        
    def visit_if(self, node) :
        _, bool_stmt, then, _else = node
        
        stmt_eval = self.visit(bool_stmt)
        
        if stmt_eval :
            self.visit(then)
        
        else :
            self.visit(_else)
        
    def visit_while(self, node) :
        _, bool_stmt, loop = node
        
        loop = loop[1]
        self.sym_table.new_scope()
        while self.visit(bool_stmt):
            for stmt in loop :
                self.visit(stmt)
        self.sym_table.leave_scope()
    
    def visit_sequence(self, node) :
        print(f'visiting node {node}')
        _, stmt_list = node
        for stmt in stmt_list :
            self.visit(stmt)
    
    def visit_return(self, node) :
         _, return_val = node
         print(f'returning {node}')
         return self.visit(return_val)
     
    
    def visit_func_call(self, node) :
        try :
            _, func_id, params, body = node
        except ValueError:
            print(f'Invalid node structure :{node}')
            return
        
        if self.sym_table.exist(func_id):
            raise Exception(f'Function {func_id} already exists')
        
        self.sym_table.insert(func_id, token_type = "function", token_value =(params, body))
        
        self.sym_table.new_scope()
        
        for param in params :
            name = param[1]
            if not self.sym_table.exist(name):
                self.sym_table.insert(name, token_type = "parameter", token_value= self.sym_table.default)
        
        for stmt in body :
            self.visit(stmt)
            
        self.sym_table.leave_scope()
        
    def visit_arithExpr_binOP(self, node) :
        _, left, operator, right = node
        print(f"visiting arithmetic operation: {left} {operator} {right}")
        
        left_val = left[1] #'number'
        right_val = right[1] #'number'
        
        
        if isinstance(left_val, str):
            left_val = self.sym_table.lookup(left_val)["Value"]
        
        if isinstance(right_val, str) :
            right_val = self.sym_table.lookup(right_val)["Value"]
            
        return utils.process_arith_binOp(left_val, operator, right_val)
        
    def visit_boolExpr(self, node) :
        
        _, left, operator, right = node
        
        left_val = left[1] #'number'
        right_val = right[1] #'number'
        
        
        if isinstance(left_val, str):
            left_val = self.sym_table.lookup(left_val)["Value"]
        
        if isinstance(right_val, str) :
            right_val = self.sym_table.lookup(right_val)["Value"]
        
        return utils.process_bool_binOp(left_val, operator, right_val)
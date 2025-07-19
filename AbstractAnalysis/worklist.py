from abstract_flow import AbstractEnvironment
from abstractDomain import AbstractDomain
from my_warnings import Warnings, WarningType
from utils import ops, num_to_string, bool_ops_reverse
import copy
class Worklist:
    def __init__(self):
        self.array_sizes = {} # used for keeping tracks of array sizes, facilitates checking when using a constant as index
        self.abstract_environement = AbstractEnvironment()
        self.conditions = []
        self.warnings = Warnings()
        self.work_list = []
        self.abs_env_collection = {}
        
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
    
    #---------------------------------------    
    
    def visit_program(self, node) :
        _, program_body = node #(p[0] = ('program', p[1])) in grammar_parser.py, p[1] is program body
        main = (program_body[0], program_body[1]) #name and stmtlist
        prog_functions = program_body[2] # functionlist
        
        '''program functions must be analyzed first, as they might be used in main program'''
        print("Visiting program")
        # ----------------Functions analysis----------------

        if prog_functions != [None] : 
            for func in prog_functions :
                self.visit(func)
            
        # ----------------Main analysis----------------
        self.visit(main)
        
        
    #------------------------------------------    
    def visit_main(self, node):
        print("Visiting main")
        _, stmt_list = node
        
        for stmt in stmt_list :
            self.visit(stmt)
     
    def visit_function(self, node) :
        try:
            _, function_id, param_list, stmt_list = node
            print(f'visiting function {function_id}')
            for param in param_list:
                self.abstract_environement.abs_env[param[1]] = AbstractDomain.TOP
            
            for stmt in stmt_list :
                self.visit(stmt)
        except ValueError:
            print(f"Invalid function node : {node}")
            return 
     
            
            
    def visit_sequence(self, node) :
        print(f'visiting node {node}')
        _, stmt_list = node
        for stmt in stmt_list :
            self.visit(stmt)
        return self.abstract_environement.abs_env
    
    #def visit_return(self, node) :
     #   _, return_val = node
      #  print(f'returning {node}')
       # self.visit(return_val)
    
    def visit_number(self, node) :
        _, val = node
        return val
    
    def visit_negnumber(self, node) :
        _, _, val = node
        return -val
    
    def visit_assign(self, node) :
        _, var_id, value = node
        print(f'visiting assign : {var_id} = {value}')
            
        node_name = value[0]
        
        if node_name == 'negnumber' :
            self.abstract_environement.constant_assign_flow_function(var_id, -value[2])
            
        val = value[1]
        if node_name == 'number' or node_name == 'bool' :
            self.abstract_environement.constant_assign_flow_function(var_id, val)
            
        elif node_name == 'var' :
            self.abstract_environement.variable_assign_flow_function(var_id, val)
        
        elif node_name == "arithExpr_binOp":
            oprnd1, op, oprnd2 = value[1:]
            print(value[1:])
            self.process_arithmetic_worklist(var_id, oprnd1, op, oprnd2)
            
        elif node_name == 'array_expr' :
            self.visit(value)
          
            
    def visit_array_create(self, node) :
        _, array_id, size = node
        
        match size :
            case ('negnumber',_, const) :
                self.warnings.add_warning(WarningType.ERROR, f"constant {const} is negative and cannot be used as an array size")
                self.array_sizes[array_id] = -const
                print(f"added array {array_id} with size {const}")
            
            case('number', const) :
                self.array_sizes[array_id] = const
                
            case('boprnd', bool_const) :
                self.warnings.add_warning(WarningType.ERROR, f"constant {bool_const} is a boolean and cannot be used as an array size") 
                
            case('var', var_id) :
                abstract_val = self.abstract_environement.abs_env[var_id]
                if abstract_val == AbstractDomain.NEGATIVE :
                
                    self.warnings.add_warning(WarningType.ERROR, f"variable {var_id} is negative and cannot be used as an array size")
                    
                elif abstract_val not in AbstractDomain :
                        if abstract_val < 0 :  
                            self.warnings.add_warning(WarningType.ERROR, f"variable {var_id} is negative and cannot be used as an array size")
                            
                elif (abstract_val == AbstractDomain.NOTNUMERIC) :
                    self.warnings.add_warning(WarningType.ERROR, f"variable {var_id} is a boolean and cannot be used as an array size")
                    return 
                self.array_sizes[array_id] = abstract_val    
                print(f"added array {array_id} with abstract size {abstract_val}")
    
    def visit_array_assign(self, node) :
        # i.e z[5] = 4
        _, array_id, index, _ = node
        
        if array_id not in self.array_sizes.keys() :
            self.warnings.add_warning(WarningType.ERROR, f"trying to update value of an array {array_id} that does not exist")
            return
        array_size = self.array_sizes[array_id]
        if array_size in AbstractDomain :
            self.warnings.add_warning(WarningType.WARNING, f'trying to update an item in array {array_id} whose size is uncertain or invalid: {array_size}')
        match index:
            
            case ('number', value) :
                
                if array_size not in AbstractDomain and value > array_size :
                    self.warnings.add_warning(WarningType.ERROR, f'Trying to write in array {array_id} at index {value} when its max size is {array_size}')  
                    
            case('boprnd', bool_const) :
                self.warnings.add_warning(WarningType.ERROR, f"index {bool_const} is invalid (boolean)  with array {array_id}")      

            case('negnumber', _, _) :
                self.warnings.add_warning(WarningType.ERROR, f' trying to write in array {array_id} at a negative index, will cause an error')
            
            case ('var', var_id) :
                if var_id not in self.abstract_environement.abs_env :
                    self.warnings.add_warning(WarningType.ERROR, f'trying to write in array {array_id} at index variable {var_id} that does not exist')
                    return
                    
                var_abs_val = self.abstract_environement.abs_env[var_id]
                is_concrete = var_abs_val not in AbstractDomain
                
                is_concrete_array_size = self.array_sizes[array_id] not in AbstractDomain
                is_invalid_index = None
                
                if is_concrete_array_size:
                    is_invalid_index = self.array_sizes[array_id] > 0 and var_abs_val > 0 and var_abs_val > self.array_sizes[array_id]
                
                if is_concrete :
                    if var_abs_val < 0 :
                        self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is negative, cannot write in array {array_id}')
                    
                    elif is_invalid_index :
                        self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is bigger than array max size, cannot write')
                
                if var_abs_val == AbstractDomain.NOTNUMERIC :
                    self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is boolean and trying to write in array {array_id} will cause an error')
                
                elif array_size == var_abs_val == AbstractDomain.POSITIVE :
                    self.warnings.add_warning(WarningType.WARNING, f'index variable {var_id} may be bigger than array {array_id} size')
                    
                elif var_abs_val == AbstractDomain.NEGATIVE :
                    self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is negative and trying to write in array {array_id} is invalid')
                
                elif var_abs_val == AbstractDomain.UNSURE and array_size in {AbstractDomain.POSITIVE, AbstractDomain.UNSURE} :
                    self.warnings.add_warning(WarningType.WARNING, f'variable index {var_id} could be invalid to use with array {array_id}')
                
                elif var_abs_val == AbstractDomain.TOP :
                    self.warnings.add_warning(WarningType.WARNING(f'variable index {var_id} may be bigger than array {array_id} size'))    
            
    def visit_array_expr(self, node) :
        # i.e z = array[8]
        _, array_id, index = node
        
        if array_id not in self.array_sizes.keys() :
            self.warnings.add_warning(WarningType.ERROR, f"trying to access value of an array {array_id} that does not exist")
            return
        
        array_size = self.array_sizes[array_id]
        if array_size in AbstractDomain :
            self.warnings.add_warning(WarningType.WARNING, f'trying to access an item in array {array_id} whose size is uncertain or invalid : {array_size}')
        match index:
            
            case ('number', value) :
                
                if value > AbstractDomain.TOP :
                    self.warnings.add_warning(WarningType.ERROR, f"trying to access array {array_id} further than what is allowed")
                
                if array_size not in AbstractDomain and value > array_size :
                    self.warnings.add_warning(WarningType.ERROR, f'Trying to write in array {array_id} at index {value} when its max size is {array_size}')        

            case('boprnd', bool_const) :
                self.warnings.add_warning(WarningType.ERROR, f"index {bool_const} is invalid (boolean), will not access {array_id}")

            case('negnumber', _, _) :
                self.warnings.add_warning(WarningType.ERROR, f' trying to write in array {array_id} at a negative index, will cause an error')
            
            case ('var', var_id) :
                if var_id not in self.abstract_environement.abs_env.keys() :
                    self.warnings.add_warning(WarningType.ERROR, f'trying to write in array {array_id} at index variable {var_id} that does not exist')
                    return
                    
                var_abs_val = self.abstract_environement.abs_env[var_id]
                is_concrete = var_abs_val not in AbstractDomain
                
                if array_size not in AbstractDomain and is_concrete :
                    if var_abs_val > 0 and var_abs_val > array_size :
                        self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is bigger than size {array_size} of array {array_id}, cannot access value')
                
                if var_abs_val == AbstractDomain.NOTNUMERIC :
                    self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is boolean and trying to access array {array_id} will cause an error')
                
                elif array_size == var_abs_val == AbstractDomain.POSITIVE :
                    self.warnings.add_warning(WarningType.WARNING, f'index variable {var_id} may be bigger than array {array_id} size')
                    
                elif var_abs_val == AbstractDomain.NEGATIVE :
                    self.warnings.add_warning(WarningType.ERROR, f'variable index {var_id} is negative and trying to access array {array_id} is invalid')
                
                elif var_abs_val == AbstractDomain.UNSURE and array_size in {AbstractDomain.POSITIVE, AbstractDomain.UNSURE} :
                    self.warnings.add_warning(WarningType.WARNING, f'variable index {var_id} could be invalid to use with array {array_id}')
                    
                elif var_abs_val == AbstractDomain.TOP :
                    self.warnings.add_warning(WarningType.WARNING, f'variabe index {var_id} could be bigger and not access array {array_id}')
        
        
    def visit_if(self, node) :
        _, bool_stmt, then, _else = node
        match bool_stmt :
            case (_, oprnd1, op, oprnd2) :
                self.conditions.append((oprnd1[1], op, oprnd2[1])) 
        
        pred_abs_env = copy.deepcopy(self.abstract_environement.abs_env)
        
        self.abstract_environement.conditions_handler(self.conditions)
        
        self.visit(then)
        then_abs_env = copy.deepcopy(self.abstract_environement.abs_env)
        
        #restore abstract_env old state for else branch visit
        self.abstract_environement.abs_env = pred_abs_env
        
        if_cond = self.conditions.pop()
        else_cond = (if_cond[0], bool_ops_reverse[if_cond[1]], if_cond[2])
        self.conditions.append(else_cond)
        
        self.abstract_environement.conditions_handler(self.conditions)
        
        self.visit(_else)
        else_abs_env = copy.deepcopy(self.abstract_environement.abs_env)
        
        
        
        #joining then and else abstract env
        self.abstract_environement.abs_env = pred_abs_env
        self.abstract_environement.join(then_abs_env, else_abs_env)
        
        self.conditions.pop()
        
    def visit_while(self, node):
        _, bool_stmt, loop = node
        
        print('visiting while statement')
        
        pred_abs_env = copy.deepcopy(self.abstract_environement.abs_env)
        
        match bool_stmt:
            case('boolExpr', oprnd1, op, oprnd2) :
                match (oprnd1, oprnd2):
                    case(('var', var1), (_, var2)) :
                        if var2 not in self.abstract_environement.abs_env.keys():
                            self.abstract_environement.while_widening_handler(loop)
                        
                        else:
                            val1 = self.abstract_environement.abs_env[var1]
                            val2 = self.abstract_environement.abs_env[var2]
                            
                            if val1 not in AbstractDomain and val2 not in AbstractDomain :
                                match op :
                                    case '>' | '>=' :
                                        iterations = val1 - val2 
                                    
                                    case '<' | '<=' :
                                        iterations = val2 - val1
                                        
                                    case '!=' :
                                        iterations = abs(val2 - val1)
                                    
                                    case _:
                                        iterations = 0
                                
                                
                                if iterations > 0 :
                                    for i  in range(iterations):
                                        print("\n")
                                        print(f'loop n° {i+1}')
                                        print("\n")
                                        self.visit(loop)
                                    
                                    
                                after_loops_abs_env = copy.deepcopy(self.abstract_environement.abs_env)

                                self.abstract_environement.join(pred_abs_env, after_loops_abs_env)
            case _ :
                return                           
     
    def while_handler(self, node, iterations):
        _, loop_stmts = node

        if iterations == 0:
            return
        
        for stmt in loop_stmts:
            match stmt:
                case('assign', var_id, value):
                    match value:
                        case ('arithExpr_binOp', oprnd1, op, oprnd2):
                            for _ in range(iterations) :
                                self.process_arithmetic_worklist(var_id, oprnd1, op, oprnd2)
                                
                        case _ :
                            return
                
                case _: 
                    return
    
    
                                    
        
    def process_arithmetic_worklist(self, var_symbol, oprnd1, op, oprnd2) :
        arith_op = ops[op]
        op = num_to_string[op]
        match (oprnd1, oprnd2):
            case (('number', val1), ('number', val2)) :
                self.abstract_environement.constant_assign_flow_function(var_symbol, arith_op(val1, val2))

            case (('var', val1), ('number', val2)):
                flow_function_name = f'var_const_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                return flow_function(var_symbol, val1, val2)
                
            case (('number', val1),('var', val2)) :
                flow_function_name = f'const_var_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                return flow_function(var_symbol, val1, val2)
                
            case (('var', val1), ('var', val2)):
                flow_function_name = f'variable_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                return flow_function(var_symbol, val1, val2)

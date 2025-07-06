from abstract_flow import AbstractEnvironment
from abstractDomain import AbstractDomain
from .warnings import Warnings, WarningType
from utils import get_operator_to_string, ops
class Worklist:
    def __init__(self):
        self.array_sizes = {} # used for keeping tracks of array sizes, facilitates checking when using a constant as index
        self.abstract_environement = AbstractEnvironment()
        self.conditions = []
        self.warnings = Warnings()
        self.work_list = []
        
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
            
            
    def visit_sequence(self, node) :
        print(f'visiting node {node}')
        _, stmt_list = node
        for stmt in stmt_list :
            self.visit(stmt)
        return self.abstract_environement
    
    def visit_number(self, node) :
        _, val = node
        return val
    
    def visit_assign(self, node) :
        _, var_id, value = node
        print(f'visiting assign : {var_id} = {value}')
        node_name = value[0]
        val = value[1]
        if node_name == 'num' :
            self.abstract_environement.constant_assign_flow_function(var_id, val)
            
        elif node_name == 'var' :
            self.abstract_environement.variable_assign_flow_function(var_id, val)
        
        elif node_name == "arithExpr":
            oprnd1, op, oprnd2 = value[1:]

            self.process_arithmetic_worklist(var_id, oprnd1, op, oprnd2)
            
        elif node_name == 'array_expr' :
            self.visit(value)
            
            
    def visit_array_create(self, node) :
        _, array_id, size = node
        
        match size :
            case ('num', const) :
                if const < 0 :
                    self.warnings.add_warning(WarningType.ERROR, f"constant {const} is negative and cannot be used as an array size")
                    return
                self.array_sizes[array_id] = const
                print(f"added array {array_id} with size {const}")
                
            case('boprnd', bool_const) :
                self.warnings.add_warning(WarningType.ERROR, f"constant {bool_const} is a boolean and cannot be used as an array size") 
                
            case('var', var_id) :
                abstract_val = self.abstract_environement.abs_env[var_id]
                if (abstract_val == AbstractDomain.NEGATIVE) :
                    self.warnings.add_warning(WarningType.ERROR, f"variable {var_id} is negative and cannot be used as an array size")
                    
                elif (abstract_val == AbstractDomain.NOTNUMERIC) :
                    self.warnings.add_warning(WarningType.ERROR, f"variable {var_id} is a boolean and cannot be used as an array size")
                    return 
                self.array_sizes[array_id] = abstract_val    
                print(f"added array {array_id} with abstract size {abstract_val}")
    
    def process_arithmetic_worklist(self, var_symbol, oprnd1, op, oprnd2) :
        op = get_operator_to_string(op)
        
        match (oprnd1, oprnd2):
            case (('num', val1), ('num', val2)) :
                self.abstract_environement.constant_assign_flow_function(var_symbol, ops[op](val1, val2))

            case (('var', val1), ('num', val2)):
                flow_function_name = f'var_const_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                flow_function(var_symbol, val1, val2)
                
            case (('num', val1),('var', val2)) :
                flow_function_name = f'const_var_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                flow_function(var_symbol, val1, val2)
                
            case (('var', val1), ('var', val2)):
                flow_function_name = f'variable_{op}_assign_flow_function'
                flow_function = getattr(self.abstract_environement, flow_function_name)
                flow_function(var_symbol, val1, val2)

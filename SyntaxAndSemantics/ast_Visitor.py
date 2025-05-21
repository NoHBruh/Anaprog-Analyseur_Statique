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
        visitor = getattr(self, visitor_name, self.default_visitor(node))
        return visitor(node)    
    
    def default_visitor(self,node) :
        """default visitor for unsupported node types"""
        raise Exception(f"Unsupported node type for {node[0]} node, no visitor found")
    
    
    def visit_program(self, node) :
        
        
    def visit_main(self, node):
        
    
    def visit_function(self, node) :
        
    
    def visit_var(self, node) :
        
     
    def visit_number(self, node) :
        
        
    def visit_assign(self, node) :
        
        
    def visit_assign_func_call(self, node):
        
        
    def visit_array_create(self, node) :
        
        
    def visit_array_assign(self, node) :
       
        
    def visit_array_expr(self, node) :
        
        
    def visit_if(self, node) :
        
        
    def visit_while(self, node) :
        
    
    def visit_sequence(self, node) :
        
    
    def visit_return(self, node) :
        
    
    def visit_func_call(self, node) :
        
        
    def visit_arithExpr_binOP(self, node) :
        
        
    def visit_boolExpr(self, node) :
        
        
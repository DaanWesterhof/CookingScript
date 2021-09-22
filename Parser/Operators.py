from Definitions import *
from Parser.AST_Nodes import *

class AST_Operator(AST_Node):
    def __init__(self, operator_type):
        if operator_type == "Dummy":
            super().__init__("Dummy")
        else:
            super().__init__("AST_Operator")

        self.left: AST_Node = None
        self.right: AST_Node = None
        self.operator = operator_type
        self.value = 0
        if operator_type in operators_level1:
            self.value = 1
        elif operator_type in operators_level2:
            self.value = 2

class AST_PlusOperator(AST_Operator):
    def __init__(self):
        super().__init__("AST_PlusOperator")
        self.value = 2

class AST_MinusOperator(AST_Operator):
    def __init__(self):
        super().__init__("AST_MinusOperator")
        self.value = 2

class AST_MulitplyOperator(AST_Operator):
    def __init__(self):
        super().__init__("AST_MulitplyOperator")
        self.value = 3

class AST_DivideOperator(AST_Operator):
    def __init__(self):
        super().__init__("AST_DivideOperator")
        self.value = 3

class AST_OperatorExpression(AST_Operator):
    def __init__(self, operator_type):
        super().__init__(operator_type)

class AST_AssignmentOperator(AST_Operator):
    def __init__(self):
        super().__init__("=")
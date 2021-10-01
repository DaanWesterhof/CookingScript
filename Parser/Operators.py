from Definitions import *
from Parser.AST_Nodes import *

class AST_Operator(AST_Node):
    def __init__(self, operator_type: str):
        if operator_type == "Dummy":
            super().__init__("Dummy")
        elif operator_type in RelationalOperator:
            super().__init__("AST_RelationalOperator")
        else:
            super().__init__("AST_Operator")

        self.left: AST_Node = None
        self.right: AST_Node = None
        self.operator: str = operator_type
        self.value = 0
        if operator_type in RelationalOperator:
            self.value = 1
        if operator_type in operators_level1:
            self.value = 2
        elif operator_type in operators_level2:
            self.value = 3

    def __str__(self) -> str:
        if self.operator == "+":
            return "PlusOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "-":
            return "MinOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "/":
            return "DevideOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "*":
            return "MulitplyOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "=":
            return "AssignmentOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "==":
            return "EqualsOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "<=":
            return "SmallerEqualsOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == ">=":
            return "LargerEqualsOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "!=":
            return "NotEqualOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == "<":
            return "SmallerThenOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        elif self.operator == ">":
            return "LargerThenOperator" + "( " + self.left.__str__() + ", " + self.right.__str__() + " )"
        else:
            return "Something is wrongt" + " self.operator"





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


class AST_RelationalOperators(AST_Operator):
    def __init__(self, operator_type):
        super().__init__(operator_type)
        self.operator = operator_type
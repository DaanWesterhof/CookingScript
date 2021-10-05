from Definitions import *
from Parser.AST_Nodes import *

class AST_Operator(AST_Node):
    """ A class for operator expressions

        Attributes
        ----------
        left : AST_Node
            The AST node on the left of the operator

        right : AST_Node
            The AST node on the right of the operator

        operator : str
            The operator in string form for example: "+

        value : int
            The higher the number the higher its priority in a calculation for example:
                multiply has value 3 while plus has value 2 so multiply is evaluated before the plus
    """
    def __init__(self, operator_type: str = "Dummy"):
        """ Initialize the object and set its operator and type

            Parameters
            ----------
            operator_type : str, optional
                The operator_type determines what kind of calculation this operator wil do.
                The default value is Dummy to create a dummy operator that does nothing

        """
        if operator_type == "Dummy":
            super().__init__("Dummy")
        elif operator_type in RelationalOperator:
            super().__init__("AST_RelationalOperator")
        else:
            super().__init__("AST_Operator")

        self.left: AST_Node = None
        self.right: AST_Node = None
        self.operator: str = operator_type
        self.value: int = 0
        if operator_type in RelationalOperator:
            self.value = 1
        if operator_type in operators_level1:
            self.value = 2
        elif operator_type in operators_level2:
            self.value = 3

    def __str__(self, index=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
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
            return self.operator



class AST_OperatorExpression(AST_Operator):
    """ A class to identify OperatorExpressions
    """
    def __init__(self, operator_type: str):
        """ Initialize the object and sets the type using the innit of its superclass

                Parameters
                ----------
                operator_type : str
                    The string version of the desired operator. for exapmple: "+" or "*"
        """

        super().__init__(operator_type)


class AST_AssignmentOperator(AST_Operator):
    """ A class to identify AssignmentOperators
    """
    def __init__(self):
        """Initialize the object and sets the type using the innit of its superclass"""
        super().__init__("=")


class AST_RelationalOperators(AST_Operator):
    """ A class to identify RelationalOperators
    """
    def __init__(self, operator_type: str):
        """ Initialize the object and sets the type using the innit of its superclass

                Parameters
                ----------
                operator_type : str
                    The string version of the desired operator. for exapmple: "<" or "=="
        """
        super().__init__(operator_type)
from Definitions import *

class AST_Node(object):
    def __init__(self, node_type):
        self.node_type: str = node_type
        pass

    def __str__(self):
        return f"Node({self.node_type})"


class AST_Primitive(AST_Node):
    def __init__(self, type, value):
        super().__init__("AST_Primitive")
        self.type = type
        self.value = value


class AST_ArgumentList(AST_Node):
    def __init__(self):
        super().__init__("AST_ArgumentList")
        self.argument_nodes = []


class AST_FunctionArgument(AST_Node):
    def __init__(self, type, name):
        super().__init__("AST_FunctionArgument")
        self.type = type
        self.name = name
        self.value = None


class AST_Variable(AST_Node):
    def __init__(self):
        super().__init__("AST_Variable")
        self.name = None
        self.value = None
        self.type = None


class AST_VariableReference(AST_Node):
    def __init__(self, variable_name):
        super().__init__("AST_VariableReference")
        self.name = variable_name


class AST_BinairyExpression(AST_Node):
    def __init__(self):
        super().__init__("AST_BinairyExpression")
        self.operator = None
        self.left_code = None
        self.right_code = None


class AST_IfStatement(AST_Node):
    def __init__(self):
        super().__init__("AST_IfStatement")
        self.CodeSequence = None
        self.condition = None


class AST_Loop(AST_Node):
    def __init__(self):
        super().__init__("AST_Loop")
        self.CodeSequence = None
        self.condition = None

class AST_Label(AST_Node):
    def __init__(self):
        super().__init__("AST_Label")
        self.CodeSequence = None
        self.label_number = None



class AST_ReturnStatement(AST_Node):
    def __init__(self):
        super().__init__("AST_ReturnStatement")
        self.value = None


class AST_FunctionCall(AST_Node):
    def __init__(self, ast_type: str="AST_FunctionCall"):
        super().__init__(ast_type)
        self.FunctionName = None
        self.ParameterValues = []


class AST_PrintFunctionCall(AST_FunctionCall):
    def __init__(self, args: AST_ArgumentList):
        super().__init__("AST_PrintFunctionCall")
        self.FunctionName = "Print"
        self.ParameterValues = args


class AST_CodeSequence(AST_Node):
    def __init__(self):
        super().__init__("AST_CodeSequence")
        self.code = []
        self.Variables = []


class AST_Function(AST_Node):
    def __init__(self):
        super().__init__("AST_Function")
        self.name = None
        self.argumentList = None
        self.CodeSequence = None
        self.ReturnType = None


class AST_Program:
    def __init__(self):
        self.Functions: [AST_Function] = None
        self.Variables = []
        self.CodeSequence = None


class AST_Literal(AST_Node):
    def __init__(self, type, type_name):
        super().__init__(type_name)
        self.type = type


class AST_Integer(AST_Literal):
    def __init__(self, value: int):
        super().__init__("Integer", "AST_Integer")
        self.value: int = value


class AST_Bool(AST_Literal):
    def __init__(self, value: bool):
        super().__init__("Bool", "AST_Bool")
        self.value: bool = value


class AST_String(AST_Literal):
    def __init__(self, value: str):
        super().__init__("String", "AST_String")
        self.value: str = value

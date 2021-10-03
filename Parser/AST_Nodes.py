from Definitions import *

class AST_Node(object):
    def __init__(self, node_type):
        self.node_type: str = node_type
        pass

    def __str__(self):
        return f"Node({self.node_type})"



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

    def __str__(self):
        return "Variable: " + self.name + ": " + self.type


class AST_VariableReference(AST_Node):
    def __init__(self, variable_name):
        super().__init__("AST_VariableReference")
        self.name = variable_name
        self.value = variable_name

    def __str__(self):
        return "VariableReference: " + self.name


class AST_IfStatement(AST_Node):
    def __init__(self):
        super().__init__("AST_IfStatement")
        self.CodeSequence = None
        self.condition = None

    def __str__(self):
        return "IfStatement: "


class AST_Loop(AST_Node):
    def __init__(self):
        super().__init__("AST_Loop")
        self.CodeSequence = None
        self.condition = None

#todo implement in runner
class AST_Label(AST_Node):
    def __init__(self):
        super().__init__("AST_Label")
        self.label_number = None



class AST_ReturnStatement(AST_Node):
    def __init__(self):
        super().__init__("AST_ReturnStatement")
        self.value = None


#todo implement in runner
class AST_FunctionVariable(AST_Node):
    def __init__(self, ast_type: str="AST_FunctionVariable"):
        super().__init__(ast_type)
        self.name = None
        self.FunctionName = None
        self.value = []


class AST_FunctionCallExecution(AST_Node):
    def __init__(self, ast_type: str="AST_FunctionExecution"):
        super().__init__(ast_type)
        self.name = None


class AST_PrintFunctionCall(AST_FunctionCallExecution):
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
        self.Functions = {}
        self.CodeSequence = []


class AST_Literal(AST_Node):
    def __init__(self, type, type_name, value):
        super().__init__(type_name)
        self.type = type
        self.val: str = value

    def __str__(self):
        return self.type + ": " + str(self.val)


class AST_Integer(AST_Literal):
    def __init__(self, value: int):
        super().__init__("Integer", "AST_Integer", str(value))
        self.value: int = value


class AST_Bool(AST_Literal):
    def __init__(self, value: bool):
        super().__init__("Bool", "AST_Bool", str(bool))
        self.value: bool = value


class AST_String(AST_Literal):
    def __init__(self, value: str):
        super().__init__("String", "AST_String", value)
        self.value: str = value

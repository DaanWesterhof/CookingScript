from Parser.AST_Nodes import *
from Parser.Operators import *
from Definitions import *
from typing import *
from ErrorHandler.ErrorHandler import *


def evaluate_operator(operator, a, b) -> AST_Node:
    if operator == '+':
        return AST_Integer(a.value + b.value)
    elif operator == '-':
        return AST_Integer(a.value - b.value)
    elif operator == '/':
        return AST_Integer(a.value / b.value)
    elif operator == '*':
        return AST_Integer(a * b)

    elif operator == "==":
        return AST_Integer(int(a == b))
    elif operator == "<=":
        return AST_Integer(int(a <= b))
    elif operator == ">=":
        return AST_Integer(int(a >= b))
    elif operator == "!=":
        return AST_Integer(int(a != b))
    elif operator == ">":
        return AST_Integer(int(a > b))
    elif operator == "<":
        return AST_Integer(int(a < b))

def generateOperatorString_var_var_int(operator, )


def simplifyNode(node):
    if isinstance(node, AST_Literal):
        return node
    elif isinstance(node, AST_Operator):
        left = simplifyNode(node.left)
        right = simplifyNode(node.right)
        node.left = left
        node.right = right
        if isinstance(left, AST_Literal) and isinstance(right, AST_Literal):
            return evaluate_operator(node.operator, left, right)
        return node


def formatCodeLine(operator, start_reg, value):
    str_this = ""
    if operator == '+':
        str_this = "sub     r{}, r{}, {}\n".format(start_reg, start_reg, value)
    elif operator == '-':
        str_this = "sub     r{}, r{}, {}\n".format(start_reg, start_reg, value)
    elif operator == '/':
        str_start_div1 = "push    {r4, r5, r6, r7}\n"
        str_start_div2 = "push    {r0, r1, r2, r3}\n"
        str_load_to_div = "movs    r0, r{} \nmovs r1, {}\n".format(start_reg, value)
        str_do_div = "bl      __aeabi_idiv\n"
        str_get_val1 = "mov     r4, r0\n"
        str_stop_div2 = "pop     {r0, r1, r2, r3}\n"
        str_get_val2 = "mov     r{}, r4\n".format(start_reg)
        str_get_val3 = "pop     {r4, r5, r6, r7}\n"
        str_this = str_start_div1 + str_start_div2 + str_load_to_div + str_do_div + str_get_val1 + str_stop_div2 + str_get_val2 + str_get_val3
    elif operator == '*':
        str_this = "mul r{}, r{}, {}\n".format(start_reg, start_reg, value)
    return str_this

def composeCalculation(node, var_dict, start_reg = 0) -> str:
    if isinstance(node.left, AST_Operator) and isinstance(node.right, AST_Operator):
        str_left = composeCalculation(node.left, var_dict, start_reg)
        str_right = composeCalculation(node.right, var_dict, start_reg + 1)
        str_this = formatCodeLine(node.operator, start_reg, "r{}".format(start_reg+1))
        return str_left + str_right + str_this
    elif isinstance(node.left, AST_Operator):
        str_left = composeCalculation(node.left, var_dict, start_reg)
        if isinstance(node.right, AST_Literal):
            return str_left + formatCodeLine(node.operator, start_reg, "#" +str(node.right.value))
        elif isinstance(node.right, AST_VariableReference):
            return str_left + formatCodeLine(node.operator, start_reg, var_dict[node.right.name])


    elif isinstance(node.right, AST_Operator):
        str_right = composeCalculation(node.right, var_dict, start_reg)
        if isinstance(node.left, AST_Literal):
            return str_right + formatCodeLine(node.operator, start_reg, "#" +str(node.left.value))
        elif isinstance(node.left, AST_VariableReference):
            return str_right + formatCodeLine(node.operator, start_reg, var_dict[node.left.name])



def compileAssignment(node, var_dict):
    if isinstance(node.left, AST_Variable):
        var_dict[node.left.name] = "r"
        var_dict[node.left.name] = "r" + str(3 + len(var_dict))
    simple_node = simplifyNode(node.right)
    if isinstance(simple_node, AST_Integer):
        return "MOV " + var_dict[node.left.name] + ", " + str(simple_node.value)
    else:
        code_string =


def compileCodeBlock(code_sequence: [AST_Node], var_dict) -> str:
        if isinstance(code_sequence[0], AST_AssignmentOperator):
            pass
        elif isinstance(code_sequence[0], AST_Loop):
            pass
        elif isinstance(code_sequence[0], AST_IfStatement):
            pass
        elif isinstance(code_sequence[0], AST_ReturnStatement):
            pass
        elif isinstance(code_sequence[0], AST_PrintFunctionCall):
            pass







def startFunctionCodeBlock(func: AST_Function):
    start_string = func.name + "()" +"\n"
    push_string = "push    {r5, r6, r7, r8, lr}\n"
    pop_string =  "pop     {r5, r6, r7, r8, pc}\n"
    var_dict = {}
    code_string = compileCodeBlock(func.CodeSequence, var_dict)




from Parser.AST_Nodes import *
from Parser.Operators import *
from Definitions import *
from typing import *
from ErrorHandler.ErrorHandler import *


comparator_operator_dict = {
    "<" : "bge",
    ">" : "ble",
    "<=": "bgt",
    ">=": "blt",
    "!=": "beq",
    "==": "bne"
}


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


def formatCodeLine(operator, start_reg, value, value2= ""):
    if value2 == "":
        value2 = "r{}".format(start_reg)
    str_this = ""
    if operator == '+':
        str_this = "sub     r{}, {}, {}\n".format(start_reg, value2, value)
    elif operator == '-':
        str_this = "sub     r{}, {}, {}\n".format(start_reg, value2, value)
    elif operator == '/':
        str_start_div1 = "push    {r4, r5, r6, r7}\n"
        str_start_div2 = "push    {r0, r1, r2, r3}\n"
        str_load_to_div = "movs    r0, {} \nmovs r1, {}\n".format(value2, value)
        str_do_div = "bl      __aeabi_idiv\n"
        str_get_val1 = "mov     r4, r0\n"
        str_stop_div2 = "pop     {r0, r1, r2, r3}\n"
        str_get_val2 = "mov     r{}, r4\n".format(start_reg)
        str_get_val3 = "pop     {r4, r5, r6, r7}\n"
        str_this = str_start_div1 + str_start_div2 + str_load_to_div + str_do_div + str_get_val1 + str_stop_div2 + str_get_val2 + str_get_val3
    elif operator == '*':
        str_this = "mul r{}, {}, {}\n".format(start_reg, value2, value)
    return str_this



def compileCalculation(node, var_dict, start_reg) -> str: #we have to parse it to r0 and r1
    if isinstance(node, AST_Operator):
        left_str = ""
        right_str = ""
        if isinstance(node.left, (AST_VariableReference, AST_Literal)):


        if isinstance(node.right, (AST_VariableReference, AST_Literal)):


def composeCalculation(node, var_dict, start_reg = 0) -> str:
    if isinstance(node.left, AST_Operator) and isinstance(node.right, AST_Operator):
        str_left = composeCalculation(node.left, var_dict, start_reg)
        str_right = composeCalculation(node.right, var_dict, start_reg + 1)
        str_this = formatCodeLine(node.operator, start_reg, var_dict, "r{}".format(start_reg+1))
        return str_left + str_right + str_this


    elif isinstance(node.left, AST_Operator):
        str_left = composeCalculation(node.left, var_dict, start_reg)
        if isinstance(node.right, AST_Literal):
            return str_left + formatCodeLine(node.operator, start_reg, var_dict, node.right)
        elif isinstance(node.right, AST_VariableReference):
            get_var_str = "ldr    r{}, [r7, #{}]\n".format(start_reg+1, var_dict[node.right.name])
            return get_var_str + formatCodeLine(node.operator, start_reg, "r{}".format(start_reg), "r{}".format(start_reg+1))
    elif isinstance(node.right, AST_Operator):
        str_right = composeCalculation(node.right, var_dict,  start_reg)
        if isinstance(node.left, (AST_Literal, AST_VariableReference)):
            return str_right + formatCodeLine(node.operator, start_reg, var_dict, node.left)
    else:

# for a list we will just allocate a lot of space on the stack. Then to access a variable we will just substract index * 4 from its adress and set or load the value



# for variable instead of storing just location store size aswell, to make it easy for lists
def compileAssignment(node, var_dict, var_place):
    if isinstance(node.left, AST_Variable):
        var_dict[node.left.name] = var_place
        var_place = var_place-4
    simple_node = simplifyNode(node.right)
    if isinstance(simple_node, (AST_Integer, AST_Bool)):
        store_string = "movs   r3, #{}\n".format(int(simple_node.value))
        store_string += "str    r3, [r7, #{}]\n".format(var_dict[node.left.name])
        return store_string, var_dict, var_place
    else:
        code_string = composeCalculation(node.right, var_dict, 0)
        return code_string + "movs    " + var_dict[node.left.name] + ", r0\n"

        ldr     r3, [r7, #12]
        cmp     r3, #29
        bgt     .L2


def compileLoop(node: AST_Loop, var_dict, depth, count):
    if isinstance(node.condition, AST_RelationalOperators):
        operator_string = ""
        passable_par1 = ""
        passable_par2 = ""
        if isinstance(node.condition.left, AST_Operator):
            calc_l = composeCalculation(node.condition.left, var_dict, 0)
            operator_string += calc_l
            passable_par1 = "r0"
        elif isinstance(node.condition.left, AST_Literal):
            passable_par1 = "#" + str(int(node.condition.left.value))
        elif isinstance(node.condition.left, AST_VariableReference):
            passable_par1 = var_dict[node.condition.left.name]

        if isinstance(node.condition.right, AST_Operator):
            calc_2 = composeCalculation(node.condition.right, var_dict, 0)
            operator_string += calc_2
            passable_par2 = "r1"
        elif isinstance(node.condition.right, AST_Literal):
            passable_par2 = "#" + str(int(node.condition.right.value))
        elif isinstance(node.condition.right, AST_VariableReference):
            passable_par2 = var_dict[node.condition.right.name]



        strings = "cmp     {}, {}\n" \
                  "{}     {}".format(passable_par1, passable_par2, comparator_operator_dict[node.condition.operator], label)#if its not good skip the loop
    elif isinstance(node.condition, AST_Bool):
        if node.condition.value:
            pass #do the loop until return
        else:
            pass #do not compile codeblock but give warning
    else:


    #create start loop label,
    #create condition
    #create codeblock



def count_variables(code_sequence: [AST_Node]) -> int:
    if len(code_sequence) == 0:
        return 0
    if isinstance(code_sequence[0], AST_AssignmentOperator):
        if isinstance(code_sequence[0].left, AST_Variable):
            return count_variables(code_sequence[1:]) + 1
    elif isinstance(code_sequence[0], (AST_Loop, AST_IfStatement)):
        return count_variables(code_sequence[0].CodeSequence) + count_variables(code_sequence[1:])
    return count_variables(code_sequence[1:])

def compileCodeBlock(code_sequence: [AST_Node], var_dict) -> str:
        if isinstance(code_sequence[0], AST_AssignmentOperator):
            val = compileAssignment()
        elif isinstance(code_sequence[0], AST_Loop):
            pass
        elif isinstance(code_sequence[0], AST_IfStatement):
            pass
        elif isinstance(code_sequence[0], AST_ReturnStatement):
            pass
        elif isinstance(code_sequence[0], AST_PrintFunctionCall):
            pass

def compile_return_statement(node, var_dict):


def startFunctionCodeBlock(func: AST_Function):
    var_count: int = count_variables(func.CodeSequence)
    var_value: int = var_count*4 if var_count%2 == 0 else (var_count+1)*4
    start_string = func.name + "()" +"\n"
    push_string = "push    {r5, r6, r7, r8, lr}\n"
    pop_string =  "pop     {r5, r6, r7, r8, pc}\n"
    var_string = "sub     sp, sp, #{}\nadd    r7, sp, #0".format(var_value)
    var_dict = {}
    code_string = compileCodeBlock(func.CodeSequence, var_dict)




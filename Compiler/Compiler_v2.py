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

comparator_subroutine_dict = {
    "<": "__smallerthan",
    ">": "__largerthan",
    "<=": "__smallerequals",
    ">=": "__largerequals",
    "!=": "__notequals",
    "==": "__equals()"
}



def getComparisonSubRoutines():
    subroutine_equals = "" \
                  "__equals():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    beq     .__equals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__equals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_notequals = "" \
                  "__notequals():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bne     .__notequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__notequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_smallerthen = "" \
                  "__smallerthan():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    blt     .__smallerthan_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__smallerthan_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_largerthen = "" \
                  "__largerthan():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bgt     .__largerthan_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__largerthan_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_smallerequals = "" \
                  "__smallerequals():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    ble     .__smallerequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__smallerequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_largerequals = "" \
                  "__largerequals():\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bge     .__largerequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  ".__largerequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    return subroutine_equals + subroutine_notequals +subroutine_smallerthen + subroutine_smallerequals + subroutine_largerthen + subroutine_largerequals





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


def getFreeReg(regs) -> int:
    if len(regs) == 0:
        return -12
    if not regs[0]:
        return 0
    else:
        return getFreeReg(regs[1:]) + 1


def getVariableRegs(amount, index=0) -> [bool]:
    if index == 11:
        return [False]
    if index == 7:
        return [True] + getVariableRegs(amount, index + 1)
    elif index < amount:
        return [True] + getVariableRegs(amount, index + 1)
    else:
        return [False] + getVariableRegs(amount, index + 1)


def formatCodeLine(operator, start_reg, value, value2=""):
    if value2 == "":
        value2 = "r{}".format(start_reg)
    str_this = ""
    if operator == '+':
        str_this =  "sub     r{}, {}, {}\n".format(start_reg, value2, value)
    elif operator == '-':
        str_this =  "sub     r{}, {}, {}\n".format(start_reg, value2, value)
    elif operator == '/':
        str_this += "push    {r4, r5, r6, r7}\n"
        str_this += "push    {r0, r1, r2, r3}\n"
        str_this += "mov     r0, {} \n".format(value2)
        str_this += "mov     r1, {}\n".format(value)
        str_this += "bl      __aeabi_idiv\n"
        str_this += "mov     r4, r0\n"
        str_this += "pop     {r0, r1, r2, r3}\n"
        str_this += "mov     r{}, r4\n".format(start_reg)
        str_this += "pop     {r4, r5, r6, r7}\n"
    elif operator == '*':
        str_this =  "mul     r{}, {}, {}\n".format(start_reg, value2, value)
    return str_this


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


def count_variables(code_sequence: [AST_Node]) -> int:
    if len(code_sequence) == 0:
        return 0
    if isinstance(code_sequence[0], AST_AssignmentOperator):
        if isinstance(code_sequence[0].left, AST_Variable):
            return count_variables(code_sequence[1:]) + 1
    elif isinstance(code_sequence[0], (AST_Loop, AST_IfStatement)):
        return count_variables(code_sequence[0].CodeSequence) + count_variables(code_sequence[1:])
    return count_variables(code_sequence[1:])


def compileCondition(condition: [AST_Node], var_dict, function_name, loop_count) -> str:
    return ""


def compileLoop(loop_node: AST_Loop, var_dict, function_name, loop_count) -> (str, int):
    loop_string = ""
    #start label
    loop_string += ".{}_{}:\n".format(function_name, loop_count)

    #evaluate condition
    loop_string += compileCondition(simplifyNode(loop_node.condition), var_dict, function_name, loop_count+1)

    #compile codeblock
    codeblock_string, count = compileCodeBlock(loop_node.CodeSequence, var_dict, function_name, loop_count+2)
    loop_string += codeblock_string

    #label for rest, to continue
    loop_string += ".{}_{}:\n".format(function_name, loop_count+1)
    return loop_string, loop_count + 2 + count


def compileIf(if_node: AST_Loop, var_dict, function_name, loop_count) -> (str, int):
    loop_string = ""
    # evaluate condition
    loop_string += compileCondition(simplifyNode(if_node.condition), var_dict, function_name, loop_count)

    # compile codeblock
    codeblock_string, count = compileCodeBlock(if_node.CodeSequence, var_dict, function_name, loop_count + 1)
    loop_string += codeblock_string

    # label for rest, to continue
    loop_string += ".{}_{}:\n".format(function_name, loop_count)
    return loop_string, loop_count + 1 + count


def compileCalculation(node, var_dict, reg_list, reg=0):
    if isinstance(node, AST_RelationalOperators):
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        reg_2 = getFreeReg(reg_list)
        reg_list[reg_2] = True
        left_str = compileCalculation(node.left, var_dict, reg_list, reg_1)
        right_str = compileCalculation(node.right, var_dict, reg_list, reg_2)
        comp_string = ""
        comp_string += "push    {r0, r1}\n"
        comp_string += "mov     r0, r{}\n".format(reg_1)
        comp_string += "mov     r1, r{}\n".format(reg_2)
        comp_string += "bl      {}\n".format(comparator_subroutine_dict[node.operator])
        comp_string += "mov     r0, r{}\n".format(reg_1)
        comp_string += "pop     {r0, r1}\n"
        comp_string += "mov     r{}, r{}\n".format(reg_1, reg)
        reg_list[reg_1] = False
        reg_list[reg_2] = False
    elif isinstance(node, AST_Operator):
        if isinstance(node.)
        return formatCodeLine(node.operator, reg, val_1, val_2)

def startCalculation


def compileAssignment(node, var_dict, reg_list) -> (str, dict, list):
    index = len(var_dict)-1
    if node.left.name not in var_dict:
        var_dict[node.left.name] = index * 4

    # calculate_right to assign to left
    reg = getFreeReg(reg_list)
    reg_list[reg] = True

    assign_string = compileCalculation()

    assign_string += "str     r{}, [r7, #{}]\n".format(reg, var_dict[node.left.name])
    reg_list[reg] = False
    return assign_string, var_dict, reg_list


def storeParameters(argumentlist, adress, index=0) -> (str, dict):
    if len(argumentlist) > 0:
        store_str = "str     r{}, [r7, #{}]\n".format(index, adress)
        string, var_dict = storeParameters(argumentlist[1:], adress+4, index)
        var_dict[argumentlist[0].name] = index*4
        return store_str + string, var_dict
    else:
        return "", {}




def compileCodeBlock(code_sequence: [AST_Node], var_dict, reg_list, function_name, loop_count = 0) -> str:
        if isinstance(code_sequence[0], AST_AssignmentOperator):
            val = compileAssignment()
        elif isinstance(code_sequence[0], AST_Loop):
            string, count = compileLoop(code_sequence[0], var_dict, function_name, loop_count)
            return string + compileCodeBlock(code_sequence[1:], var_dict, function_name, count)
        elif isinstance(code_sequence[0], AST_IfStatement):
            string, count = compileIf(code_sequence[0], var_dict, function_name, loop_count)
            return string + compileCodeBlock(code_sequence[1:], var_dict, function_name, count)
        elif isinstance(code_sequence[0], AST_ReturnStatement):
            pass
        elif isinstance(code_sequence[0], AST_PrintFunctionCall):
            pass


#todo if it turns out there are more than 4 parameters, they need to be fetched from the stack, and when calling another function with more then 4 parameters they need to be put on the stack!
def compileFunction(func: AST_Function):
    var_count: int = count_variables(func.CodeSequence)
    var_value: int = var_count*4 if var_count % 2 == 0 else (var_count+1)*4
    func_string = func.name + "()" +"\n"
    func_string += "push    {r5, r6, r7, r8, lr}\n"
    func_string += "pop     {r5, r6, r7, r8, pc}\n"
    func_string += "sub     sp, sp, #{}\n".format(var_value)
    func_string += "add     r7, sp, #0\n"
    store_string, var_dict = storeParameters(func.argumentList, var_value)
    func_string += store_string
    reg_list = getVariableRegs(len(func.argumentList))
    code_string = compileCodeBlock(func.CodeSequence, var_dict, reg_list, func.name)

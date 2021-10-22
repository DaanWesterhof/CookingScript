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
        if value2[0] == "#":
            str_this += "movs    r{}, {}\n".format(start_reg, value2)
        str_this +=  "add     r{}, {}, r{}\n".format(start_reg, value, start_reg)
    elif operator == '-':
        str_this =  "subs    r{}, {}, {}\n".format(start_reg, value, value2)
    elif operator == '/':
        str_this += "push    {r4, r5, r6, r7}\n"
        str_this += "push    {r0, r1, r2, r3}\n"
        if value[0] == "#":
            str_this += "movs    r0, {} \n".format(value)
        else:
            str_this += "mov     r0, {} \n".format(value)

        if value2[0] == "#":
            str_this += "movs    r1, {}\n".format(value2)
        else:
            str_this += "mov      r1, {}\n".format(value2)
        str_this += "bl      __aeabi_idiv\n"
        str_this += "mov     r4, r0\n"
        str_this += "pop     {r0, r1, r2, r3}\n"
        str_this += "mov     r{}, r4\n".format(start_reg)
        str_this += "pop     {r4, r5, r6, r7}\n"
    elif operator == '*':
        if value2[0] == "#":
            str_this += "movs    r{}, {}\n".format(start_reg, value2)
        str_this += "muls    r{}, {}, {}\n".format(start_reg, value, value2)
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
    else:
        return node



#todo add more space for storing function variables
def count_variables(ast_main, code_sequence: [AST_Node]) -> int:
    if len(code_sequence) == 0:
        return 0
    if isinstance(code_sequence[0], AST_AssignmentOperator):
        if isinstance(code_sequence[0].left, AST_List):
            if isinstance(code_sequence[0].right, AST_Integer):
                print("hey its a thing")
                return count_variables(ast_main, code_sequence[1:]) + code_sequence[0].right.value
            else:
                throw_error_compiletime("CompiledListsStatic", code_sequence[0].left.name)
        if isinstance(code_sequence[0].left, AST_FunctionVariable):
            return count_variables(ast_main, code_sequence[1:]) + len(ast_main.Functions[code_sequence[0].left.FunctionName].argumentList)
        elif isinstance(code_sequence[0].left, AST_Variable):
            return count_variables(ast_main, code_sequence[1:]) + 1
    elif isinstance(code_sequence[0], (AST_Loop, AST_IfStatement)):
        return count_variables(ast_main, code_sequence[0].CodeSequence) + count_variables(ast_main, code_sequence[1:])
    return count_variables(ast_main, code_sequence[1:])


def compileCondition(ast_main, condition: [AST_Node], var_dict, reg_list, funcvar_dict, function_name, loop_count) -> str:
    comp_str = ""
    if isinstance(condition, AST_RelationalOperators):
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        reg_2 = getFreeReg(reg_list)
        reg_list[reg_2] = True
        comp_str += compileCalculation(ast_main, condition.left, var_dict, reg_list, funcvar_dict, reg_1)
        comp_str += compileCalculation(ast_main, condition.right, var_dict, reg_list, funcvar_dict, reg_2)
        comp_str += "{}     r{}, r{}\n".format(comparator_operator_dict[condition.operator], reg_1, reg_2)
        reg_list[reg_1] = False
        reg_list[reg_2] = False
    else:
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        comp_str += compileCalculation(ast_main, condition.right, var_dict, reg_list, funcvar_dict, reg_1)
        comp_str += "beq     r{}, #0\n".format(reg_1)
        reg_list[reg_1] = False

    comp_str += "b       .{}_{}:\n".format(function_name, loop_count)
    return comp_str


def compileLoop(ast_main, loop_node: AST_Loop, var_dict, reg_list, funcvar_dict, function_name, loop_count) -> (str, int):
    var_dict_copy = var_dict
    funcvar_dict_copy = funcvar_dict
    loop_string = ""
    #start label
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count)

    #evaluate condition
    loop_string += compileCondition(ast_main, simplifyNode(loop_node.condition), var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count+1)

    #compile codeblock
    codeblock_string, count = compileCodeBlock(ast_main, loop_node.CodeSequence, var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count+2)
    loop_string += codeblock_string
    loop_string += "b    .{}_{}\n".format(function_name, loop_count)

    #label for rest, to continue
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count+1)
    return loop_string, count


def compileIf(ast_main, if_node: AST_Loop, var_dict, reg_list, funcvar_dict, function_name, loop_count) -> (str, int):
    loop_string = ""
    var_dict_copy = var_dict
    funcvar_dict_copy = funcvar_dict
    # evaluate condition
    loop_string += compileCondition(ast_main, simplifyNode(if_node.condition), var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count)

    # compile codeblock
    codeblock_string, count  = compileCodeBlock(ast_main, if_node.CodeSequence, var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count + 1)
    loop_string += codeblock_string

    # label for rest, to continue
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count)
    return loop_string, count


def compileCalculation(ast_main, node, var_dict, reg_list, funcvar_dict, reg=0):
    calc_string = ""

    if isinstance(node, AST_RelationalOperators):
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        reg_2 = getFreeReg(reg_list)
        reg_list[reg_2] = True
        calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, reg_1)
        calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, reg_2)
        calc_string += "push    {r0, r1}\n"
        calc_string += "mov     r0, r{}\n".format(reg_1)
        calc_string += "mov     r1, r{}\n".format(reg_2)
        calc_string += "bl      {}\n".format(comparator_subroutine_dict[node.operator])
        calc_string += "mov     r0, r{}\n".format(reg_1)
        calc_string += "pop     {r0, r1}\n"
        calc_string += "mov     r{}, r{}\n".format(reg_1, reg)
        reg_list[reg_1] = False
        reg_list[reg_2] = False
    elif isinstance(node, AST_Operator):
        #do left first
        reg_1 = -1
        reg_2 = -1
        if isinstance(node.left, AST_Literal):
            val_1 = "#{}".format(node.left.value)
        elif isinstance(node.left, AST_ListAcces):
            reg_1 = getFreeReg(reg_list)
            reg_list[reg_1] = True
            compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, reg_1)
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_VariableReference):
            reg_1 = getFreeReg(reg_list)
            reg_list[reg_1] = True
            calc_string += "ldr     r{}, [r7, #{}]\n".format(reg_1, var_dict[node.left.name])
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_FunctionCallExecution):
            reg_1 = getFreeReg(reg_list)
            reg_list[reg_1] = True
            calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, reg_1)
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_Operator):
            reg_1 = reg
            calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, reg_1)
            val_1 = "r{}".format(reg_1)

        if isinstance(node.right, AST_Literal):
            val_2 = "#{}".format(node.right.value)
        elif isinstance(node.right, AST_ListAcces):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, reg_2)
            val_1 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_VariableReference):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            calc_string += "ldr     r{}, [r7, #{}]\n".format(reg_2, var_dict[node.right.name])
            val_2 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_FunctionCallExecution):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, reg_2)
            val_2 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_Operator):
            if reg_1 == reg:
                reg_2 = getFreeReg(reg_list)
                reg_list[reg_2] = True
            else:
                reg_2 = reg
            calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, reg_2)
            val_2 = "r{}".format(reg_2)

        calc_string += formatCodeLine(node.operator, reg, val_1, val_2)

        if reg_1 >= 0 and reg_1 != reg:
            var_dict[reg_1] = False

        if reg_2 >= 0 and reg_2 != reg:
            var_dict[reg_2] = False

    elif isinstance(node, AST_ListAcces):
        reg2 = getFreeReg(reg_list)
        reg_list[reg2] = True
        assign_string = compileCalculation(ast_main, simplifyNode(node.node), var_dict, reg_list, funcvar_dict, reg2)
        assign_string += "muls    r{}, #4\n".format(reg2)
        assign_string += "add     r{}, #{}\n".format(reg2, var_dict[node.name])
        assign_string += "ldr     r{}, [r7, r{}]\n".format(reg, reg2)
        reg_list[reg2] = False
        calc_string += assign_string

    elif isinstance(node, AST_VariableReference):
        calc_string += "ldr     r{}, [r7, #{}]\n".format(reg, var_dict[node.name])

    elif isinstance(node, AST_Literal):
        calc_string += "movs    r{}, #{}\n".format(reg, int(node.value))
    elif isinstance(node, AST_FunctionCallExecution):
        put_reg = getFreeReg(reg_list[4:])+4
        reg_list[reg] = True

        calc_string += "push    {r0, r1, r2, r3}\n"
        calc_string += load_arguments_for_call(ast_main, node, var_dict, funcvar_dict)
        calc_string += "bl      {}()\n".format(funcvar_dict[node.name])
        calc_string += "mov     r{}, r0\n".format(put_reg)
        calc_string += "pop     {r0, r1, r2, r3}\n"
        calc_string += "mov     r{}, r{}\n".format(put_reg, reg)

        reg_list[reg] = False

    return calc_string


count = [0]
def store_function_arguments(ast_main, args, var_dict, reg_list, funcvar_dict, location, index = 0):
    if len(args.argument_nodes) == index:
        return ""
    reg = getFreeReg(reg_list)
    reg_list[reg] = True
    string = compileCalculation(ast_main, args.argument_nodes[index], var_dict, reg_list, funcvar_dict, reg)
    string += "str     r{}, [r7, #{}]\n".format(reg, location + index*4)
    reg_list[reg] = False
    string += store_function_arguments(ast_main, args, var_dict, reg_list, funcvar_dict, location, index+1)
    return string

def load_arguments_for_call(ast_main, node, var_dict, funcvar_dict, index=0):
    if len(ast_main.Functions[funcvar_dict[node.name]].argumentList) == index:
        return ""
    string = "ldr     r{}, [r7, #{}]\n".format(index, var_dict[node.name] + 4*index)
    return string + load_arguments_for_call(ast_main, node, var_dict, funcvar_dict, index+1)



def compileAssignment(ast_main, node, var_dict, reg_list, funcvar_dict) -> (str, dict, list):
    index = len(var_dict)-1
    size = 1

    if isinstance(node.left, (AST_Variable)):
        if node.left.type == type_dict["string"]:
            throw_error_compiletime("StringsCompile", node.left.name)

    if isinstance(node.left, AST_FunctionVariable):
        size = len(ast_main.Functions[node.left.FunctionName].argumentList)
    elif isinstance(node.left, AST_List):
        size = node.right.value
    if node.left.name not in var_dict:
        print(node.left.name)
        var_dict[node.left.name] = (var_dict['size'])
        var_dict['size'] = var_dict['size'] + (size*4)

    # calculate_right to assign to left

    if isinstance(node.left, AST_FunctionVariable):
        assign_string = store_function_arguments(ast_main, node.right, var_dict, reg_list, funcvar_dict, var_dict[node.left.name], 0)
        funcvar_dict[node.left.name] = node.left.FunctionName
    elif isinstance(node.left, AST_List):
        return "", var_dict, reg_list, funcvar_dict
    else:
        index = 0
        reg = getFreeReg(reg_list)
        reg_list[reg] = True

        if isinstance(node.left, AST_ListAcces):
            reg2 = getFreeReg(reg_list)
            reg_list[reg2] = True
            assign_string = compileCalculation(ast_main, simplifyNode(node.left.node), var_dict, reg_list, funcvar_dict, reg)
            assign_string += "muls    r{}, #4\n".format(reg)
            assign_string += "add     r{}, #{}\n".format(reg, var_dict[node.left.name])
            assign_string += compileCalculation(ast_main, simplifyNode(node.right), var_dict, reg_list, funcvar_dict, reg2)
            assign_string += "str     r{}, [r7, r{}]\n".format(reg2, reg)
            reg_list[reg2] = False
        else:
            assign_string = compileCalculation(ast_main, simplifyNode(node.right), var_dict, reg_list, funcvar_dict, reg)
            assign_string += "str     r{}, [r7, #{}]\n".format(reg, var_dict[node.left.name])
        reg_list[reg] = False

    return assign_string, var_dict, reg_list, funcvar_dict


def storeParameters(argumentlist, adress, index=0) -> (str, dict):
    if len(argumentlist) > 0:
        store_str = "str     r{}, [r7, #{}]\n".format(index, index*4)
        string, var_dict = storeParameters(argumentlist[1:], adress+4, index+1)
        var_dict[argumentlist[0].name] = index*4
        var_dict['size'] = var_dict['size'] + index*4
        return store_str + string, var_dict
    else:
        var_dict = {}
        var_dict['size'] = 0
        return "", var_dict

def compileReturn(ast_main, node: AST_ReturnStatement, var_dict, reg_list, funcvar_dict, function_name):
    calc = compileCalculation(ast_main, simplifyNode(node.value), var_dict, reg_list, funcvar_dict, 0)
    calc += "B       .__{}_return:\n".format(function_name)
    return calc




def compileCodeBlock(ast_main, code_sequence: [AST_Node], var_dict, reg_list, funcvar_dict, function_name, loop_count = 0) -> (str, int):
    if len(code_sequence) == 0:
        return "" , loop_count
    else:
        if isinstance(code_sequence[0], AST_AssignmentOperator):
            assign_string, var_dict, reg_list, funcvar_dict = compileAssignment(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict)
            block_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict,
                                             function_name, loop_count)
            return assign_string + block_string, count

        elif isinstance(code_sequence[0], AST_Loop):
            string, count = compileLoop(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            block_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, count)
            return string + block_string, count

        elif isinstance(code_sequence[0], AST_IfStatement):
            string, count = compileIf(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            block_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, count)
            return string + block_string, count

        elif isinstance(code_sequence[0], AST_ReturnStatement):
            string = compileReturn(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name)
            block_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            return string + block_string, count

        elif isinstance(code_sequence[0], AST_FunctionCallExecution):
            if isinstance(code_sequence[0], AST_PrintFunctionCall):
                string = load_arguments_for_call(ast_main, code_sequence[0], var_dict, funcvar_dict)
                string += "bl      {}()\n".format(funcvar_dict[code_sequence[0].name])
                block_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
                return string + block_string, count
            else:
                return compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
        else:
            return compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)


#todo if it turns out there are more than 4 parameters, they need to be fetched from the stack, and when calling another function with more then 4 parameters they need to be put on the stack!
def compileFunction(ast_main, func: AST_Function):
    var_count: int = count_variables(ast_main, func.CodeSequence)
    var_count += len(func.argumentList)
    var_value: int = var_count*4 if var_count % 2 == 0 else (var_count+1)*4
    func_string = func.name + "()" +"\n"
    func_string += "push    {r4, r5, r6, r7, r8, r9, r10, r11, lr}\n"

    func_string += "sub     sp, sp, #{}\n".format(var_value)
    func_string += "add     r7, sp, #0\n"
    store_string, var_dict = storeParameters(func.argumentList, var_value)
    funcvar_dict = {}
    func_string += store_string
    reg_list = getVariableRegs(0)
    f_str , loop_count = compileCodeBlock(ast_main, func.CodeSequence, var_dict, reg_list, funcvar_dict, func.name)
    func_string += f_str
    func_string += "\n.__{}_return:\n".format(func.name)
    func_string += "mov     sp, r7\n"
    func_string += "add     sp, sp, #{}\n".format(var_value)
    func_string += "pop     {r4, r5, r6, r7, r8, r9, r10, r11, pc}\n"
    return func_string


def compile(ast_main):
    for func in list(ast_main.Functions.values()):
        print(compileFunction(ast_main, func))

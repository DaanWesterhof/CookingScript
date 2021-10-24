from Parser.AST_Nodes import *
from Parser.Operators import *
from Definitions import *
from typing import *
from ErrorHandler.ErrorHandler import *

""" This Dictionairy helps with converting operators to assembly instructions

"""
comparator_operator_dict = {
    "<" : "bge",
    ">" : "ble",
    "<=": "bgt",
    ">=": "blt",
    "!=": "beq",
    "==": "bne"
}

""" This Dictionairy holds a label for each operator to look up wich function to call for wich operator

"""
comparator_subroutine_dict = {
    "<": "__smallerthan",
    ">": "__largerthan",
    "<=": "__smallerequals",
    ">=": "__largerequals",
    "!=": "__notequals",
    "==": "__equals()"
}


# printTokens :: [String]
def getComparisonSubRoutines() -> str:
    """ This function returns default labels for doing comparison operators

        Returns
        -------
        String
            Assembly code for functions that can be used for comparing in assembly
    """
    subroutine_equals = "" \
                  "__equals:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    beq     .__equals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__equals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_notequals = "" \
                  "\n__notequals:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bne     .__notequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__notequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_smallerthen = "" \
                  "\n__smallerthan:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    blt     .__smallerthan_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__smallerthan_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_largerthen = "" \
                  "\n__largerthan:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bgt     .__largerthan_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__largerthan_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_smallerequals = "" \
                  "\n__smallerequals:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    ble     .__smallerequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__smallerequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    subroutine_largerequals = "" \
                  "\n__largerequals:\n" \
                  "    push    {lr}\n" \
                  "    cmp     r0, r1\n" \
                  "    bge     .__largerequals_true\n" \
                  "    mov     r0, #0\n" \
                  "    pop     {pc}" \
                  "\n" \
                  "\n.__largerequals_true:\n" \
                  "    mov     r0, #1\n" \
                  "    pop     {pc}\n"

    return subroutine_equals + subroutine_notequals +subroutine_smallerthen + subroutine_smallerequals + subroutine_largerthen + subroutine_largerequals




# evaluate_operator :: [String] → AST_Literal → AST_Literal → AST_Integer
def evaluate_operator(operator: str, a: AST_Literal, b: AST_Literal) -> AST_Integer:
    """ This function evaluates the result of an operator

        Parameters
        ----------
        operator : String
            This is the operator to evaluate

        a : AST_Literal
            the left value to be evaluated

        b : AST_Literal
            the right value to be evaluated

        Returns
        -------
        AST_Integer
            Returns an integer value that can be used by the compiler
    """
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


# getFreeReg :: List[bool] → int
def getFreeReg(regs: List[bool]) -> int:
    """ This function returns a free register

        Parameters
        ----------
        regs : List[Int]
            A list of booleans that tell if a list is occupied
        Returns
        -------
        Int
            A free register
    """
    if len(regs) == 0:
        return -12
    if not regs[0]:
        return 0
    else:
        return getFreeReg(regs[1:]) + 1

# getVariableRegs :: int → int → List[bool]
def getVariableRegs(amount: int, index: int=0) -> List[bool]:
    """ This function returns a list of bools resembeling the registers of the cpu

        Parameters
        ----------
        amount : int
            the amount of registers

        index : int, optional
            the current register being created, default value = 0
        Returns
        -------
        List[Bool]
            A free register
    """
    if index == 11:
        return [False]
    if index == 7:
        return [True] + getVariableRegs(amount, index + 1)
    elif index < amount:
        return [True] + getVariableRegs(amount, index + 1)
    else:
        return [False] + getVariableRegs(amount, index + 1)

# formatCodeLine :: str → int → str → str → str
def formatCodeLine(operator: str, start_reg: int, value: str, value2: str="") -> str:
    """ This function returns a string of a formatted assembly calculation eg "a + b"

        Parameters
        ----------
        operator : String
            the operator to use in the calculation

        start_reg : Int
            The register that should contain the result

        value : String
            the left value of the calculation, should always be a register

        value2 : String, optional
            the right value of the register, can be a immidiat value or a register, default = ""

        Returns
        -------
        String
            A formatted calculation
    """

    if value2 == "":
        value2 = "r{}".format(start_reg)
    str_this = ""
    if operator == '+':
        if value2[0] == "#":
            str_this += "    movs    r{}, {}\n".format(start_reg, value2)
            value_2 = "r{}".format(start_reg)
        str_this +=  "    add     r{}, {}, {}\n".format(start_reg, value, value2)
    elif operator == '-':

        str_this =  "    sub     r{}, {}, {}\n".format(start_reg, value, value2)
    elif operator == '/':
        str_this += "    push    {r4, r5, r6, r7}\n"
        str_this += "    push    {r0, r1, r2, r3}\n"
        if value[0] == "#":
            str_this += "    movs    r0, {} \n".format(value)
        else:
            str_this += "    mov     r0, {} \n".format(value)

        if value2[0] == "#":
            str_this += "    movs    r1, {}\n".format(value2)
        else:
            str_this += "    mov      r1, {}\n".format(value2)
        str_this += "    bl      __aeabi_idiv\n"
        str_this += "    mov     r4, r0\n"
        str_this += "    pop     {r0, r1, r2, r3}\n"
        str_this += "    mov     r{}, r4\n".format(start_reg)
        str_this += "    pop     {r4, r5, r6, r7}\n"
    elif operator == '*':
        if value2[0] == "#":
            str_this += "    movs    r{}, {}\n".format(start_reg, value2)
            value2 = "r{}".format(start_reg)
        str_this += "    mul     r{}, {}, {}\n".format(start_reg, value, value2)
    return str_this


# simplifyNode :: AST_Node → AST_Node
def simplifyNode(node: AST_Node) -> AST_Node:
    """ This function evaluates a node to its simpelest version, to optimize for the compiler.
        It calculates everything that can be calculated on compile time

        Parameters
        ----------
        node : AST_Node
            The node we wish to simplify

        Returns
        -------
        AST_Node
            A simplified node
    """
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


# count_variables :: AST_Program →  List[AST_Node] →  int
def count_variables(ast_main: AST_Program, code_sequence: List[AST_Node]) -> int:
    """ This function counts the amount of variables created in the function, every list index is counted as 1 variable

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        code_sequence : List[AST_Node]
            A list of noces containing the code for the codeblock

        Returns
        -------
        int
            the amount of variables found in the codeblock including list size
    """
    if len(code_sequence) == 0:
        return 0
    if isinstance(code_sequence[0], AST_AssignmentOperator):
        if isinstance(code_sequence[0].left, AST_List):
            if isinstance(code_sequence[0].right, AST_Integer):
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


# compileCondition :: AST_Program →  AST_Node →  Dict[int] →  List[bool] →  Dict[str] →  str →  int →  str
def compileCondition(ast_main: AST_Program, condition: AST_Node, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str, loop_count: int) -> str:
    """ This function compiles a condition for a branch for a loop or if

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        condition : AST_Node
            The condition to be compiled

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        loop_count : Int
            A integer that tells how many loops or ifs exist in the function for label naming

        Returns
        -------
        String
            A string containing the compiled condition
    """
    comp_str = ""
    if isinstance(condition, AST_RelationalOperators):
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        reg_2 = getFreeReg(reg_list)
        reg_list[reg_2] = True
        comp_str += compileCalculation(ast_main, condition.left, var_dict, reg_list, funcvar_dict, function_name, reg_1)
        comp_str += compileCalculation(ast_main, condition.right, var_dict, reg_list, funcvar_dict, function_name, reg_2)
        comp_str += "    cmp    r{}, r{}\n".format(reg_1, reg_2)
        reg_list[reg_1] = False
        reg_list[reg_2] = False
    else:
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        comp_str += compileCalculation(ast_main, condition.right, var_dict, reg_list, funcvar_dict, function_name, reg_1)
        comp_str += "    cmp     r{}, #0\n".format(reg_1)
        reg_list[reg_1] = False

    comp_str += "    {}     .{}_{}\n".format(comparator_operator_dict[condition.operator], function_name, loop_count)
    return comp_str


# compileLoop :: AST_Program →  AST_Loop →  Dict[int] →  List[bool] →  Dict[str] →  str →  int →  (str, str, int)
def compileLoop(ast_main: AST_Program, loop_node: AST_Loop, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str, loop_count: int) -> (str, str, int):
    """ This function compiles a loop
        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        loop_node : AST_Loop
            The node of the loop to be compiled

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        loop_count : Int
            A integer that tells how many loops or ifs exist in the function for label naming

        Returns
        -------
        String
            A string containing the compiled loop
    """
    var_dict_copy = var_dict
    funcvar_dict_copy = funcvar_dict
    loop_string = ""
    #start label
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count)

    #evaluate condition
    loop_string += compileCondition(ast_main, simplifyNode(loop_node.condition), var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count+1)

    #compile codeblock
    codeblock_string, label_string, count = compileCodeBlock(ast_main, loop_node.CodeSequence, var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count+2)
    loop_string += codeblock_string
    loop_string += "    b       .{}_{}\n".format(function_name, loop_count)

    #label for rest, to continue
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count+1)
    return loop_string, label_string, count

# compileIf :: AST_Program →  AST_IfStatement →  Dict[int] →  List[bool] →  Dict[str] →  str →  int →  (str, str, int)
def compileIf(ast_main: AST_Program, if_node: AST_IfStatement, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str, loop_count: str) -> (str, str, int):
    """ This function compiles a if statement

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        if_node : AST_IfStatement
            The node of the loop to be compiled

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        loop_count : Int
            A integer that tells how many loops or ifs exist in the function for label naming

        Returns
        -------
        String
            A string containing the compiled if statement
    """
    loop_string = ""
    var_dict_copy = var_dict
    funcvar_dict_copy = funcvar_dict
    # evaluate condition
    loop_string += compileCondition(ast_main, simplifyNode(if_node.condition), var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count)

    # compile codeblock
    codeblock_string, label_string, count  = compileCodeBlock(ast_main, if_node.CodeSequence, var_dict_copy, reg_list, funcvar_dict_copy, function_name, loop_count + 1)
    loop_string += codeblock_string

    # label for rest, to continue
    loop_string += "\n.{}_{}:\n".format(function_name, loop_count)
    return loop_string, label_string, count

# load_reg_with_val :: int →  int →  int → str
def load_reg_with_val(reg: int, val: int, index: int=0) -> str:
    """ This function compiles code to load a value into a register

        Parameters
        ----------
        reg : int
            The register to fill

        val : int
            the value to fill the reg with

        index : int, optional
            the integer telling how many times it hass added a value to the register

        -------
        String
            A string containing the assembly of the code
    """
    if index == 0:
        if val > 255:
            string = "    movs    r{}, #{}\n".format(reg, 255)
            return string + load_reg_with_val(reg, val-255, index+1)
        else:
            string = "    movs    r{}, #{}\n".format(reg, val)
            return string
    else:
        if val > 124:
            string = "    add     r{}, #{}\n".format(reg, 124)
            return string + load_reg_with_val(reg, val-124, index+1)
        else:
            string = "    add     r{}, #{}\n".format(reg, val)
            return string


# compileCalculation :: AST_Program →  AST_Node →  Dict[int] →  List[bool] →  Dict[str] →  str →  int →  str
def compileCalculation(ast_main: AST_Program, node: AST_Node, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str, reg: int=0) -> str:
    """ This function compiles a calculation code line

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        node : AST_Node
            The node that should be compiled

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        reg : Int, optional
            The register that should contain the result of the calculation

        Returns
        -------
        String
            A string containing the compiled calculation
    """
    calc_string = ""

    if isinstance(node, AST_RelationalOperators):
        reg_1 = getFreeReg(reg_list)
        reg_list[reg_1] = True
        reg_2 = getFreeReg(reg_list)
        reg_list[reg_2] = True
        calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, function_name, reg_1)
        calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, function_name, reg_2)
        calc_string += "    push    {r0, r1}\n"
        calc_string += "    mov     r0, r{}\n".format(reg_1)
        calc_string += "    mov     r1, r{}\n".format(reg_2)
        calc_string += "    bl      {}\n".format(comparator_subroutine_dict[node.operator])
        calc_string += "    mov     r0, r{}\n".format(reg_1)
        calc_string += "    pop     {r0, r1}\n"
        calc_string += "    mov     r{}, r{}\n".format(reg_1, reg)
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
            compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, function_name, reg_1)
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_VariableReference):
            reg_1 = getFreeReg(reg_list)
            reg_list[reg_1] = True
            if var_dict[node.left.name] > 120:
                calc_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg_1, function_name, node.left.name)
                calc_string += "    ldr     r{}, [r7, r{}]\n".format(reg_1, reg_1)
            else:
                calc_string += "    ldr     r{}, [r7, #{}]\n".format(reg_1, var_dict[node.left.name])
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_FunctionCallExecution):
            reg_1 = getFreeReg(reg_list)
            reg_list[reg_1] = True
            calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, function_name, reg_1)
            val_1 = "r{}".format(reg_1)
        elif isinstance(node.left, AST_Operator):
            reg_1 = reg
            calc_string += compileCalculation(ast_main, node.left, var_dict, reg_list, funcvar_dict, function_name, reg_1)
            val_1 = "r{}".format(reg_1)

        if isinstance(node.right, AST_Literal):
            val_2 = "#{}".format(node.right.value)
        elif isinstance(node.right, AST_ListAcces):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, function_name, reg_2)
            val_1 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_VariableReference):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            if var_dict[node.right.name] > 120:
                calc_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg_2, function_name, node.right.name)
                calc_string += "    ldr     r{}, [r7, r{}]\n".format(reg_2, reg_2)
            else:
                calc_string += "    ldr     r{}, [r7, #{}]\n".format(reg_2, var_dict[node.right.name])
            val_2 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_FunctionCallExecution):
            reg_2 = getFreeReg(reg_list)
            reg_list[reg_2] = True
            calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, function_name, reg_2)
            val_2 = "r{}".format(reg_2)
        elif isinstance(node.right, AST_Operator):
            if reg_1 == reg:
                reg_2 = getFreeReg(reg_list)
                reg_list[reg_2] = True
            else:
                reg_2 = reg
            calc_string += compileCalculation(ast_main, node.right, var_dict, reg_list, funcvar_dict, function_name, reg_2)
            val_2 = "r{}".format(reg_2)

        calc_string += formatCodeLine(node.operator, reg, val_1, val_2)

        if reg_1 >= 0 and reg_1 != reg:
            var_dict[reg_1] = False

        if reg_2 >= 0 and reg_2 != reg:
            var_dict[reg_2] = False

    elif isinstance(node, AST_ListAcces):
        reg2 = getFreeReg(reg_list)
        reg_list[reg2] = True
        print(function_name)
        if node.name in get_var_names(ast_main.Functions[function_name]):
            assign_string = ""
            # get the location of the list
            if var_dict[node.name] > 120:
                assign_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg2, function_name, node.name)
                assign_string += "    ldr     r{}, [r7, r{}]\n".format(reg, reg2)
            else:
                assign_string += "    ldr     r{}, [r7, #{}]\n".format(reg, var_dict[node.name])

            # get index to reg
            assign_string += compileCalculation(ast_main, simplifyNode(node.node), var_dict, reg_list,
                                                funcvar_dict, function_name, reg2)

            reg3 = getFreeReg(reg_list)
            reg_list[reg3] = True
            assign_string += "    movs    r{}, #4\n".format(reg3)
            assign_string += "    mul     r{}, r{}\n".format(reg2, reg3)
            assign_string += "    add     r{}, r{}, r{}\n".format(reg2, reg2, reg)
            reg_list[reg3] = False

            assign_string += "    ldr     r{}, [r{}]\n".format(reg, reg2)

        else:
            assign_string = compileCalculation(ast_main, simplifyNode(node.node), var_dict, reg_list, funcvar_dict, function_name, reg2)
            assign_string += "    movs    r{}, #4\n".format(reg2)
            assign_string += "    mul     r{}, r{}\n".format(reg2, reg)
            if var_dict[node.name] > 120:
                assign_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg, function_name, node.name)
                assign_string += "    add     r{}, r{}\n".format(reg2, reg)
            else:
                assign_string += "    add     r{}, #{}\n".format(reg2, var_dict[node.name])

            assign_string += "    ldr     r{}, [r7, r{}]\n".format(reg, reg2)

        reg_list[reg2] = False
        calc_string += assign_string

    elif isinstance(node, AST_VariableReference):
        if var_dict[node.name] > 120:
            calc_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg, function_name, node.name)
            calc_string += "    ldr     r{}, [r7, r{}]\n".format(reg, reg)
        else:
            calc_string += "    ldr     r{}, [r7, #{}]\n".format(reg, var_dict[node.name])

    elif isinstance(node, AST_Literal):
        calc_string += load_reg_with_val(reg, int(node.value))
    elif isinstance(node, AST_FunctionCallExecution):
        put_reg = getFreeReg(reg_list[4:])+4
        reg_list[reg] = True

        calc_string += "    push    {r0, r1, r2, r3}\n"
        calc_string += load_arguments_for_call(ast_main, node, var_dict, funcvar_dict)
        calc_string += "    bl      {}\n".format(funcvar_dict[node.name])
        calc_string += "    mov     r{}, r0\n".format(put_reg)
        calc_string += "    pop     {r0, r1, r2, r3}\n"
        calc_string += "    mov     r{}, r{}\n".format(reg, put_reg)

        reg_list[reg] = False

    return calc_string


# store_function_arguments :: AST_Program → AST_Node → Dict[int] → List[bool] → Dict[str] → int → str → int → (str, Dict[int])
def store_function_arguments(ast_main: AST_Program, args: AST_ArgumentList, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], location: int, function_name: str, index: int=0) -> (str, Dict[int]):
    """ This function compiles code for storing values used in prepare for an functioncall

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        args : AST_ArgumentList
            The argumentlist that tells how many arguments are to be passed to the function

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        location : Int
            The location of the argumentlist on the stack

        function_name : String
            The name of the function currently being compiled

        index : Int, optional
            An int counting the amount of arguments already stored

        Returns
        -------
        String
            A string containing the assembly for stroring the arguments

        Dict[Int]
            A dictionairy that contains the locations of each variable on the stack
    """

    if len(args.argument_nodes) == index:
        return ""
    reg = getFreeReg(reg_list)
    reg_list[reg] = True
    string = compileCalculation(ast_main, args.argument_nodes[index], var_dict, reg_list, funcvar_dict, function_name, reg)
    string += "    str     r{}, [r7, #{}]\n".format(reg, int(location) + index*4)
    reg_list[reg] = False
    string += store_function_arguments(ast_main, args, var_dict, reg_list, funcvar_dict, location, function_name, index+1)
    return string


# load_arguments_for_call :: AST_Program → AST_Node → Dict[int] → Dict[str] → int → str
def load_arguments_for_call(ast_main: AST_Program, node: AST_Node, var_dict: Dict[int], funcvar_dict: Dict[str], index: int=0) -> str:
    """ This function compiles code for loading values stored in a function variable for a function call

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        node : AST_Node
            The node that should be compiled

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack


        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        index : Int, optional
            The register that should contain the result of the calculation

        Returns
        -------
        String
            A string containing the compiled condition
    """
    if len(ast_main.Functions[funcvar_dict[node.name]].argumentList) == index:
        return ""
    string = "    ldr     r{}, [r7, #{}]\n".format(index, var_dict[node.name] + 4*index)
    return string + load_arguments_for_call(ast_main, node, var_dict, funcvar_dict, index+1)

# get_var_names :: AST_Function → int → List[str]
def get_var_names(func: AST_Function, index=0) -> [str]:
    """ This function returns a list of strings containing the names of function argument variables

        Parameters
        ----------
        func : AST_Function
            The function of wich we want the variable names

        index : Int, optional
            The value that tells how many variables we have already gotten
        Returns
        -------
        List[String]
            A list of strings containing the variable names
    """
    if len(func.argumentList) == index:
        return []
    else:
        return [func.argumentList[index].name] + get_var_names(func, index +1)


# compileAssignment :: AST_Program → AST_AssignmentOperator → Dict[int] → List[bool] → Dict[str] → str → (str, str, Dict[Int], List[Bool], Dict[String])
def compileAssignment(ast_main: AST_Program, node: AST_AssignmentOperator, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str) -> (str, str, Dict[int], List[bool], Dict[str]):
    """ This function compiles a calculation code line

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        node : AST_AssignmentOperator
            A node that resembles a variable assignment

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        Returns
        -------
        String
            A string that contains the assembly for the assignment
        String
            A string containing possible assembly labels that need to be created
        Dict[Int]
            A dictionary containing the locations of variables on the stack
        List[Bool]
            A list of booleans representing registers
        Dict[String]
            A dictionairy containing the function names that are linked to a variable function
    """
    index = len(var_dict)-1
    size = 1
    label_string = ""
    if isinstance(node.left, (AST_Variable)):
        if node.left.type == type_dict["string"]:
            throw_error_compiletime("StringsCompile", node.left.name)

    if isinstance(node.left, AST_FunctionVariable):
        size = len(ast_main.Functions[node.left.FunctionName].argumentList)
    elif isinstance(node.left, AST_List):
        size = node.right.value
    if node.left.name not in var_dict:
        var_dict[node.left.name] = (var_dict['size'])
        var_dict['size'] = var_dict['size'] + (size*4)

        if var_dict[node.left.name] > 120:
            label_string += ".__{}__{}__sp:\n".format(function_name, node.left.name)
            label_string += "   .word    {}\n".format(var_dict[node.left.name])

    # calculate_right to assign to left



    if isinstance(node.left, AST_FunctionVariable):
        assign_string = store_function_arguments(ast_main, node.right, var_dict, reg_list, funcvar_dict, var_dict[node.left.name], function_name, 0)
        funcvar_dict[node.left.name] = node.left.FunctionName
    elif isinstance(node.left, AST_List):
        return "", "", var_dict, reg_list, funcvar_dict
    else:
        index = 0
        reg = getFreeReg(reg_list)
        reg_list[reg] = True

        if isinstance(node.left, AST_ListAcces):
            reg2 = getFreeReg(reg_list)
            reg_list[reg2] = True
            if node.left.name in get_var_names(ast_main.Functions[function_name]):
                print("its in here")


                assign_string = ""
                #get the location of the list
                if var_dict[node.left.name] > 120:
                    assign_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg, function_name, node.left.name)
                    assign_string += "    ldr     r{}, [r7, r{}]\n".format(reg2, reg)
                else:
                    assign_string += "    ldr     r{}, [r7, #{}]\n".format(reg2, var_dict[node.left.name])

                #get index to reg
                assign_string += compileCalculation(ast_main, simplifyNode(node.left.node), var_dict, reg_list,
                                                   funcvar_dict, function_name, reg)

                reg3 = getFreeReg(reg_list)
                reg_list[reg3] = True
                assign_string += "    movs    r{}, #4\n".format(reg3)
                assign_string += "    mul     r{}, r{}\n".format(reg, reg3)
                assign_string += "    add     r{}, r{}, r{}\n".format(reg, reg, reg2)
                reg_list[reg3] = False


                assign_string += compileCalculation(ast_main, simplifyNode(node.right), var_dict, reg_list,
                                                    funcvar_dict, function_name, reg2)
                assign_string += "    str     r{}, [r{}]\n".format(reg2, reg)


            else:
                assign_string = compileCalculation(ast_main, simplifyNode(node.left.node), var_dict, reg_list, funcvar_dict, function_name, reg)
                assign_string += "    movs    r{}, #4\n".format(reg)
                assign_string += "    mul     r{}, r{}\n".format(reg, reg2)

                if var_dict[node.left.name] > 120:
                    assign_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg2, function_name, node.left.name)
                    assign_string += "    add     r{}, r{}\n".format(reg, reg2)
                else:
                    assign_string += "    add     r{}, #{}\n".format(reg, var_dict[node.left.name])

                assign_string += compileCalculation(ast_main, simplifyNode(node.right), var_dict, reg_list, funcvar_dict, function_name, reg2)
                assign_string += "    str     r{}, [r7, r{}]\n".format(reg2, reg)
            reg_list[reg2] = False
        else:
            assign_string = compileCalculation(ast_main, simplifyNode(node.right), var_dict, reg_list, funcvar_dict, function_name, reg)
            if var_dict[node.left.name] > 120:
                reg2 = getFreeReg(reg_list)
                reg_list[reg2] = True
                assign_string += "    ldr     r{}, .__{}__{}__sp\n".format(reg2, function_name, node.left.name)
                assign_string += "    str     r{}, [r7, r{}]\n".format(reg, reg2)
                reg_list[reg2] = False
            else:
                assign_string += "    str     r{}, [r7, #{}]\n".format(reg, var_dict[node.left.name])
        reg_list[reg] = False



    return assign_string, label_string, var_dict, reg_list, funcvar_dict

# storeParameters ::  List[AST_FunctionArgument] → int → int → (str, Dict[int])
def storeParameters(argumentlist: List[AST_FunctionArgument], adress: int, index: int=0) -> (str, dict):
    """ This function compiles code for storing parameters of a function

        Parameters
        ----------
        argumentlist : List[AST_FunctionArgument]
            A list containing arguments for a function

        adress: Int
            An int stroring the adress where the variable should be placed

        index: Int
            An int telling wich variable is being compiled

        Returns
        -------
        String
            A string containing the assembly for stroring the arguments

        Dict[Int]
            A dictionairy that contains the locations of each variable on the stack
    """
    if len(argumentlist) > 0:
        store_str = "    str     r{}, [r7, #{}]\n".format(index, index*4)
        string, var_dict = storeParameters(argumentlist[1:], adress+4, index+1)
        var_dict[argumentlist[0].name] = index*4
        var_dict['size'] = var_dict['size'] + 4
        return store_str + string, var_dict
    else:
        var_dict = {}
        var_dict['size'] = 0
        return "", var_dict


# compileReturn :: AST_Program → AST_ReturnStatement → Dict[int] → List[bool] → Dict[str] → str → str
def compileReturn(ast_main: AST_Program, node: AST_ReturnStatement, var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str) -> str:
    """ This function compiles a return statement

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        node : AST_AssignmentOperator
            A node that resembles a variable assignment

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        Returns
        -------
        String
            A string containing the assembly for returning a value from a function
    """
    calc = compileCalculation(ast_main, simplifyNode(node.value), var_dict, reg_list, funcvar_dict, function_name, 0)
    calc += "    B       .__{}_return\n".format(function_name)
    return calc



# compileCodeBlock :: AST_Program → List[AST_Node] → Dict[int] → List[bool] → Dict[str] → str → int → (str → str → int)
def compileCodeBlock(ast_main: AST_Program, code_sequence: List[AST_Node], var_dict: Dict[int], reg_list: List[bool], funcvar_dict: Dict[str], function_name: str, loop_count: int=0) -> (str, str, int):
    """ This function compiles a CodeBlock

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        code_sequence : List[AST_Node]
            A node that resembles a variable assignment

        var_dict : Dict[int]
            A dictionairy with the index values of a variable on the stack

        reg_list : List[Bool]
            A list of booleans that tell if a list is occupied

        funcvar_dict : Dict[String]
            A dictionairy containing the function names that are paired with a function variable

        function_name : String
            A string that tells the name of the current function being compiled

        loop_count : Int
            A integer that tells how many loops or ifs exist in the function for label naming


        Returns
        -------
        String
            A string containing the assembly for the codeblock

        String
            A string containing labels to store .words that are needed by the function

        Int
            A integer that keeps track how many loops and ifs are created so far
    """
    if len(code_sequence) == 0:
        return "", "", loop_count
    else:
        if isinstance(code_sequence[0], AST_AssignmentOperator):
            assign_string, label_string, var_dict, reg_list, funcvar_dict = compileAssignment(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name)
            block_string, leb_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict,
                                             function_name, loop_count)
            return assign_string + block_string, label_string + leb_string, count

        elif isinstance(code_sequence[0], AST_Loop):
            string, leb_string, count = compileLoop(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            block_string, label_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, count)
            return string + block_string, leb_string + label_string, count

        elif isinstance(code_sequence[0], AST_IfStatement):
            string, leb_string, count = compileIf(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            block_string, label_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, count)
            return string + block_string, leb_string + label_string, count

        elif isinstance(code_sequence[0], AST_ReturnStatement):
            string = compileReturn(ast_main, code_sequence[0], var_dict, reg_list, funcvar_dict, function_name)
            block_string, label_string, count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
            return string + block_string, label_string, count

        elif isinstance(code_sequence[0], AST_FunctionCallExecution):
            if isinstance(code_sequence[0], AST_PrintFunctionCall):
                string = load_arguments_for_call(ast_main, code_sequence[0], var_dict, funcvar_dict)
                string += "    bl      {}():\n".format(funcvar_dict[code_sequence[0].name])
                block_string, label_string ,count = compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
                return string + block_string, label_string, count
            else:
                return compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)
        else:
            return compileCodeBlock(ast_main, code_sequence[1:], var_dict, reg_list, funcvar_dict, function_name, loop_count)


#todo if it turns out there are more than 4 parameters, they need to be fetched from the stack, and when calling another function with more then 4 parameters they need to be put on the stack!
# compileFunction :: AST_Program → AST_Function → str
def compileFunction(ast_main: AST_Program, func: AST_Function) -> str:
    """ This function compiles a function

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        func : AST_Function
            The function that needs to be compiled

        Returns
        -------
        String
            A string containing the assembly version of the function

    """
    var_count: int = count_variables(ast_main, func.CodeSequence)
    var_count += len(func.argumentList)
    var_value: int = var_count*4 if var_count % 2 == 0 else (var_count+1)*4
    lab_string = ""

    if var_value > 500:
        lab_string += ".__{}__ssize:\n".format(func.name)
        lab_string += "   .word    -{}\n".format(var_value)
        lab_string += "   .word    {}\n\n".format(var_value)

    func_string = func.name  +":\n"
    func_string += "    push    {r4, r5, r6, r7, lr}\n"

    if var_value > 500:
        func_string += "    ldr     r7, .__{}__ssize\n".format(func.name)
        func_string += "    add     sp, sp, r7\n".format(var_value)
    else:
        func_string += "    sub     sp, sp, #{}\n".format(var_value)

    func_string += "    add     r7, sp, #0\n"
    store_string, var_dict = storeParameters(func.argumentList, var_value)
    funcvar_dict = {}
    func_string += store_string
    reg_list = getVariableRegs(0)
    f_str, label_string, loop_count = compileCodeBlock(ast_main, func.CodeSequence, var_dict, reg_list, funcvar_dict, func.name)
    func_string += f_str
    func_string += "\n.__{}_return:\n".format(func.name)
    func_string += "    mov     sp, r7\n"
    if var_value > 500:
        func_string += "    mov     r4, r0\n"
        func_string += "    ldr     r0, .__{}__ssize+4\n".format(func.name)
        func_string += "    add     sp, sp, r0\n".format(var_value)
        func_string += "    mov     r0, r4\n"
    else:
        func_string += "    add     sp, sp, #{}\n".format(var_value)

    func_string += "    pop     {r4, r5, r6, r7, pc}\n\n"
    func_string += lab_string
    func_string += label_string
    func_string += "\n\n\n"
    return func_string

# compileFunctions :: AST_Program → List[AST_Function] → str
def compileFunctions(ast_main: AST_Program, funcs: List[AST_Function]) -> str:
    """ This function compiles all functions in the ast

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        funcs : List[AST_Function]
            The functions that needs to be compiled

        Returns
        -------
        String
            A string containing the assembly version of the functions

    """
    if len(funcs) == 0:
        return ""
    return compileFunction(ast_main, funcs[0]) + compileFunctions(ast_main, funcs[1:])

# setGlobals :: List[AST_Function] → str
def setGlobals(funcs: List[AST_Function]):
    """ This function compiles all functions in the ast

        Parameters
        ----------
        funcs : List[AST_Function]
            The functions that needs to be declared in the assembly so they can be called

        Returns
        -------
        String
            A string containing assembly that exposes the functions

    """
    if len(funcs) == 0:
        return ""
    return "    .global {}\n".format(funcs[0].name) + setGlobals(funcs[1:])


# compileFunctions :: AST_Program → str → None
def compile(ast_main: AST_Program, target_file: str):
    """ This function Compiles the AST and outputs it to a targetfile

        Parameters
        ----------
        ast_main : AST_Program
            The main code tree of the program

        target_file : String
            The file that should contain the output of the program

    """
    compiled = ""
    compiled += "    .cpu cortex-m0\n"
    compiled += "    .align 4\n"
    compiled += "    .data\n"
    compiled += "    .text\n\n"
    compiled += setGlobals(list(ast_main.Functions.values()))
    compiled += "\n\n"
    compiled += getComparisonSubRoutines()
    compiled += "\n\n"
    compiled += compileFunctions(ast_main, list(ast_main.Functions.values()))

    file = open(target_file, 'w')
    file.write(compiled)


from Parser.AST_Nodes import *
from Parser.Operators import *
from Lexer.LEX_Tokens import *
from typing import *
import operator


# is_it_a_function :: LEX_Identifier → AST_Program → bool
def is_it_a_function(token: LEX_Identifier, ast_main: AST_Program) -> bool:
    """Checks if an identifier is known as a function

            Parameters
            ----------
            token : LEX_Identifier
                An identifier that might refer to a function

            ast_main : AST_Program
                The AST_Program that contains all previous declared functions

            Returns
            -------
            bool
                True if the identifier refers to a function else its false
    """
    if token in ast_main.Functions:
        return True
    return False


#todo make . a operator for functions and class values?
# parseCodeLine :: [LEX_Type] → LEX_Type → AST_Program → (str) → ([AST_Node], [AST_Operator], [LEX_Type])
def parseCodeLine(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> ([AST_Node], [AST_Operator], [LEX_Type]):
    """Parses a line of code to extract all values/nodes and operators into two lists

            Parameters
            ----------
            tokens : [LEX_Identifier]
                An identifier that might refer to a function

            last_token : LEX_Type
                The last lex token parsed by this function

            ast_main : AST_Program
                The AST_Program that contains all previous declared functions

            delimiters : Tuple[str, ...], optional
                A tuple containing the delemiters

            Returns
            -------
            tuple[list[AST_Node], list[AST_Operator], list[LEX_Type]]
                list[AST_Node]
                    A list of values/nodes that are not operators found in the code line

                list[AST_Operator]
                    A list of operators found in the code line

                list[LEX_Type]
                    A list of the remaining lex tokens

    """
    if tokens[0].value in delimiters:
        return [], [], tokens
    else:

        if isinstance(tokens[0], LEX_Operator):

            return tuple(map(operator.add, ([], [AST_OperatorExpression(tokens[0].value)], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
        if isinstance(tokens[0], LEX_RelationalOperator):
            return tuple(map(operator.add, ([], [AST_RelationalOperators(tokens[0].value)], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))

        elif isinstance(tokens[0], LEX_AssignmentOperator):
            return tuple(map(operator.add, ([], [AST_AssignmentOperator()], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
        elif tokens[0].value == "{":
            print(tokens[0])
            ls: AST_ArgumentList
            rest: [LEX_Type]
            ls, rest = parseArgumentList(tokens[1:], tokens[0], ast_main)
            return tuple(map(operator.add, ([ls], [], []), parseCodeLine(rest, rest[0], ast_main, delimiters)))

        elif isinstance(tokens[0], LEX_Identifier):
            if is_it_a_function(tokens[0], ast_main):
                return tuple(map(operator.add, ([], [], []),
                                 parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
            else:
                # its either a regular variable or a function bake or a list access
                if tokens[1].value == ".":  # its a bake
                    if len(tokens) > 5:
                        if tokens[2].value == "bake":
                            if tokens[3].value == "(" and tokens[4].value == ")":
                                f: AST_FunctionCallExecution = AST_FunctionCallExecution()
                                f.name = tokens[0].value
                                return tuple(map(operator.add, ([f], [], []), parseCodeLine(tokens[5:], tokens[0], ast_main, delimiters)))

                elif tokens[1].value == "[":  # its a list access
                    node: AST_Node
                    rest: [LEX_Type]
                    node, rest = getNodeFromLine(tokens[2:], tokens[1], ast_main, (']',))
                    var: AST_ListAcces = AST_ListAcces(tokens[0].value, node)
                    return tuple(map(operator.add, ([var], [], []), parseCodeLine(rest[1:], rest[0], ast_main, delimiters)))
                else:  # its a regular variable

                    return tuple(map(operator.add, ([AST_VariableReference(tokens[0].value)], [], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))

                #not sure how to handle this yet


        elif isinstance(tokens[0], LEX_Primitive):
            if tokens[0].subtype == "String":
                return tuple(map(operator.add, ([AST_String(tokens[0].value)], [], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))

            elif tokens[0].subtype == "Number":
                return tuple(map(operator.add, ([AST_Integer(int(tokens[0].value))], [], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
            elif tokens[0].subtype == "Bool":
                if tokens[0].value == true_keyword:
                    return tuple(map(operator.add, ([AST_Integer(True)], [], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
                elif tokens[0].value == false_keyword:
                    return tuple(map(operator.add, ([AST_Integer(False)], [], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
        elif isinstance(tokens[0], LEX_Keyword):
            if tokens[0].value == "prepare":
                if tokens[1].value == "(":
                    val: AST_ArgumentList
                    rest: [LEX_Type]
                    val, rest = parseArgumentList(tokens[2:], tokens[1], ast_main)
                    return tuple(map(operator.add, ([val], [], []), parseCodeLine(rest, rest[0], ast_main, delimiters)))
            else:
                return tuple(
                    map(operator.add, ([], [], []), (parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters))))

        else:
            return tuple(map(operator.add, ([], [], []), (parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters))))


#equal: left goes left in right
#left > right: left goes left in right
#right > left: right goes right in left

# putInPlace :: AST_Operator → AST_Operator → AST_Operator
def putInPlace(left: AST_Operator, right: AST_Operator) -> AST_Operator:
    """Parses a line of code to extract all values/nodes and operators into two lists

            Parameters
            ----------
            left : AST_Operator
                An operator that is on the left of the right operator on the line of code

            right : AST_Operator
                An operator that is on the right of the left operator on the line of code

            Returns
            -------
            AST_Operator
                An operator that has either the left or right operator as a leaf
    """
    if left.value >= right.value:
        if right.left is not None:
            right.left = putInPlace(left, right.left)
            return right
        elif right.left is None:
            right.left = left
            return right
    elif left.value < right.value:
        if left.right is not None:
            left.right = putInPlace(left.right, right)
            return left
        elif left.right is None:
            left.right = right
            return left


# putValue :: AST_Node → AST_Operator → (Bool, AST_Operator)
def putValue(value: AST_Node, node: AST_Operator) -> (bool, AST_Operator):
    """Fills an operator tree with values, starting with the left most free spot.
     If the spot is taken it moves to 1 spot on the right

            Parameters
            ----------
            value : AST_Node
                The value that needs to be placed in the operator tree

            node : AST_Operator
                The operator in which the value is to be placed

            Returns
            -------
            tuple[bool, AST_Operator]
                Bool:
                    True if the value was successfully placed in the operator
                AST_Operator:
                    The operator containing the value if operation was successful

    """
    if node.left is None: #we can put it left
        node.left = value
        return True, node

    elif isinstance(node.left, AST_Operator): #we can put it in an operator to the left
        res: bool
        returned_node: AST_Operator
        res, returned_node = putValue(value, node.left)
        if res:
            node.left = returned_node
            return True, node
        else:
            if node.right is None:
                node.right = value
                return True, node
            elif isinstance(node.right, AST_Operator):
                res, returned_node = putValue(value, node.right)
                if res:
                    node.right = returned_node
                    return True, node
        return False, AST_Operator("Dummy")

    elif not isinstance(node.left, AST_Operator) and not isinstance(node.left, AST_AssignmentOperator):  # we cant put it left as its not an operator
        if node.right is None:
            node.right = value
            return True, node

        elif isinstance(node.right, AST_Operator):  # we can put it in an operator to the left
            res: bool
            returned_node: AST_Operator
            res, returned_node = putValue(value, node.right)
            if res:
                node.right = returned_node
                return True, node
        return False, AST_Operator("Dummy")

    else:
        return False, AST_Operator("Dummy")


# construct :: [AST_Operator] → AST_Operator
def construct(OperatorList: [AST_Operator]) ->AST_Operator:
    """ Puts all operators together into one tree

            Parameters
            ----------
            OperatorList : [AST_Operator]
                The list of operators that will be put together into 1 tree

            Returns
            -------
            AST_Operator:
                A tree of operators

    """
    if len(OperatorList) == 1:
        return OperatorList[0]
    else:
        return putInPlace(OperatorList[0], construct(OperatorList[1:]))


# fill :: [AST_Node] → AST_Operator → AST_Operator
def fill(values: [AST_Node], node: AST_Operator) -> AST_Operator:
    """ Fills the operator tree with values

            Parameters
            ----------
            values : [AST_Node]
                A list of values that have to be placed in the operator tree

            Returns
            -------
            AST_Operator:
                A tree of operators where all non operator leaves are filled with values

    """
    if len(values) == 0:
        return node
    else:
        res: bool
        filled: AST_Operator
        res, filled = putValue(values[-1], fill(values[:-1], node))
        return filled


# getNodeFromLine :: [LEX_Type] → LEX_Type  → AST_Program → (str) → (AST_Operator, [LEX_Type])
def getNodeFromLine(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> (AST_Operator, [LEX_Type]):
    """ Parses a line of code and creates a runnable operator tree with the values found

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens wich can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            delimiters : Tuple[str, ...], optional
                The delimiters used to determine the end of the code line (the default is ('\n',)), which is a line end)

            Returns
            -------
            tuple[AST_Operator, list[LEX_Type]
                AST_Operator
                    A tree of operators where all non operator leaves are filled with values
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    values: [AST_Node]
    ops: [AST_Operator]
    rest: [LEX_Type]
    values, ops, rest = parseCodeLine(tokens, last_token, ast_main, delimiters)
    if len(values) == 1 and len(ops) == 0:
        return values[0], rest
    elif len(ops) == 0 and len(values) == 0:
        return None, rest
    op: AST_Operator = fill(values, construct(ops))
    return op, rest

# parseArgumentList :: [LEX_Type] → LEX_Type  → AST_Program → (AST_ArgumentList, [LEX_Type])
def parseArgumentList(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_ArgumentList, [LEX_Type]):
    """ Parses the arguments given to a function and creates an argument list

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens wich can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_ArgumentList, list[LEX_Type]
                AST_ArgumentList
                    An ArgumentList object containing all nodes/arguments passed to a function
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == ')' or last_token.value == '}':
        return AST_ArgumentList(), tokens
    elif last_token.value == '(' or last_token.value == ',' or last_token.value == '{':
        op: AST_Operator
        rest: [LEX_Type]
        op, rest = getNodeFromLine(tokens, last_token, ast_main, (',', ')', '}'))
        args: AST_ArgumentList
        toks: [LEX_Type]
        args, toks = parseArgumentList(rest[1:], rest[0], ast_main)
        args.argument_nodes.insert(0, op)
        return (args, toks)


# parseWeigh :: [LEX_Type] → LEX_Type  → AST_Program → (AST_IfStatement, [LEX_Type])
def parseWeigh(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_IfStatement, [LEX_Type]):
    """ Parses code until the done keyword to create a if statement code block

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_IfStatement, list[LEX_Type]
                AST_IfStatement
                    An AST_IfStatement object containing a condition and code
                    that is to be executed when the condition results in true
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "weigh":
        if tokens[0].value == "(":
            cond: AST_Operator
            rest: [LEX_Type]
            codeblock: [AST_Node]
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            ifs: AST_IfStatement = AST_IfStatement()
            ifs.CodeSequence = codeblock
            ifs.condition = cond
            return ifs, rest


# parseMix :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Loop, [LEX_Type])
def parseMix(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Loop, [LEX_Type]):
    """ Parses tokens until the done keyword to create a Loop code block

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_Loop, list[LEX_Type]
                AST_Loop
                    An AST_Loop object containing a condition and code
                    that is to be executed while the condition results in true
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "mix":
        if tokens[0].value == "(":
            cond: AST_Operator
            rest: [LEX_Type]
            codeblock: [AST_Node]
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            loop: AST_Loop = AST_Loop()
            loop.CodeSequence = codeblock
            loop.condition = cond
            return loop, rest


# parseStep :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Label, [LEX_Type])
def parseStep(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Label, [LEX_Type]): #todo this isnt actualy implemented in the runnen
    """ Parses tokens to create a label that can be used as a goto statement

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_Label, list[LEX_Type]
                AST_Label
                    An AST_Label object that can be jumped like a goto statement
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "Step":
        if isinstance(tokens[0], LEX_Numerical):
            node: AST_Label
            node = parseStep(tokens[1:], tokens[0], ast_main)
            node.label_number = tokens[0].value
            return node
    elif isinstance(last_token, LEX_Numerical):
        if isinstance(tokens[0], LEX_Other):
            if tokens[0].value == ":":
                return AST_Label(), tokens


# parseTaste :: [LEX_Type] → LEX_Type  → AST_Program → (AST_PrintFunctionCall, [LEX_Type])
def parseTaste(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_PrintFunctionCall, [LEX_Type]):
    """ Parses tokens to create a print function call

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_PrintFunctionCall, list[LEX_Type]
                AST_PrintFunctionCall
                    An AST_PrintFunctionCall object that will print its arguments to the terminal
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "taste":
        if tokens[0].value == "(":
            args: AST_ArgumentList
            lex_tokens: [LEX_Type]
            args, lex_tokens = parseArgumentList(tokens[1:], tokens[0], ast_main)
            return AST_PrintFunctionCall(args), lex_tokens


# parseServe :: [LEX_Type] → LEX_Type  → AST_Program → (AST_ReturnStatement, [LEX_Type])
def parseServe(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_ReturnStatement, [LEX_Type]):
    """ Parses tokens to create a AST_ReturnStatement, which is used to return values from a function

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_ReturnStatement, list[LEX_Type]
                AST_ReturnStatement
                    An AST_ReturnStatement object will return values from a function
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "serve":
        node: AST_ReturnStatement = AST_ReturnStatement()
        rest: [LEX_Type]
        node.value, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        return node, rest


# parseVariableCreation :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Variable, [LEX_Type])
def parseVariableCreation(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Variable, [LEX_Type]):
    """ Parses tokens to create a AST_Variable, which is used to declare a variable

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_Variable, list[LEX_Type]
                AST_Variable
                    An AST_Variable object will declare a variable in the running context
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if isinstance(last_token, LEX_Types):

        if isinstance(tokens[0], LEX_Identifier):
            if last_token.value == "groceries":
                var = AST_List()
                var.name = tokens[0].value
                var.type = last_token.value
                vals: [AST_Node]
                ops: [AST_Operator]
                rest: [LEX_Type]
                vals, ops, rest = parseCodeLine(tokens[1:], tokens[0], ast_main, ('\n',))
                vals = [var] + vals
                return fill(vals, construct(ops)), rest
            else:
                var = AST_Variable()
                var.name = tokens[0].value
                var.type = last_token.value
                vals: [AST_Node]
                ops: [AST_Operator]
                rest: [LEX_Type]
                vals, ops, rest = parseCodeLine(tokens[1:], tokens[0], ast_main, ('\n',))
                vals = [var] + vals
                return fill(vals, construct(ops)), rest


# parseFunctionVariable :: [LEX_Type] → LEX_Type → AST_Program → (AST_FunctionVariable, [LEX_Type])
def parseFunctionVariable(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_FunctionVariable, [LEX_Type]):
    """ Parses tokens to create a AST_FunctionVariable, which is used to declare a variable

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_FunctionVariable, list[LEX_Type]
                AST_FunctionVariable
                    An AST_FunctionVariable object will declare a variable in the running context that is used to run a function
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value in ast_main.Functions:
        if isinstance(tokens[0], LEX_Identifier):
            var = AST_FunctionVariable()
            var.name = tokens[0].value
            var.FunctionName = last_token.value
            vals: [AST_Node]
            ops: [AST_Operator]
            rest: [LEX_Type]
            vals, ops, rest = parseCodeLine(tokens[1:], tokens[0], ast_main, ('\n',))
            vals = [var] + vals
            return fill(vals, construct(ops)), rest


# createCodeBlock :: [LEX_Type] → LEX_Type → AST_Program → ([AST_Node], [LEX_Type])
def createCodeBlock(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> ([AST_Node], [LEX_Type]):
    """ Parses tokens to create a list of executable trees, that represent the code block in tree form

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[list[AST_Node], list[LEX_Type]
                list[AST_Node]
                    An list of nodes that can be evaluated by the runner to run the parsed program
                list[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if len(tokens) == 0 or tokens[0].value == "done": #or isinstance(tokens, LEX_CodeBlockEnd)
        return [], tokens
    elif isinstance(tokens[0], LEX_Keyword) and (tokens[0].value != "bake" or tokens[0].value != "prepare"):
        if tokens[0].value == "recipe" or tokens[0].value == "->":
            pass #todo fix this
        elif tokens[0].value == "weigh":
            node: AST_IfStatement
            rest: [LEX_Type]
            node, rest = parseWeigh(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "mix":
            node: AST_Loop
            rest: [LEX_Type]
            node, rest = parseMix(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "step":
            node: AST_Label
            rest: [LEX_Type]
            node, rest = parseStep(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "taste":
            node: AST_PrintFunctionCall
            rest: [LEX_Type]
            node, rest = parseTaste(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "serve":
            node: AST_ReturnStatement
            rest: [LEX_Type]
            node, rest = parseServe(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest

    elif isinstance(tokens[0], LEX_Types):
        node: AST_Variable
        rest: [LEX_Type]
        node, rest = parseVariableCreation(tokens[1:], tokens[0], ast_main)
        seq: [AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, node)
        return seq, rest
    elif tokens[0].value in ast_main.Functions: #todo gotta get this to work
        node: AST_FunctionVariable
        rest: [LEX_Type]
        node, rest = parseFunctionVariable(tokens[1:], tokens[0], ast_main)
        seq: [AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, node)
        return seq, rest
    elif isinstance(tokens[0], LEX_LineEnd):
        return createCodeBlock(tokens[1:], tokens[0], ast_main)
    else:
        node: AST_Operator
        rest: [LEX_Type]
        op, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        seq: [AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, op)
        return seq, rest

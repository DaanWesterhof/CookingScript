from Parser.AST_Nodes import *
from Parser.Operators import *
from Lexer.LEX_Tokens import *
from typing import *
from ErrorHandler.ErrorHandler import *
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


# todo make . a operator for functions and class values?
# parseCodeLine :: [LEX_Type] → LEX_Type → AST_Program → (str) → ([AST_Node], [AST_Operator], [LEX_Type])
def parseCodeLine(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> (List[AST_Node], List[AST_Operator], List[LEX_Type]):
    """Parses a line of code to extract all values/nodes and operators into two lists

            Parameters
            ----------
            tokens : List[LEX_Identifier]
                An identifier that might refer to a function

            last_token : LEX_Type
                The last lex token parsed by this function

            ast_main : AST_Program
                The AST_Program that contains all previous declared functions

            delimiters : Tuple[str, ...], optional
                A tuple containing the delemiters

            Returns
            -------
            tuple[List[AST_Node], List[AST_Operator], List[LEX_Type]]
                List[AST_Node]
                    A list of values/nodes that are not operators found in the code line

                List[AST_Operator]
                    A list of operators found in the code line

                List[LEX_Type]
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
            rest: List[LEX_Type]
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
                    rest: List[LEX_Type]
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
                    rest: List[LEX_Type]
                    val, rest = parseArgumentList(tokens[2:], tokens[1], ast_main)
                    if val.argument_nodes[0] is None:
                        throw_error("MissingParameters", last_token.file, last_token.line, tokens[0].value)
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
def construct(OperatorList: List[AST_Operator]) -> AST_Operator:
    """ Puts all operators together into one tree

            Parameters
            ----------
            OperatorList : List[AST_Operator]
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
def fill(values: List[AST_Node], node: AST_Operator) -> AST_Operator:
    """ Fills the operator tree with values

            Parameters
            ----------
            values : List[AST_Node]
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
def getNodeFromLine(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> (AST_Operator, List[LEX_Type]):
    """ Parses a line of code and creates a runnable operator tree with the values found

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens wich can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            delimiters : Tuple[str, ...], optional
                The delimiters used to determine the end of the code line (the default is ('\n',)), which is a line end)

            Returns
            -------
            tuple[AST_Operator, List[LEX_Type]
                AST_Operator
                    A tree of operators where all non operator leaves are filled with values
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    values: List[AST_Node]
    ops: List[AST_Operator]
    rest: List[LEX_Type]
    values, ops, rest = parseCodeLine(tokens, last_token, ast_main, delimiters)
    if len(values) == 1 and len(ops) == 0:
        return values[0], rest
    elif len(ops) == 0 and len(values) == 0:
        return None, rest
    op: AST_Operator = fill(values, construct(ops))
    return op, rest

# parseArgumentList :: [LEX_Type] → LEX_Type  → AST_Program → (AST_ArgumentList, [LEX_Type])
def parseArgumentList(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_ArgumentList, [LEX_Type]):
    """ Parses the arguments given to a function and creates an argument list

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens wich can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_ArgumentList, List[LEX_Type]
                AST_ArgumentList
                    An ArgumentList object containing all nodes/arguments passed to a function
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == ')' or last_token.value == '}':
        return AST_ArgumentList(), tokens
    elif last_token.value == '(' or last_token.value == ',' or last_token.value == '{':
        op: AST_Operator
        rest: List[LEX_Type]
        op, rest = getNodeFromLine(tokens, last_token, ast_main, (',', ')', '}'))
        args: AST_ArgumentList
        toks: List[LEX_Type]
        args, toks = parseArgumentList(rest[1:], rest[0], ast_main)
        args.argument_nodes.insert(0, op)
        return (args, toks)


# parseWeigh :: [LEX_Type] → LEX_Type  → AST_Program → (AST_IfStatement, [LEX_Type])
def parseWeigh(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_IfStatement, List[LEX_Type]):
    """ Parses code until the done keyword to create a if statement code block

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            tuple[AST_IfStatement, List[LEX_Type]
                AST_IfStatement
                    An AST_IfStatement object containing a condition and code
                    that is to be executed when the condition results in true
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "weigh":
        if tokens[0].value == "(":
            cond: AST_Operator
            rest: List[LEX_Type]
            codeblock: List[AST_Node]
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            if cond is None:
                throw_error("ExpectedAfter", last_token.file, last_token.line, "condition", last_token.value)
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            ifs: AST_IfStatement = AST_IfStatement()
            ifs.CodeSequence = codeblock
            ifs.condition = cond
            return ifs, rest
        else:
            throw_error("ExpectedAfterInstead", last_token.file, last_token.line, "(", last_token.value, tokens[0].value)


# parseMix :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Loop, [LEX_Type])
def parseMix(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Loop, List[LEX_Type]):
    """ Parses tokens until the done keyword to create a Loop code block

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_Loop, List[LEX_Type]
                AST_Loop
                    An AST_Loop object containing a condition and code
                    that is to be executed while the condition results in true
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "mix":
        if tokens[0].value == "(":
            cond: AST_Operator
            rest: List[LEX_Type]
            codeblock: List[AST_Node]
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            if cond is None:
                throw_error("ExpectedAfter", last_token.file, last_token.line, "condition", last_token.value)
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            loop: AST_Loop = AST_Loop()
            loop.CodeSequence = codeblock
            loop.condition = cond
            return loop, rest
        else:
            throw_error("ExpectedAfterInstead", last_token.file, last_token.line, "(", last_token.value, tokens[0].value)


# parseStep :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Label, [LEX_Type])
def parseStep(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Label, List[LEX_Type]): #todo this isnt actualy implemented in the runnen
    """ Parses tokens to create a label that can be used as a goto statement

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_Label, List[LEX_Type]
                AST_Label
                    An AST_Label object that can be jumped like a goto statement
                List[LEX_Type]
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
def parseTaste(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_PrintFunctionCall, List[LEX_Type]):
    """ Parses tokens to create a print function call

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_PrintFunctionCall, List[LEX_Type]
                AST_PrintFunctionCall
                    An AST_PrintFunctionCall object that will print its arguments to the terminal
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "taste":
        if tokens[0].value == "(":
            args: AST_ArgumentList
            lex_tokens: List[LEX_Type]
            args, lex_tokens = parseArgumentList(tokens[1:], tokens[0], ast_main)
            if args.argument_nodes[0] is None:
                throw_error("MissingParameters", last_token.file, last_token.line, last_token.value)
            return AST_PrintFunctionCall(args), lex_tokens
        else:
            throw_error("ExpectedAfterInstead", last_token.file, last_token.line, "(", last_token.value, tokens[0].value)


# parseServe :: [LEX_Type] → LEX_Type  → AST_Program → (AST_ReturnStatement, [LEX_Type])
def parseServe(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_ReturnStatement, List[LEX_Type]):
    """ Parses tokens to create a AST_ReturnStatement, which is used to return values from a function

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_ReturnStatement, List[LEX_Type]
                AST_ReturnStatement
                    An AST_ReturnStatement object will return values from a function
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value == "serve":
        node: AST_ReturnStatement = AST_ReturnStatement()
        rest: List[LEX_Type]
        node.value, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        if node.value is None:
            throw_error("ExpectedAfter", last_token.file, last_token.line, "ReturnValue", last_token.value)
        return node, rest


# parseVariableCreation :: [LEX_Type] → LEX_Type  → AST_Program → (AST_Variable, [LEX_Type])
def parseVariableCreation(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Variable, List[LEX_Type]):
    """ Parses tokens to create a AST_Variable, which is used to declare a variable

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_Variable, List[LEX_Type]
                AST_Variable
                    An AST_Variable object will declare a variable in the running context
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if isinstance(last_token, LEX_Types):

        if isinstance(tokens[0], LEX_Identifier):
            if last_token.value == "groceries":
                var = AST_List()
                var.name = tokens[0].value
                var.type = last_token.value
                vals: List[AST_Node]
                ops: List[AST_Operator]
                rest: List[LEX_Type]
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
        else:
            throw_error("ExpectedAfterInstead", tokens[0].file, tokens[0].line, last_token.value, "Identifier", tokens[0].type)


# parseFunctionVariable :: [LEX_Type] → LEX_Type → AST_Program → (AST_FunctionVariable, [LEX_Type])
def parseFunctionVariable(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_FunctionVariable, List[LEX_Type]):
    """ Parses tokens to create a AST_FunctionVariable, which is used to declare a variable

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[AST_FunctionVariable, List[LEX_Type]
                AST_FunctionVariable
                    An AST_FunctionVariable object will declare a variable in the running context that is used to run a function
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if last_token.value in ast_main.Functions:
        if isinstance(tokens[0], LEX_Identifier):
            var = AST_FunctionVariable()
            var.name = tokens[0].value
            var.FunctionName = last_token.value
            vals: List[AST_Node]
            ops: List[AST_Operator]
            rest: List[LEX_Type]
            vals, ops, rest = parseCodeLine(tokens[1:], tokens[0], ast_main, ('\n',))
            vals = [var] + vals
            return fill(vals, construct(ops)), rest
        else:
            throw_error("ExpectType", tokens[0].file, tokens[0].line, "Identifier", tokens[0].type)
    else:
        throw_error("UnknownFunction", last_token.file, last_token.line, last_token.value)



# createCodeBlock :: [LEX_Type] → LEX_Type → AST_Program → ([AST_Node], [LEX_Type])
def createCodeBlock(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (List[AST_Node], List[LEX_Type]):
    """ Parses tokens to create a list of executable trees, that represent the code block in tree form

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens which can be parsed

            last_token : LEX_Type
                The last token parsed by this function

            ast_main : AST_Program
                The root off the program tree containing all program information

            Returns
            -------
            Tuple[List[AST_Node], List[LEX_Type]
                List[AST_Node]
                    An list of nodes that can be evaluated by the runner to run the parsed program
                List[LEX_Type]
                    A list of the remaining lexer tokens

    """
    if len(tokens) == 0 or tokens[0].value == "done": #or isinstance(tokens, LEX_CodeBlockEnd)
        if len(tokens) == 0:
            throw_error("ExpectedBefore", last_token.file, last_token.line, "done", "EOF")
        return [], tokens
    elif isinstance(tokens[0], LEX_Keyword) and (tokens[0].value != "bake" or tokens[0].value != "prepare"):
        if tokens[0].value in non_code_keywords:
            throw_error_with_token("UnexpectedKeyword", tokens[0])
        elif tokens[0].value == "weigh":
            node: AST_IfStatement
            rest: List[LEX_Type]
            node, rest = parseWeigh(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "mix":
            node: AST_Loop
            rest: List[LEX_Type]
            node, rest = parseMix(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "step":
            node: AST_Label
            rest: List[LEX_Type]
            node, rest = parseStep(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "taste":
            node: AST_PrintFunctionCall
            rest: List[LEX_Type]
            node, rest = parseTaste(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "serve":
            node: AST_ReturnStatement
            rest: List[LEX_Type]
            node, rest = parseServe(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest

    elif isinstance(tokens[0], LEX_Types):
        node: AST_Variable
        rest: List[LEX_Type]
        node, rest = parseVariableCreation(tokens[1:], tokens[0], ast_main)
        seq: List[AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, node)
        return seq, rest
    elif isinstance(tokens[0], LEX_Identifier) and isinstance(tokens[1], LEX_Identifier):
        if tokens[0].value in ast_main.Functions: #todo gotta get this to work
            node: AST_FunctionVariable
            rest: List[LEX_Type]
            node, rest = parseFunctionVariable(tokens[1:], tokens[0], ast_main)
            seq: List[AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        else:
            throw_error("UnknownFunction", tokens[0].file, tokens[0].line, tokens[0].value)
    elif isinstance(tokens[0], LEX_LineEnd):
        return createCodeBlock(tokens[1:], tokens[0], ast_main)
    else:
        node: AST_Operator
        rest: List[LEX_Type]
        op, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        seq: List[AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, op)
        return seq, rest

from Parser.AST_Nodes import *
from Parser.Operators import *
from Lexer.LEX_Tokens import *
from typing import Tuple
import operator


def is_it_a_function(token: LEX_Identifier, ast_main: AST_Program, index=0):
    if len(ast_main.Functions) > index:
        if token.value == ast_main.Functions[index].name:
            return True
        else:
            is_it_a_function(token, ast_main, index+1)
    else:
        return False


def do_we_know_this_variable(token, codesequence:  AST_CodeSequence, index=0):
    if len(codesequence.Variables) > index:
        if token.name == codesequence.Variables[index].name:
            return True
        else:
            do_we_know_this_variable(token, codesequence, index+1)
    else:
        return False


# def found_identifier(tokens, last_token, ast_main):
#     if isinstance(last_token, LEX_Identifier):
#         if is_it_a_function(last_token, ast_main):
#
#         else:
#             #its either a variable, or a function call object
#             if isinstance(tokens[0], LEX_Other):
#                 #its a function call object
#                 return found_identifier(tokens[1:], tokens[0], ast_main)
#             else:
#                 #its a vairable:
#                 return AST_VariableReference(last_token)
#
#     elif isinstance(last_token, LEX_Other):
#         if isinstance(tokens[0], LEX_Keyword):
#             if tokens[0].value == "bake":
#                 return found_identifier(tokens[1:], tokens[0], ast_main)
#     elif isinstance(last_token, LEX_Keyword):
#         if last_token.value == "bake":
#             if isinstance(tokens[0], LEX_Bracket):
#                 if tokens[0].value == ')':
#                 return found_identifier(tokens[1:], tokens[0], ast_main)
#     elif isinstance(last_token, LEX_Bracket):
#         if isinstance(tokens[0], LEX_Bracket):
#             if last_token.value == '(' and tokens[0].value == ')':
#                 return AST_E


def parseCodeLine(tokens, last_token, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> ([AST_Node], [AST_Operator], [LEX_Type]):
    if tokens[0].value in delimiters:
        return [], [], tokens
    else:

        if isinstance(tokens[0], LEX_Operator):

            return tuple(map(operator.add, ([], [AST_OperatorExpression(tokens[0].value)], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
        if isinstance(tokens[0], LEX_RelationalOperator):
            return tuple(map(operator.add, ([], [AST_RelationalOperators(tokens[0].value)], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))

        elif isinstance(tokens[0], LEX_AssignmentOperator):
            return tuple(map(operator.add, ([], [AST_AssignmentOperator()], []), parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))

        elif isinstance(tokens[0], LEX_Identifier):
            if is_it_a_function(tokens[0], ast_main):
                return tuple(map(operator.add, ([], [], []),
                                 parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters)))
            else:
                #its either a regular variable or a function bake
                if tokens[1].value == ".":
                    if len(tokens > 5):
                        if tokens[2].value == "bake":
                            if tokens[3].value == "(" and tokens[4].value == ")":
                                f = AST_FunctionCall()
                                f.FunctionName = tokens[0].value
                                return tuple(map(operator.add, (f, [], []), parseCodeLine(tokens[5:], tokens[0], ast_main, delimiters)))
                    #its a bake
                else:
                    #its a regular variable
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
        else:

            return tuple(map(operator.add, ([], [], []), (parseCodeLine(tokens[1:], tokens[0], ast_main, delimiters))))


#equal: left goes left in right
#left > right: left goes left in right
#right > left: right goes right in left

def putInPlace(left, right) -> AST_Operator:
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


#todo it swaps stuff
def putValue(value, node: AST_Operator) -> (bool, AST_Operator):
    if node.left is None: #we can put it left
        node.left = value
        return True, node

    elif isinstance(node.left, AST_Operator): #we can put it in an operator to the left
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
            res, returned_node = putValue(value, node.right)
            if res:
                node.right = returned_node
                return True, node
        return False, AST_Operator("Dummy")

    else:
        return False, AST_Operator("Dummy")


def construct(OperatorList: [AST_Operator]) ->AST_Operator:
    if len(OperatorList) == 1:
        return OperatorList[0]
    else:
        return putInPlace(OperatorList[0], construct(OperatorList[1:]))


def fill(values: [AST_Node], node: AST_Operator) -> AST_Operator:
    if len(values) == 0:
        return node
    else:
        bool, filled = putValue(values[-1], fill(values[:-1], node))
        return filled


def getNodeFromLine(tokens, last_token, ast_main: AST_Program, delimiters: Tuple[str, ...]=('\n',)) -> (AST_Operator, [LEX_Type]):
    values, ops, rest = parseCodeLine(tokens, last_token, ast_main, delimiters)
    if len(values) == 1 and len(ops) == 0:
        return values[0], rest
    elif len(ops) == 0 and len(values) == 0:
        return None, rest
    op: AST_Operator = fill(values, construct(ops))
    return op, rest


def parseArgumentList(tokens, last_token, ast_main, functionContext=None) -> (AST_ArgumentList, [LEX_Type]):
    if last_token.value == ')':
        return AST_ArgumentList(), tokens
    elif last_token.value == '(' or last_token.value == ',':
        op, rest = getNodeFromLine(tokens, last_token, ast_main, (',', ')'))
        args: AST_ArgumentList
        toks: [LEX_Type]
        args, toks = parseArgumentList(rest[1:], rest[0], ast_main, functionContext)
        args.argument_nodes.insert(0, op)
        return (args, toks)



def parseWeigh(tokens, last_token, ast_main) -> (AST_IfStatement, [LEX_Type]):
    if last_token.value == "weigh":
        if tokens[0].value == "(":
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            ifs = AST_IfStatement()
            ifs.CodeSequence = codeblock
            ifs.condition = cond
            return ifs, rest


def parseMix(tokens, last_token, ast_main) -> (AST_Loop, [LEX_Type]):
    if last_token.value == "mix":
        if tokens[0].value == "(":
            cond, rest = getNodeFromLine(tokens[1:], tokens[0], ast_main, (')',))
            codeblock, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            lop = AST_Loop()
            lop.CodeSequence = codeblock
            lop.condition = cond
            return lop, rest

def parseStep(tokens: [LEX_Type], last_token: LEX_Type, ast_main) -> (AST_Label, [LEX_Type]):
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


def parseTaste(tokens, last_token, ast_main) -> (AST_PrintFunctionCall, [LEX_Type]):
    if last_token.value == "taste":
        if tokens[0].value == "(":
            args, lex_tokens = parseArgumentList(tokens[1:], tokens[0], ast_main)
            return AST_PrintFunctionCall(args), lex_tokens


def parseServe(tokens, last_token, ast_main) -> (AST_ReturnStatement, [LEX_Type]):
    if last_token.value == "serve":
        node: AST_ReturnStatement = AST_ReturnStatement()
        node.value, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        return node, rest

def parseVariableCreation(tokens, last_token, ast_main) -> (AST_Variable, [LEX_Type]):
    if isinstance(last_token, LEX_Types):
        if isinstance(tokens[0], LEX_Identifier):
            var = AST_Variable()
            var.name = tokens[0].value
            var.type = last_token.value
            vals, ops, rest = parseCodeLine(tokens[1:], tokens[0], ast_main, ('\n',))
            vals = [var] + vals
            return fill(vals, construct(ops)), rest





def check_if_function_without_variable(token: LEX_Type, ast_main: AST_Program):
    if isinstance(token, LEX_Identifier):
        return is_it_a_function(token, ast_main)
    return False



def createCodeBlock(tokens: [LEX_Type], last_token, ast_main: AST_Program) -> ([AST_Node], [LEX_Type]):
    if len(tokens) == 0 or tokens[0].value == "done": #or isinstance(tokens, LEX_CodeBlockEnd)
        return [], tokens
    elif isinstance(tokens[0], LEX_Keyword) and (tokens[0].value != "bake" or tokens[0].value != "prepare"):
        if tokens[0].value == "recipe" or tokens[0].value == "->":
            pass #todo fix this
        elif tokens[0].value == "weigh":
            node, rest = parseWeigh(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "mix":
            node, rest = parseMix(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "step":
            node, rest = parseStep(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "taste":
            node, rest = parseTaste(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest
        elif tokens[0].value == "serve":
            node, rest = parseServe(tokens[1:], tokens[0], ast_main)
            seq: [AST_Node]
            seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
            seq.insert(0, node)
            return seq, rest

    elif isinstance(tokens[0], LEX_Types):
        node, rest = parseVariableCreation(tokens[1:], tokens[0], ast_main)
        seq: [AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, node)
        return seq, rest
    elif check_if_function_without_variable(tokens[0], ast_main):
        pass #todo function object variable
    elif isinstance(tokens[0], LEX_LineEnd):
        return createCodeBlock(tokens[1:], tokens[0], ast_main)
    else:
        rest: [LEX_Type]
        op, rest = getNodeFromLine(tokens, last_token, ast_main, ('\n',))
        seq: [AST_Node]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.insert(0, op)
        return seq, rest

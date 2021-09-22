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


def parseCodeLine(tokens, last_token, delimiters: Tuple[str, ...]=(LEX_LineEnd('\n').type,)) -> ([AST_Node], [AST_Operator], [LEX_Type]):
    if tokens[0].type in delimiters:
        return [], AST_CodeSequence, tokens
    else:
        if isinstance(tokens[0], LEX_Operator):
            return tuple(map(operator.add, ([], [AST_OperatorExpression(tokens[0].value)], []), parseCodeLine(tokens[1:], tokens[0])))

        elif isinstance(tokens[0], LEX_AssignmentOperator):
            return tuple(map(operator.add, ([], [AST_AssignmentOperator()], []), parseCodeLine(tokens[1:], tokens[0])))

        elif isinstance(tokens[0], LEX_Identifier):
            pass

        elif isinstance(tokens[0], LEX_Primitive):
            if tokens[0].subtype == "String":
                return tuple(map(operator.add, ([AST_String(tokens[0].value)], [], []), parseCodeLine(tokens[1:], tokens[0])))

            elif tokens[0].subtype == "Number":
                return tuple(map(operator.add, ([AST_Integer(tokens[0].value)], [], []), parseCodeLine(tokens[1:], tokens[0])))
            elif tokens[0].subtype == "Bool":
                if tokens[0].value == true_keyword:
                    return tuple(map(operator.add, ([AST_Integer(True)], [], []), parseCodeLine(tokens[1:], tokens[0])))
                elif tokens[0].value == false_keyword:
                    return tuple(map(operator.add, ([AST_Integer(False)], [], []), parseCodeLine(tokens[1:], tokens[0])))


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


def putValue(value, node: AST_Operator) -> (bool, AST_Operator):
    if node.left is None: #we can put it left
        node.left = value
        return True, node

    elif isinstance(node.left, AST_Operator): #we can put it in an operator to the left
        res, returned_node = putValue(value, AST_Operator(node.left))
        if res:
            node.left = returned_node
            return True, node
        else:
            if node.right is None:
                node.right = value
                return True, node
            elif isinstance(node.right, AST_Operator):
                res, returned_node = putValue(value, AST_Operator(node.right))
                if res:
                    node.right = returned_node
                    return True, node
        return False, AST_Operator("Dummy")

    elif not isinstance(node.left, AST_Operator) and not isinstance(node.left, AST_AssignmentOperator):  # we cant put it left as its not an operator
        if node.right is None:
            node.right = value
            return True, node

        elif isinstance(node.right, AST_Operator):  # we can put it in an operator to the left
            res, returned_node = putValue(value, AST_Operator(node.left))
            if res:
                node.left = returned_node
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
        bool, filled = putValue(values[0], fill(values[1:], node))
        return filled


def parseArgumentList(tokens, last_token, ast_main, functionContext=None) -> (AST_ArgumentList, [LEX_Type]):
    if tokens[0].value == ')':
        return AST_ArgumentList(), tokens
    elif last_token.value == '(' or last_token.value == ',':
        values, ops, rest = parseCodeLine(tokens, last_token, (',', ')'))
        op: AST_Operator = fill(values, construct(ops))
        args: AST_ArgumentList
        toks: [LEX_Type]
        args, toks = parseArgumentList(toks[1:], toks[0], ast_main, functionContext)
        args.argument_nodes.insert(0, op)
        return args, toks



def parseWeigh(tokens, last_token, ast_main) -> AST_IfStatement:


def parseMix() -> AST_Loop:

def parseStep(tokens, last_token, ast_main) -> AST_Label:
    if last_token.value == "Step":
        node: AST_Label
        node = parseStep(tokens[2:], tokens[1], ast_main)
        node.label_number = tokens[1]
        return node

#def parseDone(tokens, last_token, ast_main) -> AST:

def parseTaste(tokens, last_token, ast_main) -> (AST_PrintFunctionCall, [LEX_Type]):
    if last_token.value == "Taste":
        if tokens[0].value == "(":
            args, lex_tokens = parseArgumentList(tokens[1:], tokens[0], ast_main)
            return AST_PrintFunctionCall(args), lex_tokens


def parseServe(tokens, last_token, ast_main) -> AST_ReturnStatement:


def createCodeBlock(tokens: [LEX_Type], last_token, ast_main: AST_Program) -> (AST_CodeSequence, [LEX_Type]):
    if len(tokens) == 0: #or isinstance(tokens, LEX_CodeBlockEnd)
        return AST_CodeSequence(), tokens
    elif isinstance(tokens[0], LEX_Keyword) and (tokens[0].value != "bake" or tokens[0].value != "prepare"):
        if tokens[0].value == "recipe" or tokens[0].value == "->":
            pass
        elif tokens[0].value == "Weigh":
            node, rest = parseWeigh(tokens[1:], tokens[0], ast_main)
        elif tokens[0].value == "Step":
            node, rest = parseStep(tokens[1:], tokens[0], ast_main)
        elif tokens[0].value == "taste":
            node, rest = parseTaste(tokens[1:], tokens[0], ast_main)
            
    else:
        nodes, ops, rest = parseCodeLine(tokens, last_token)
        seq: AST_CodeSequence
        rest: [LEX_Type]
        seq, rest = createCodeBlock(rest[1:], rest[0], ast_main)
        seq.code.append(fill(nodes, construct(ops)))
        return seq, rest
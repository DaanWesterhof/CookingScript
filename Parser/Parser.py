from Parser.AST_Nodes import *
from Lexer.LEX_Tokens import *
from Parser.Operators import *
import operator












# def createCodeBlock(tokens, last_token, ast_main: AST_Program, codesequence:  AST_CodeSequence) -> AST_CodeSequence:
#     if len(tokens) == 0:
#         return codesequence
#
#     elif tokens[0].value == "done":
#         return codesequence
#
#     else:
#         pass
#
#     if tokens[0].type == "Keyword":
#         pass
#     elif tokens[0].type == "Identifier":
#         if is_it_a_function(tokens[0], ast_main):
#             #return functioncall object
#             pass
#         elif do_we_know_this_variable(tokens[0], codesequence):
#             pass
#
#
#     elif tokens[0].type == "LineEnd":
#         pass
#
#     #we create a code block

def StartCodeBlockCreation(tokens, last_token, ast_main: AST_Program) -> AST_CodeSequence:
    code:  AST_CodeSequence= AST_CodeSequence()
    return createCodeBlock(tokens, last_token, ast_main, code)










def parseFromKeyword(tokens, last_token, ast_main):
    #its a new function
    if tokens[0].value == "recipe":
        #lets create a new function
        return parseFunction(tokens[1:], last_token, ast_main)
    elif tokens[0].value == "weigh":
        pass
    elif tokens[0].value == "mix":
        pass
    elif tokens[0].value == "taste":
        pass
    elif tokens[0].value == "serve":
        pass


    return 1, 2, 3

def parseFromIdentifier(tokens, last_token):
    pass
    #do we know the identifier?
        #yes
            #its a function
            #or
            #its a variable
                #we are asigning the variable
        #no
            #its a new variable



def recursiveParse(tokens, last_token, ast_main: AST_Program):
    if len(tokens) > 0:
        if tokens[0].type == "Keyword":
            item, rest_of_tokens, returned_token = parseFromKeyword(tokens[1:], tokens[0], ast_main)
            #if item.type == "Function":
                #ast_main.Functions.append(item)
            recursiveParse(rest_of_tokens, returned_token)


        recursiveParse(tokens[1:], ast_main)


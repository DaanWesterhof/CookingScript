from Parser.Parser import *
from Lexer.Lexer import *



def printTokens(tokens, index=0):
    if len(tokens) == 0:
        print("]")
        return
    if index == 0:
        print("[", end='')
        if tokens[0].type == "LineEnd":
            print("\\n", end='')
        else:
            print(tokens[0].value, end='')
        printTokens(tokens[1:], index+1)
    else:
        if tokens[0].type == "LineEnd":
            print(', ',"\\n", end='')
        else:
            print(', ', tokens[0].value, end='')
        printTokens(tokens[1:], index+1)

# these functions are used to split the list of tokens even more not based on spaces


# function verifies if a print statement is valid


def verifyPrint2(tokens):
    if tokens[0] == "(" and tokens[1] == '"' and tokens[3] == '"' and tokens[4] == ')':
        return tokens[5:], True, tokens[2]
    else:
        return tokens[1:], False, ""

# a recursive function that currently only checks for a printing keyword



token = lexer("main.cook")
printTokens(token)
#recursiveParse(token)

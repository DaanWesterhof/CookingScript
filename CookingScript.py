from Parser.Parser import *
from Lexer.Lexer import *
from Runner.Runner import *



def printTokens(tokens: [LEX_Type], index: int=0):
    # todo fix error check
    def print_items(args: [AST_Literal]):
        """ This function prints the passed arguments to the terminal

            Parameters
            ----------
            tokens : [AST_Literal]
                This is a list with lexed tokens that need to be print to the terminal

            index : int, optional
                this is used to know if it is the first time printing a token the default value = 0

        """
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


# a recursive function that currently only checks for a printing keyword
tokens: [LEX_Type] = lexer("main.cook")
#printTokens(tokens)
ast: AST_Program = AST_Program()
ast = recursiveParse(tokens, ast)
print(ast)
context: [running_context] = [running_context()]
executingCodeBlock(ast.CodeSequence, 0, ast, context)


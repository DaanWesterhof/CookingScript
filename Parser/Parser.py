from Parser.AST_Nodes import *
from Lexer.LEX_Tokens import *
from Parser.Operators import *
from Parser.ParseCodeBlock import *
from Parser.ParseFunction import *
import operator


def recursiveParse(tokens, last_token, ast_main: AST_Program):
    if len(tokens) > 0:
        if tokens[0].type == "Keyword":
            if tokens[0].value == "recipe":
                func, toks, rest = parseFunction(tokens[1:], tokens[0], ast_main)
                ast_main.Functions.append(func)
                return recursiveParse(toks, rest, ast_main)
            elif tokens[0].value == "start":
                if tokens[1].value == ":":

                    ast_main.CodeSequence, rest = createCodeBlock(tokens[2:], tokens[1], ast_main)
                    return ast_main
        else:
            return recursiveParse(tokens[1:], tokens[0], ast_main)
    else:
        return ast_main



from Parser.Operators import *
from Lexer.LEX_Tokens import *


def getFunctionArguments(tokens, last_token) -> ([AST_FunctionArgument], [LEX_Type]):
    if tokens[0].type == "LineEnd":
        if tokens[1].type == "Keyword":
            return [], tokens
        return getFunctionArguments(tokens[1:], last_token)
    if tokens[0].type == "ItemLister":
        if tokens[1].type == "Types":
            if tokens[2].type == "Identifier":
                arguments, last = getFunctionArguments(tokens[3:], last_token)
                return [AST_FunctionArgument(tokens[1].value, tokens[2].value)] + arguments, last


def parseFunction(tokens, last_token, ast_main: AST_Program):
    if last_token.value == "recipe":
        if tokens[0].type == "Identifier":
            func, rest_tokens, final_token = parseFunction(tokens[1:], tokens[0], ast_main)
            func.name = tokens[0].value
            if func.CodeSequence is None:
                print("no code in function, expected code after Bake:")
                exit()
            return func, rest_tokens, final_token
        else:
            print("missing_identifier")
            exit()
    elif last_token.type == "Identifier":
        if tokens[0].value == "->":
            if tokens[1].type == "Type":
                func, rest_tokens, final_token = parseFunction(tokens[2:], tokens[1], ast_main)
                func.ReturnType = tokens[1].value
                return func, rest_tokens, final_token
            else:
                print("expected return type")
                exit()
        else:
            print("expected \"->\" after identifier")
            exit()
    elif tokens[0].type == "Keyword":
        if tokens[0].value == "Prepare":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    arguments, rest_tokens = getFunctionArguments(tokens[2:], last_token)
                    func, rest_tokens, final_token = parseFunction(rest_tokens[1:], rest_tokens[0], ast_main)
                    func.argumentList = arguments
                    return func, rest_tokens, final_token
                else:
                    print("expected \":\" after \"Prepare\"")
                    exit()
        elif tokens[0].value == "Bake":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    code, rest_tokens, final_token = createCodeBlock(tokens[1:], tokens[0], ast_main)
                    func = AST_Function()
                    func.CodeSequence = code
                    return func, rest_tokens, final_token
                else:
                    print("expected \":\" after Bake")
                    exit()
            else:
                print("expected \"\\n\" before Bake")
                exit()
    else:
        return parseFunction(tokens[1:], tokens[0], ast_main)
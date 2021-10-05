from Parser.Operators import *
from Lexer.LEX_Tokens import *
from Parser.ParseCodeBlock import *


def getFunctionArguments(tokens : [LEX_Type], last_token : LEX_Type) -> ([AST_FunctionArgument], [LEX_Type]):
    """ Parsed lexer tokens to create a list of arguments that are expected by a function

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens that can be used to parse code

            last_token : LEX_Type
                The last token that has been parsed

            Returns
            -------
            tuple[list[AST_FunctionArgument], list[LEX_Type]]
                list[AST_FunctionArgument]
                    A list of function arguments expected by the function
                list[LEX_Type]
                    The remaining lexer tokens
    """
    if tokens[0].type == "LineEnd":
        if tokens[1].type == "Keyword":
            return [], tokens
        return getFunctionArguments(tokens[1:], last_token)
    if tokens[0].type == "ItemLister":
        if tokens[1].type == "Type":
            if tokens[2].type == "Identifier":
                arguments: [AST_FunctionArgument]
                last: [LEX_Type]
                arguments, last = getFunctionArguments(tokens[3:], last_token)
                return [AST_FunctionArgument(tokens[1].value, tokens[2].value)] + arguments, last


def parseFunction(tokens: [LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Function, [LEX_Type], LEX_Type):
    """ Parses tokens to create a function object after a recipe token has been found

            Parameters
            ----------
            tokens : [LEX_Type]
                A list of lexer tokens that can be used to parse code

            last_token : LEX_Type
                The last token that has been parsed

            ast_main : AST_Program
                The root node of the program tree containing all program information,
                this is used to be able to verify if an identifier refers to a function

            Returns
            -------
            tuple[AST_Function, list[LEX_Type], LEX_Type]
                AST_Function
                    An AST_Function node

                list[LEX_Type]
                    The remaining lexer tokens

                LEX_Type
                    The last parsed lexer token
    """
    if last_token.value == "recipe":
        if tokens[0].type == "Identifier":
            ast_main.Functions[tokens[0].value] = AST_Function()
            func: AST_Function
            rest_tokens: [LEX_Type]
            final_token: LEX_Type
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
                func: AST_Function
                rest_tokens: [LEX_Type]
                final_token: LEX_Type
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
        if tokens[0].value == "prepare":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    arguments: [AST_FunctionArgument]
                    rest_tokens: [LEX_Type]
                    arguments, rest_tokens = getFunctionArguments(tokens[2:], last_token)
                    func, rest_tokens, final_token = parseFunction(rest_tokens[1:], rest_tokens[0], ast_main)
                    func.argumentList = arguments
                    return func, rest_tokens, final_token
                else:
                    print("expected \":\" after \"Prepare\"")
                    exit()
        elif tokens[0].value == "bake":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    func: AST_Function = AST_Function()
                    code: [AST_Node]
                    rest_tokens: [LEX_Type]
                    code, rest_tokens = createCodeBlock(tokens[2:], tokens[1], ast_main)
                    func.CodeSequence = code
                    return func, rest_tokens[1:], rest_tokens[0]
                else:
                    print("expected \":\" after Bake")
                    exit()
            else:
                print("expected \"\\n\" before Bake")
                exit()
    else:
        return parseFunction(tokens[1:], tokens[0], ast_main)

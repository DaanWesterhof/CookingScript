from Parser.Operators import *
from Lexer.LEX_Tokens import *
from Parser.ParseCodeBlock import *
from ErrorHandler.ErrorHandler import *
from typing import *


# get_recipe_names :: [LEX_Type] → AST_Program → (AST_Program, [AST_Node])
def get_recipe_names(tokens: List[LEX_Type], ast_main: AST_Program) -> (AST_Program, List[LEX_Type]):
    """ This function checks the file for predifined recipes

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens that can be used to parse code

            ast_main : AST_Program
                The root node of the program

            Returns
            -------
            tuple[AST_Program, List[LEX_Type]]
                AST_Program
                    The root node of the program containing the new functions
                List[LEX_Type]
                    The remaining lexer tokens
    """
    if tokens[0].value == "done":
            return ast_main, tokens[1:]
    elif tokens[0].type == "ItemLister":
        if tokens[1].type == "Identifier":
            ast_main.Functions[tokens[1].value] = AST_Function()
            return get_recipe_names(tokens[2:], ast_main)
    else:
        return get_recipe_names(tokens[1:], ast_main)


# getFunctionArguments :: [LEX_Type] → LEX_Type → ([AST_FunctionArgument], [LEX_Type])
def getFunctionArguments(tokens: List[LEX_Type], last_token: LEX_Type) -> (List[AST_FunctionArgument], List[LEX_Type]):
    """ Parsed lexer tokens to create a list of arguments that are expected by a function

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens that can be used to parse code

            last_token : LEX_Type
                The last token that has been parsed

            Returns
            -------
            tuple[List[AST_FunctionArgument], List[LEX_Type]]
                list[AST_FunctionArgument]
                    A list of function arguments expected by the function
                List[LEX_Type]
                    The remaining lexer tokens
    """
    if tokens[0].type == "LineEnd":
        if tokens[1].type == "Keyword":
            return [], tokens
        return getFunctionArguments(tokens[1:], last_token)
    if tokens[0].type == "ItemLister":
        if tokens[1].type == "Type":
            if tokens[2].type == "Identifier":
                arguments: List[AST_FunctionArgument]
                last: List[LEX_Type]
                arguments, last = getFunctionArguments(tokens[3:], last_token)
                return [AST_FunctionArgument(tokens[1].value, tokens[2].value)] + arguments, last


# parseFunction :: [LEX_Type] → LEX_Type → AST_Program → (AST_Function, [LEX_Type], LEX_Type, AST_Program)
def parseFunction(tokens: List[LEX_Type], last_token: LEX_Type, ast_main: AST_Program) -> (AST_Function, List[LEX_Type], LEX_Type, AST_Program):
    """ Parses tokens to create a function object after a recipe token has been found

            Parameters
            ----------
            tokens : List[LEX_Type]
                A list of lexer tokens that can be used to parse code

            last_token : LEX_Type
                The last token that has been parsed

            ast_main : AST_Program
                The root node of the program tree containing all program information,
                this is used to be able to verify if an identifier refers to a function

            Returns
            -------
            tuple[AST_Function, List[LEX_Type], LEX_Type]
                AST_Function
                    An AST_Function node

                List[LEX_Type]
                    The remaining lexer tokens

                LEX_Type
                    The last parsed lexer token

                AST_Program
                    The program as we already create a dictionary location for the function is this function
    """
    if last_token.value == "recipe":
        if tokens[0].type == "Identifier":
            ast_main.Functions[tokens[0].value] = AST_Function()
            func: AST_Function
            rest_tokens: List[LEX_Type]
            final_token: LEX_Type
            func, rest_tokens, final_token, ast_main = parseFunction(tokens[1:], tokens[0], ast_main)
            func.name = tokens[0].value
            if func.CodeSequence is None:
                print("no code in function, expected code after Bake:")
                exit()
            return func, rest_tokens, final_token, ast_main
        else:
            throw_error_with_token("MissingIdentifier", tokens[0])
    elif last_token.type == "Identifier":
        if tokens[0].value == "->":
            if tokens[1].type == "Type":
                func: AST_Function
                rest_tokens: List[LEX_Type]
                final_token: LEX_Type
                func, rest_tokens, final_token, ast_main = parseFunction(tokens[2:], tokens[1], ast_main)
                func.ReturnType = tokens[1].value
                return func, rest_tokens, final_token, ast_main
            else:
                throw_error_with_token("ExpectedReturnType", tokens[1])
        else:
            throw_error_with_token("ExpectedArrow", tokens[0])
    elif tokens[0].type == "Keyword":
        if tokens[0].value == "prepare":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    arguments: List[AST_FunctionArgument]
                    rest_tokens: List[LEX_Type]
                    arguments, rest_tokens = getFunctionArguments(tokens[2:], last_token)
                    if len(arguments) == 0:
                        throw_error("ExpectedAfter", tokens[0].file, tokens[0].line, "FunctionArguments", tokens[0].value)
                    func, rest_tokens, final_token, ast_main = parseFunction(rest_tokens[1:], rest_tokens[0], ast_main)
                    func.argumentList = arguments
                    return func, rest_tokens, final_token, ast_main
                else:
                    throw_error("ExpectedAfter", tokens[0].file, tokens[0].line, ":", tokens[0].value)
            else:
                throw_error("ExpectedBefore", tokens[0].file, tokens[0].line, "LineEnd", tokens[0].value)
        elif tokens[0].value == "bake":
            if last_token.type == "LineEnd":
                if tokens[1].value == ":":
                    func: AST_Function = AST_Function()
                    code: List[AST_Node]
                    rest_tokens: List[LEX_Type]
                    code, rest_tokens = createCodeBlock(tokens[2:], tokens[1], ast_main)
                    func.CodeSequence = code
                    if len(code) == 0:
                        throw_error("CodeBlockEmpty", tokens[1].file, tokens[1].line, tokens[1].value)
                    return func, rest_tokens[1:], rest_tokens[0], ast_main
                else:
                    throw_error("ExpectedAfter", tokens[0].file, tokens[0].line, ":", tokens[0].value)
            else:
                throw_error("ExpectedBefore", tokens[0].file, tokens[0].line, "LineEnd", tokens[0].value)
    else:
        return parseFunction(tokens[1:], tokens[0], ast_main)

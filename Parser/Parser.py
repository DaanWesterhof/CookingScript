from Parser.AST_Nodes import *
from Lexer.LEX_Tokens import *
from Lexer.Lexer import *
from Parser.Operators import *
from Parser.ParseCodeBlock import *
from Parser.ParseFunction import *
import operator


# recursiveParse :: [LEX_Type] → AST_Program → AST_Program
def recursiveParse(tokens: [LEX_Type], ast_main: AST_Program, parseCodeBlock: bool=True) -> AST_Program:
    """Parsed the tokens provided into a runnable AST

                Parameters
                ----------
                tokens : [LEX_Type]
                    A list of LEX_Type tokens

                Returns
                -------
                AST_Program
                    A runnable AST containing all program data
        """
    if len(tokens) > 0:
        if tokens[0].type == "Keyword":
            if tokens[0].value == "recipe":

                func, toks, rest, ast_main = parseFunction(tokens[1:], tokens[0], ast_main)
                ast_main.Functions[func.name] = func
                return recursiveParse(toks, ast_main)
            elif tokens[0].value == "start" and parseCodeBlock:
                if tokens[1].value == ":":

                    ast_main.CodeSequence, rest = createCodeBlock(tokens[2:], tokens[1], ast_main)
                    return ast_main
            elif tokens[0].value == "cookbook":
                if isinstance(tokens[1], LEX_String):
                    ast_main = recursiveParse(lexer(tokens[1].value), ast_main, False)
                    return recursiveParse(tokens[2:], ast_main)
        else:
            return recursiveParse(tokens[1:], ast_main)
    else:
        return ast_main



from Parser.Parser import *
from Lexer.Lexer import *
from Runner.Runner import *
from Compiler.Compiler_v2 import *
import sys


# printTokens :: [LEX_Type] → int → None
def printTokens(tokens: List[LEX_Type], index: int=0):    # todo fix error check
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


# printTokens :: [String] → [running_context] → Int → [running_context]
def addCommandLineArguments(arguments: List[str], context: List[running_context], index: int=0) -> List[running_context]:
    """ This function adds commandline passed arguments to the running_context, so that these arguments can be accessed in the program

        Parameters
        ----------
        arguments : List[String]
            This is a list with the arguments given on the commandline

        context : List[running_context]
            This is a list of running_contexts, this stores the variables that are created

        index : Int, optional
            The index is used to check if we have parsed all items from the arguments, and is added to the name of the variable

        Returns
        -------
        List[running_context]
            It returns the context with the newly added variables based on the commandline arguments
    """
    if len(arguments) == 0:
        val: AST_Integer = AST_Integer(index)
        var: AST_Variable = AST_Variable()
        var.name = "$arglen"
        var.value = val
        var.type = "litre"
        context[0].variables["$arglen"] = var
        return context
    else:
        if arguments[0].lower() == "true" or arguments[0].lower() == true_keyword:
            val: AST_Bool = AST_Bool(True)
            var: AST_Variable = AST_Variable()
            var.name = "$arg" + str(index)
            var.value = val
            var.type = "egg"
            context[0].variables["$arg" + str(index)] = var
        elif arguments[0].lower() == "false" or arguments[0].lower() == false_keyword:
            val: AST_Bool = AST_Bool(False)
            var: AST_Variable = AST_Variable()
            var.name = "$arg" + str(index)
            var.value = val
            var.type = "egg"
            context[0].variables["$arg" + str(index)] = var
        elif arguments[0].isnumeric():
            val: AST_Integer = AST_Integer(int(arguments[0]))
            var: AST_Variable = AST_Variable()
            var.name = "$arg" + str(index)
            var.value = val
            var.type = "litre"
            context[0].variables["$arg" + str(index)] = var
        elif arguments[0].isalnum():
            print("we are adding a string")
            val: AST_String = AST_String(arguments[0])
            var: AST_Variable = AST_Variable()
            var.name = "$arg" + str(index)
            var.value = val
            var.type = "cheese"
            context[0].variables["$arg" + str(index)] = var

        return addCommandLineArguments(arguments[1:], context, index+1)


# a recursive function that currently only checks for a printing keyword
tokens: [LEX_Type] = lexer(sys.argv[1])
printTokens(tokens)
ast: AST_Program = AST_Program()
ast = recursiveParse(tokens, ast)
print(100*"=")
print(ast)
print(100*"=")
if sys.argv[2] == "compile":
    compile(ast, "compiled_cook.asm")
else:
    context: [running_context] = [running_context()]
    context = addCommandLineArguments(sys.argv[2:], context)
    executingCodeBlock(ast.CodeSequence, 0, ast, context)



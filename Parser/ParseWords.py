from Parser.AST_Nodes import *
from Parser.Operators import *

keywordDict = {
    "weigh": lambda: AST_IfStatement(),
    "serve": lambda: AST_ReturnStatement(),
    "taste": lambda: AST_Print(),
    "bake": lambda: AST_Execute(),
    "prepare": lambda: AST_Prepare(),
    "done": lambda: AST_DoneStatement(),
    "step": lambda: AST_Label()
}
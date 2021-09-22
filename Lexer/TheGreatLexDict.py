
from Lexer.LEX_Tokens import *


big_dict = {
    "recipe": lambda: LEX_Function(),
    "weigh": lambda: LEX_IfStatement(),
    "->": lambda: LEX_Arrow(),
    "serve": lambda: LEX_Return(),
    "taste": lambda: LEX_Print(),
    "bake": lambda: LEX_Execute(),
    "prepare": lambda: LEX_Prepare(),
    "done": lambda: LEX_Done(),
    "step": lambda: LEX_Label(),
    "liter": lambda: LEX_Numerical(),
    "milliliter": lambda: LEX_Numerical(),
    "eggs": lambda: LEX_Bool(),
    "cheese": lambda: LEX_String(),
    "<": lambda: LEX_BinairyOperator("<"),
    ">": lambda: LEX_BinairyOperator(">"),
    "==": lambda: LEX_BinairyOperator("=="),
    "<=": lambda: LEX_BinairyOperator("<="),
    ">=": lambda: LEX_BinairyOperator(">="),
    "!=": lambda: LEX_BinairyOperator("!="),
    "+": lambda: LEX_Operator("+"),
    "-": lambda: LEX_Operator("-"),
    "/": lambda: LEX_Operator("/"),
    "*": lambda: LEX_Operator("*"),
    ':': lambda: LEX_Other(':'),
    '"': lambda: LEX_Other('"'),
    ',': lambda: LEX_Other(','),
    '.': lambda: LEX_Other('.'),
}

"""
A list containing all keywords of the programing language
"""
keywordslist = [
    "recipe",
    "weigh",
    "mix",
    "->",
    "serve",
    "taste",
    "bake",
    "prepare",
    "done",
    "step",
    "start",
    "cookbook",
    "recipes"
]

"""
A list of keywords wich should not be found inside a code block
"""
non_code_keywords = [
    "recipe",
    "->",
    "start",
    "cookbook",
    "recipes"
]


"""
A list of all types supported by the programing language
"""
typeList = [
    "litre",
    "egg",
    "cheese",
    "groceries"
]

"""
A dictionairy converting basic python types to CookingScript types
"""
type_dict = {
    "int": "liter",
    "bool": "egg",
    "string": "cheese"
}

"""
A list of all resaltional operators supported by CookingScript
"""
RelationalOperator = [
    "<",
    ">",
    "==",
    "<=",
    ">=",
    "!="
]

"""
A list of all calculation operators supported by CookingScript
"""
operators = [
    "+",
    "-",
    "/",
    "*",
]

"""
A list of all level 1 operators
"""
operators_level1 = [
    "+",
    "-"
]

"""
A list of all level 2 operators
"""
operators_level2 = [
    "*",
    "/"
]


"""
A list containing all "other" type values
"""
otherList = [
    ':',
    '"',
    ',',
    '.',
    '->',
    '[',
    ']',
    '{',
    '}'
]

""" The keyword for True"""
true_keyword = "whole"
"""The keyword for false"""
false_keyword = "broken"
from Lexer.LEX_Tokens import *
from Definitions import *
import re


def validateForString(tokens: [str], last_token: str) -> bool:
    if len(tokens) > 1:
        if last_token == '"':
            if tokens[1] == '"':
                return True
    return False


def assignTypes(tokens: [str], last_token: str=None) -> [LEX_Type]:
    if len(tokens) == 0:
        return []
    if validateForString(tokens, last_token):
        return [LEX_String(tokens[0])] + assignTypes(tokens[2:], tokens[0])
    elif tokens[0] == '"':
        return assignTypes(tokens[1:], tokens[0])
    elif tokens[0] in keywordslist:
        return [LEX_Keyword(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] in typeList:
        return [LEX_Types(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == '=':
        return [LEX_AssignmentOperator(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == '-' and last_token == '\n':
        return [LEX_ItemLister(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] in "+-\*":
        return [LEX_Operator(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == '(' or tokens[0] == ')':
        return [LEX_Bracket(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] in RelationalOperator:
        return [LEX_RelationalOperator(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] in [':', ',', '.', '->']:
        return [LEX_Other(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == '\n':
        return [LEX_LineEnd(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0].isnumeric():
        return [LEX_Numerical(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == true_keyword or tokens[0] == false_keyword:
        return [LEX_Bool(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0].isalnum():
        return [LEX_Identifier(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    return assignTypes(tokens[1:], tokens[0])


def remove_useless(tokens: [str]) -> [str]:
    if len(tokens) == 0:
        return []
    else:
        if tokens[0] == '':
            return remove_useless(tokens[1:])
        else:
            return [tokens[0]] + remove_useless(tokens[1:])


def subsplit(tokens: [str]) -> [str]:
    if len(tokens) == 1:
        if tokens[0] == "->":
            return remove_useless([tokens[0]] + subsplit(tokens[1:]))
        else:
            return remove_useless(re.split('([\n:.,()+-/*"])', tokens[0]))
    else:
        if tokens[0] == "->":
            return remove_useless([tokens[0]] + subsplit(tokens[1:]))
        else:
            return remove_useless(re.split('([\n:.,()+-/*"])', tokens[0]) + subsplit(tokens[1:]))

# these functions are used to fix the strings during the lexing phase


def fixingString(tokens: [str]) -> [str]:
    if len(tokens) == 0:
        return []
    if tokens[0] != '"' and '\\' not in tokens[0]:
        if len(tokens) >= 2:
            x = fixingString(tokens[1:])
            if x[0] != '"':
                return [tokens[0] + x[0]] + x[1:]
            else:
                return [tokens[0]] + x
        else:
            return [tokens[0]] + fixingString(tokens[1:])
    elif tokens[0] == '"':
        return [tokens[0]] + fixStrings(tokens[1:])
    elif tokens[0] == "\\":
        if tokens[1] == '"':
            x = fixingString(tokens[2:])
            return ['"' + x[0]] + x[1:]
    elif "\\" in tokens[0]:
        if tokens[1] == '"':
            x = fixingString(tokens[2:])
            return [tokens[0][:-1] + '"' + x[0]] + x[1:]


def fixStrings(tokens: [str]) -> [str]:
    if len(tokens) > 0:
        if tokens[0] == '"':
            return [tokens[0]] + fixingString(tokens[1:])
        elif tokens[0] != " ":
            return [tokens[0]] + fixStrings(tokens[1:])
        else:
            return fixStrings(tokens[1:])
    else:
        return []

# these are the head tokanizer/lexer funtions, might put them together

def add_escaped_char(tokens):
    if len(tokens) > 1:
        return tokens[0], tokens[0]
    else:
        print("hey we were in the middle of a string and it ended?")


def fix_string(tokens) -> (str, [str]):
    if len(tokens) == 0 or tokens[0] == '"':
        return "", tokens
    elif tokens[0][-1] == '\\': #its an escape character
        char, rest = add_escaped_char(tokens[1:])
        string, rest = fix_string(rest[1:])
        return char + string, rest
    else:
        string, rest = fix_string(tokens[1:])
        return tokens[0] + string, rest


def fix_the_strings(tokens) -> [str]:
    if len(tokens) > 0:
        if tokens[0] == '"':
            string, rest = fix_string(tokens[1:])
            return [string] + fix_the_strings(rest[1:])
        elif tokens[0] == ' ':
            return fix_the_strings(tokens[1:])
        else:
            return [tokens[0]] + fix_the_strings(tokens[1:])
    else:
        return []




def tokanizer(input_str: str) -> [str]:
    val = subsplit(re.split("( )", input_str))
    return fixStrings(val)


def lexer(file_name: str) -> [LEX_Type]:
    f = open(file_name, "r")
    tokens = tokanizer(f.read())
    tokens = assignTypes(tokens)
    return tokens
from Lexer.LEX_Tokens import *
from Definitions import *
import re


# validateForString :: String → String → Bool
def validateForString(tokens: [str], last_token: str) -> bool:
    """ Checks if the current token is a string

            Parameters
            ----------
            tokens : [str]
                A list of strings

            last_token : str
                The last token that was lexed

            Returns
            -------
            bool
                True if the current token is a string
    """
    if len(tokens) > 1:
        if last_token == '"':
            if tokens[1] == '"':
                return True
    return False

# assignTypes :: [String] → String → [LEX_Type]
def assignTypes(tokens: [str], last_token: str=None) -> [LEX_Type]:
    """Assigns the right LEX_Type to the string and adds it to the list in the correct order

            Parameters
            ----------
            tokens : [str]
                A list of strings
            last_token : str, optional
                The last token that was assigned a type

            Returns
            -------
            list
                A list of tokens with the right types
        """
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
    elif tokens[0] in [':', ',', '.', '->', '[', ']', '{', '}']:
        return [LEX_Other(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == '\n':
        return [LEX_LineEnd(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0].isnumeric():
        return [LEX_Numerical(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0] == true_keyword or tokens[0] == false_keyword:
        return [LEX_Bool(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    elif tokens[0].isalnum() or (tokens[0][0] == '$' and tokens[0][1:].isalnum()):
        return [LEX_Identifier(tokens[0])] + assignTypes(tokens[1:], tokens[0])
    return assignTypes(tokens[1:], tokens[0])


# remove_useless :: [String] → [String]
def remove_useless(tokens: [str]) -> [str]:
    """Removes unwanted strings from the list

            Parameters
            ----------
            tokens : [str]
                A list of strings

            Returns
            -------
            list
                A list of strings
    """
    if len(tokens) == 0:
        return []
    else:
        if tokens[0] == '':
            return remove_useless(tokens[1:])
        else:
            return [tokens[0]] + remove_useless(tokens[1:])


# subsplit :: [String] → [String]
def subsplit(tokens: [str]) -> [str]:
    """Splits the list of strings into even smaller strings, based on a predifined set of delimiters
            Delimiters
            ----------
            [\n:.,()+-/*"]

            Parameters
            ----------
            tokens : [str]
                A list of strings

            Returns
            -------
            list
                A list of strings
    """
    if len(tokens) == 1:
        if tokens[0] == "->":
            return remove_useless([tokens[0]] + subsplit(tokens[1:]))
        else:
            return remove_useless(re.split('([\[\]\n:.,()+-/*"{}])', tokens[0]))
    else:
        if tokens[0] == "->":
            return remove_useless([tokens[0]] + subsplit(tokens[1:]))
        else:
            return remove_useless(re.split('([\[\]\n:.,()+-/*"{}])', tokens[0]) + subsplit(tokens[1:]))

# these functions are used to fix the strings during the lexing phase


# fixingString :: [String] → [String]
def fixingString(tokens: [str]) -> [str]:
    """Concatinates multiple strings into 1 string untill a " is found,
        must not be called by the user. But only by fixStrings()

            Parameters
            ----------
            tokens : [str]
                A list of strings

            Returns
            -------
            list
                A list of strings
    """
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


# fixStrings :: [String] → [String]
def fixStrings(tokens: [str]) -> [str]:
    """Removes spaces from the list of strings unless a " is found,
        it then calls fixingString() to keep that string intact with spaces

            Parameters
            ----------
            tokens : [str]
                A list of strings

            Returns
            -------
            list
                A list of strings
    """
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



#todo fix this guz its nicer
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


# tokanizer :: String → [String]
def tokanizer(input_str: str) -> [str]:
    """Splits the given string into a list of strings,
        these strings are then split even further into smaller strings with the subsplit function

            Parameters
            ----------
            input_str : str
                A string

            Returns
            -------
            list
                A list of strings
    """
    val = subsplit(re.split("( )", input_str))
    return fixStrings(val)


# lexer :: String → [LEX_Type]
def lexer(file_name: str) -> [LEX_Type]:
    """Splits the contents of a file into Lexed Tokens

            Parameters
            ----------
            file_name : str
                The name of the file to Lex

            Returns
            -------
            list
                A list of Lexer Tokens
    """
    f = open(file_name, "r")
    tokens = tokanizer(f.read())
    tokens = assignTypes(tokens)
    return tokens
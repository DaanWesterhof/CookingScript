import re

keywordslist = [
    "recipe",
    "weigh",
    "->"
]

types = [
    "liter",
    "milliliter",
    "eggs",
    "cheese"
]

def remove_useless(list):
    if len(list) == 0:
        return []
    else:
        if list[0] == '':
            return remove_useless(list[1:])
        else:
            return [list[0]] + remove_useless(list[1:])

def subsplit(list):
    if len(list) == 1:
        return remove_useless(re.split('([\n:.,()"])', list[0]))
    else:
        return remove_useless(re.split('([\n:.,()"])', list[0]) + subsplit(list[1:]))



def fixingString(list):
    if len(list) == 0:
        return []
    if list[0] != '"' and '\\' not in list[0]:
        if len(list) >= 2:
            x = fixingString(list[1:])
            if x[0] != '"':
                return [list[0] + x[0]] + x[1:]
            else:
                return [list[0]] + x
        else:
            return [list[0]] + fixingString(list[1:])
    elif list[0] == '"':
        return [list[0]] + fixStrings(list[1:])
    elif list[0] == "\\":
        if list[1] == '"':
            x = fixingString(list[2:])
            return ['"' + x[0]] + x[1:]
    elif "\\" in list[0]:
        if list[1] == '"':
            x = fixingString(list[2:])
            return [list[0][:-2] + '"'] + x


def fixStrings(list):
    if len(list) > 0:
        if list[0] == '"':
            return [list[0]] + fixingString(list[1:])
        elif list[0] != " ":
            return [list[0]] + fixStrings(list[1:])
        else:
            return fixStrings(list[1:])
    else:
        return []



def tokanizer(input):
    val = subsplit(re.split("( )", input))
    print(val)
    return fixStrings(val)

def lexer():
    f = open("main.cook", "r")
    tokens = tokanizer(f.read())
    print(tokens)
    return tokens



class Node:
  def __init__(self):
    pass


class CodeSequence(Node):
    pass

class Function(Node):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.CodeSequence = None


class Variable(Node):
  def __init__(self, name):
    super().__init__()
    self.name = name



class Program:
    def __init__(self):
        self.Functions = []
        self.Variables = []
        self.CodeSequence = None

def defineFunction(tokens):
    new_function = Function
    if tokens[0] not in keywordslist and tokens[0].isalnum():
        new_function.name = tokens[0]

    new_function.name = tokens[0]


def verifyPrint(tokens, index) -> ([], bool, str):
    if index == 0:
        if tokens[0] == "(":
            return verifyPrint(tokens[1:], index+1)
        else:
            return tokens[1:], False, ""
    elif index == 1:
        if tokens[0] == '"': #or it is a variable that we can print
            return verifyPrint(tokens[1:], index+1)
    else:
        if tokens[0] == "\\":
            if tokens[1] == '"':
                return verifyPrint(tokens[2:], index+2)
        if tokens[0] == '"':
            if tokens[1] == ')':
                return (tokens, True, "")

        else:
            x, y, z = verifyPrint(tokens[1:], index+1)
            z = tokens[0] + z
            return (x, y, z)







def recursiveParse(tokens):
    if len(tokens) > 0:
        if tokens[0] == "taste":
            tokens, good, tekst = verifyPrint(tokens[1:], 0)
            if good:
                print(tekst)
        recursiveParse(tokens[1:])



def parser(tokens, program_class: Program):
    for i in range(0,len(tokens)):
        if tokens[i] == "recipe":
            program_class.Functions.append(defineFunction(tokens[i+1:]))





token = lexer()
recursiveParse(token)
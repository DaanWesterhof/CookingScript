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
            return [list[0][:-1] + '"' + x[0]] + x[1:]


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
    return fixStrings(val)

def lexer():
    f = open("main.cook", "r")
    tokens = tokanizer(f.read())
    print(tokens)
    return tokens




def defineFunction(tokens):
    new_function = Function
    if tokens[0] not in keywordslist and tokens[0].isalnum():
        new_function.name = tokens[0]

    new_function.name = tokens[0]


def verifyPrint2(tokens):
    if tokens[0] == "(" and tokens[1] == '"' and tokens[3] == '"' and tokens[4] == ')':
        return tokens[5:], True, tokens[2]
    else:
        return tokens[1:], False, ""


def recursiveParse(tokens):
    if len(tokens) > 0:
        if tokens[0] == "taste":
            tokens, good, tekst = verifyPrint2(tokens[1:])
            if good:
                print(tekst)
        recursiveParse(tokens[1:])



def parser(tokens, program_class: Program):
    for i in range(0,len(tokens)):
        if tokens[i] == "recipe":
            program_class.Functions.append(defineFunction(tokens[i+1:]))





token = lexer()
recursiveParse(token)
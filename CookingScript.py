import re

keywordslist = [
    "recipe",
    "weigh",
    "->"
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
        return remove_useless(re.split('([\n:.,()])', list[0]))
    else:
        return remove_useless(re.split('([\n:.,()])', list[0]) + subsplit(list[1:]))


def tokanizer(input):
    return subsplit(input.split(" "))

def lexer():
    f = open("main.cook", "r")
    tokens = tokanizer(f.read())
    print(tokens)



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






def parser(tokens, program_class: Program):
    for i in range(0,len(tokens)):
        if tokens[i] == "recipe":
            program_class.Functions.append(defineFunction(tokens[i+1:]))





lexer()
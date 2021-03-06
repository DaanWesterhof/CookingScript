from Definitions import *
import operator
import functools
from functools import reduce
from typing import List



class AST_Node(object):
    """ Default class for AST_Nodes ensures that all child classes can be passed as function arguments

        Attributes
        ----------
        node_type : str
            The type of the node
    """
    def __init__(self, node_type):
        """ Initialize the object and sets the type

                Parameters
                ----------
                node_type : str
                    The type of the node

        """
        self.node_type: str = node_type

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object
        """
        return f"Node({self.node_type})"


class AST_ArgumentList(AST_Node):
    """ Class for storing values given as parameters to functions

        Attributes
        ----------
        argument_nodes : List[AST_Node]
            The list containing all AST_Node parameters
    """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("ArgumentList")
        self.argument_nodes: List[AST_Node] = []

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "ArgumentList(" + reduce(lambda x, y: x+y.__str__(), self.argument_nodes, ", ") + ")"


class AST_FunctionArgument(AST_Node):
    """ Class to define an argument expected by a function

        Attributes
        ----------
        type : str
            The type of the argument
        name : str
            The name of the argument
    """
    def __init__(self, type: str, name: str):
        """ Initialize the object and set its values

                Parameters
                ----------
                type : str
                    The type of the argument

                name : str
                    The name of the argument

        """
        super().__init__("FunctionArgument")
        self.type: str = type
        self.name: str = name

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "FunctionArgument(" + self.type + " " + self.name + " )"


class AST_Variable(AST_Node):
    """ Class to define a variable in the context

        Attributes
        ----------
        name : str
            The name of the variable

        value : AST_Node
            The value of the variable

        type : str
            The type of the variable

    """
    def __init__(self):
        """  Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("Variable")
        self.name: str = None
        self.value: AST_Node = None
        self.type: str = ""

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "Variable( " + self.name + ": " + self.type + ": (" + self.value.__str__() + "))"


class AST_VariableReference(AST_Node):
    """ A class used to reference a variable in the context

        Attributes
        ----------
        name : str
            The name of the variable
    """
    def __init__(self, variable_name: str):
        """ Initialize the object and set its values

            Parameters
            ----------
            variable_name : str
                The name of the variable

        """
        super().__init__("VariableReference")
        self.name: str = variable_name

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "VariableReference( " + self.name + ")"


class AST_List(AST_Variable):
    """ A class used to for a list variable, it is able to store multiple literals

        Attributes
        ----------
        value : List[AST_Node]
            The name of the variable

        length : Int
            The length of the list

    """
    def __init__(self):
        super().__init__()
        self.value: List[AST_Node] = []
        self.length: int = 0




class AST_ListAcces(AST_VariableReference):
    """ A class used to reference a list variable, you can get or set values to the list.

        Attributes
        ----------
        name : str
            The name of the variable

        node : AST_Node
            A node that can be evaluated to a index value

    """
    def __init__(self, variable_name: str, index_node: AST_Node):
        super().__init__(variable_name)
        self.name: str = variable_name
        self.node: AST_Node = index_node



class AST_IfStatement(AST_Node):
    """ A class used for if statements, if the evaluation of the condition results true, the code block is executed

        Attributes
        ----------
        CodeSequence : List[AST_Node]
            A list of evaluatable nodes
        condition : AST_Node
            A AST_Node that results in either True or False
    """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("IfStatement")
        self.CodeSequence: List[AST_Node] = None
        self.condition: AST_Node = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "IfStatement( " + self.condition.__str__() + "):" + "\n" + stringify(self.CodeSequence, index)


class AST_Loop(AST_Node):
    """ A class used for while loops, while the evaluation of the condition results true, the code block is executed

        Attributes
        ----------
        CodeSequence : List[AST_Node]
            A list of evaluatable nodes
        condition : AST_Node
            A AST_Node that results in either True or False
    """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("Loop")
        self.CodeSequence: List[AST_Node] = None
        self.condition: AST_Node = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : Int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "LoopStatement( " + self.condition.__str__() + "):" + "\n" + stringify(self.CodeSequence, index)


#todo implement in runner
class AST_Label(AST_Node):
    """ A class used for labels. These classes will function as a spot in the code where you can jump to

            Attributes
            ----------
            label_number : Int
                The number of the step in the recipe
        """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("Label")
        self.label_number = None


class AST_ReturnStatement(AST_Node):
    """ A class used for Return Statements

        Attributes
        ----------
        value : AST_Node
            An evaluatable node that will be returned from the function it resides in
    """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("ReturnStatement")
        self.value: AST_Node = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "ReturnStatement( " + self.value.__str__(index) + ")"



class AST_FunctionVariable(AST_Node):
    """ A class used to reference a function and parameters

        Attributes
        ----------
        name : str
            A string that is the name of the variable

        FunctionName : str
            The name of the function it refers to

        value : AST_ArgumentList
            An object that holds the argument that are to be passed to the function
    """
    def __init__(self):
        """ Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("FunctionVariable")
        self.name: str = None
        self.FunctionName: str = None
        self.value: AST_ArgumentList = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "FunctionVariable( Name: " + self.name + " FunctionName: " + self.FunctionName + ")" #todo add the argument_list


class AST_FunctionCallExecution(AST_Node):
    """ A class used to reference a FunctionVariable, will be used as superclass for language functions, currently only for the print function

        Attributes
        ----------
        name : str
            A string that is the name of the variable
    """
    def __init__(self, ast_type: str="FunctionExecution"):
        """ Initialize the object and set its values

            Parameters
            ----------
            ast_type : str
                The type of the function execution, this is changeable for compatibility with language functions like print

        """
        super().__init__(ast_type)
        self.name: str = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "FunctionExecutor( FunctionVariable: "+ self.name + " )"


class AST_PrintFunctionCall(AST_FunctionCallExecution):
    """ A class used to identify a print function call

        Attributes
        ----------
        ParameterValues : AST_ArgumentList
            Holds the values that need to be printed to the console
    """
    def __init__(self, args: AST_ArgumentList):
        """ Initialize the object and set the argument list

            Parameters
            ----------
            args : AST_ArgumentList
                The nodes of which the evaluated value should be printed to the console

        """
        super().__init__("PrintFunctionCall")
        self.ParameterValues: AST_ArgumentList = args

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "PrintCall( "+ self.ParameterValues.__str__(index) +" )"


class AST_Function(AST_Node):
    """ A class used to identify a print function call

        Attributes
        ----------
        name : str
            The name of the function

        argumentList : [AST_FunctionArgument]
            A list of arguments expected by the function

        CodeSequence : [AST_Node]
            A list of evaluatable nodes that represent the code block of the function

        ReturnType:
            The type of the value that is returned by the function

    """
    def __init__(self):
        """Initialize the object and sets the type using the innit of its superclass
        """
        super().__init__("Function")
        self.name: str = None
        self.argumentList: List[AST_FunctionArgument] = None
        self.CodeSequence: List[AST_Node] = None
        self.ReturnType: str = None

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "Function:\n" + (index+1)*"    " + "Name: " +self.name + "\n" + (index+1)*"    "+ "ReturnType: " + \
               self.ReturnType.__str__() + "\n"+ (index+1)*"    " + "Arguments: \n" + \
               stringify(self.argumentList, index+1) + (index+1)*"    " +\
               ") " + " \n" +(index+1)*"    " + "Code: \n" + \
               stringify(self.CodeSequence, index+1)


class AST_Literal(AST_Node):
    """ A base class for literal values

        Attributes
        ----------
        type : str
            The type of the node

        val : str
            A string version of the value
    """
    def __init__(self, type: str, type_name: str, value: str):
        """ Initialize the object and set its values and type

            Parameters
            ----------
            type : str
                The type of the Class in string form

            type_name : str
                The TypeName of the class for AST printing purposes forexample: "AST_Integer"

            value : str
                A string version of the value stored by the node

        """
        super().__init__(type_name)
        self.type: str = type
        self.val: str = value

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return self.type + ": " + str(self.val)


class AST_Integer(AST_Literal):
    """ A class to store integer values

        Attributes
        ----------
        value : int
            The stored value
    """
    def __init__(self, value: int):
        """ Initialize the object and set its values and type

            Parameters
            ----------
            value : int
                The value to be stored by the node

        """
        super().__init__("litre", "Integer", str(value))
        self.value: int = value


class AST_Bool(AST_Literal):
    """ A class to store boolean values

        Attributes
        ----------
        value : bool
            The stored value
    """
    def __init__(self, value: bool):
        """ Initialize the object and set its values and type

            Parameters
            ----------
            value : bool
                The value to be stored by the node

        """
        super().__init__("egg", "Bool", str(bool))
        self.value: bool = value


class AST_String(AST_Literal):
    """ A class to store strings

        Attributes
        ----------
        value : str
            The stored string
    """
    def __init__(self, value: str):
        """ Initialize the object and set its values and type

            Parameters
            ----------
            value : bool
                The value to be stored by the node

        """
        super().__init__("cheese", "String", value)
        self.value: str = value


class AST_Program:
    """ A class that is the root of the program, it holds all functions and the main code

        Attributes
        ----------
        Functions : {AST_Function}
            A dictionairy that contains all functions as a value and their name as their key

        CodeSequence : [AST_Node]
            A list of evaluatable nodes that represent the code block of the program
    """
    def __init__(self):
        """Initialize the object
        """
        self.Functions: {AST_Function} = {}
        self.CodeSequence: List[AST_Node] = []

    def __str__(self, index: int=0) -> str:
        """ Returns a string version of the object and je subnodes of the object

                Parameters
                ----------
                index : int
                    Integer value indicating the tree depth of the code block the node resides in

                Returns
                -------
                str
                    A string version of the object and its subnodes
        """
        return "Functions: \n" + stringify(list(self.Functions.values()), index) + \
               "\n" + " \nCode: \n" + \
               stringify(self.CodeSequence, index)


# stringifyCode :: AST_Node ??? Int ??? String
def stringifyCode(codeLine: AST_Node, index: int) -> str:
    """ Turns a codeline into a string, withc indexing for code blocks

            Parameters
            ----------
            codeline : AST_Node
                A node that needs to be turned into a string

            index : token
                The amount of tabs infront of the line

            Returns
            -------
            str
                The codeline in string form with possibly tabs infront
    """
    return index * "    " + codeLine.__str__(index) + "\n"


# returnFunc :: AST_Function ??? Int ??? String
def returnFunc(func: AST_Function, index: int=0) -> str:
    """ Turns a codeline into a string, withc indexing for code blocks

            Parameters
            ----------
            codeline : AST_Node
                A node that needs to be turned into a string

            index : token
                The amount of tabs infront of the line

            Returns
            -------
            str
                The codeline in string form with possibly tabs infront
    """
    return index * "    " + func.__str__(index+1) + "\n"


# rec_str :: [AST_Node] ??? Int ??? String
def stringify(values: List[AST_Node], index: int) -> str:
    """ Creates a string of a list of Nodes using the stringifyCode and rec_string functions

            Parameters
            ----------
            values : List[AST_Node]
                A list of AST nodes

            index : int
                The index of the code block, it tells how many tabs need to be placed infront of a code line

            Returns
            -------
            str
                A long string made form all the string versions of nodes in the values list
    """
    if len(values) > 0:
        return reduce(lambda x, y: x+y, list(map(functools.partial(stringifyCode, index=index + 1), values)))
    else:
        return ""



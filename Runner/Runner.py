from Parser.AST_Nodes import *
from Parser.Operators import *
from Definitions import *
from typing import *


class running_context():
    """ A class used to store variables at runtime, it acts a bit like a stack

        Attributes
        ----------
        variables : {AST_Node}
            A dictionairy containing all variable nodes with the name of the variable as its key
    """
    def __init__(self):
        """ Initialize the object
        """
        self.variables: AST_Node = {}


def evaluate_condition(node: AST_Node, ast_main: AST_Program, context: [running_context]) -> bool:
    """ Evaluate a condition that needs to result in true or false.
        It results true if the evaluation results in true or an integer bigger than 0

            Parameters
            ----------
            node : AST_Node
                The node containing the condition to be evaluated

            ast_main : AST_Program
                The root of the program tree containing all program data

            context : [running_context]
                The context of the code in runtime

            Returns
            -------
            bool
                A bool indicating the result of the evaluation

        """
    val, context = evaluate_tree(node, ast_main, context)
    if isinstance(val, AST_Bool):
        return val.value
    elif isinstance(val, AST_Integer):
        if val.value > 0:
            return True
        else:
            return False
    return False


def evaluate_argument_list(node_list: [AST_Node], ast_main: AST_Program, context: [running_context]) -> [AST_Literal]:
    """ Evaluate all nodes in an argument list and return a list of just AST literals

            Parameters
            ----------
            node_list : [AST_Node]
                A list containing all arguments to a function

            ast_main : AST_Program
                The root of the program tree containing all program data

            context : [running_context]
                The context of the code in runtime

            Returns
            -------
            list[AST_Literal]
                A list containing the literal values of the results of the evaluation of the nodes of node_list

        """
    if len(node_list) == 0:
        return []
    else:
        val: AST_Literal
        new_context: [running_context]
        val, new_context = evaluate_tree(node_list[0], ast_main, context)
        return [val] + evaluate_argument_list(node_list[1:], ast_main, new_context)


#todo fix error check
def print_items(args: [AST_Literal]):
    """ This function prints the passed arguments to the terminal

        Parameters
        ----------
        args: [AST_Literal]
            This is a list of literals that need to be printed to the terminal

    """
    if len(args) == 0:
        print("expexted parameter in serve()")
        exit()
    elif len(args) == 1:
        print(args[0].value)
    else:
        print(args[0].value, end=' ')
        print_items(args[1:])


def executingCodeBlock(nodes: [AST_Node], index: int, ast_main: AST_Program, context: [running_context]) -> (AST_Node, [running_context]):

    """ This function executes the code of a code block and returns a value if a return statement is encountered

        Parameters
        ----------
        nodes: [AST_Node]
            This is a list of code lines in the code block which need to be evaluated

        index : int
            this is the index that tells which node of the nodes is being evaluated

        ast_main: AST_Program
            This is the root node of the program containing all program data

        context: [running_context]
            This is the context of the code where the variables are stored,
            evey scoped code block adds a entry if they are allowed to access the previous scope as well
            If they are not allowed to access the previous scope, a new list will be passed thru to them

        Returns
        -------
        Tuple[AST_Literal, list[running_context]]
            AST_Literal
                If it encounters a Return statement it will return the calulated value of that statement,
                otherwise this function will return none.
            list[running_context]
                It will also return the context as the context might have changed during the execution of one of the nodes
    """
    if index == len(nodes):
        return None, context[:1]
    elif isinstance(nodes[index], AST_IfStatement):
        val = None
        if evaluate_condition(nodes[index].condition,ast_main, context):
            val, context = executingCodeBlock(nodes[index].CodeSequence, 0, ast_main, context + [running_context()])
            if val is not None:
                return val, context[:1]
        return executingCodeBlock(nodes, index+1, ast_main, context)

    elif isinstance(nodes[index], AST_Loop):
        if evaluate_condition(nodes[index].condition, ast_main, context):
            val, context = executingCodeBlock(nodes[index].CodeSequence, 0, ast_main, context + [running_context()])
            if val is not None:
                return val, context[:1]
            return executingCodeBlock(nodes, index, ast_main, context)
        return executingCodeBlock(nodes, index + 1, ast_main, context)

    elif isinstance(nodes[index], AST_ReturnStatement): #todo check if the return type is correct
        val, context = evaluate_tree(nodes[index].value, ast_main, context)
        return val, context

    elif isinstance(nodes[index], AST_PrintFunctionCall):
        val = evaluate_argument_list(nodes[index].ParameterValues.argument_nodes, ast_main, context)
        print_items(val)
        return executingCodeBlock(nodes, index + 1, ast_main, context)
    else:
        val, context = evaluate_tree(nodes[index], ast_main, context)
        return executingCodeBlock(nodes, index+1, ast_main, context)


def find_value_in_context_list(name, context: [running_context]):
    if len(context) == 0:
        return None
    if name in context[-1].variables:
        return context[-1].variables[name], -1
    else:
        val, ind = find_value_in_context_list(name, context[:1])
        return val, ind-1


def evaluate_add(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Literal]:
    """ Evaluate a plus operator expresion with a left and right node.
        Can only be used by strings with strings and ints with ints

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Literal
            A literal that is the result of the sum of the left and right node

    """
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(left_node.value + right_node.value)
    elif isinstance(left_node, AST_String) and isinstance(right_node, AST_String):
        return AST_String(left_node.value + right_node.value)
    else:
        return None


def evaluate_min(left_node: AST_Integer, right_node: AST_Integer) -> Optional[AST_Integer]:
    """ Evaluate a minus operator expression with a left and right node.
        Can only be used with ints and ints

        Parameters
        ----------
        left_node : AST_Integer
            the left literal in the expression

        right_node : AST_Integer
            the right literal in the expression

        Returns
        -------
        AST_Integer
            A literal that is the result of the subtraction of the left on right node
    """
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        val = left_node.value - right_node.value
        if val < 0:
            val = 0
        return AST_Integer(val)
    else:
        return None


def evaluate_devide(left_node: AST_Integer, right_node: AST_Integer) -> Optional[AST_Integer]:
    """ Evaluate a division operator expression with a left and right node.
        Can only be used with ints and ints. Wil only return full numbers

        Parameters
        ----------
        left_node : AST_Integer
            the left literal in the expression

        right_node : AST_Integer
            the right literal in the expression

        Returns
        -------
        AST_Integer
            A integer that is the result of the division of the left on right node, only returns full numbers
    """
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(int(left_node.value / right_node.value))
    else:
        return None


def evaluate_multiply(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Literal]:
    """ Evaluate a multiplication operator expression with a left and right node.
        Can only be used with ints and ints and with ints and strings.
        If used with ints and strings it will return a string with int times the content of the string

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Literal
            A integer that is the result of the multiplication of the left on right node
    """
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(left_node.value * right_node.value)
    elif isinstance(left_node, AST_String) and isinstance(right_node, AST_Integer) or isinstance(left_node, AST_Integer) and isinstance(right_node, AST_String):
        return AST_String(left_node.value * right_node.value)
    else:
        return None


def evaluate_equals(left_node: AST_Literal, right_node: AST_Literal) -> AST_Bool:
    """ Evaluate if the left and right node are equal

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the nodes were equal and false if they were not
    """
    return AST_Bool(left_node.value == right_node.value)


def evaluate_smaller_equals(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Bool]:
    """ Evaluate if the left node is smaller or the same as the right node. Can only be used with ints and booleans

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the left node was smaller or equal to the right node
    """
    if ((type(left_node) is type(right_node)) and (
            isinstance(left_node, AST_Bool) or isinstance(left_node, AST_Integer))) or (
            isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (
            isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node <= right_node)
    else:
        return None


def evaluate_larger_equals(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Bool]:
    """ Evaluate if the left node is larger or the same as the right node. Can only be used with ints and booleans

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the left node was larger or equal to the right node
    """
    if ((type(left_node) is type(right_node)) and (
            isinstance(left_node, AST_Bool) or isinstance(left_node, AST_Integer))) or (
            isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (
            isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node >= right_node)
    else:
        return None


def evaluate_not_equal(left_node: AST_Literal, right_node: AST_Literal) -> AST_Bool:
    """ Evaluate if the left and right node are not equal

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the nodes are not equal and false if they are equal
    """
    return AST_Bool(left_node.value != right_node.value)


def evaluate_larger_then(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Bool]:
    """ Evaluate if the left node is larger then right node. Can only be used with ints and booleans

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the left node is larger then right node
    """
    if ((type(left_node) is type(right_node)) and (
            isinstance(left_node, AST_Bool) or isinstance(left_node, AST_Integer))) or (
            isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (
            isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node.value > right_node.value)
    else:
        return None


def evaluate_smaller_then(left_node: AST_Literal, right_node: AST_Literal) -> Optional[AST_Bool]:
    """ Evaluate if the left node is smaller then right node. Can only be used with ints and booleans

        Parameters
        ----------
        left_node : AST_Literal
            the left literal in the expression

        right_node : AST_Literal
            the right literal in the expression

        Returns
        -------
        AST_Bool
            A AST_Bool object with the value true if the left node is smaller then right node
    """
    if ((type(left_node) is type(right_node)) and (
            isinstance(left_node, AST_Bool) or isinstance(left_node, AST_Integer))) or (
            isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (
            isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node.value < right_node.value)
    else:
        return None


def add_arguments_to_context(argument_list: [AST_Node], args: [AST_Literal], context: [running_context], index: int=0) -> [running_context]: #todo check if the variable type is correct
    """ Add parameter values to the context to act ass variables for a function

        Parameters
        ----------
        argument_list: [AST_Node]
            This is the list of arguments expected by the functions

        args: [AST_Literal]
            This is the list of values passed to the function as parameters

        context: [running_context]
            This is the context of the function where the variables need to be placed

        index: int, optional
            This is the index of which item of the args is now to be added (default value = 0)
    """

    if len(args) == index:
        return context
    else:
        new_var: AST_Variable = AST_Variable()
        new_var.value = args[index]
        new_var.name = argument_list[index].name
        new_var.node_type = argument_list[index].type
        context[-1].variables[argument_list[index].name] = new_var
        return add_arguments_to_context(argument_list, args, context, index+1)


#todo error check for types and add functioncall support
def evaluate_tree(tree: AST_Node, ast_main: AST_Program, context: [running_context]) -> (AST_Literal, [running_context]):
    """ This function evaluates a tree of nodes to execute its functions, assignments or other calculations.
            Even if the code has no further impact, for example: "6+6" it will still be evaluated

        Parameters
        ----------
        tree: AST_Node
            This is the list of arguments expected by the functions

        ast_main: AST_Program
            This is the root node of the program containing all program data

        context: [running_context]
            This is the context of the code where the variables are stored,
            evey scoped code block adds a entry if they are allowed to access the previous scope as well
            If they are not allowed to access the previous scope, a new list will be passed thru to them

        Returns
        -------
        Tuple[AST_literal, list[running_context]]
            It returns the calculated value if there is one, other wise its non, it will also return the context
            as it might have changed due to variable assignments
    """
    if isinstance(tree, AST_Literal):
        return tree, context
    elif isinstance(tree, AST_VariableReference):
        var, index = find_value_in_context_list(tree.name, context)
        if var is not None:
            return var.value, context
    elif isinstance(tree, AST_FunctionCallExecution):
        val, ind = find_value_in_context_list(tree.name, context)
        new_context = [running_context()]
        if len(ast_main.Functions[val.FunctionName].argumentList) == len(val.value.argument_nodes):
            arg_list = evaluate_argument_list(val.value.argument_nodes, ast_main, context)
            new_context = add_arguments_to_context(ast_main.Functions[val.FunctionName].argumentList, arg_list, new_context)
        else:
            #todo throw error
            print("the amount of passed arguments is not the same as the expected amount")
            exit()
        val, bad_context = executingCodeBlock(ast_main.Functions[val.FunctionName].CodeSequence, 0, ast_main, new_context)
        return val, context
    elif isinstance(tree, AST_AssignmentOperator):
        if isinstance(tree.left, AST_Variable):
            val, context = evaluate_tree(tree.right, ast_main, context)
            tree.left.value = val
            context[-1].variables[tree.left.name] = tree.left
            return None, context
        elif isinstance(tree.left, AST_VariableReference):
            val, context = evaluate_tree(tree.right, ast_main, context)
            var, ind = find_value_in_context_list(tree.left.name, context)
            var.value = val

            context[ind].variables[tree.left.name] = var
            return None, context
        elif isinstance(tree.left, AST_FunctionVariable):
            val, context = evaluate_tree(tree.right, ast_main, context)
            tree.left.value = val
            context[-1].variables[tree.left.name] = tree.left
            return None, context

    elif isinstance(tree, AST_Operator):
        val_l, context = evaluate_tree(tree.left, ast_main, context)
        val_r, context = evaluate_tree(tree.right, ast_main, context)

        if tree.operator == '+':
            return evaluate_add(val_l, val_r), context
        elif tree.operator == '-':
            return evaluate_min(val_l, val_r), context
        elif tree.operator == '/':
            return evaluate_devide(val_l, val_r), context
        elif tree.operator == '*':
            return evaluate_multiply(val_l, val_r), context

        elif tree.operator == "==":
            return evaluate_equals(val_l, val_r), context
        elif tree.operator == "<=":
            return evaluate_smaller_equals(val_l, val_r), context
        elif tree.operator == ">=":
            return evaluate_larger_equals(val_l, val_r), context
        elif tree.operator == "!=":
            return evaluate_not_equal(val_l, val_r), context
        elif tree.operator == ">":
            return evaluate_larger_then(val_l, val_r), context
        elif tree.operator == "<":
            return evaluate_smaller_then(val_l, val_r), context
    elif isinstance(tree, AST_ArgumentList):
        return tree, context
    else:
        return None, context

from Parser.AST_Nodes import *
from Parser.Operators import *
from Definitions import *


class running_context():
    def __init__(self):
        self.variables = {}


def evaluate_condition(node, ast_main, context):
    val, context = evaluate_tree(node, ast_main, context)
    if isinstance(val, AST_Bool):
        return val.value
    elif isinstance(val, AST_Integer):
        if val.value > 0:
            return True
        else:
            return False
    return False


def evaluate_argument_list(list, ast_main, context: [running_context]):
    if len(list) == 0:
        return []
    else:
        val, context = evaluate_tree(list[0], ast_main, context)
        return [val] + evaluate_argument_list(list[1:], ast_main, context)


#todo fix error check
def print_items(args):
    if len(args) == 0:
        print("expexted parameter in serve()")
        exit()
    elif len(args) == 1:
        print(args[0].value)
    else:
        print(args[0].value, end=' ')
        print_items(args[1:])


def executingCodeBlock(nodes, index, ast_main, context: [running_context]) -> (AST_Node, [running_context]):
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


def evaluate_add(left_node, right_node):
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(left_node.value + right_node.value)
    elif isinstance(left_node, AST_String) and isinstance(right_node, AST_String):
        return AST_String(left_node.value + right_node.value)
    else:
        return None


def evaluate_min(left_node, right_node):
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        val = left_node.value - right_node.value
        if val < 0:
            val = 0
        return AST_Integer(val)
    else:
        return None


def evaluate_devide(left_node, right_node):
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(int(left_node.value / right_node.value))
    else:
        return None


def evaluate_multiply(left_node, right_node):
    if isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Integer):
        return AST_Integer(left_node.value * right_node.value)
    elif isinstance(left_node, AST_String) and isinstance(right_node, AST_Integer) or isinstance(left_node, AST_Integer) and isinstance(right_node, AST_String):
        return AST_String(left_node.value * right_node.value)
    else:
        return None


def evaluate_equals(left_node, right_node):
    return AST_Bool(left_node.value == right_node.value)


def evaluate_smaller_equals(left_node, right_node):
    if (type(left_node) is type(right_node)) or (isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node <= right_node)
    else:
        return None


def evaluate_larger_equals(left_node, right_node):
    if (type(left_node) is type(right_node)) or (isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node >= right_node)
    else:
        return None


def evaluate_not_equal(left_node, right_node):
    return AST_Bool(left_node.value != right_node.value)


def evaluate_larger_then(left_node, right_node):
    if (type(left_node) is type(right_node)) or (isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node.value > right_node.value)
    else:
        return None


def evaluate_smaller_then(left_node, right_node):
    if (type(left_node) is type(right_node)) or (isinstance(left_node, AST_Bool) and isinstance(right_node, AST_Integer)) or (isinstance(left_node, AST_Integer) and isinstance(right_node, AST_Bool)):
        return AST_Bool(left_node.value < right_node.value)
    else:
        return None


def add_arguments_to_context(parameter_list: [AST_Node], args: AST_ArgumentList, context: [running_context], index=0): #todo check if the variable type is correct
    if len(args) == index:
        return context
    else:
        new_var = AST_Variable()
        new_var.value = args[index]
        new_var.name = parameter_list[index].name
        new_var.node_type = parameter_list[index].type
        context[-1].variables[parameter_list[index].name] = new_var
        return add_arguments_to_context(parameter_list, args, context, index+1)


#todo error check for types and add functioncall support
def evaluate_tree(tree, ast_main, context: [running_context]):
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

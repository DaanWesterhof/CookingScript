# CookingScript
The language I made an interperter for is CookingScript. 
CookingScript is a programming language I designed myself. 
Its a language based on terms from the kitchen. Hence the name: CookingScript.

CookingScript is a turing complete language. As it supports variables, functions, lists, loops and basic operators,
It has the ability to implement all functionalities brainfuck can as well. 
And as brainfuck is a turing complete language this means CookingScript is turing complete as well. 
With a list you can make a list just like brainfucks data list. In a vraibale you can store the index/pointer to te correct location int he list.
And using list assignments and basic operators you can increase and decrease the value on the location of the pointer.
Loops can be implemented using variables with an index as well, checking if the value at the index location is 0.


##Language definition

###Types
CookingScript has the following Types:

```
integers:   litre       : 10
booleans:   egg         : whole
strings:    cheese      : "Hello there"
lists:      groceries   : {1, 2, 3, 4, 5, "boo", broken}
```

####Variables
These types can also be used as variables, by first declaring the type and then the variable name like below:
```
type variable_name = value
```
for more information about the variable types see examples below:

#####Litres
Litres are the CookingScript equivalents of integers
```
litre i = 0
```

#####Eggs
Eggs are the CookingScript equivalents of booleans. whole is true and broken is false
```
egg i = whole
egg j = broken
```

#####Cheese
Cheese is the CookingScript equivalent of a string. Its stringy cheese.
```
cheese i = "this is a string"
```

#####Groceries
Groceries are the CookingScript equivalent of lists. These list can be filled with all types and duplicates, they are basically variables that can store multiple values
```
groceries i = 100 
//This makes a list of length 100 filled with integer 0's

litre j = 9
groceries i = {1, 2, 3, 4, 5, 6, 7, 8, 9, j +1} 
//This makes a list of length 10, with the values as in between the {}, the j + 1 wil be evaluated as 10, 

groceries x = {"hey", "i", "am", "in", "a", "list"}
cheese y = x[0]
x[1] = "I"
//you can access a list using the [] operator 
```

###Code Blocks

Just like most languages CookingScript has code blocks, these can be in while loops, functions or your main program code.
There is one important thing all these code blocks have in common. That is that they end with "done".
If the interpreter encounters the "done" statement it will exit that scope.

####Scopes
CookingScript is a scoped language. The scope of a function is limited as the function cannot access variables defined outside of the function.
In the code blocks themselves there is also scoping. Variables created in a while loop cannot be accessed outside of that while loop. 
And will not be saved when the loop is restarted. But the while loop is able to access variables created outside of the while loop like the Main code block, or the function code block.
So you can say scopes in this language work a bit like a stack

####Main code
The main code is the code that is run on the start of your program, you can put a loop in this or just let it end.
You define the main code block using "start:" as in the example below:

```
start:
    litre val = 10
    fib func_call = prepare(9)
    val = func_call.bake() + val
    taste(val)
done
```


###Statments

####If statement example:
```
weigh( i < 5 )
    i = 0
done
```
An weigh/if statement does not have an else statement, as when you are cooking you dont bake something else if you dont have enough sugar, you add more sugar.
However you can simulate an else statement by adding another weigh statement but invert the condition. See the example below
```
weigh( i < 5 )
    i = 0
done
weigh( i >= 5 )
    i = 10
done
```

####While loops example:
While loops in CookingScript are defined as a mix. As you are mixing a substance until its good. They behave very similar to weigh statements, 
except they repeat the codeblock until the condition results in false/broken
 ```
mix(i < 5)
    i = i + 1
done
```

####Functions example:
Functions in CookingScript are a bit different than in other languages. You define a function as a recipe. You give it a name and a return type. 
Then to set the parameters you starts with a prepare: keyword and add a list of types using a - for each entry.
The actual code of the statement is defined in the bake: section and behaves like a normal code block. A file can contain as much functions as you like.
But you can also put functions in other files and Include the file.
```
recipe fib -> litre
    prepare:
        - litre n
    bake:
        weigh n <= 1
            serve n
        done
        fib fib_left = prepare(n - 1)
        fib fib_right = prepare(n - 2)
        serve fib_left.bake() + fib_right.bake()
    done
```

Functions also support recursion as shown in the example above. 
You can also call other functions in the codeblock of a function.
These functions have to be defined before you use them, either in another included file or in the same file above te function you are currently defining.

To return from a function you use the serve statement. It is the CookingScript equivalent of the return statement. It can be seen in the example above.

####Function call example:
Function calls in CookingScript are a bit unconventional. As the first step you have to prepare the ingredients. 
After they are prepared you can bake it. Baking the ingredients will execute the function. See the example below:

``` 
fib fib_call = prepare(10) 
//here we prepare the ingerdients for the fib function. We declare what function we want, the name for the variable, and we assign it with the prepared values using prepare()

litre number = fib_call.bake() 
//here we execute the function using.bake() on the object that contains the prepared ingredients
```

###Build in functions:
####Print statement example:
```
litre i = 10
taste(i)
taste(5)
```

####Include other files
You can include other .cook files using the cookbook statement. This will include the recipes defined in that file into your program so you can use them.
```
cookbook "example.cook"
```

####Use commandline parameters
You can pass arguments to your program using the commandline.
```
python CookingScript.py main.cook hey i am a commandline passed argumen 1 2 3 broken flase true
```
These arguments will be available in he program as variables. These are named "$arg" + the number of the argument.
So "hey" in this call would be "$arg0" in your program.

```
litre param1 = $arg0
```

## Interpreter Code
The interpreter has been written completeley in functional style, 
with haskell type-annotation in the comments and Python-Style type-annotations in the function definitions <br>

It makes used off classed to give meaning to the tokens form the lexer so they can easily be parsed into a usable AST.
The AST is a tree made of nodes. These nodes are all based on the AST_Node base class so they can easily be passed into functions no matter their actual type. Except for the root node (AST_Program).
By printing the root node of the tree, you can print the entire AST with correct indexing. This gives a good overview of the structure of your program.
All classes support this printing, even the classes not part of the AST.

These classes with inheritance can be found in the following files:
 - [Lexer/LEX_Tokens.py]
 - [Parser/AST_Nodes.py]
 - [Parser/Operators.py]
 The most intresting example is this one: [Parser/AST_Nodes.py] - [388]


To simplify the comparison operators i have made a python decorator. This decorator checks if the two values that will be compared are compatible.
This decorator [Runner/Runner.py] - [327] is aplied on the evaluators for the following operators:
- <=    [Runner/Runner.py] - [361]
- \>=   [Runner/Runner.py] - [382]
- \>    [Runner/Runner.py] - [423]
- <     [Runner/Runner.py] - [444]
 
 
To simplify some functions i have also applied higher order funtions in my code. These functions accept a function as their parameter and they apply this function on a iteratable object (list)
I have used these higher order funtions in the following locations:

1. [Parser/ParseCodeBlock.py] - [68] It map() is used multiple times in this function, i have only listed it once here as the usage is identical. I use it to sum the values of 2 tuples into 1 tuple of the same length

2. [Lexer/Lexer.py] - [97] Here filter() is used to filter out useless tokens such as ''. These hold no value for the program so they should be removed, it is used a few times in the same way so i only include it in this list once.

3. [Parser/AST_Nodes.py] - [675] Here we use reduce() and map() in one code line, this function is used to turn ASt_Nodes into strings, so we can print the AST
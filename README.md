# CookingScript
The language I made is CookingScript. 
CookingScript is a programming language I designed myself. 
Its a language based on terms from the kitchen. Hence the name: CookingScript.

CookingScript is a turing complete language. As it supports variables, functions, lists, loops and basic operators,
It has the ability to implement all functionalities brainfuck can as well. 
And as brainfuck is a turing complete language this means CookingScript is turing complete as well. 
With a list you can make a list just like brainfucks data list. In a variable you can store the index/pointer to te correct location int he list.
And using list assignments and basic operators you can increase and decrease the value on the location of the pointer.
Loops can be implemented using variables with an index as well, checking if the value at the index location is 0.


##Interpreter VS Compiler

This language has a interperter AND a compiler, but there are some difrences between the execution of the same code.
Wherever there is a diffrence i will note this below the paragraph to prevent confusion and why some things 
might not work in the compiler and vise versa

##Language definition

###Types
CookingScript has the following Types:

```
integers:   litre       : 10
booleans:   egg         : whole
strings:    cheese      : "Hello there"
lists:      groceries   : {1, 2, 3, 4, 5, "boo", broken}
```

**The compiler does not support strings, only integers, booleans and lists**

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
**Strings are not supported by the compiler**

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
**Strings are not supported by the compiler so they cant be stored in a list**<br>
**In the compiler version lists can only be initialized with an integer, not an initializer list**
See below for valid use of lists when compiling instead of interpreting
```
groceries i = 100
//create a list

i[10] = 5
litre b = i[99[

```

###Code Blocks

Just like most languages CookingScript has code blocks, these can be in while loops, functions or your main program code.
There is one important thing all these code blocks have in common. That is that they end with "done".
If the interpreter or compiler encounters the "done" statement it will exit that scope.

####Scopes
CookingScript is a scoped language. The scope of a function is limited as the function cannot access variables defined outside of the function.
In the code blocks themselves there is also scoping. Variables created in a while loop cannot be accessed outside of that while loop. 
And will not be saved when the loop is restarted. But the while loop is able to access variables created outside of the while loop like the Main code block, or the function code block.
So you can say scopes in this language work a bit like a stack

**Note that the compiler does not support scopes in while loops and if statements, only function scopes are supported**

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
**Note in the compiled version the main code is not compiled, only the functions and the functions from the included files**

####Operators

CookingScript supports multiple operators. All these operators follow the calculation rules of what operator is supposed to be done first.
For example a * operator should be evaluated before a + operator.

#####Plus operator
The plus operator supports additions between ints and additions between strings

```
i = 1 + 1
i = "hello " + "world"
```

**Strings are not supported in the compiled version so you can use a + operator with those**
#####Minus operator
The minus operator only allows substractiosn between ints
```
i = 2 - 1
```

#####Multiplication operator
The multiplication operator allows multiplications of ints and ints and multiplactions of ints and strings
```
i = 2 * 2
i = 5 * "cheesy string"
```
**Strings are not supported in the compiled version so you can use a * operator with those**
#####Devision operator
The devision operator only allows divisions of integers and will alwways round to a full number.
```
i = 4 / 2
```

#####Relational operators
The equals and does not equal operator allows for comparison between all types.
```
egg i = 5 == "hello" //result = broken because they are not equal
egg j = 6 != broken //result = true because 6 does not equal broken
```
**Strings are not supported in the compiled version so you can use relational operators with those**

The other relational operators only allow comparisons between ints and bools.
```
egg i = 5 < 6
egg j = 0 <= whole
egg k = 10 > whole
egg l = 10 >= 5
```

#####Multiple operators
CookingScript supports complex code lines with multiple operators with correct calculation order, for example:
```
foo bar = prepare(10)
egg result = 5 + 6 /2 == bar.bake() * 10 - 5
```
This statements results in a evaluation where 6/2 is calulated firs, and then its added onto 5.
After that it evaluates bar.bake() and muliplies the result by 10. And then substracts 5.
After the calulations of the left and righ side of the == are done,
it compares the results and returns a boolean value wich is stored in result


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
The actual code of the statement is defined in the bake: section and behaves like a normal code block. A file can contain as many functions as you like.
But you can also put functions in other files and Include the file.
```
recipe fib -> litre
    prepare:
        - litre n
    bake:
        weigh( n <= 1 )
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

You can predefine functions in a file using the recipes keyword. This acts as a table of contents for a file, this way you can use double recursion. But it is not required:
```
recipes
    - foo
    - bar
done
```

**Note:**
 In the interperter you pass lists as values to a function. But in the compiler all lists are passed like a pointer, 
 you cannot return lists in the compiled version. So when passing a list to a function in the compiler you can change the its values but you do not need to return int

####Function call example:
Function calls in CookingScript are a bit unconventional. As the first step you have to prepare the ingredients. 
After they are prepared you can bake it. Baking the ingredients will execute the function. See the example below:

``` 
fib fib_call = prepare(10) 
//here we prepare the ingerdients for the fib function. 
//We declare what function we want, the name for the variable, and we assign it with the prepared values using prepare()

litre number = fib_call.bake() 
//here we execute the function using.bake() on the object that contains the prepared ingredients
```

###Build in functions:
####Print statement example:
**Print statements are not supported by the compiler**

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
**This is not supported by the compiler**
You can pass arguments to your program using the commandline.
```
python CookingScript.py main.cook hey i am a commandline passed argumen 1 2 3 broken flase true
```
These arguments will be available in he program as variables. These are named "$arg" + the number of the argument.
So "hey" in this call would be "$arg0" in your program.
To see if there are any arguments avalaible you can check the "$arglen" variable. This variable tells how many arguments have been passed

```
litre arguments = $arglen
litre param1 = $arg0
```

####ErrorHandling
CookingScript has a very helpfull error handler. If syntax errors have been found by the lexer or parserm, the program will announce this to the user.
The error it has found will then reveal in wich file and on wich line the error is located. For Example:
```
litre = 5
```
The error message then becomes:
```
Expected '[FILE: 'example.cook', LINE: '1'] Identifier' after 'litre' got '=' instead
```

If a error is found while running the code, for example:
```
litre var = broken
```
Then the error will annouce what the problem is.
The error message then becomes:
```
Expected '[Runntime Error] Expected value of type 'litre' for variable 'var' got value of type 'egg' instead
```

If a error is found while compiling the code, for example:
```
litre var = broken
```
Then the error will annouce what the problem is.
The error message then becomes:
```
Expected '[CompileError] Expected value of type 'litre' for variable 'var' got value of type 'egg' instead
```



## Interpreter Code
The interpreter has been written completeley in functional style, 
with haskell type-annotation in the comments and Python-Style type-annotations in the function definitions <br>

It makes used off classed to give meaning to the tokens form the lexer so they can easily be parsed into a usable AST.
The AST is a tree made of nodes. These nodes are all based on the AST_Node base class so they can easily be passed into functions no matter their actual type. Except for the root node (AST_Program).
By printing the root node of the tree, you can print the entire AST with correct indexing. This gives a good overview of the structure of your program.
All classes support this printing, even the classes not part of the AST.

These classes with inheritance can be found in the following files:
 - [[Lexer/LEX_Tokens.py]](Lexer/LEX_Tokens.py)
 - [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py)
 - [[Parser/Operators.py]](Parser/Operators.py)
 The most intresting example is this one: [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py) - [211]


To simplify the comparison operators i have made a python decorator. This decorator checks if the two values that will be compared are compatible.
This decorator [Runner/Runner.py] - [327] is aplied on the evaluators for the following operators:
- <=    [[Runner/Runner.py]](Runner/Runner.py) - [364]
- \>=   [[Runner/Runner.py]](Runner/Runner.py) - [385]
- \>     [[Runner/Runner.py]](Runner/Runner.py) - [426]
- <      [[Runner/Runner.py]](Runner/Runner.py) - [447]
 
 
To simplify some functions i have also applied higher order funtions in my code. These functions accept a function as their parameter and they apply this function on a iteratable object (list)
I have used these higher order funtions in the following locations:

1. [[Parser/ParseCodeBlock.py]](Parser/ParseCodeBlock.py) - [68] It map() is used multiple times in this function, i have only listed it once here as the usage is identical. I use it to sum the values of 2 tuples into 1 tuple of the same length

2. [[Lexer/Lexer.py]](Lexer/Lexer.py) - [102] Here filter() is used to filter out useless tokens such as ''. These hold no value for the program so they should be removed, it is used a few times in the same way so i only include it in this list once.

3. [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py) - [702] Here we use reduce() and map() in one code line, this function is used to turn ASt_Nodes into strings, so we can print the AST


## CompilerCode Code

The compiler has been written completeley in functional style, 
with haskell type-annotation in the comments and Python-Style type-annotations in the function definitions <br>

It makes used off classes to give meaning to the tokens form the lexer so they can easily be parsed into a usable AST.
The AST is a tree made of nodes. These nodes are all based on the AST_Node base class so they can easily be passed into functions no matter their actual type. Except for the root node (AST_Program).
By printing the root node of the tree, you can print the entire AST with correct indexing. This gives a good overview of the structure of your program.
All classes support this printing, even the classes not part of the AST.


#ATP Checklist Compiler
###Gekozen taal:
Cooking Script: Zelf ontworpen

###Turing-compleet omdat:
De taal lists, variabelen, loops, integers assignment operators en gewone operators ondersteund.
Daardoor kan hij alle functionaliteiten van brainfuck implementeren, en is net zoals brainfuck dus turing complete
 

###Code is geschreven in functionele stijl.
Ja mijn code is volledig geschreven in functionele stijl


###Taal ondersteunt:
Mijn taal ondersteund onderandere de minimale onderstaande eisen
Loops Voorbeeld: [[main.cook]](main.cook) - [11]
If statements: [[main.cook]](main.cook) - [31]

###Libraries die worden gebruikt:
- functools
- typing
- sys
- operator

Deze zitten allemaal standaard in python en zouden geen probleem moeten leveren.

###Mij Code Bevat:

**Classes met inheritance**: bijvoorbeeld [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py) - [211]

**Object-printing voor elke class**: [ja]

Type-annotatie: Haskell-stijl in comments: [ja]; Python-stijl in functiedefinities: [ja]

**Compiler-functionaliteit Must-have**:

**Functies**: [meer per file]
Alle functies van zowel de gecompilde file as geinclude file worden gecompiled naar 1 .asm bestand, en kunnen worden aangeroepen vanuit C

**Functies kunnen andere functies aanroepen**: zie voorbeeld [[example_double_rec.cook]](example_double_rec.cook) - [15]

**Compiler-functionaliteit (should/could-have)**:
- ErrorHandling (minimaal in compiler)
- Includes en Meer Functies per file
- Lijsten
- Lange en complexe berekeningen

voor meer uitleg zie het laatste hoofdstuk voor elk onderdeel

##Should Haves



#ATP Checklist Interpreter
###Gekozen taal:
Cooking Script: Zelf ontworpen

###Turing-compleet omdat:
De taal lists, variabelen, loops, integers assignment operators en gewone operators ondersteund.
Daardoor kan hij alle functionaliteiten van brainfuck implementeren, en is net zoals brainfuck dus turing complete
 

###Code is geschreven in functionele stijl.
Ja mijn code is volledig geschreven in functionele stijl


###Taal ondersteunt:
Mijn taal ondersteund onderandere de minimale onderstaande eisen
Loops Voorbeeld: [[main.cook]](main.cook) - [11]
If statements: [[main.cook]](main.cook) - [31]

###Libraries die worden gebruikt:
- functools
- typing
- sys
- operator

Deze zitten allemaal standaard in python en zouden geen probleem moeten leveren.

###Mij Code Bevat:

**Classes met inheritance**: bijvoorbeeld [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py) - [211]

**Object-printing voor elke class**: [ja]

**Decorator: functiedefinitie op** [[Runner/Runner.py]](Runner/Runner.py) - [327], toegepast op 
- <=    [[Runner/Runner.py]](Runner/Runner.py) - [364]
- \>=   [[Runner/Runner.py]](Runner/Runner.py) - [385]
- \>    [[Runner/Runner.py]](Runner/Runner.py) - [426]
- <     [[Runner/Runner.py]](Runner/Runner.py) - [447]

Type-annotatie: Haskell-stijl in comments: [ja]; Python-stijl in functiedefinities: [ja]

**Minstens drie toepassingen van hogere-orde functies:**

1. [[Parser/ParseCodeBlock.py]](Parser/ParseCodeBlock.py) - [68] It map() is used multiple times in this function, i have only listed it once here as the usage is identical. I use it to sum the values of 2 tuples into 1 tuple of the same length

2. [[Lexer/Lexer.py]](Lexer/Lexer.py) - [102] Here filter() is used to filter out useless tokens such as ''. These hold no value for the program so they should be removed, it is used a few times in the same way so i only include it in this list once.

3. [[Parser/AST_Nodes.py]](Parser/AST_Nodes.py) - [702] Here we use reduce() and map() in one code line, this function is used to turn ASt_Nodes into strings, so we can print the AST

 

**Interpreter-functionaliteit Must-have**:

**Functies**: [meer per file]

**Functie-parameters kunnen aan de interpreter meegegeven worden door**:
    door bij het starten van het programma in de commandline na de bestandsnaam parameters mee te geven.

**Functies kunnen andere functies aanroepen**: zie voorbeeld [[example_double_rec.cook]](example_double_rec.cook) - [15]

**Functie resultaat wordt op de volgende manier weergegeven:**
    Je kan de taste() functie gebruiken om waardes naar de terminal te printen
    [[main.cook]](main.cook) - [30]
    
    
**Interpreter-functionaliteit (should/could-have)**:

- ErrorHandling
- Strings
- Includes en Meer Functies per file
- CodeBlock Scoping
- Lijsten
- Lange en complexe berekeningen

voor meer uitleg zie het laatste hoofdstuk voor elk onderdeel

##Should Haves

______________________________________
**ErrorHandling**<br>
CookingScript heeft een erg handige error handler. Als er syntax fouten worden opgemerkt door de lexer en parser word dit bekend gemaakt aan de gebruiker. 
De error message geeft dan aan in welk bestand en op welke regel de fout is gevonden. Bijvoorbeeld:
```
litre = 5
```
De error message word dan:
```
Expected '[FILE: 'example.cook', LINE: '1'] Identifier' after 'litre' got '=' instead
```

Als er een fout word gevonden tijdens het runnen van de code bijvoorbeeld:
```
litre var = broken
```
Dan word er door de error handler aangegeven wat het probleem is.
De error message word dan:
```
Expected '[Runntime Error] Expected value of type 'litre' for variable 'var' got value of type 'egg' instead
```

**geïmplementeerd door middel van de volgende functies:<br>**
 a) [throw_error] in [ErrorHandler/ErrorHandler.py] op [24] <br>
 b) [throw_error_runtime] in [ErrorHandler/ErrorHandler.py] op [46] <br>
 c) [throw_error_with_token] in [ErrorHandler/ErrorHandler.py] op [68] <br>

______________________________________
**Strings** <br>
Ook ondersteund cookingscript Strings. Dit is een simpele implementatie van een string.
Je kan ze opslaan in een variabele, ze bij elkaar optellen en een string vermenigvuldigen met een int.
<br><br>**geïmplementeerd door middel van de volgende functies en classes:<br>**
 a) [parseCodeLine] in [Parser/ParseCodeBlock.py] op [33] <br>
 b) [evaluate_tree] in [Runner/Runner.py] op [512] <br>
 c) [AST_String] in [Parser/AST_Nodes.py] op [588] <br>


______________________________________
**Includes en Meer Functies per file** <br>
In CookingScript kan je zo veel functies per file aanmaken als je wilt.
Hierbij kan je ook gebruik maken van het recipes keyword om dubbele recursie mogenlijk te maken.
Daarnaast kan je ook andere bestanden includen om functies uit die bestanden te kunnen gebruiken.
```
cookbook "example.cook"
```
<br>**geïmplementeerd door middel van de volgende functies:<br>**
 a) [recursiveParse] in [Parser/Parser.py] op [512] <br>

______________________________________
**Code Block scoping**<br>
Ook ondersteund CookingScript codeblock scoping. Dit is scoping waarbij code geen toegang heeft tot variabelen die zijn aangemaakt in een whileloop binnen zichzelf.
De ScopeBlocks kunnen alleen kijken naar waar de huidige scope zich in bevind. ScopesBlocks kunnen niet kijken scopes die worden aangemaakt in zichelf
Het functioneerd een beetje als een stack.
<br>**geïmplementeerd door middel van de volgende functies en classes:<br>**
 a) [running_context] in [Runner/Runner.py] op [8] <br>
 b) [evaluate_tree] in [Runner/Runner.py] op [512] <br>
 c) [executingCodeBlock] in [Runner/Runner.py] op [131] <br>

______________________________________
**Lijsten**<br>
CookingScript ondersteund variabele lijsten. Je kan een lijst aanmaken met een specefieke grote.
In deze lijst kan je alle waarden toevoegen die je wilt. Ook andere lijsten, **let op:** `[][]` worden niet ondersteund.
Je kan een waarde uit een lijst of in een lijst zetten via een access `[ ]` operator. 

Je kan een lijst zijn intiele waarden en lengte geven met een intializer list `{1, 2, 3, 4, 5, 6}`.
Of door het te assignen met een integer, de lijst krijgt dan de groote van het getal en word gevuld met nullen.

<br><br>**geïmplementeerd door middel van de volgende functies en classes:<br>**
 a) [parseCodeLine] in [Parser/ParseCodeBlock.py] op [33] <br>
 c) [parseArgumentList] in [Parser/ParseCodeBlock.py] op [320] <br>
 d) [evaluate_tree] in [Runner/Runner.py] op [512] <br>
 e) [AST_List] in [Parser/AST_Nodes.py] op [191] <br>
 
______________________________________
**Lange en complexe berekeningen**<br>
CookingScript ondersteund ook lange en complexe berekeningen. Op een regel kan je zoveel operators zetten als je wilt (zolang de syntax maar klopt).
Hierbij word ook rekening gehouden met de rekenvolgorde van de operators.
**Let Op**: Haakjes () worden in gewone rekenregels genegeerd, dus berekeningen daarin krijgen geen voorang.
<br><br>**geïmplementeerd door middel van de volgende functies:<br>**
 a) [parseCodeLine] in [Parser/ParseCodeBlock.py] op [33] <br>
 b) [putInPlace] in [Parser/ParseCodeBlock.py] op [142] <br>
 c) [putValue] in [Parser/ParseCodeBlock.py] op [175] <br>
 d) [construct] in [Parser/ParseCodeBlock.py] op [237] <br>
 e) [fill] in [Parser/ParseCodeBlock.py] op [258] <br>
 f) [getNodeFromLine] in [Parser/ParseCodeBlock.py] op [282] <br>
 ______________________________________


<br><br>Voor extra uitleg over functionaliteiten zie de uitlag in het engels bovenaan het bestand


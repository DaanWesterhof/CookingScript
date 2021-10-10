from Lexer.LEX_Tokens import *

error_dict = {
    "ExpectType": " Expected '{}' got '{}' instead",
    "ExpectTypes": " Expected '{}' or '{}' got '{}' and '{}' instead",
    "UnexpectedKeyword": " Unexpected keyword ''{}'' found",
    "ExpectedBefore": " Expected '{}' before '{}'",
    "ExpectedAfter": " Expected '{}' after '{}'",
    "ExpectedAfterInstead": " Expected '{}' after '{}' got '{}' instead",
    "UnknownFunction": " Unknown function: '{}'",
    "UnknownVar": " Unknown variable: '{}'",
    "ExpectedReturnType": " Expected return type after function definition",
    "ExpectedArrow": " Expected -> after function name in function definition",
    "ExpectedIdentifier": " ",
    "CodeBlockEmpty": " Expected code after '{}'",
    "MissingParameters": " Expected Parameters for '{}'",
    "WrongListLength": " Expected list with length of '{}' got length '{}' instead",
    "ArgumentCount": " Expected '{}' arguments got '{}' arguments instead",
    "WrongVariableAssignment": " Expected value of type '{}' for variable '{}' got value of type '{}' instead",
}


# throw_error :: str → list → None
def throw_error(key: str, *args):
    """ Prints an error message to the terminal based on the key: argument. The message is filled with data from the *args argument
        Including the file name and file line the error is found on.
        Then exits the program

            Parameters
            ----------
            key : str
                The key for the desired error message

            *args :
                The list of valuas to format into the error message
    """
    if key in error_dict:
        print(("[FILE: '{}', LINE: '{}']"+error_dict[key]).format(*args))
        exit()
    else:
        print("[FILE: '{}', LINE: '{}'] Unknown Error".format(*args))
        exit()


# throw_error_runtime :: str → list → None
def throw_error_runtime(key: str, *args):
    """ Prints an error message to the terminal based on the key: argument. The message is filled with data from the *args argument
        Excluding the file name and file line as these are not know during runtime
        Then exits the program

            Parameters
            ----------
            key : str
                The key for the desired error message

            *args :
                The list of values to format into the error message
    """
    if key in error_dict:
        print(("[RuntimeError]" + (error_dict[key])).format(*args))
        exit()
    else:
        print("[RuntimeError] Unknown Error")
        exit()


# throw_error_with_token :: str → LEX_Type → None
def throw_error_with_token(key: str, token: LEX_Type):
    """ Prints an error message to the terminal based on the key: argument. The message is filled with data from the token argument
        Including the file name and file line the error is found on.
        Then exits the program

            Parameters
            ----------
            key : str
                The key for the desired error message

            token : LEX_Type
                A token holding the necessary information for the error message
    """
    throw_error(key, token.file, token.line, token.value, token.type)

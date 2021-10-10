class LEX_Type:
    """ Default class for LEX_Tokens ensures that all child classes can be passed as function arguments

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
        line:
            The location of the token in a file
        file_name:
            The name of the file where the token is found
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        self.value: str = value
        self.type: str = "BasicToken"
        self.line: int = line
        self.file: str = file_name

    def __str__(self) -> str:
        """ Returns a string version of the object

            Returns
            -------
            str
                A string version of the object
        """
        return "LexToken("+self.type + ": " + self.value + ")"


class LEX_Keyword(LEX_Type):
    """ Class for Keyword tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Keyword"


class LEX_Types(LEX_Type):
    """ Class for Type tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Type"


class LEX_Identifier(LEX_Type):
    """ Class for Identifier tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Identifier"


class LEX_Operator(LEX_Type):
    """ Class for Operator tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Operator"


class LEX_RelationalOperator(LEX_Type):
    """ Class for RelationalOperator tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "RelationalOperator"


class LEX_AssignmentOperator(LEX_Type):
    """ Class for AssignmentOperator tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "AsignmentOperator"


class LEX_Bracket(LEX_Type):
    """ Class for Bracket tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Bracket"


class LEX_Primitive(LEX_Type):
    """ Class for Primitive tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.type: str = "Primitive"

class LEX_Bool(LEX_Primitive):
    """ Class for Boolean tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        """ Initialize the object and sets the correct type

                Parameters
                ----------
                value : str
                    The value of the token

        """
        super().__init__(value, file_name, line)
        self.subtype: str = "Bool"


class LEX_Numerical(LEX_Primitive):
    """ Class for Numerical tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        super().__init__(value, file_name, line)
        self.subtype: str = "Number"


class LEX_String(LEX_Primitive):
    """ Class for String tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        super().__init__(value, file_name, line)
        self.subtype: str = "String"


class LEX_Other(LEX_Type):
    """ Class for Other tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        super().__init__(value, file_name, line)
        self.type: str = "Other"


class LEX_LineEnd(LEX_Type):
    """ Class for LineEnd tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        super().__init__(value, file_name, line)
        self.type: str = "LineEnd"


class LEX_ItemLister(LEX_Type):
    """ Class for ItemLister tokens

        Attributes
        ----------
        value : str
            The value of the token
        type : str
            The type of the token
    """
    def __init__(self, value: str, file_name: str, line: int):
        super().__init__(value, file_name, line)
        self.type: str = "ItemLister"
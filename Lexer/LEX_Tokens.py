class LEX_Type:
    def __init__(self, value: str):
        self.value: str = value


class LEX_Keyword(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Keyword"


class LEX_Types(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Type"


class LEX_Identifier(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Identifier"


class LEX_Operator(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Operator"


class LEX_BinairyOperator(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "BinairyOperator"


class LEX_AssignmentOperator(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "AsignmentOperator"


class LEX_Bracket(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Bracket"


class LEX_Primitive(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Primitive"

class LEX_Bool(LEX_Primitive):
    def __init__(self, value: str):
        super().__init__(value)
        self.subtype: str = "Bool"


class LEX_Numerical(LEX_Primitive):
    def __init__(self, value: str):
        super().__init__(value)
        self.subtype: str = "Number"


class LEX_String(LEX_Primitive):
    def __init__(self, value: str):
        super().__init__(value)
        self.subtype: str = "String"


class LEX_Other(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "Other"


class LEX_LineEnd(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "LineEnd"


class LEX_ItemLister(LEX_Type):
    def __init__(self, value: str):
        super().__init__(value)
        self.type: str = "ItemLister"
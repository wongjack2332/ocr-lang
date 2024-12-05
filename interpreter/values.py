class ValueType:
    def __init__(self, value_type: str) -> None:
        self.value_type = self.__parse_type(value_type)

    def __parse_type(self, value_type: str) -> str:
        available_types = (
            'NULL',
            'NUMBER',
            'STRING',
            'BOOLEAN',
            'EXT_FUNC_NAME'
        )

        if value_type in available_types:
            return value_type
        raise ValueError(f'Invalid value type: {value_type}')


class RuntimeVal:
    def __init__(self, value_type: str, value=None, access_type='NORM') -> None:
        self.value_type: ValueType = ValueType(value_type)
        self.value = value
        self.access_type = access_type

    def get_type(self):
        return self.value_type.value_type

    def get_access_type(self):
        return self.access_type

    def set_const(self):
        self.access_type = 'CONST'

    def is_const(self):
        return self.access_type == 'CONST'

    def __str__(self):
        return str(self.value)


class BoolVal(RuntimeVal):
    def __init__(self, value: bool = False) -> None:
        super().__init__('BOOLEAN')
        self.value: bool = value

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return self.value


class NullVal(RuntimeVal):
    def __init__(self) -> None:
        super().__init__('NULL')
        self.value = None

    def __str__(self):
        return 'None'


class NumberVal(RuntimeVal):
    def __init__(self, value: int = 0) -> None:
        super().__init__('NUMBER')
        self.value: int = value

    def __str__(self):
        return str(self.value)

class StringVal(RuntimeVal):
    def __init__(self, value: str = '') -> None:
        super().__init__('STRING')
        self.value: str = value

class ExtFuncName(RuntimeVal):
    def __init__(self, value: str = '') -> None:
        super().__init__('EXT_FUNC_NAME')
        self.value: str = value # name of function in python 


def MK_NUMBER(value: int = 0) -> NumberVal:
    return NumberVal(value)


def MK_NULL() -> NullVal:
    return NullVal()


def MK_BOOL(value: bool = True) -> BoolVal:
    return BoolVal(value)


def MK_STRING(value: str = '') -> StringVal:
    return StringVal(value)

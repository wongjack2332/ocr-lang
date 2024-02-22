class ValueType:
    def __init__(self, value_type: str) -> None:
        self.value_type = self.__parse_type(value_type)

    def __parse_type(self, value_type: str) -> str:
        available_types = (
            'NULL',
            'NUMBER',
            'BOOLEAN'
        )

        if value_type in available_types:
            return value_type
        raise ValueError(f'Invalid value type: {value_type}')


class RuntimeVal:
    def __init__(self, value_type: str, value=None) -> None:
        self.value_type: ValueType = ValueType(value_type)
        self.value = value

    def get_type(self):
        return self.value_type.value_type

    def __str__(self):
        return str(self.value)


class BoolVal(RuntimeVal):
    def __init__(self, value: bool = False) -> None:
        super().__init__('BOOLEAN')
        self.value: bool = value

    def __str__(self):
        return str(self.value)


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


def MK_NUMBER(value: int = 0) -> NumberVal:
    return NumberVal(value)


def MK_NULL() -> NullVal:
    return NullVal()

def MK_BOOL(value: bool = True) -> BoolVal:
    return BoolVal(value)

class ValueType:
    def __init__(self, value_type: str) -> None:
        self.value_type = self.__parse_type(value_type)

    def __parse_type(self, value_type: str) -> str:
        available_types = (
            'NULL',
            'NUMBER'
        )

        if value_type in available_types:
            return value_type
        raise ValueError(f'Invalid value type: {value_type}')


class RuntimeVal:
    def __init__(self, value_type: str) -> None:
        self.value_type: ValueType = ValueType(value_type)

    def get_type(self):
        return self.value_type.value_type


class NullVal(RuntimeVal):
    def __init__(self) -> None:
        super().__init__('NULL')


class NumberVal(RuntimeVal):
    def __init__(self, value: int) -> None:
        super().__init__('NUMBER')
        self.value: int = value

    def __str__(self):
        return str(self.value)

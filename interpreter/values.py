from typing import Any, Self


class ValueType:
    def __init__(self, value_type: str) -> None:
        self.value_type = self.__parse_type(value_type)

    def __parse_type(self, value_type: str) -> str:
        available_types = (
            'NULL',
            'NUMBER',
            'STRING',
            'BOOLEAN',
            'EXT_NAME',
            'LIST'
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
        self.value: int | float = value

    def __str__(self):
        return str(self.value)

class StringVal(RuntimeVal):
    def __init__(self, value: str = '') -> None:
        super().__init__('STRING')
        self.value: str = value
        self.length = len(self.value)
        self.attribute_set = {
            "value": self.value,
            "length": MK_NUMBER(self.length)
        }

        self.method_set = {
            "substring": self.substring,
            "left": self.left,
            "right": self.right,
            "upper": self.upper,
            "lower": self.lower
        }
    

    def substring(self, x, i):
        """returns i characters starting from x"""
        return MK_STRING(self.value[x.value:x.value+i.value])
    
    def left(self, i):
        return MK_STRING(self.value[:i.value])
    
    def right(self, i):
        return MK_STRING(self.value[-i.value:])
    
    def upper(self):
        return MK_STRING(self.value.upper())
    
    def lower(self):
        return MK_STRING(self.value.lower())
    
    @staticmethod
    def ASC(char):
        return ord(char.value)
    
    @staticmethod
    def CHR(num):
        return chr(num.value)
    
    def get_index(self, index: int) -> Any:
        if index >= self.length:
            raise IndexError(f"INDEX IS TOO LARGE, INDEX = {index}, LENGTH = {self.length}")
        

        return self.value[index]
    
    def __add__(self, other):
        return MK_STRING(self.value + other.value)
    
    def __repr__(self) -> str:
        return self.value


class ExtName(RuntimeVal):
    def __init__(self, value: str = '') -> None:
        super().__init__('EXT_NAME')
        self.value: str = value # name of function in python 
    
    def get_type(self) -> str:
        return 'EXT_NAME'


class ObjectVal(RuntimeVal):
    def __init__(self, value: object) -> None:
        super().__init__('OBJECT')
        self.value: object = value
    
    def get_type(self) -> str:
        return self.value.get_name()

class ListVal(RuntimeVal):
    def __init__(self, value: list[Any]=[]) -> None:
        super().__init__('LIST')
        self.value: list[Any] = value
        self.length = len(self.value)
        self.attribute_set = {
            "length": MK_NUMBER(self.length)
        }
        self.method_set = {
            "append": self.append,
            "pop": self.pop,
            "insert": self.insert,
            "slice": self.slice_,
            "head": self.head,
            "tail": self.tail

        }
    
    def append(self, value: Any) -> Any:
        self.value.append(value)
        self.length += 1
        return MK_LIST(self.value)
    
    def pop(self, i=-1) -> Any:
        self.length -= 1
        return MK_VALUE(self.value.pop(i))
    
    def insert(self, i, value) -> Any:
        self.length += 1
        self.value.insert(i, value)
        return MK_LIST(self.value)
    
    def slice_(self, start, n) -> Any:
        """returns n characters from start"""
        return MK_LIST(self.value[start.value:start.value+n.value])
    
    def head(self, n=None) -> Any:
        if n is None:
            return self.value[0]
        return MK_LIST(self.value[:n.value])
    
    def tail(self, n=None) -> Any:
        """returns the rest of the array starting from n(inclusive)"""
        if n is None:
            return MK_LIST(self.value[1:])
        return MK_LIST(self.value[-n.value:])

    def get_index(self, index: int) -> Any:
        if index >= self.length:
            raise IndexError(f"INDEX IS TOO LARGE, INDEX = {index}, LENGTH = {self.length}")
        
        return self.value[index]
            
    def set_index(self, index: int, value: Any) -> None:
        if index >= self.length:
            raise IndexError(f"INDEX IS TOO LARGE, INDEX = {index}, LENGTH = {self.length}")
        
        self.value[index] = value
     
    def __str__(self) -> str:
        def get_list_str(lst):
            s = "["
            for i in lst:
                if isinstance(i, list):
                    s += get_list_str(i) + ","
                    continue
                s += str(i) + ","
            s += "]"
            return s
        
        s = get_list_str(self.value)
        return s
    
    def get_type(self) -> str:
        return "LIST_VAL"


def MK_VALUE(value) -> RuntimeVal:
    value_type = type(value)
    if value_type == int:
        return MK_NUMBER(value)
    elif value_type == str:
        return MK_STRING(value)
    elif value_type == bool:
        return MK_BOOL(value)
    elif value_type == list:
        return MK_LIST(value)
    else:
        raise TypeError(f"INVALID TYPE: invalid type of value: {value_type}, unable to create value")

def MK_LIST(value: list[Any]=[]) -> ListVal:
    return ListVal(value)

def MK_NUMBER(value: int | float = 0) -> NumberVal:
    return NumberVal(value)


def MK_NULL() -> NullVal:
    return NullVal()


def MK_BOOL(value: bool = True) -> BoolVal:
    return BoolVal(value)


def MK_STRING(value: str = '') -> StringVal:
    return StringVal(value)


def is_iterable(value: RuntimeVal) -> bool:
    return 'get_index' in dir(value)

def is_mutable_iterable(value: RuntimeVal) -> bool:
    return 'set_index' in dir(value)
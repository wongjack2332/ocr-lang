from . import RuntimeVal


class Environment:
    def __init__(self, parent = None) -> None:
        self.parent = parent
        self.variables: dict[str, RuntimeVal] = {}  # identifier: value

    def declare_var(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        if varname in self.variables:
            raise ValueError(f'Variable {varname} already declared')

        self.variables[varname] = value
        return value

    def assign_var(self, varname: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(varname)
        env.variables[varname] = value

        return value

    def get_var(self, varname: str) -> RuntimeVal:
        env = self.resolve(varname)
        return env.variables[varname]

    def resolve(self, varname: str):
        if varname in self.variables:
            return self
        if self.parent is None:
            raise ValueError(f'Variable {varname} not found')
        return self.parent.resolve(varname)

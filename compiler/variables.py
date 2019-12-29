from exceptions import VariableMultipleDefinition


class VariablesManager():

    def __init__(self):
        self.variables = set()
        self.arrays = set()

    def is_variable_declared(self, var):
        return var in self.variables

    def is_array_declared(self, array):
        return array in self.arrays

    def add_variable(self, var, lineno):
        if self.is_variable_declared(var):
            raise VariableMultipleDefinition(f'{lineno}: Variable {var} is already defined')

        self.variables.add(var)

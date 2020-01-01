from exceptions import (ArrayMultipleDeclaration, ArrayWrongSizeDeclaration,
                        VariableMultipleDeclaration)


class VariablesManager():

    def __init__(self):
        self.variables = list()
        self.arrays = list()

    def is_variable_declared(self, var):
        return var in self.variables

    def is_array_declared(self, array):
        return array in self.arrays

    def add_variable(self, var, lineno):
        if self.is_variable_declared(var):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {var} is already defined')
        self.variables.append(var)

    def add_array(self, name, start, end, lineno):
        array = Array(name, start, end, lineno)
        if self.is_array_declared(array):
            raise ArrayMultipleDeclaration(f'{lineno}: Array {name} is already defined')
        elif self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {name} is already defined')
        self.arrays.append(array)


class Array():

    def __init__(self, name, start, end, lineno):
        if not self._is_start_before_end(start, end):
            raise ArrayWrongSizeDeclaration(f'{lineno}: Starting index of array must be bigger than ending.')
        self.name = name
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'{self.name}({self.start}:{self.end})'

    def _is_start_before_end(self, start, end):
        return start <= end

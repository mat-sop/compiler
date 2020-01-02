from exceptions import (ArrayMultipleDeclaration, ArrayWrongSizeDeclaration,
                        VariableMultipleDeclaration)


class MemoryManager():

    def __init__(self):
        self._variables = list()
        self._arrays = list()
        self._iterators = list()

        self._first_free_index = 0

        self._determine_called = False

    def is_variable_declared(self, name):
        return name in [v.name for v in self._variables]

    def is_array_declared(self, name):
        return name in [a.name for a in self._arrays]

    def add_variable(self, name, lineno):
        if self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {name} is already defined')
        self._variables.append(Variable(name))

    def add_array(self, name, start, end, lineno):
        array = Array(name, start, end, lineno)
        if self.is_array_declared(name):
            raise ArrayMultipleDeclaration(f'{lineno}: Array {name} is already defined')
        elif self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {name} is already defined')
        self._arrays.append(array)

    def determine_indexes_in_memory(self):  # shoudl be called only once after DECLARE

        if self._determine_called:
            return
        print('declare')
        for v in self._variables + self._arrays:
            v.index_in_memory = self._first_free_index
            self._first_free_index += v.length

        self._determine_called = True

    def get_variable(self, name):
        for v in self._variables:
            if v.name == name:
                return v


class Variable():

    def __init__(self, name):
        self.name = name
        self.index_in_memory = None
        self.length = 1

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.name


class Array():

    def __init__(self, name, start, end, lineno):
        if not self._is_start_before_end(start, end):
            raise ArrayWrongSizeDeclaration(f'{lineno}: Starting index of array must be bigger than ending.')
        self.name = name
        self.start = start
        self.end = end
        self.index_in_memory = None

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'{self.name}({self.start}:{self.end})'

    def _is_start_before_end(self, start, end):
        return start <= end

    @property
    def length(self):
        return self.end - self.start + 1

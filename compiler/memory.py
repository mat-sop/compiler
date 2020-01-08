from exceptions import (ArrayMultipleDeclaration, ArrayWrongSizeDeclaration,
                        VariableMultipleDeclaration)

import re
from lexer import t_NUM, SEPARATOR


class MemoryManager():

    def __init__(self):
        self._variables = list()
        self._arrays = list()
        self._iterators = list()

        self._first_free_index = 1

        self._determine_called = False

    def is_variable_declared(self, name):
        return name in [v.name for v in self._variables]

    def is_array_declared(self, name):
        return name in [a.name for a in self._arrays]

    def add_variable(self, name, lineno):
        if self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {name} is already defined')
        self._variables.append(Variable(name, self._first_free_index))
        self._first_free_index += 1

    def add_array(self, name, start, end, lineno):
        array = Array(name, start, end, lineno)
        if self.is_array_declared(name):
            raise ArrayMultipleDeclaration(f'{lineno}: Array {name} is already defined')
        elif self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'{lineno}: Variable {name} is already defined')

        array.index = self._first_free_index
        self._first_free_index += array.length
        self._arrays.append(array)

    def get_variable(self, name):
        for v in self._variables:
            if v.name == name:
                return v

    def get_array(self, name):
        for a in self._arrays:
            if a.name == name:
                return a

    def get_index(self, identifier):
        additional_commands = []
        if SEPARATOR not in identifier:  # single variable
            return self.get_variable(identifier).index, additional_commands,

        else:  # array
            name, a_index = identifier.split(SEPARATOR)
            if re.compile(t_NUM).match(a_index):  # id(num)
                return self.get_array(name).index + int(a_index), additional_commands

            else:
                return '1', additional_commands

class Variable():

    def __init__(self, name, index):
        self.name = name
        self.index = index
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
        self.index = None

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

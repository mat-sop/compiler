from exceptions import (ArrayMultipleDeclaration, ArrayWrongSizeDeclaration,
                        VariableMultipleDeclaration)

import re
from lexer import t_NUM, SEPARATOR


class MemoryManager():

    def __init__(self):
        self._variables = list()
        self._arrays = list()
        self.iterators = list()
        self.constants = set()

        self._first_free_index = 11

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
        self.add_constant(array.index)
        self._first_free_index += array.length
        self._arrays.append(array)

    def add_constant(self, n):
        self.constants.add(int(n))

    def add_iterator(self, name):
        v = Variable(name, self._first_free_index)
        self.iterators.append(v)
        self._first_free_index += 1
        return v.index

    def remove_iterator(self, name):
        self.iterators.remove(Variable(name, 0))

    def get_variable(self, name):
        for v in self._variables + self.iterators:
            if v.name == name:
                return v

    def get_array(self, name):
        for a in self._arrays:
            if a.name == name:
                return a

    def get_index(self, identifier):
        if 'const_' in identifier:
            return identifier, []
        additional_commands = []
        if SEPARATOR not in identifier:  # single variable
            v = self.get_variable(identifier)
            if v is None:
                return 
            return v.index, additional_commands,

        else:  # name(const)
            array_name, array_index = identifier.split(SEPARATOR)
            if re.compile(t_NUM).match(array_index):  # id(num)
                return self.get_array(array_name).get_index(int(array_index)), additional_commands

            else:   # name(identifier)
                name, identifier = identifier.split(SEPARATOR)
                id_index, additional_commands = self.get_index(identifier)
                array = self.get_array(name)
                new_index = self._first_free_index
                self._first_free_index += 1

                additional_commands += [
                    f'LOAD {id_index}',
                    f'JNEG k_4',
                    f'LOAD const_{array.index}',
                    f'ADD {id_index}',
                    f'JUMP k_3',
                    f'LOAD const_{array.index}',
                    f'SUB {id_index}',

                    f'STORE {new_index}',
                    f'LOADI {new_index}',
                    f'STORE {new_index}'
                ]
                return new_index, additional_commands

    def get_free_index(self):
        i = self._first_free_index
        self._first_free_index += 1
        return i


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

    def get_index(self, i):
        if i > 0:
            return self.index + i
        else:
            return self.index - i

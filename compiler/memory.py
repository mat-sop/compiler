from exceptions import (ArrayWrongSizeDeclaration, VariableMultipleDeclaration,
                        VariableNotDeclared, VariableNotInitialized)

from config import CONST_PREFIX, DYNAMIC_PREFIX, ITERATOR_PREFIX, STATIC_PREFIX


class MemoryManager():

    def __init__(self):
        self.variables = list()
        self.arrays = list()
        self.iterators = list()
        self.constants = set()

        self.first_free_index = 20

    def is_variable_declared(self, name):
        for v in self.variables:
            if v.name == name:
                return True
        return False

    def initialize_variable(self, name):
        v = self.get_variable(name)
        v.initialized = True

    def raise_error_if_variable_not_initialized(self, name, lineno):
        if CONST_PREFIX in name:
            return
        elif not self.get_variable(name).initialized:
            raise VariableNotInitialized(f'Błąd w linii {lineno}: użycie niezainicjowanej zmiennej {name}')

    def add_variable(self, name, lineno):
        if self.is_variable_declared(name):
            raise VariableMultipleDeclaration(f'Błąd w linii {lineno-1}: druga deklaracja {name}')

        self.variables.append(Variable(name, self.first_free_index))
        self.first_free_index += 1

    def add_array(self, name, start, end, lineno):
        array = Array(name, start, end, lineno)
        array.set_starting_index(self.first_free_index)
        self.first_free_index += array.length
        self.arrays.append(array)

    def add_constant(self, n):
        self.constants.add(int(n))

    def get_variable(self, name):
        for v in self.variables:
            if v.name == name:
                return v

    def get_array(self, name):
        for a in self.arrays:
            if a.name == name:
                return a

    def get_index(self, identifier, lineno, dynamic_assign=False):
        if CONST_PREFIX in identifier:  # NUM
            return identifier, []

        elif STATIC_PREFIX in identifier:  # name(const)
            array_name, array_index = identifier.split(STATIC_PREFIX)
            return self.get_array(array_name).get_index(int(array_index)), []

        elif DYNAMIC_PREFIX in identifier:  # name(identifier)
            name, identifier = identifier.split(DYNAMIC_PREFIX)
            id_index, additional_commands = self.get_index(identifier, lineno)
            array = self.get_array(name)
            self.add_constant(array.index_of_0)
            new_index = self.first_free_index
            self.first_free_index += 1

            additional_commands += [
                f'LOAD {CONST_PREFIX}{array.index_of_0}',
                f'ADD {id_index}',
                f'STORE {new_index}'
            ]

            if not dynamic_assign:
                additional_commands += [
                    f'LOADI {new_index}',
                    f'STORE {new_index}'
                ]
            return new_index, additional_commands

        else:  # single variable
            v = self.get_variable(identifier)
            if v is None:  # probably iterator
                return f'{ITERATOR_PREFIX}{identifier}', []
            return v.index, []

    def get_free_index(self):
        i = self.first_free_index
        self.first_free_index += 1
        return i


class Variable():

    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.length = 1
        self.initialized = False

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.name


class Array():

    def __init__(self, name, start, end, lineno):
        if not self._is_start_before_end(start, end):
            raise ArrayWrongSizeDeclaration(
                f'Błąd w linii {lineno-1}: niewłaściwy zakres tablicy {name}')
        self.name = name
        self.start = start
        self.end = end
        self.index_start = None
        self.index_of_0 = None

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

    def set_starting_index(self, index):
        self.index_start = index
        self.index_of_0 = self.index_start - self.start

    def get_index(self, index):
        return self.index_of_0 + index

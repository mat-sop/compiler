from config import CONST_PREFIX, DYNAMIC_PREFIX, ITERATOR_PREFIX, STATIC_PREFIX


class MemoryManager():

    def __init__(self):
        self.variables = list()
        self.arrays = list()
        self.iterators = list()
        self.constants = set()

        self.first_free_index = 20

    def add_variable(self, name, lineno):
        self.variables.append(Variable(name, self.first_free_index))
        self.first_free_index += 1

    def add_array(self, name, start, end, lineno):
        array = Array(name, start, end, lineno)
        array.index = self.first_free_index
        self.add_constant(array.index)
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

    def get_index(self, identifier, dynamic_assign=False):
        if CONST_PREFIX in identifier:  # NUM
            return identifier, []

        elif STATIC_PREFIX in identifier:  # name(const)
            array_name, array_index = identifier.split(STATIC_PREFIX)
            return self.get_array(array_name).get_index(int(array_index)), []

        elif DYNAMIC_PREFIX in identifier:  # name(identifier)
            name, identifier = identifier.split(DYNAMIC_PREFIX)
            id_index, additional_commands = self.get_index(identifier)
            array = self.get_array(name)
            new_index = self.first_free_index
            self.first_free_index += 1

            additional_commands += [
                f'LOAD {id_index}',
                f'JNEG k_4',
                f'LOAD {CONST_PREFIX}{array.index}',
                f'ADD {id_index}',
                f'JUMP k_3',
                f'LOAD {CONST_PREFIX}{array.index}',
                f'SUB {id_index}',

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
                f'{lineno}: Starting index of array must be bigger than ending.')
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

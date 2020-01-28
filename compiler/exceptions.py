class VariableMultipleDeclaration(Exception):
    '''Variable defined multiple times.'''


class VariableNotDeclared(Exception):
    '''Variable used without declaration.'''


class VariableNotInitialized(Exception):
    '''Variable accessed when not yet initialized'''


class ArrayWrongSizeDeclaration(Exception):
    '''Startind index of array was bigger than ending'''


class ArrayMultipleDeclaration(Exception):
    '''Array defined multiple times.'''

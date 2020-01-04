def read(identifier, memory_manager):
    index = memory_manager.get_index(identifier)
    return [
        'GET',
        f'STORE {index}'
    ]


def write(identifier, memory_manager):
    index = memory_manager.get_index(identifier)
    return [
        f'LOAD {index}',
        'PUT'
    ]


def assign(identifier, expression, memory_manager):
    index = memory_manager.get_index(identifier)
    return expression + [
        f'STORE {index}'
    ]


def plus(identifier1, identifier2, memory_manager):
    index1 = memory_manager.get_index(identifier1)
    index2 = memory_manager.get_index(identifier2)
    return [
        f'LOAD {index1}',
        F'ADD {index2}'
    ]

def minus(identifier1, identifier2, memory_manager):
    index1 = memory_manager.get_index(identifier1)
    index2 = memory_manager.get_index(identifier2)
    return [
        f'LOAD {index1}',
        F'SUB {index2}'
    ]

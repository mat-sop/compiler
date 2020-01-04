def read(name, memory_manager):
    var = memory_manager.get_variable(name)
    return [
        'GET',
        f'STORE {var.index}'
    ]


def write(name, memory_manager):
    var = memory_manager.get_variable(name)
    return [
        f'LOAD {var.index}',
        'PUT'
    ]


def assign(name, expression, memory_manager):
    var = memory_manager.get_variable(name)
    return expression + [
        f'STORE {var.index}'
    ]


def plus(name1, name2, memory_manager):
    var1 = memory_manager.get_variable(name1)
    var2 = memory_manager.get_variable(name2)
    return [
        f'LOAD {var1.index}',
        F'ADD {var2.index}'
    ]

def minus(name1, name2, memory_manager):
    var1 = memory_manager.get_variable(name1)
    var2 = memory_manager.get_variable(name2)
    return [
        f'LOAD {var1.index}',
        F'SUB {var2.index}'
    ]

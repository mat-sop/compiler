def read(identifier, memory_manager):
    commands, index = memory_manager.get_index(identifier)
    return commands + [
        'GET',
        f'STORE {index}'
    ]


def write(identifier, memory_manager):
    commands, index = memory_manager.get_index(identifier)
    return commands + [
        f'LOAD {index}',
        'PUT'
    ]


def assign(identifier, expression, memory_manager):
    index, commands = memory_manager.get_index(identifier)
    return expression + commands + [
        f'STORE {index}'
    ]


def plus(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'ADD {index2}'
    ]


def minus(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}'
    ]


def con_eq(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JZERO eq_jzero_2',
        'INC'
    ]


def if_then(condition, commands):
    return condition + [

    ]

def determine_jumps(commands):
    for i in range(len(commands)):
        if 'eq_jzero' in commands[i]:
            k_diff = int(commands[i].split('_')[-1])
            commands[i] = f'JZERO {i+k_diff}'
    return commands

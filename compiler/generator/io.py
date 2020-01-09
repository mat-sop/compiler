def read(identifier, memory_manager):
    index, commands = memory_manager.get_index(identifier)
    return commands + [
        'GET',
        f'STORE {index}'
    ]


def write(identifier, memory_manager):
    index, commands = memory_manager.get_index(identifier)
    return commands + [
        f'LOAD {index}',
        'PUT'
    ]

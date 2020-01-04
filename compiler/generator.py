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

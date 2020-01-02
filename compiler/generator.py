def read(name, memory_manager):
    var = memory_manager.get_variable(name)
    print(var.name)
    return [
        'PUT',
        f'STORE {var.index_in_memory}'
    ]

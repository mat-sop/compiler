def assign(identifier, expression, memory_manager):
    index, commands = memory_manager.get_index(identifier)
    return expression + commands + [
        f'STORE {index}'
    ]

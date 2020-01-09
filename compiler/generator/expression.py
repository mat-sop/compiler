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

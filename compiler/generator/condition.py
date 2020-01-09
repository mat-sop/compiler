set_true = ['SUB 0', 'INC']
set_false = ['SUB 0']


def con_eq(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JZERO k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_neq(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JZERO k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]


def con_le(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JNEG k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_ge(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JPOS k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_leq(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JPOS k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]


def con_geq(identifier1, identifier2, memory_manager):
    index1, commands1 = memory_manager.get_index(identifier1)
    index2, commands2 = memory_manager.get_index(identifier2)
    return commands1 + commands2 + [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JNEG k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]

set_true = ['SUB 0', 'INC']
set_false = ['SUB 0']


def con_eq(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JZERO k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_neq(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JZERO k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]


def con_le(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JNEG k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_ge(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JPOS k_{len(set_false)+2}',
        *set_false,
        f'JUMP k_{len(set_true)+1}',
        *set_true
    ]


def con_leq(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JPOS k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]


def con_geq(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}',
        f'JNEG k_{len(set_true)+2}',
        *set_true,
        f'JUMP k_{len(set_false)+1}',
        *set_false
    ]

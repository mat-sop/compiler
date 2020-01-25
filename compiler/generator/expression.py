from .condition import con_ge, con_geq
from .loop import while_do


def value(index):
    return [
        f'LOAD {index}'
    ]


def plus(index1, index2):
    return [
        f'LOAD {index1}',
        f'ADD {index2}'
    ]


def minus(index1, index2):
    return [
        f'LOAD {index1}',
        f'SUB {index2}'
    ]


def times(index1, index2):
    '''
    def t(a, b):
        result = 0
        factor = 1
        left = -b if b < 0 else b
        while left > factor:  # loop_1
            factor *= 2
        while left > 0:  # loop_2
            while (factor - 1) > left:  # loop_3
                factor /= 2
            result += factor * a
            left = left - factor
        return result if b > 0 else -result
    '''
    a = index1
    b = index2
    result = 6
    factor = 5
    left = 4
    shift = 3
    factor_pow = 2
    tmp = 9
    zero = 10

    initialize = [
        'SUB 0',
        f'STORE {result}',  # result = 0
        f'STORE {zero}',
        f'STORE {factor_pow}',

        'INC',
        f'STORE {factor}',  # factor = 1
        f'STORE {shift}',   # shift = 1

        f'LOAD {b}',
        'JPOS k_3',
        'SUB 0',
        f'SUB {b}',
        f'STORE {left}',  # left = -b if b < 0 else b
    ]
    con_loop_1 = con_ge(left, factor)  # left > factor
    loop_1 = [  # factor *= 2, factor_pow += 1
        f'LOAD {factor}',
        f'SHIFT {shift}',
        f'STORE {factor}',
        f'LOAD {factor_pow}',
        'INC',
        f'STORE {factor_pow}'
    ]
    con_loop_3 = con_ge(factor, left)  # factor > left
    loop_3 = [  # factor /= 2, factor_pow -= 1
        f'LOAD {factor}',
        f'SHIFT {shift}',
        f'STORE {factor}',
        f'LOAD {factor_pow}',
        'DEC',
        f'STORE {factor_pow}',
    ]
    con_loop_2 = con_ge(left, zero)
    loop_2 = [
        *while_do(con_loop_3, loop_3),

        f'LOAD {a}',  # result += factor * a
        f'SHIFT {factor_pow}',
        f'STORE {tmp}',
        f'LOAD {result}',
        f'ADD {tmp}',
        f'STORE {result}',
        f'LOAD {left}',  # left = left - factor
        f'SUB {factor}',

        f'STORE {left}'
    ]
    fix_sign = [
        f'LOAD {b}',
        'JPOS k_5',
        f'LOAD {result}',
        f'SUB 0',
        f'SUB {result}',
        f'STORE {result}'
    ]

    return [
        *initialize,
        *while_do(con_loop_1, loop_1),

        f'LOAD {shift}',
        'DEC',
        'DEC',
        f'STORE {shift}',  # shift = -1

        *while_do(con_loop_2, loop_2),

        *fix_sign,

        f'LOAD {result}'
    ]


def div(index1, index2):
    """
    def divide(a, b):
        q = 0
        while a >= b:
            a -= b
            q += 1
        return (q, a)
    """
    a = 2
    b = index2
    q = 3

    initialize = [
        f'LOAD {index1}',
        f'STORE {a}',
        'SUB 0',
        f'STORE {q}'
    ]
    condition = con_geq(a, b)
    loop = [
        f'LOAD {a}',
        f'SUB {b}',
        f'STORE {a}',
        f'LOAD {q}',
        'INC',
        f'STORE {q}'
    ]
    division = [
        *initialize,
        *while_do(condition, loop),
        f'LOAD {q}'
    ]
    return [
        f'LOAD {index2}',
        f'JZERO k_{len(division)+1}',
        *division,
    ]


def mod(index1, index2):
    a = 2
    b = index2
    q = 3

    initialize = [
        f'LOAD {index1}',
        f'STORE {a}',
        'SUB 0',
        f'STORE {q}'
    ]
    condition = con_geq(a, b)
    loop = [
        f'LOAD {a}',
        f'SUB {b}',
        f'STORE {a}',
        f'LOAD {q}',
        'INC',
        f'STORE {q}'
    ]
    mod = [
        *initialize,
        *while_do(condition, loop),
        f'LOAD {a}'
    ]
    return mod

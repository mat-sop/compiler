from .condition import con_ge
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
        f'LOAD {factor} # LOOP 1',
        f'SHIFT {shift}',
        f'STORE {factor}',
        f'LOAD {factor_pow}',
        'INC',
        f'STORE {factor_pow}'
    ]
    con_loop_3 = [  # (factor - 1) > left
        f'LOAD {factor}',
        'DEC',
        f'STORE {tmp}',
        *con_ge(tmp, left)
    ]
    loop_3 = [  # factor /= 2, factor_pow -= 1
        f'LOAD {factor} # LOOP 3',
        f'SHIFT {shift}',
        f'STORE {factor}',
        f'LOAD {factor_pow}',
        'DEC',
        f'STORE {factor_pow}',
    ]
    con_loop_2 = con_ge(left, zero)
    loop_2 =[
        *while_do(con_loop_3, loop_3),

        f'LOAD {a} # LOOP 2',  # result += factor * a
        f'SHIFT {factor_pow}',
        f'STORE {tmp}',
        f'LOAD {result}',
        f'ADD {tmp}',
        f'STORE {result}',
        f'LOAD {left}',  # left = left - factor
        f'SUB {factor}',

        f'STORE {left}'
    ]

    return [
        *initialize,
        *while_do(con_loop_1, loop_1),

        f'LOAD {shift}',
        'DEC',
        'DEC',
        f'STORE {shift}',  # shift = -1

        *while_do(con_loop_2, loop_2),

        f'LOAD {result}'
    ]

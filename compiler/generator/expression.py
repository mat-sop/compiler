from .condition import con_ge, con_geq, con_le
from .conditional import if_then
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
    def times(a, b):
        result = 0
        factor = 1
        left = -b if b < 0 else b con_geq,
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
    '''
    def div(index1, index2):
        a = index1
        b = index2
        factor = 1
        left = a
        result = 0
        tmp = b
        while(factor < left):  # loop1
            factor *= 2
            tmp *= 2

        while(left >= b):  # loop2
            while (tmp > left):  # loop3
                factor = factor/2
                tmp = tmp/2
            result += factor
            left = left - tmp
        return result
    '''

    factor = 2
    left = 3
    result = 4
    tmp = 5
    pow2 = 6
    a = 7
    b = 8

    initialize = [
        f'LOAD {a}',
        f'STORE {left}',
        f'LOAD {b}',
        f'STORE {tmp}',
        'SUB 0',
        f'STORE {result}',
        f'INC',
        f'STORE {factor}',
        f'STORE {pow2}'
    ]

    loop1_condition = con_le(factor, left)
    loop1_commands = [
        f'LOAD {factor}',
        f'SHIFT {pow2}',
        f'STORE {factor}',
        f'LOAD {tmp}',
        f'SHIFT {pow2}',
        f'STORE {tmp}',
    ]
    loop1 = while_do(loop1_condition, loop1_commands)

    loop3_condition = con_ge(tmp, left)
    loop3_commands = [
        f'LOAD {factor}',
        f'SHIFT {pow2}',
        f'STORE {factor}',
        f'LOAD {tmp}',
        f'SHIFT {pow2}',
        f'STORE {tmp}',
    ]
    loop3 = [
        'SUB 0',
        'DEC',
        f'STORE {pow2}',
        *while_do(loop3_condition, loop3_commands)
    ]

    loop2_condition = con_geq(left, b)
    loop2_commands = [
        *loop3,
        f'LOAD {result}',
        f'ADD {factor}',
        f'STORE {result}',
        f'LOAD {left}',
        f'SUB {tmp}',
        f'STORE {left}'
    ]
    loop2 = while_do(loop2_condition, loop2_commands)

    change_signs_to_plus = [
        f'LOAD {index1}',
        'JPOS k_3',
        f'SUB {index1}',
        f'SUB {index1}',
        f'STORE {a}',
        f'LOAD {index2}',
        'JPOS k_3',
        f'SUB {index2}',
        f'SUB {index2}',
        f'STORE {b}',
    ]

    fix_sign = [
        f'LOAD {index1}',
        'JPOS k_5',
        f'LOAD {result}',
        f'SUB {result}',
        f'SUB {result}',
        f'STORE {result}',

        f'LOAD {index2}',
        'JPOS k_5',
        f'LOAD {result}',
        f'SUB {result}',
        f'SUB {result}',
        f'STORE {result}'
    ]

    division = [
        *change_signs_to_plus,
        *initialize,
        *loop1,
        *loop2,
        *fix_sign,
        f'LOAD {result}'
    ]

    return [
        f'LOAD {index2}',
        f'JZERO k_{len(division)+3}',
        f'LOAD {index1}',
        f'JZERO k_{len(division)+1}',
        *division
    ]


def mod(index1, index2):
    '''
    def modd(index1, index2):
        a = index1
        b = index2

        scaled_divisor = b
        remain = a
        result = 0
        multiple = 1

        while(scaled_divisor < a):  # loop1
            scaled_divisor *= 2
            multiple *= 2

        tmp = True  # pythonic do-while  # loop2
        while tmp:
            if (remain >= scaled_divisor):  # if2
                remain -= scaled_divisor
                result += multiple
            scaled_divisor = scaled_divisor//2
            multiple = multiple//2
            tmp = bool(multiple != 0)

        return remain
    '''

    scaled_divisor = 2
    remain = 3
    result = 4
    multiple = 5
    pow2 = 6
    a = 7
    b = 8

    initialize = [
        f'LOAD {b}',
        f'STORE {scaled_divisor}',
        f'LOAD {a}',
        f'STORE {remain}',
        'SUB 0',
        f'STORE {result}',
        'INC',
        f'STORE {multiple}',
        f'STORE {pow2}'
    ]

    loop1_condition = con_le(scaled_divisor, a)
    loop1_commands = [
        f'LOAD {scaled_divisor}',
        f'SHIFT {pow2}',
        f'STORE {scaled_divisor}',
        f'LOAD {multiple}',
        f'SHIFT {pow2}',
        f'STORE {multiple}'
    ]
    loop1 = while_do(loop1_condition, loop1_commands)

    if1_condition = con_geq(remain, scaled_divisor)
    if1_commands = [
        f'LOAD {remain}',
        f'SUB {scaled_divisor}',
        f'STORE {remain}',
        f'LOAD {result}',
        f'ADD {multiple}',
        f'STORE {result}'
    ]
    if1 = if_then(if1_condition, if1_commands)

    loop2_commands = [
        *if1,
        f'LOAD {scaled_divisor}',
        f'SHIFT {pow2}',
        f'STORE {scaled_divisor}',
        f'LOAD {multiple}',
        f'SHIFT {pow2}',
        f'STORE {multiple}'
    ]
    loop2 = [
        'SUB 0',
        'DEC',
        f'STORE {pow2}',
        *loop2_commands,
        f'LOAD {multiple}',
        'JZERO k_2',
        f'JUMP k_{-len(loop2_commands)-2}'
    ]

    change_signs_to_plus = [
        f'LOAD {index1}',
        'JPOS k_3',
        f'SUB {index1}',
        f'SUB {index1}',
        f'STORE {a}',
        f'LOAD {index2}',
        'JPOS k_3',
        f'SUB {index2}',
        f'SUB {index2}',
        f'STORE {b}',
    ]

    fix_sign = [
        f'LOAD {index1}',
        f'JPOS k_12',
        f'LOAD {index2}',
        f'JPOS k_6',
        f'LOAD {remain}',
        f'SUB {remain}',
        f'SUB {remain}',
        f'STORE {remain}',
        f'JUMP k_3',
        f'LOAD {index2}',
        f'SUB {remain}',
        f'STORE {remain}',
        f'JUMP k_5',
        f'LOAD {index2}',
        f'JPOS k_3',
        f'ADD {remain}',
        f'STORE {remain}'
    ]

    modulo = [
        *change_signs_to_plus,
        *initialize,
        *loop1,
        *loop2
    ]

    return [
        f'LOAD {index2}',
        f'JZERO k_{len(modulo)+3}',
        f'LOAD {index1}',
        f'JZERO k_{len(modulo)+1}',
        *modulo,
        *fix_sign,
        f'LOAD {remain}'
    ]

import math

LIMIT = 64


def gen_const(n, index):   # TODO MAKE FASTER
    sign_c = 'INC' if n > 0 else 'DEC'
    pows = []
    while n > LIMIT:
        p = math.floor(math.log2(n))
        pows.append(p)
        n -= 2**p

    commands = ['SUB 0', 'STORE 2', 'STORE 1']
    last_pow = 0
    for p in reversed(pows):
        commands += ['LOAD 1']
        commands += (p - last_pow) * ['INC']
        last_pow = p
        commands += [
            'STORE 1',
            'SUB 0',
            sign_c,
            'SHIFT 1',
            'ADD 2',
            'STORE 2']
    commands += ['LOAD 2']
    commands += n * [sign_c]
    commands += [f'STORE {index}']

    return commands

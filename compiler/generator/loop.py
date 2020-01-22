def while_do(condition, expression):
    return [
        *condition,
        f'JZERO k_{len(expression)+2}',
        *expression,
        f'JUMP k_{-len(condition)-len(expression)-1}'
    ]


def do_while(condition, expression):
    return [
        *expression,
        *condition,
        f'JPOS k_{-len(condition)-len(expression)}'
    ]


def for_from(iterator, start, end, expression):
    return [
        f'LOAD {start}',
        f'STORE {iterator}',

        f'LOAD {end}',
        f'SUB {iterator}',
        f'JNEG k_{len(expression)+5}',
        *expression,
        f'LOAD {iterator}',
        'INC',
        f'STORE {iterator}',
        f'JUMP k_{-len(expression)-3-1}',
    ]

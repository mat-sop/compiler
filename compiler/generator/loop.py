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


def for_to(iterator, start, end, expression, free_index):
    return [
        f'LOAD {start}',
        f'STORE {iterator}',
        f'LOAD {end}',
        f'STORE {free_index}',

        f'LOAD {free_index}',
        f'SUB {iterator}',
        f'JNEG k_{len(expression)+5}',
        *expression,
        f'LOAD {iterator}',
        'INC',
        f'STORE {iterator}',
        f'JUMP k_{-len(expression)-6}',
    ]


def for_downto(iterator, start, end, expression, free_index):
    return [
        f'LOAD {start}',
        f'STORE {iterator}',
        '### iterator_start___{iterator}'
        f'LOAD {end}',
        f'STORE {free_index}',

        f'LOAD {iterator}',
        f'SUB {free_index}',
        f'JNEG k_{len(expression)+5}',
        *expression,
        f'LOAD {iterator}',
        'DEC',
        f'STORE {iterator}',
        '### iterator_end___{iterator}',
        f'JUMP k_{-len(expression)-6}'
    ]

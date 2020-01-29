from process import len_without_comments


def while_do(condition, expression):
    return [
        *condition,
        f'JZERO k_{len_without_comments(expression)+2}',
        *expression,
        f'JUMP k_{-len(condition)-len_without_comments(expression)-1}'
    ]


def do_while(condition, expression):
    return [
        *expression,
        *condition,
        f'JPOS k_{-len(condition)-len(expression)}'
    ]


def for_to(iterator, start, end, expression, free_index):
    return [
        f'# iterator_start_{iterator}',
        f'LOAD {start}',
        f'STORE {iterator} # IT',
        f'LOAD {end}',
        f'STORE {free_index}',
        f'LOAD {free_index}',
        f'SUB {iterator}',
        f'JNEG k_{len_without_comments(expression)+5}',
        *expression,
        f'LOAD {iterator}',
        'INC',
        f'STORE {iterator} # IT',
        f'JUMP k_{-len_without_comments(expression)-6}',
        f'# iterator_end_{iterator}'
    ]


def for_downto(iterator, start, end, expression, free_index):
    return [
        f'# iterator_start_{iterator}',
        f'LOAD {start}',
        f'STORE {iterator} # IT',
        f'LOAD {end}',
        f'STORE {free_index}',
        f'LOAD {iterator}',
        f'SUB {free_index}',
        f'JNEG k_{len_without_comments(expression)+5}',
        *expression,
        f'LOAD {iterator}',
        'DEC',
        f'STORE {iterator} # IT',
        f'JUMP k_{-len_without_comments(expression)-6}',
        f'# iterator_end_{iterator}'
    ]

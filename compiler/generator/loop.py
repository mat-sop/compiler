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

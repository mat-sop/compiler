from process import len_without_comments


def if_then(condition, commands):
    return condition + [
        f'JZERO k_{len_without_comments(commands)+1}'
    ] + commands


def if_then_else(condition, then_commands, else_commands):
    return condition + [
        f'JZERO k_{len_without_comments(then_commands)+2}',
        *then_commands,
        f'JUMP k_{len_without_comments(else_commands)+1}',
        *else_commands
    ]

from generator.const import gen_const


def process(commands, memory_manager):
    commands = resolve_constances(commands, memory_manager)
    commands = determine_jumps(commands)
    return commands


def determine_jumps(commands):
    for i in range(len(commands)):
        if 'k_' in commands[i]:
            k_diff = int(commands[i].split('_')[-1])
            jmp = commands[i].split(' ')[0]
            commands[i] = f'{jmp} {i+k_diff}'
    return commands


def resolve_constances(commands, memory_manager):
    generated = []
    constants = {}
    for n in memory_manager.constants:
        i = memory_manager.get_free_index()
        generated += gen_const(n, i)
        constants[n] = i

    for i in range(len(commands)):
        if 'const_' in commands[i]:
            n = int(commands[i].split('_')[-1])
            c = commands[i].split(' ')[0]
            commands[i] = f'{c} {constants[n]}'
    return generated + commands

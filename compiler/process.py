def determine_jumps(commands):
    for i in range(len(commands)):
        if 'k_' in commands[i]:
            k_diff = int(commands[i].split('_')[-1])
            jmp = commands[i].split(' ')[0]
            commands[i] = f'{jmp} {i+k_diff}'
    return commands

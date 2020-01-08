def determine_jumps(commands):
    for i in range(len(commands)):
        if 'k_' in commands[i]:
            k_diff = int(commands[i].split('_')[-1])
            commands[i] = f'JZERO {i+k_diff}'
    return commands

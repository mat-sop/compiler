def gen_const(n, index):
    sign_c = 'INC' if n > 0 else 'DEC'
    commands = ['SUB 0', 'INC', 'STORE 1', 'SUB 0']
    for b in bin(n)[2:]:
        commands += ['SHIFT 1']
        if b == '1':
            commands += [sign_c]
    commands += [f'STORE {index}']
    return commands

def assign(index, relative_index=False):
    return [
        f'STORE {index}' if not relative_index else f'STOREI {index}'
    ]

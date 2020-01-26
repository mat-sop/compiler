def read(index, relative_index=False):
    return [
        'GET',
        f'STORE {index}' if not relative_index else f'STOREI {index}'
    ]


def write(index):
    return [
        f'LOAD {index}',
        'PUT'
    ]

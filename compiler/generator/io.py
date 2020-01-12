def read(index):
    return [
        'GET',
        f'STORE {index}'
    ]


def write(index):
    return [
        f'LOAD {index}',
        'PUT'
    ]

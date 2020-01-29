from config import CONST_PREFIX, ITERATOR_PREFIX
from generator.const import gen_const
from exceptions import VariableNotDeclared


def process(commands, memory_manager):
    validate_iterators(commands, memory_manager)
    commands = remove_comments(commands)
    commands = resolve_constances(commands, memory_manager)
    commands = determine_jumps(commands)
    commands = resolve_iterators(commands, memory_manager)
    return commands


def len_without_comments(commands):
    return len(remove_comments(commands))


def remove_comments(commands):
    tmp = commands.copy()
    for i in range(len(tmp)):
        if '# ' in tmp[i] and '###' not in tmp[i]:
            tmp[i] = tmp[i].split(' #')[0]
    tmp = [c for c in tmp if '#' not in c]
    return [c for c in tmp if c != '']

def validate_iterators(commands, memory_manager):
    iterators = []
    for c in commands:
        if 'iterator_start' in c:
            for v in memory_manager.variables:
                if v.name == c.split(ITERATOR_PREFIX)[-1]:
                    raise Exception('uzycie zmiennej globalnej o tej samej nazwie co iterator w zakresie petli')
            iterators.append(c.split(ITERATOR_PREFIX)[-1])
        elif 'iterator_end' in c:
            iterators.remove(c.split(ITERATOR_PREFIX)[-1])
        elif ITERATOR_PREFIX in c:
            identifier = c.split(' ')[1].split('_'+ITERATOR_PREFIX)[1]
            if identifier not in iterators:
                lineno, var_name = c.split(' ')[1].split('_'+ITERATOR_PREFIX)
                raise VariableNotDeclared(f'Błąd w linii {lineno}: Niezadeklarowana zmienna {var_name}')
            if 'STORE' in c and '# IT' not in c:
                raise Exception('modyfikacja iteratora w petli')


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
        if CONST_PREFIX in commands[i]:
            n = int(commands[i].split('_')[-1])
            c = commands[i].split(' ')[0]
            commands[i] = f'{c} {constants[n]}'
    return generated + commands


def resolve_iterators(commands, memory_manager):
    indexes = {}
    for i in range(len(commands)):
        if ITERATOR_PREFIX in commands[i]:
            iterator = commands[i].split(ITERATOR_PREFIX)[-1]
            if iterator not in indexes:
                indexes[iterator] = memory_manager.get_free_index()
            index = indexes[iterator]
            c = commands[i].split(' ')[0]
            commands[i] = f'{c} {index}'
    return commands

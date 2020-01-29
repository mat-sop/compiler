import ply.yacc as yacc

from config import CONST_PREFIX, DYNAMIC_PREFIX, ITERATOR_PREFIX, STATIC_PREFIX
from generator.assign import assign
from generator.condition import (con_eq, con_ge, con_geq, con_le, con_leq,
                                 con_neq)
from generator.conditional import if_then, if_then_else
from generator.expression import div, minus, mod, plus, times, value
from generator.io import read, write
from generator.loop import do_while, for_downto, for_to, while_do
from lexer import tokens  # noqa: F401
from memory import MemoryManager

memory_manager = MemoryManager()


def p_program_declarations_commands(p):
    '''program : DECLARE declarations BEGIN commands END'''
    p[0] = p[4] + ['HALT']


def p_program_commands(p):
    '''program : BEGIN commands END'''
    p[0] = p[2] + ['HALT']


def p_declarations_declarations_id(p):
    '''declarations : declarations COMMA ID'''
    memory_manager.add_variable(p[3], p.lexer.lineno)


def p_declarations_declarations_tab(p):
    '''declarations : declarations COMMA ID LEFTB NUM COLON NUM RIGHTB'''
    memory_manager.add_array(p[3], int(p[5]), int(p[7]), p.lexer.lineno)


def p_declarations_id(p):
    '''declarations : ID'''
    memory_manager.add_variable(p[1], p.lexer.lineno)


def p_declarations_tab(p):
    '''declarations : ID LEFTB NUM COLON NUM RIGHTB'''
    memory_manager.add_array(p[1], int(p[3]), int(p[5]), p.lexer.lineno)


def p_commands_commands_command(p):
    '''commands : commands command'''
    p[0] = p[1] + p[2]


def p_commands_command(p):
    '''commands : command'''
    p[0] = p[1]


def p_command_assign(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    dynamic_array = True if DYNAMIC_PREFIX in p[1] else False
    index, commands = memory_manager.get_index(p[1], p.lexer.lineno, dynamic_array)
    memory_manager.initialize_variable(p[1], p.lexer.lineno)
    p[0] = commands + p[3] + assign(index, dynamic_array)


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    p[0] = if_then_else(p[2], p[4], p[6])


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    p[0] = if_then(p[2], p[4])


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    p[0] = while_do(p[2], p[4])


def p_command_do_while(p):
    '''command : DO commands WHILE condition ENDDO'''
    p[0] = do_while(p[4], p[2])


def p_command_for_from_to_do(p):
    '''command : FOR ID FROM value TO value DO commands ENDFOR'''
    memory_manager.raise_error_if_variable_not_initialized(p[4], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[6], p.lexer.lineno)
    start_index, commands1 = memory_manager.get_index(p[4], p.lexer.lineno)
    end_index, commands2 = memory_manager.get_index(p[6], p.lexer.lineno)
    free_index = memory_manager.get_free_index()
    p[0] = commands1 + commands2 + for_to(f'{p.lexer.lineno}_{ITERATOR_PREFIX}{p[2]}', start_index, end_index, p[8], free_index)


def p_command_for_from_downto_do(p):
    '''command : FOR ID FROM value DOWNTO value DO commands ENDFOR'''
    memory_manager.raise_error_if_variable_not_initialized(p[4], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[6], p.lexer.lineno)
    start_index, commands1 = memory_manager.get_index(p[4], p.lexer.lineno)
    end_index, commands2 = memory_manager.get_index(p[6], p.lexer.lineno)
    free_index = memory_manager.get_free_index()
    p[0] = commands1 + commands2 + for_downto(f'{p.lexer.lineno}_{ITERATOR_PREFIX}{p[2]}', start_index, end_index, p[8], free_index)

def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    memory_manager.initialize_variable(p[2], p.lexer.lineno)
    dynamic_array = True if DYNAMIC_PREFIX in p[2] else False
    index, commands = memory_manager.get_index(p[2], p.lexer.lineno, dynamic_array)
    p[0] = commands + read(index, dynamic_array)


def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    memory_manager.raise_error_if_variable_not_initialized(p[2], p.lexer.lineno-1)
    index, commands = memory_manager.get_index(p[2], p.lexer.lineno)
    p[0] = commands + write(index)


def p_expression_value(p):
    '''expression : value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    index, commands = memory_manager.get_index(p[1], p.lexer.lineno)
    p[0] = commands + value(index)


def p_expression_plus(p):
    '''expression : value PLUS value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + plus(index1, index2)


def p_expression_minus(p):
    '''expression : value MINUS value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + minus(index1, index2)


def p_expression_times(p):
    '''expression : value TIMES value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + times(index1, index2)


def p_expression_div(p):
    '''expression : value DIV value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + div(index1, index2)

def p_expression_mod(p):
    '''expression : value MOD value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + mod(index1, index2)


def p_condition_eq(p):
    '''condition : value EQ value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_eq(index1, index2)


def p_condition_neq(p):
    '''condition : value NEQ value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_neq(index1, index2)


def p_condition_le(p):
    '''condition : value LE value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_le(index1, index2)


def p_condition_ge(p):
    '''condition : value GE value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_ge(index1, index2)


def p_condition_leq(p):
    '''condition : value LEQ value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_leq(index1, index2)


def p_condition_geq(p):
    '''condition : value GEQ value'''
    memory_manager.raise_error_if_variable_not_initialized(p[1], p.lexer.lineno)
    memory_manager.raise_error_if_variable_not_initialized(p[3], p.lexer.lineno)
    index1, commands1 = memory_manager.get_index(p[1], p.lexer.lineno)
    index2, commands2 = memory_manager.get_index(p[3], p.lexer.lineno)
    p[0] = commands1 + commands2 + con_geq(index1, index2)


def p_value_num(p):
    '''value : NUM'''
    memory_manager.add_constant(p[1])
    p[0] = f'{CONST_PREFIX}{p[1]}'


def p_value_identifier(p):
    '''value : identifier'''
    p[0] = p[1]


def p_identifier_id(p):
    '''identifier : ID'''
    p[0] = p[1]


def p_identifier_tab_id(p):
    '''identifier : ID LEFTB ID RIGHTB'''
    p[0] = f'{p[1]}{DYNAMIC_PREFIX}{p[3]}'


def p_identifier_tab_num(p):
    '''identifier : ID LEFTB NUM RIGHTB'''
    p[0] = f'{p[1]}{STATIC_PREFIX}{p[3]}'


def p_error(p):
    raise Exception(f'Błąd w linii {p.lineno}: nierozpoznany napis {p.value}')


parser = yacc.yacc()

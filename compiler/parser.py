import ply.yacc as yacc

from generator.assign import assign
from generator.condition import (con_eq, con_ge, con_geq, con_le, con_leq,
                                 con_neq)
from generator.conditional import if_then, if_then_else
from generator.expression import minus, plus
from generator.io import read, write
from lexer import SEPARATOR, tokens  # noqa: F401
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
    p[0] = assign(p[1], p[3], memory_manager)


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    p[0] = if_then_else(p[2], p[4], p[6])


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    p[0] = if_then(p[2], p[4])


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''


def p_command_do_while(p):
    '''command : DO commands WHILE condition ENDDO'''


def p_command_for_from_to_do(p):
    '''command : FOR ID FROM value TO value DO commands ENDFOR'''


def p_command_for_from_downto_do(p):
    '''command : FOR ID FROM value DOWNTO value DO commands ENDFOR'''


def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    p[0] = read(p[2], memory_manager)


def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    p[0] = write(p[2], memory_manager)


def p_expression_value(p):
    '''expression : value'''
    p[0] = p[1]


def p_expression_plus(p):
    '''expression : value PLUS value'''
    p[0] = plus(p[1], p[3], memory_manager)


def p_expression_minus(p):
    '''expression : value MINUS value'''
    p[0] = minus(p[1], p[3], memory_manager)


def p_expression_times(p):
    '''expression : value TIMES value'''


def p_expression_div(p):
    '''expression : value DIV value'''


def p_expression_mod(p):
    '''expression : value MOD value'''


def p_condition_eq(p):
    '''condition : value EQ value'''
    p[0] = con_eq(p[1], p[3], memory_manager)


def p_condition_neq(p):
    '''condition : value NEQ value'''
    p[0] = con_neq(p[1], p[3], memory_manager)


def p_condition_le(p):
    '''condition : value LE value'''
    p[0] = con_le(p[1], p[3], memory_manager)


def p_condition_ge(p):
    '''condition : value GE value'''
    p[0] = con_ge(p[1], p[3], memory_manager)


def p_condition_leq(p):
    '''condition : value LEQ value'''
    p[0] = con_leq(p[1], p[3], memory_manager)


def p_condition_geq(p):
    '''condition : value GEQ value'''
    p[0] = con_geq(p[1], p[3], memory_manager)


def p_value_num(p):
    '''value : NUM'''
    memory_manager.add_constant(p[1])
    p[0] = f'const_{p[1]}'


def p_value_identifier(p):
    '''value : identifier'''
    p[0] = p[1]


def p_identifier_id(p):
    '''identifier : ID'''
    p[0] = p[1]


def p_identifier_tab_id(p):
    '''identifier : ID LEFTB ID RIGHTB'''
    p[0] = f'{p[1]}{SEPARATOR}{p[3]}'


def p_identifier_tab_num(p):
    '''identifier : ID LEFTB NUM RIGHTB'''
    p[0] = f'{p[1]}{SEPARATOR}{p[3]}'


def p_error(p):
    raise Exception(f'exception: {p.lineno}, {p.value}')


parser = yacc.yacc()

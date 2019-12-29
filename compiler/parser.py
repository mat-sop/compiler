import sys

import ply.yacc as yacc

from lexer import tokens  # noqa: F401


def p_program_declarations_commands(p):
    '''program : DECLARE declarations BEGIN commands END'''
    print('program_declarations_commands')


def p_program_commands(p):
    '''program : BEGIN commands END'''
    print('program_commands')


def p_declarations_declarations_id(p):
    '''declarations : declarations COMMA ID'''
    print('declarations_declarations_id')


def p_declarations_declarations_tab(p):
    '''declarations : declarations COMMA ID LEFTB NUM COLON NUM RIGHTB'''
    print('declarations_declarations_tab')


def p_declarations_id(p):
    '''declarations : ID'''
    print('declarations_id')


def p_declarations_tab(p):
    '''declarations : ID LEFTB NUM COLON NUM RIGHTB'''
    print('declarations_tab')


def p_commands_commands_command(p):
    '''commands : commands command'''
    print('commands_commands_command')


def p_commands_command(p):
    '''commands : command'''
    print('commands_command')


def p_command_assign(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    print('command_assign')


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    print('command_if_then_else')


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    print('command_if_then')


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    print('command_while_do')


def p_command_do_while(p):
    '''command : DO commands WHILE condition ENDDO'''
    print('command_do_while')


def p_command_for_from_to_do(p):
    '''command : FOR ID FROM value TO value DO commands ENDFOR'''
    print('command_for_from_to_do')


def p_command_for_from_downto_do(p):
    '''command : FOR ID FROM value DOWNTO value DO commands ENDFOR'''
    print('command_for_from_downto_do')


def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    print('command_read')


def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    print('command_write')


def p_expression_value(p):
    '''expression : value'''
    print('expression_value')


def p_expression_plus(p):
    '''expression : value PLUS value'''
    print('expression_plus')


def p_expression_minus(p):
    '''expression : value MINUS value'''
    print('expression_minus')


def p_expression_times(p):
    '''expression : value TIMES value'''
    print('expression_times')


def p_expression_div(p):
    '''expression : value DIV value'''
    print('expression_div')


def p_expression_mod(p):
    '''expression : value MOD value'''
    print('expression_mod')


def p_condition_eq(p):
    '''condition : value EQ value'''
    print('condition_eq')


def p_condition_neq(p):
    '''condition : value NEQ value'''
    print('condition_neq')


def p_condition_le(p):
    '''condition : value LE value'''
    print('condition_le')


def p_condition_ge(p):
    '''condition : value GE value'''
    print('condition_ge')


def p_condition_leq(p):
    '''condition : value LEQ value'''
    print('condition_leq')


def p_condition_geq(p):
    '''condition : value GEQ value'''
    print('condition_geq')


def p_value_num(p):
    '''value : NUM'''
    print('value_num')


def p_value_identifier(p):
    '''value : identifier'''
    print('value_identifier')


def p_identifier_id(p):
    '''identifier : ID'''
    print('identifier_id')


def p_identifier_tab_id(p):
    '''identifier : ID LEFTB ID RIGHTB'''
    print('identifier_tab_id')


def p_identifier_tab_num(p):
    '''identifier : ID LEFTB NUM RIGHTB'''
    print('identifier_tab_num')


def p_error(p):
    raise Exception(f'exception: {p.lineno}, {p.value}')


parser = yacc.yacc()

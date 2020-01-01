import ply.yacc as yacc

from lexer import tokens  # noqa: F401
from variables import VariablesManager


variables_manager = VariablesManager()


def p_program_declarations_commands(p):
    '''program : DECLARE declarations BEGIN commands END'''
    p[0] = 'test test test'


def p_program_commands(p):
    '''program : BEGIN commands END'''


def p_declarations_declarations_id(p):
    '''declarations : declarations COMMA ID'''
    variables_manager.add_variable(p[3], p.lexer.lineno)


def p_declarations_declarations_tab(p):
    '''declarations : declarations COMMA ID LEFTB NUM COLON NUM RIGHTB'''
    variables_manager.add_array(p[3], int(p[5]), int(p[7]), p.lexer.lineno)


def p_declarations_id(p):
    '''declarations : ID'''
    variables_manager.add_variable(p[1], p.lexer.lineno)


def p_declarations_tab(p):
    '''declarations : ID LEFTB NUM COLON NUM RIGHTB'''
    variables_manager.add_array(p[1], int(p[3]), int(p[5]), p.lexer.lineno)


def p_commands_commands_command(p):
    '''commands : commands command'''


def p_commands_command(p):
    '''commands : command'''


def p_command_assign(p):
    '''command : identifier ASSIGN expression SEMICOLON'''


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''


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


def p_command_write(p):
    '''command : WRITE value SEMICOLON'''


def p_expression_value(p):
    '''expression : value'''


def p_expression_plus(p):
    '''expression : value PLUS value'''


def p_expression_minus(p):
    '''expression : value MINUS value'''


def p_expression_times(p):
    '''expression : value TIMES value'''


def p_expression_div(p):
    '''expression : value DIV value'''


def p_expression_mod(p):
    '''expression : value MOD value'''


def p_condition_eq(p):
    '''condition : value EQ value'''


def p_condition_neq(p):
    '''condition : value NEQ value'''


def p_condition_le(p):
    '''condition : value LE value'''


def p_condition_ge(p):
    '''condition : value GE value'''


def p_condition_leq(p):
    '''condition : value LEQ value'''


def p_condition_geq(p):
    '''condition : value GEQ value'''


def p_value_num(p):
    '''value : NUM'''


def p_value_identifier(p):
    '''value : identifier'''


def p_identifier_id(p):
    '''identifier : ID'''


def p_identifier_tab_id(p):
    '''identifier : ID LEFTB ID RIGHTB'''


def p_identifier_tab_num(p):
    '''identifier : ID LEFTB NUM RIGHTB'''


def p_error(p):
    raise Exception(f'exception: {p.lineno}, {p.value}')


parser = yacc.yacc()

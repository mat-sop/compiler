import ply.yacc as yacc

from generator import assign, con_eq, if_then, minus, plus, read, write
from lexer import SEPARATOR, tokens  # noqa: F401
from memory import MemoryManager

memory_manager = MemoryManager()


def p_program_declarations_commands(p):
    '''program : DECLARE declarations BEGIN commands END'''
    p[0] = p[4] + ['HALT']
    # print('''program : DECLARE declarations BEGIN commands END''')


def p_program_commands(p):
    '''program : BEGIN commands END'''
    # print('''program : BEGIN commands END''')


def p_declarations_declarations_id(p):
    '''declarations : declarations COMMA ID'''
    memory_manager.add_variable(p[3], p.lexer.lineno)
    # print('''declarations : declarations COMMA ID''')


def p_declarations_declarations_tab(p):
    '''declarations : declarations COMMA ID LEFTB NUM COLON NUM RIGHTB'''
    memory_manager.add_array(p[3], int(p[5]), int(p[7]), p.lexer.lineno)
    # print('''declarations : declarations COMMA ID LEFTB NUM COLON NUM RIGHTB''')


def p_declarations_id(p):
    '''declarations : ID'''
    memory_manager.add_variable(p[1], p.lexer.lineno)
    # print('''declarations : ID''')


def p_declarations_tab(p):
    '''declarations : ID LEFTB NUM COLON NUM RIGHTB'''
    memory_manager.add_array(p[1], int(p[3]), int(p[5]), p.lexer.lineno)
    # print('''declarations : ID LEFTB NUM COLON NUM RIGHTB''')


def p_commands_commands_command(p):
    '''commands : commands command'''
    # print('''commands : commands command''')
    p[0] = p[1] + p[2]


def p_commands_command(p):
    '''commands : command'''
    p[0] = p[1]
    # print('''commands : command''')


def p_command_assign(p):
    '''command : identifier ASSIGN expression SEMICOLON'''
    p[0] = assign(p[1], p[3], memory_manager)
    # print('''command : identifier ASSIGN expression SEMICOLON''')


def p_command_if_then_else(p):
    '''command : IF condition THEN commands ELSE commands ENDIF'''
    # print('''command : IF condition THEN commands ELSE commands ENDIF''')


def p_command_if_then(p):
    '''command : IF condition THEN commands ENDIF'''
    p[0] = if_then(p[2], p[4])
    # print('''command : IF condition THEN commands ENDIF''')


def p_command_while_do(p):
    '''command : WHILE condition DO commands ENDWHILE'''
    # print('''command : WHILE condition DO commands ENDWHILE''')


def p_command_do_while(p):
    '''command : DO commands WHILE condition ENDDO'''
    # print('''command : DO commands WHILE condition ENDDO''')


def p_command_for_from_to_do(p):
    '''command : FOR ID FROM value TO value DO commands ENDFOR'''
    # print('''command : FOR ID FROM value TO value DO commands ENDFOR''')


def p_command_for_from_downto_do(p):
    '''command : FOR ID FROM value DOWNTO value DO commands ENDFOR'''
    # print('''command : FOR ID FROM value DOWNTO value DO commands ENDFOR''')


def p_command_read(p):
    '''command : READ identifier SEMICOLON'''
    p[0] = read(p[2], memory_manager)
    # print('''command : READ identifier SEMICOLON''')


def p_command_write(p):
    '''command : WRITE value SEMICOLON'''
    # print('''command : WRITE value SEMICOLON''')
    p[0] = write(p[2], memory_manager)


def p_expression_value(p):
    '''expression : value'''
    p[0] = p[1]
    # print('''expression : value''')


def p_expression_plus(p):
    '''expression : value PLUS value'''
    p[0] = plus(p[1], p[3], memory_manager)
    # print('''expression : value PLUS value''')


def p_expression_minus(p):
    '''expression : value MINUS value'''
    p[0] = minus(p[1], p[3], memory_manager)
    # print('''expression : value MINUS value''')


def p_expression_times(p):
    '''expression : value TIMES value'''
    # print('''expression : value TIMES value''')


def p_expression_div(p):
    '''expression : value DIV value'''
    # print('''expression : value DIV value''')


def p_expression_mod(p):
    '''expression : value MOD value'''
    # print('''expression : value MOD value''')


def p_condition_eq(p):
    '''condition : value EQ value'''
    p[0] = con_eq(p[1], p[3], memory_manager)
    # print('''condition : value EQ value''')

def p_condition_neq(p):
    '''condition : value NEQ value'''
    # print('''condition : value NEQ value''')


def p_condition_le(p):
    '''condition : value LE value'''
    # print('''condition : value LE value''')


def p_condition_ge(p):
    '''condition : value GE value'''
    # print('''condition : value GE value''')


def p_condition_leq(p):
    '''condition : value LEQ value'''
    # print('''condition : value LEQ value''')


def p_condition_geq(p):
    '''condition : value GEQ value'''
    # print('''condition : value GEQ value''')


def p_value_num(p):
    '''value : NUM'''
    # print('''value : NUM''')


def p_value_identifier(p):
    '''value : identifier'''
    p[0] = p[1]
    # print('''value : identifier''')


def p_identifier_id(p):
    '''identifier : ID'''
    p[0] = p[1]
    # print('''identifier : ID''')


def p_identifier_tab_id(p):
    '''identifier : ID LEFTB ID RIGHTB'''
    p[0] = f'{p[1]}{SEPARATOR}{p[3]}'
    # print('''identifier : ID LEFTB ID RIGHTB''')


def p_identifier_tab_num(p):
    '''identifier : ID LEFTB NUM RIGHTB'''
    # print('''identifier : ID LEFTB NUM RIGHTB''')
    p[0] = f'{p[1]}{SEPARATOR}{p[3]}'


def p_error(p):
    raise Exception(f'exception: {p.lineno}, {p.value}')


parser = yacc.yacc()

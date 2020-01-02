import ply.lex as lex


tokens = (
    'SEMICOLON', 'COLON', 'COMMA', 'LEFTB', 'RIGHTB',

    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD',
    'EQ', 'NEQ', 'LE', 'GE', 'LEQ', 'GEQ',
    'ASSIGN',
    'IF', 'THEN', 'ELSE', 'ENDIF',
    'WHILE', 'DO', 'ENDWHILE', 'ENDDO',
    'FOR', 'FROM', 'TO', 'DOWNTO', 'ENDFOR',
    'READ', 'WRITE',
    'DECLARE', 'BEGIN', 'END',
    'NUM', 'ID'
)

t_PLUS = 'PLUS'
t_MINUS = 'MINUS'
t_TIMES = 'TIMES'
t_DIV = 'DIV'
t_MOD = 'MOD'

t_EQ = 'EQ'
t_NEQ = 'NEQ'
t_LE = 'LE'
t_GE = 'GE'
t_LEQ = 'LEQ'
t_GEQ = 'GEQ'

t_ASSIGN = 'ASSIGN'

t_IF = 'IF'
t_ELSE = 'ELSE'
t_THEN = 'THEN'
t_ENDIF = 'ENDIF'

t_WHILE = 'WHILE'
t_DO = 'DO'
t_ENDWHILE = 'ENDWHILE'
t_ENDDO = 'ENDDO'

t_FOR = 'FOR'
t_FROM = 'FROM'
t_TO = 'TO'
t_DOWNTO = 'DOWNTO'
t_ENDFOR = 'ENDFOR'

t_READ = 'READ'
t_WRITE = 'WRITE'

t_DECLARE = 'DECLARE'
t_BEGIN = 'BEGIN'
t_END = 'END'

t_NUM = '-?[0-9]+'
t_ID = '[_a-z]+'

t_COMMA = ','
t_COLON = ':'
t_SEMICOLON = ';'
t_LEFTB = '\('  # noqa: W605
t_RIGHTB = '\)'  # noqa: W605

t_ignore = ' \t'


def t_COMMENT(t):
    '\[.*?\]'  # noqa: W605
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print(f'Syntax error, invalid token {t.value[0]}')
    t.lexer.skip(1)


lexer = lex.lex()

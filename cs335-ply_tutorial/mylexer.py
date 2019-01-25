import ply.lex as lex

keywords = ['var']
tokens = [ 'NAME','NUMBER','PLUS','MINUS','TIMES',
           'DIVIDE', 'EQUALS', 'SEMIC'] + [k.upper() for k in keywords]
t_ignore = ' |\t|\n'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_SEMIC  = r';'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value.upper()
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

lex.lex()         # Build the lexer

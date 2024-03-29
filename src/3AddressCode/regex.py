from tokens import *
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# COMMENTS
t_COMMENT = r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'

#List of all operators in GO
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'
t_AMPERS  = r'&'
t_OR 	  = r'\|'
t_XOR     = r'\^'
t_SHL     = r'(<<)'
t_SHR	  = r'(>>)'
t_AMPCAR  = r'&\^'
t_PLUSEQ  = r'(\+=)'
t_MINUSEQ = r'(-=)'
t_TIMESEQ = r'(\*=)'
t_DIVIDEEQ= r'/='
t_MODEQ   = r'(%=)'
t_AMPEQ   = r'(&=)'
t_OREQ    = r'(\|=)'
t_CAREQ   = r'(\^=)'
t_SHL_ASSIGN    = r'(<<=)'
t_SHR_ASSIGN    = r'(>>=)'
t_AMPCAREQ= r'(&\^=)'
t_AMPAMP  = r'(&&)'
t_OROR    = r'(\|\|)'
t_LMINUS  = r'(<-)'
t_PLUSPLUS= r'(\+\+)'
t_MINUSMIN= r'(--)'
t_EQEQ    = r'(==)'
t_LESS    = r'<'
t_GREAT   = r'>'
t_EQUAL   = r'='
t_NOT     = r'!'
t_NOTEQ   = r'(!=)'
t_LEQ     = r'(<=)'
t_GEQ     = r'(>=)'
t_COLONEQ = r'(:=)'
t_DDD	  = r'(\.\.\.)'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMMA   = r'\,'
t_DOT     = r'\.'
t_SEMICOL = r'\;'
t_COLON   = r'\:'
t_LEFT_ANGLE  = r'(<<<)'
t_RIGHT_ANGLE = r'(>>>)'
t_LEFT_LEFT   = r'(\[\()'
t_RIGHT_RIGHT = r'(\)\])'
t_LEFT_OR     = r'(\(\|)'
t_OR_RIGHT    = r'(\|\))'
t_PIPE        = r'(\|\|\|)'

# Strings in quotes
def t_STRING(t):
    r'(\"[^\"]*\")|(\'[^\']*\') '
    t.value=t.value[1:-1].replace("\'","\"")
    return t

def t_INTERFACE(t):
    r'interface'
    return t

def t_TYPE(t):
    r'( ((\*)|\ )*int8 | ((\*)|\ )*int16 | ((\*)|\ )*int32 | ((\*)|\ )*int64 | ((\*)|\ )*int |((\*)|\ )*float32 | ((\*)|\ )*float64 | ((\*)|\ )*float | ((\*)|\ )*byte |((\*)|\ )*string | ((\*)|\ )*uintptr | ((\*)|\ )*uint8 | ((\*)|\ )*uint16 | ((\*)|\ )*uint32 | ((\*)|\ )*uint64 | ((\*)|\ )*uint | ((\*)|\ )*bool)'
    t.value=t.value.replace(" ","")
    return t

def t_CONSTANTS(t):
    r'(((\*)|\ )*true|((\*)|\ )*false|((\*)|\ )*iota)'
    t.value=t.value.replace(" ","")
    return t

#Identifier token for names and variables
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_FLOAT(t):
    r'(([0-9]([0-9]+)*(\.[0-9]([0-9]+)*)?)[eE]\-[0-9]([0-9]+)*)|([0-9]([0-9]+)*\.[0-9]([0-9]+)*)([eE][\+]?[0-9]([0-9]+)*)?'
    return t

def t_INTEGER(t):
    r'(0x([0-9A-Fa-f]+)) | [0-9]([0-9]+)*([Ee](\+)?[0-9]([0-9]+)*)?'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

ERROR_LIST=[]

# Error handling rule
def t_error(t):
    ERROR_LIST.append(t.value[0])
    t.lexer.skip(1)

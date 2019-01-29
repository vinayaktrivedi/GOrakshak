#These are a set of reserved tokens in GO, NOT to be used as identifiers
reserved = {
    'break':'BREAK',
    'default':'DEFAULT',
    'func':'FUNCTION',
    'interface':'INTERFACE',
    'select':'SELECT',
    'case':'CASE',
    'defer':'DEFER',
    'go':'GO',
    'map':'MAP',
    'struct':'STRUCT',
    'chan':'CHAN',
    'else':'ELSE',
    'goto':'GOTO',
    'package':'PACKAGE',
    'switch':'SWITCH',
    'const':'CONSTANT',
    'fallthrough':'FALLTHROUGH',
    'if':'IF',
    'range':'RANGE',
    'type':'TYPE',
    'continue':'CONTINUE',
    'for':'FOR',
    'import':'IMPORT',
    'return':'RETURN',
    'var':'VAR'
    }

tokens = [
    'COMMENT',
    'MINUS',
    'INTEGER',
    'FLOAT',
    'PLUS',
    'STRING',
    'TIMES',
    'DIVIDE',
    'MOD',
    'AMPERS',
    'OR',
    'AND_NOT',
    'XOR',
    'SHL',
    'SHR',
    'AMPCAR',
    'MINUSEQ',
    'DIVIDEEQ',
    'MODEQ',
    'AMPEQ',
    'OREQ',
    'CAREQ',
    'SHL_ASSIGN',
    'SHR_ASSIGN',
    'AMPCAREQ',
    'AMPAMP',
    'OROR',
    'LMINUS',
    'PLUSPLUS',
    'MINUSMIN',
    'EQEQ',
    'LESS',
    'GREAT',
    'EQUAL',
    'NOT',
    'NOTEQ',
    'LEQ',
    'GEQ',
    'COLONEQ',
    'DDD',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'DOT',
    'SEMICOL',
    'COLON',
    'IDENTIFIER', 
    'PLUSEQ',
    'TIMESEQ',
    'CONSTANTS'
]+ list(reserved.values())
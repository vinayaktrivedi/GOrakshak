#These are a set of reserved tokens in GO, NOT to be used as identifiers
reserved = {

    'for':'FOR',
    'struct':'STRUCT',
    'const':'CONSTANT',
    'continue':'CONTINUE',
    'break':'BREAK',
    'if':'IF',
    'else':'ELSE',
    'default':'DEFAULT',
    'func':'FUNCTION',
    'fallthrough':'FALLTHROUGH',
    'interface':'INTERFACE',
    'case':'CASE',
    'switch':'SWITCH',
    'return':'RETURN',
    'goto':'GOTO',
    'package':'PACKAGE',
    'import':'IMPORT',
    'range':'RANGE',
    'type':'TYPE',
    'struct':'STRUCT',
    'var':'VAR',
    'chan':'CHAN'
    }

operators = [
    'MOD',
    'XOR',
    'PLUS',
    'MINUS',
    'EQUAL',
    'NOT',
    'NOTEQ',
    'TIMES',
    'DIVIDE',
    'SHL',
    'SHR',
    'AMPEQ',
    'MINUSEQ',
    'DIVIDEEQ',
    'MODEQ',
    'SHL_ASSIGN',
    'LEQ',
    'GEQ',
    'EQEQ',
    'LESS',
    'TIMESEQ',
    'SHR_ASSIGN',
    'AMPCAREQ',
    'AMPAMP',
    'GREAT',
    'COLONEQ',
    'DDD',
    'DOT',
    'SEMICOL',
    'COLON',
    'PLUSEQ',
    'OREQ',
    'CAREQ',
    'AMPERS',
    'OR',
    'OROR',
    'LMINUS',
    'PLUSPLUS',
    'MINUSMIN',
    'PIPE',
    'RIGHT_RIGHT',
    'LEFT_LEFT',
    'OR_RIGHT',
    'LEFT_OR',
    'RIGHT_ANGLE',
    'LEFT_ANGLE'
    ]

tokens = [
    'FLOAT',
    'INTEGER',
    'IDENTIFIER',
    'STRING',
    'COMMENT',
    'CONSTANTS',
    'COMMA',
    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'AMPCAR'
    ]
    
tokens = tokens + list(operators) + list(reserved.values())
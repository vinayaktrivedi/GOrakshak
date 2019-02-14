import ply.yacc as yacc
import inspect
import mylexer            # Import lexer information
tokens = mylexer.tokens   # Need token list

def p_list_of_assign(p):
    '''assign_list : assign SEMIC assign_list
                   | empty'''
    print(inspect.stack()[0][3])
    print(p[0])
    # print(inspect.stack()[0][3])

def p_assign(p):
    '''assign : VAR NAME EQUALS expr'''
    print('var {} = {};'.format(p[2], p[4]))
    print(inspect.stack()[0][3])
    print(p[0])
    print(p[1])
    print(p[2])
    print(p[3])
    print(p[4])
    # print(inspect.stack()[0][3])

def p_expr(p):
    '''expr : expr PLUS term 
            | expr MINUS term
            | term'''
    # if len(p) > 2:
    #     if p[2] == '+':
    #         p[0] = p[1] + p[3]
    #     elif p[2] == '-':
    #         p[0] = p[1] - p[3]
    # else:
    #     p[0] = p[1]
    print(inspect.stack()[0][3])
    print(p[0])
    print(p[1])
    # print(p[2])
    # print(p[3])
    # print(inspect.stack()[0][3])

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    # if len(p) > 2:
    #     if p[2] == '*':
    #         p[0] = p[1] * p[3]
    #     elif p[2] == '/':
    #         p[0] = p[1] / p[3]
    # else:
    #     p[0] = p[1]
    print(inspect.stack()[0][3])
    print(p[0])
    print(p[1])
    # print(p[2])
    # print(p[3])
    # print(inspect.stack()[0][3])

def p_factor(p):
    '''factor : NUMBER'''
    p[0] = p[1]
    print(inspect.stack()[0][3])
    print(p[0])
    print(p[1])
    # print(inspect.stack()[0][3])

def p_empty(p):
    '''empty  : '''
    print(inspect.stack()[0][3])
    print(p[0])
    # print(inspect.stack()[0][3])

parser = yacc.yacc()            # Build the parser

with open('inp','r') as f:
    input_str = f.read()

parser.parse(input_str)

import ply.yacc as yacc
import inspect
import mylexer            # Import lexer information
tokens = mylexer.tokens   # Need token list

graph="digraph finite_state_machine {ordering=out;rankdir=UD;size=\"8,5\";node [shape = circle];\n"
cnt=0


# def handle_empty(p, node_label):


# def check(p, num_childs):
#     global cnt
#     global graph
#     for i in range(1,num_childs+1):
#         try:
#             a=p[i][1]
#         except:
#             cnt+=1
#             p[i]=[str(cnt) , str(p[i]), "NOT NULL"]
#             graph+=p[i][0] + " [label=\""+ p[i][1]+"\"];\n"

    


# def make_node( p , node_label, num_childs):
#     global cnt
#     global graph
#     check(p,num_childs)
#     not_null_flag = 0
#     for i in range(1,num_childs+1):
#         if(p[i][2] == "NOT NULL"):
#             not_null_flag=1

#     if(not_null_flag):
#         cnt+=1
#         p[0] = [str(cnt) , node_label, "NOT NULL"]
#         graph+=p[0][0] + " [label=\""+ p[0][1]+"\"];\n"

#         for i in range(1,num_childs+1):
#             if(p[i][2] == "NOT NULL"):
#                 graph+=p[0][0] + " -> "+p[i][0]+";\n"

#     else:
#         cnt+=1
#         p[0] = [str(cnt) , node_label, "NULL"]    


def make_node(p,label,childs):
    global cnt
    global graph
    cnt+=1
    p[0]=str(cnt)
    graph+=p[0] + " [label=\""+ label+"\"];\n"
    num_childs=len(childs)
    for i in childs:
        if(p[i] != "NULL"):
            graph+=p[0] + " -> "+p[i]+";\n"

def make_leaf(p,index,label="notgiven"):
    global cnt
    global graph
    if(label == "notgiven"):
        label=str(p[index])
    cnt+=1
    p[index]=str(cnt)
    graph+=p[index] + " [label=\""+ label+"\"];\n"

def bypass(p,child):
    p[0] = p[child]

def pass_empty(p):
    p[0]="NULL"



def p_list_of_assign(p):
    '''assign_list : assign SEMIC assign_list
                   | empty'''
    global cnt
    if len(p) == 4:
        make_leaf(p,2)
        make_node(p,"assign_list",[1,2,3])
    else:
        pass_empty(p);

def p_assign(p):
    '''assign : VAR NAME EQUALS expr'''
    make_leaf(p,1)
    make_leaf(p,2)
    make_leaf(p,3)
    make_node(p,"assign_list",[1,2,3,4])
    

def p_expr(p):
    '''expr : expr PLUS term 
            | expr MINUS term
            | term'''
    if len(p) > 2:
        make_leaf(p,2)
        make_node(p,"expr",[1,2,3])
    else:
        bypass(p,1)

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) > 2:
        make_leaf(p,2)
        make_node(p,"term",[1,2,3])
    else:
        bypass(p,1)

def p_factor(p):
    '''factor : NUMBER'''
    make_leaf(p,1)
    make_node(p,"factor",[1])
    #bypass(p,1);


def p_empty(p):
    '''empty  : '''

def p_error(p):
    print("Syntax error in input!")
    print(p)

parser = yacc.yacc()            # Build the parser


with open('inp','r') as f:
    input_str = f.read()

parser.parse(input_str)

graph+="}"
print(graph)
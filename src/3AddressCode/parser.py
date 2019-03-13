import sys
import os
import csv
import re
import argparse
import ply.yacc as yacc
import lexer            # Import lexer information
tokens = lexer.tokens   # Need token list

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input",help="name of GO input file")
ap.add_argument("-o", "--output",help="name of output file(.gv)")
args = vars(ap.parse_args())

if args["input"] is None:
    args["input"] = "../../tests/parser/test1.go"

if args["output"] is None:
    args["output"] = "output1.gv"

file = args["input"]
# outfile = open(args["output"],"w")

globalsymboltable = {}
stack = []
stack.append(globalsymboltable)

def make_symbol_table(func_name,label):
  prev_table = stack[-1]
  local_symbol_table = {}
  prev_table[func_name][label] = local_symbol_table
  # Does making a symbol table always require to set the current symbol table to the new one
  stack.append(local_symbol_table)
  return local_symbol_table

def go_one_level_up():
  stack = stack[:-1]

def add_variable_attribute(variable,attribute,value):
    symbol_table = stack[-1]
    try:
        if symbol_table[variable]['exists'] == 0:
            return 0
        else:
            symbol_table[variable][attribute] = value
            return 1
    except:
        return 0

def register_variable(variable):
  symbol_table = stack[-1]
  symbol_table[variable]['exists'] = 1
  return

def add_variable_attribute_api(variable,attribute,value):
  if(value['val'] == 'struct'):
    make_symbol_table(variable,'struct')
    for objects in value['struct_fields']:
      register_variable(objects['name'])
      add_variable_attribute(objects['name'],'type',objects['type'])
    go_one_level_up()

def check_if_variable_declared(variable):
    i = len(stack)-1
    while(i>=0):
        symbol_table = stack[i]
        try:
            if symbol_table[variable]['exists'] == 1:
                return 1
            else:
                i = i - 1
        except:
            i = i - 1
    return 0


def p_start(p):
  '''start : SourceFile'''
  p[0]['code'] = p[1]['code']
  print(p[0]['code'])

def p_sourcefile(p):
  '''SourceFile : cmtlist PackageClause cmtlist Imports cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist Imports cmtlist
                | cmtlist PackageClause cmtlist'''
  if(len(p) == 8):
    p[0]['code'] = p[2]['code'] + "\n" + p[4]['code'] + "\n" + p[6]['code']
  elif(len(p) == 5):
    p[0]['code'] = p[2]['code'] + "\n" + p[4]['code']
  else:
    p[0]['code'] = p[2]['code']

def p_packegeclause(p):
  '''PackageClause : PACKAGE IDENTIFIER SEMICOL'''
  register_variable(str(p[2]))
  add_variable_attribute(str(p[2]),"package",1)
  p[0]['code'] = 'package '+str(p[2])

def p_imports(p):
  '''Imports : Import SEMICOL
           | Imports cmtlist Import SEMICOL'''
  if(len(p)==2):
    p[0]['code'] = p[1]['code']
  else:
    p[0]['code'] = p[1]['code'] + "\n" + p[3]['code']

def p_import(p):
  '''Import : IMPORT ImportStmt
           | IMPORT LPAREN ImportStmtList OSemi RPAREN
           | IMPORT LPAREN RPAREN'''
  if(len(p)==3):
    p[0]['code'] = p[2]['code']

def p_importstmt(p):
  '''ImportStmt : ImportHere STRING'''
  p[0]['code'] = 'import '+str(p[2])
  register_variable(str(p[2]))
  add_variable_attribute(str(p[2]),"import",1)

def p_importstmtlist(p):
  '''ImportStmtList : ImportStmt
               | ImportStmtList SEMICOL ImportStmt'''

def p_importhere(p):
  '''ImportHere :
           | IDENTIFIER
           | DOT'''

def p_declaration(p):
  '''Declaration : CommonDecl
            | FuncDecl
            | NonDeclStmt'''
  p[0]['code'] = p[1]['code']

def p_commondecl(p):
  '''CommonDecl : CONSTANT ConstDecl
           | CONSTANT LPAREN ConstDecl OSemi RPAREN
           | CONSTANT LPAREN ConstDecl SEMICOL ConstDeclList OSemi RPAREN
           | CONSTANT LPAREN RPAREN
           | VAR VarDecl
           | VAR LPAREN VarDeclList OSemi RPAREN
           | VAR LPAREN RPAREN
           | NewType TypeDecl
           | NewType LPAREN TypeDeclList OSemi RPAREN
           | NewType LPAREN RPAREN'''


def p_vardecl(p):
  '''VarDecl   : DeclNameList NType
          | DeclNameList NType EQUAL ExprList
          | DeclNameList EQUAL ExprList'''

def p_constdecl(p):
  '''ConstDecl : DeclNameList NType EQUAL ExprList
          | DeclNameList NType
          | DeclNameList EQUAL ExprList'''
  if(len(p)==3):
    for var in p[1]['variable']:
      add_variable_attribute_api(var,'type',p[2]['type'])
  elif(len(p)==4):
    for var in p[1]['variable']:
      add_variable_attribute_api(var,'type',p[3]['type'])
  else:
    if(p[4]['type'] != p[2]['type']):
      print("Error!!")
      exit(1)
    else:
      for var in p[1]['variable']:
        add_variable_attribute_api(var,'type',p[2]['type'])


def p_constdecl1(p):
  '''ConstDecl1 : ConstDecl
           | DeclNameList'''


def p_typedeclname(p):
  '''TypeDeclName : IDENTIFIER'''

def p_typedecl(p):
  '''TypeDecl : TypeDeclName NType'''

def p_simplestmt(p):
    '''SimpleStmt : Expr
           | Expr PLUSEQ Expr
           | Expr MINUSEQ Expr
           | Expr TIMESEQ Expr
           | Expr DIVIDEEQ Expr
           | Expr MODEQ Expr
           | Expr OREQ Expr
           | Expr AMPEQ Expr
           | Expr CAREQ Expr
           | Expr SHL_ASSIGN Expr
           | Expr SHR_ASSIGN Expr
           | Expr AMPCAREQ Expr
           | ExprList EQUAL ExprList
           | ExprList COLONEQ ExprList
           | Expr PLUSPLUS
           | Expr MINUSMIN'''
    if(len(p) == 2):
        p[0]['code'] = p[1]['code']
    if(len(p) == 3):
        typ = p[1]['type']
        p[0]['code'] = p[1]['code'] + "\n"
        if(str(p[2]) == "++"):
            p[0]['code'] += (p[1]['code'] + " +" + type + " 1")
        else:
            p[0]['code'] += (p[1]['code'] + " -" + type + " 1")
    if(len(p) == 4):
        if(str(p[2]) == "+="):
            op = "+"
            typ = p[1]['type']
            if(p[2]['type'] == "float"):
                typ = "float"
        if(str(p[2]) == "-="):
            op = "-"
            typ = p[1]['type']
            if(p[2]['type'] == "float"):
                typ = "float"
        if(str(p[2]) == "*="):
            op = "*"
            typ = p[1]['type']
            if(p[2]['type'] == "float"):
                typ = "float"
        if(str(p[2]) == "/="):
            op = "/"
            typ = p[1]['type']
            if(p[2]['type'] == "float"):
                typ = "float"
        if(str(p[2]) == "%="):
            op = "%"
            typ = p[1]['type']
            if(p[1]['type'] != "int" or p[3]['type'] != "int"):
                print("error!")
                exit(1)
        if(str(p[2]) == "|="):
            op = "|"
            typ = p[1]['type']
            if((p[1]['type'] != "int" or p[3]['type'] != "int") and (p[1]['type'] != "bool" or p[3]['type'] != "bool")):
                print("error!")
                exit(1)
        if(str(p[2]) == "&="):
            op = "&"
            typ = p[1]['type']
            if((p[1]['type'] != "int" or p[3]['type'] != "int") and (p[1]['type'] != "bool" or p[3]['type'] != "bool")):
                print("error!")
                exit(1)
        if(str(p[2]) == "<<="):
            op = "<<"
            typ = p[1]['type']
            if(p[1]['type'] != "int" or p[3]['type'] != "int"):
                print("error!")
                exit(1)

        if(str(p[2]) == ">>="):
            op = ">>"
            typ = p[1]['type']
            if(p[1]['type'] != "int" or p[3]['type'] != "int"):
                print("error!")
                exit(1)

        if(str(p[2]) == "&^="):
            # what to do
            op = ""

        flag = 0
        if(str(p[2]) == "="):
            flag = 1
            if(len(p[1]['exprs']) != len(p[3]['exprs'])):
                print("error!")
                exit(1)
            p[0]['code'] = ""
            for i in range(0,len(p[1]['exprs'])):
                if(p[1]['exprs'][i]['type'] == p[3]['exprs'][i]['type']):
                    p[0]['code'] += p[1]['exprs'][i]['exp'] + " = " + p[3]['exprs'][i]['exp'] + "\n"
                else:
                    print("error!")
                    exit(1)

        if(str(p[2]) == ":="):
            # not sure about it
            flag = 1
            if(len(p[1]['exprs']) != len(p[3]['exprs'])):
                print("error!")
                exit(1)
            p[0]['code'] = ""
            for i in range(0,len(p[1]['exprs'])):
                p[0]['code'] += p[1]['exprs'][i]['exp'] + " = " + p[3]['exprs'][i]['exp'] + "\n"

        if(flag == 0):
            # can't use 'code' attribute directly
            p[0]['code'] = p[1]['code'] + " = " + p[1]['code'] + " " + op + typ + " " + p[3]['code']


def p_case(p):
  '''Case : CASE ExprOrTypeList COLON
     | CASE ExprOrTypeList EQUAL Expr COLON
     | CASE ExprOrTypeList COLONEQ Expr COLON
     | DEFAULT COLON'''


def p_compoundstmt(p):
  '''CompoundStmt : LBRACE cmtlist StmtList cmtlist RBRACE'''

def p_caseblock(p):
  '''CaseBlock : Case StmtList'''

def p_caseblocklist(p):

  '''CaseBlockList :
                   | CaseBlockList CaseBlock'''

def p_loopbody(p):

  '''LoopBody : LBRACE cmtlist StmtList  cmtlist RBRACE'''


def p_rangestmt(p):

  '''RangeStmt : ExprList EQUAL RANGE Expr
               | ExprList COLONEQ RANGE Expr
               | RANGE Expr'''




def p_forheader(p):

  '''ForHeader : OSimpleStmt SEMICOL OSimpleStmt SEMICOL OSimpleStmt
               | OSimpleStmt
               | RangeStmt'''


def p_forbody(p):

  '''ForBody : ForHeader LoopBody'''

def p_forstmt(p):

  '''ForStmt : FOR ForBody'''

def p_ifheader(p):
  '''IfHeader : OSimpleStmt
           | OSimpleStmt SEMICOL OSimpleStmt'''


def p_ifstmt(p):
  '''IfStmt : IF IfHeader LoopBody ElseIfList'''
  nextlabel = getlabel()
  exitlabel = getlabel()
  if(len(p[4]['extra']) == 0):
    p[0]['code'] = p[2]['code'] + "\n" + "if "+p[2]['place'] +"=0 goto "+exitlabel + "\n" + p[3]['code']
  else:
    p[0]['code'] = p[2]['code'] + "\n" + "if "+p[2]['place'] +"=0 goto "+nextlabel + "\n" + p[3]['code'] + "\n" + "goto "+exitlabel

  for i in range(0,len(p[4]['extra'])):
    if((i+1) == len(p[4]['extra'])):
      if(p[4]['extra'][i]['type']=="elseif"):
        p[0]['code'] += "\n" + nextlabel+":" + "\n" + p[4]['extra'][i]['ifheader_code'] + "\n" + "else if "+p[4]['extra'][i]['ifheader_place'] +"=0 goto "+exitlabel + "\n" + p[4]['extra'][i]['body']
      else:
        p[0]['code'] += "\n" + nextlabel+":" + "\n" + "else "+ "\n" + p[4]['extra'][i]['body']
    else:
      nextlabel2= getlabel()
      if(p[4]['extra'][i]['type']=="elseif"):
        p[0]['code'] += "\n" + nextlabel+":" + "\n" + p[4]['extra'][i]['ifheader_code'] + "\n" + "else if "+p[4]['extra'][i]['ifheader_place'] +"=0 goto "+nextlabel2 + "\n" + p[4]['extra'][i]['body'] + "\n" + "goto "+exitlabel
      nextlabel = nextlabel2
  p[0]['code'] += "\n" + exitlabel+":"



def p_elseif(p):
  '''ElseIf : ELSE IF IfHeader LoopBody'''
  p[0]['extra_dict'] = {}
  p[0]['extra_dict']['body'] = p[4]['code']
  p[0]['extra_dict']['type'] = "elseif"
  p[0]['extra_dict']['ifheader_code'] = p[3]['code']
  p[0]['extra_dict']['ifheader_place'] = p[3]['place']


def p_elseiflist(p):
  '''ElseIfList :
                | ElseIf ElseIfList
                | Else'''
  if(len(p)==3):
    p[0]['extra'] = []
    p[0]['extra'].append(p[1]['extra_dict'])
    p[0]['extra'].extend(p[2]['extra'])
  elif(len(p)==2):
    p[0]['extra'] = []
    p[0]['extra'].append(p[1]['extra_dict'])
  else:
    p[0]['extra'] = []


def p_else(p):
  '''Else : ELSE CompoundStmt'''
  p[0]['extra_dict'] = {}
  p[0]['extra_dict']['body'] = p[2]['code']
  p[0]['extra_dict']['type'] = "else"


def p_ntype(p):
  '''NType : FuncType
           |  OtherType
           |  PtrType
           |  DotName
           |  LPAREN NType RPAREN
           |  NewType'''
  if(len(p)==4):
    p[0]['type'] = p[2]['type']
  else:
    p[0]['type'] = p[1]['type']



def p_nonexprtype(p):
  '''NonExprType : FuncType
                 | OtherType
                 | TIMES NonExprType'''


def p_othertype(p):
  '''OtherType : LBRACK OExpr RBRACK NType
               | StructType
               | InterfaceType
               | ChannelType'''
  if(len(p) == 2):
    p[0]['type'] = p[1]['type']

  else:
    if(p[2]['type'] == 'int' or p[2]['type'] == 'void'):
      p[0]['type'] = {}
      p[0]['type']['val'] = 'array'
      p[0]['type']['arr_length'] = p[2]['value']
      p[0]['type']['arr_type'] = p[4]['type']['val']
    else:
      print("Array definition not good")
      exit(1)


def p_channeltype(p):
  '''ChannelType : CHAN NewType
                 | CHAN LMINUS NewType
                 | LMINUS CHAN NewType'''


def p_structtype(p):
  '''StructType : STRUCT LBRACE StructDeclList OSemi RBRACE
                | STRUCT LBRACE RBRACE'''
  p[0]['type'] = {}
  p[0]['type']['val'] = 'struct'
  p[0]['type']['struct_fields'] = []
  if(len(p) == 6):
    p[0]['type']['struct_fields'] = p[3]['struct_fields']



def p_interfacetype(p):
  '''InterfaceType : INTERFACE LBRACE InterfaceDeclList OSemi RBRACE
                   | INTERFACE LBRACE RBRACE'''


def p_funcdec1(p):
  '''FuncDecl : FUNCTION FuncDecl_ FuncBody'''

def p_funcdec1_(p):
  '''FuncDecl_ : IDENTIFIER ArgList FuncRes
               | LEFT_OR OArgTypeListOComma OR_RIGHT IDENTIFIER ArgList FuncRes'''


def p_functype(p):
  '''FuncType : FUNCTION ArgList FuncRes'''

def p_arglist(p):
  '''ArgList : LPAREN OArgTypeListOComma RPAREN
             | ArgList LPAREN OArgTypeListOComma RPAREN'''

def p_funcbody(p):
  '''FuncBody :
              | LBRACE  cmtlist StmtList  cmtlist RBRACE'''


def p_funcres(p):
  '''FuncRes :
             | FuncRetType
             | LEFT_OR OArgTypeListOComma OR_RIGHT'''

######################################################################################################
def p_structdeclist(p):
  '''StructDeclList : StructDecl
                    | StructDeclList SEMICOL StructDecl'''

  if(len(p)==2):
    p[0]['struct_fields'] = []
    p[0]['struct_fields'].append(p[1]['struct_fields'])
  else:
    p[0]['struct_fields'] = p[1]['struct_fields']
    p[0]['struct_fields'].append(p[3]['struct_fields'])


def p_interfacedec1list(p):
  '''InterfaceDeclList : InterfaceDecl
                       | InterfaceDeclList SEMICOL InterfaceDecl'''


def p_structdec1(p):
  '''StructDecl : NewNameList NType OLiteral
                | Embed OLiteral
                | LPAREN Embed RPAREN OLiteral
                | TIMES Embed OLiteral
                | LPAREN TIMES Embed RPAREN OLiteral
                | TIMES LPAREN Embed RPAREN OLiteral'''
  if(len(p) == 4 and str(p[1])!='*'):
    p[0]['struct_fields'] = []
    for names in p[1]['names']:
      x = {}
      x['name'] = names
      x['type'] = p[2]['type']
      p[0]['struct_fields'].append(x)


def p_interfacedec1(p):
  '''InterfaceDecl : NewName InDecl
                   | IDENTIFIER
                   | LPAREN IDENTIFIER RPAREN'''

def p_indecl(p):
  '''InDecl : LPAREN OArgTypeListOComma RPAREN FuncRes'''

def p_labelname(p):
  '''LabelName : NewName'''

def p_newname(p):
  '''NewName : IDENTIFIER'''
  p[0]['names'] = str(p[1])


def p_ptrtype(p):
  '''PtrType : TIMES NType'''
  p[0]['type'] = {}
  p[0]['type']['val'] = 'pointer'
  p[0]['type']['pointer_type'] = p[2]['type']['val']

def p_funcrettype(p):
  '''FuncRetType : FuncType
                 | OtherType
                 | PtrType
                 | DotName
                 | NewType'''

def p_dotname(p):
  '''DotName : Name
             | Name DOT IDENTIFIER'''



def p_ocomma(p):
  '''OComma :
            | COMMA'''


def p_osemi(p):
  '''OSemi :
           | SEMICOL'''


def p_osimplestmt(p):
    '''OSimpleStmt :
                 | SimpleStmt'''
    p[0]['code'] = p[1]['code']

def p_onewname(p):
  '''ONewName :
              | NewName'''

def p_oexpr(p):
  '''OExpr :
           | Expr'''
  if(len(p)==2):
    p[0]['type'] = p[1]['type']
    p[0]['value'] = p[1]['value']
  else:
    p[0]['type'] = 'void'
    p[0]['value'] = 0


def p_oexprlist(p):
    '''OExprList :
               | ExprList'''
    if(len(p)==2):
        p[0]['exprs'] = p[1]['exprs']

def p_funcliteraldecl(p):
  '''FuncLiteralDecl : FuncType'''

def p_funcliteral(p):
  '''FuncLiteral : FuncLiteralDecl LBRACE cmtlist StmtList cmtlist RBRACE'''

def p_exprlist(p):
    '''ExprList : Expr
              | ExprList COMMA Expr'''
    # if(len(p)==2):
    #     p[0]['exprs'].append({'exp':p[1]['code'],'type':p[1]['type']})
    #     p[0]['code'] = p[1]['code']
    # if(len(p)==4):
    #     p[0]['exprs'].extend(p[1]['exprs'])
    #     p[0]['exprs'].append({'exp':p[3]['code'],'type':p[3]['type']})
    # use 'place' attribute here


def p_exprortypelist(p):
  '''ExprOrTypeList : ExprOrType
                    | ExprOrTypeList COMMA ExprOrType'''

def p_oliteral(p):
  '''OLiteral :
              | Literal'''

def p_literal(p):
  '''Literal : INTEGER
             | FLOAT
             | STRING'''

def p_embed(p):
  '''Embed : IDENTIFIER'''

def p_dec1list(p):
  '''DeclList : Declaration SEMICOL
              | DeclList cmtlist Declaration SEMICOL'''
    if(len(p)==3):
      p[0]['code'] = p[1]['code']
    else:
      p[0]['code'] = p[1]['code'] + "\n" + p[3]['code']


def p_var_dec_list(p):
  '''VarDeclList : VarDecl
                   | VarDeclList SEMICOL VarDecl'''

def p_const_dec_list(p):
  '''ConstDeclList : ConstDecl1
                     | ConstDeclList SEMICOL ConstDecl1'''


def p_type_decl_list(p):
  '''TypeDeclList : TypeDecl
                    | TypeDeclList SEMICOL TypeDecl'''


def p_decl_name_list(p):
  '''DeclNameList : DeclName
                    | DeclNameList COMMA DeclName'''
  if(len(p)==2):
    p[0]['variable'] = []
    p[0]['variable'].append(p[1]['variable'])
  else:
    p[0]['variable'] = p[1]['variable']
    p[0]['variable'].append(p[3]['variable'])


def p_stmtlist(p):
  '''StmtList : Stmt SEMICOL
                | StmtList cmtlist Stmt SEMICOL'''

def p_newnamelist(p):
  '''NewNameList : NewName
                   | NewNameList COMMA NewName'''
  p[0]['names'] = []
  if(len(p)==2):
    p[0]['names'] = p[1]['names']
  else:
    p[0]['names'] = p[1]['names']
    p[0]['names'].append(p[3]['names'])


def p_keyvallist(p):
  '''KeyvalList : Keyval
                  | BareCompLitExpr
                  | KeyvalList COMMA Keyval
                  | KeyvalList COMMA BareCompLitExpr'''


def p_bracedkeyvallist(p):
  '''BracedKeyvalList :
                        | KeyvalList OComma'''


def p_declname(p):
  '''DeclName : IDENTIFIER'''
  register_variable(str(p[1]))
  p[0]['variable'] = str(p[1])


def p_name(p):
  '''Name : IDENTIFIER'''


def p_argtype(p):
  '''ArgType : NameOrType
               | IDENTIFIER NameOrType
               | IDENTIFIER DotDotDot
               | DotDotDot'''

def p_argtypelist(p):
  '''ArgTypeList : ArgType
                   | ArgTypeList COMMA ArgType'''

def p_oargtypelistocomma(p):
  '''OArgTypeListOComma :
                          | ArgTypeList OComma'''

def p_stmt(p):
    '''Stmt :
            | CompoundStmt
            | CommonDecl
            | NonDeclStmt'''
    if(len(p)==2):
        p[0]['code'] = p[1]['code']

def p_nondeclstmt(p):
    '''NonDeclStmt : SimpleStmt
                   | ForStmt
                   | SwitchStmt
                   | IfStmt
                   | LabelName COLON Stmt
                   | FALLTHROUGH
                   | BREAK ONewName
                   | CONTINUE ONewName
                   | GOTO NewName
                   | RETURN OExprList'''
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
    if(len(p)==3):
        string = ""
        if(str(p[1]) == "break"):
            string = "break"
        if(str(p[1]) == "continue"):
            string = "continue"
        if(str(p[1]) == "goto"):
            string = "goto"
        flag = 0
        if(str(p[1]) == "return"):
            flag = 1
            string = "return"
        if(flag == 0):
            p[0]['code'] = string + " " + p[2]['code']
        # not done for return in multiple exp
    if(len(p)==4):
        # what to do
        dummy = 0

def p_dotdotdot(p):
  '''DotDotDot : DDD
                 | DDD NType'''

def p_pexpr(p):
  '''PExpr : PExprNoParen
             | LPAREN ExprOrType RPAREN'''

def p_pexprnoparen(p):
  '''PExprNoParen : Literal
                    | Name
                    | PExpr DOT IDENTIFIER
                    | PExpr DOT LPAREN ExprOrType RPAREN
                    | PExpr DOT LPAREN NewType RPAREN
                    | PExpr LBRACK Expr RBRACK
                    | PExpr LBRACK OExpr COLON OExpr RBRACK
                    | PExpr LBRACK OExpr COLON OExpr COLON OExpr RBRACK
                    | PseudoCall
                    | ConvType LEFT_ANGLE Expr OComma RIGHT_ANGLE
                    | CompType LEFT_LEFT BracedKeyvalList RIGHT_RIGHT
                    | PExpr LEFT_LEFT BracedKeyvalList RIGHT_RIGHT
                    | FuncLiteral
                    | ForCompExpr'''

def p_NewType(p):
  '''NewType : TYPE'''
  p[0]['type'] = {}
  p[0]['type']['val'] =  str(p[1])

def p_convtype(p):
  '''ConvType : FuncType
                | OtherType'''

def p_comptype(p):
  '''CompType : OtherType'''

def p_keyval(p):
  '''Keyval : Expr COLON CompLitExpr'''

def p_barecomplitexpr(p):
  '''BareCompLitExpr : Expr
                       | LEFT_LEFT BracedKeyvalList RIGHT_RIGHT'''

def p_complitexpr(p):
  '''CompLitExpr : Expr
                 | LEFT_LEFT BracedKeyvalList RIGHT_RIGHT'''

def p_exportype(p):
  '''ExprOrType : Expr
                  | NonExprType'''

def p_nameortype(p):
  '''NameOrType : NType'''

def p_switchstmt(p):
  '''SwitchStmt : SWITCH IfHeader LBRACE CaseBlockList RBRACE'''

def p_prec5expr_(p):
  '''Prec5Expr_ : UExpr
                  | Prec5Expr_ DIVIDE UExpr
                  | Prec5Expr_ MOD UExpr
                  | Prec5Expr_ SHL UExpr
                  | Prec5Expr_ SHR UExpr
                  | Prec5Expr_ AMPERS UExpr
                  | Prec5Expr_ AMPCAR UExpr
                  | Prec5Expr_ TIMES UExpr'''

def p_prec4expr_(p):
  '''Prec4Expr_ : Prec5Expr_
                  | Prec4Expr_ PLUS Prec5Expr_
                  | Prec4Expr_ MINUS Prec5Expr_
                  | Prec4Expr_ XOR Prec5Expr_
                  | Prec4Expr_ OR Prec5Expr_'''

def p_prec3expr_(p):
    '''Prec3Expr_ : Prec4Expr_
                  | Prec3Expr_ EQEQ Prec4Expr_
                  | Prec3Expr_ NOTEQ Prec4Expr_
                  | Prec3Expr_ LEQ Prec4Expr_
                  | Prec3Expr_ GEQ Prec4Expr_
                  | Prec3Expr_ GREAT Prec4Expr_
                  | Prec3Expr_ LESS Prec4Expr_
                '''
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
    else:
        op = ""
        if(str(p[2]) == "=="):
            op = "=="
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] == p[3]['value'])
        if(str(p[2]) == "!="):
            op = "!="
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] != p[3]['value'])
        if(str(p[2]) == "<="):
            op = "<="
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] <= p[3]['value'])
        if(str(p[2]) == ">="):
            op = ">="
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] >= p[3]['value'])
        if(str(p[2]) == ">"):
            op = ">"
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] > p[3]['value'])
        if(str(p[2]) == "<"):
            op = "<"
            if(p[1]['value'] and p[3]['value']):
                p[0]['value'] = (p[1]['value'] < p[3]['value'])
        p[0]['place'] = newtmp()
        p[0]['code'] = p[0]['place'] + " = " p[1]['place'] + " " + op + " " + p[3]['place']
        p[0]['type'] = p[1]['type']

def p_prec2expr_(p):
    '''Prec2Expr_ : Prec3Expr_
                  | Prec2Expr_ AMPAMP Prec3Expr_'''
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
    else:
        p[0]['place'] = newtmp()
        if(p[1]['type']!='int' or p[3]['type']!='int'):
            print("error!")
            exit(1)
        p[0]['code'] = p[0]['place'] + " = " p[1]['place'] + " && " + p[3]['place']
        p[0]['type'] = p[1]['type']
        if(p[1]['value'] and p[3]['value']):
            p[0]['value'] = p[1]['value'] and p[3]['value']

def p_expr(p):
    '''Expr : Prec2Expr_
            | Expr OROR Prec2Expr_
            | CONSTANTS
            | Chexpr
            | Arrayexp'''
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
    else:
        p[0]['place'] = newtmp()
        if(p[1]['type']!='int' or p[3]['type']!='int'):
            print("error!")
            exit(1)
        p[0]['code'] = p[0]['place'] + " = " p[1]['place'] + " || " + p[3]['place']
        p[0]['type'] = p[1]['type']
        if(p[1]['value'] and p[3]['value']):
            p[0]['value'] = p[1]['value'] or p[3]['value']

def p_chexpr(p):
  '''Chexpr : LMINUS IDENTIFIER'''

def p_arrayexp(p):
  '''Arrayexp : OtherType LBRACE ExprList RBRACE'''

def p_uexpr(p):
  '''UExpr : PExpr
             | AMPERS UExpr
             | NOT UExpr
             | TIMES UExpr
             | PLUS UExpr
             | MINUS UExpr
             | XOR UExpr'''

def p_forcompexpr(p):
  '''ForCompExpr : LBRACK Expr PIPE RangeStmt RBRACK'''

def p_pseudocall(p):
  '''PseudoCall : PExpr LPAREN RPAREN
                  | PExpr LPAREN ExprOrTypeList OComma RPAREN
                  | PExpr LPAREN ExprOrTypeList DDD OComma RPAREN'''

def p_cmtlist(p):
  '''cmtlist :
              | cmtlist COMMENT'''

def p_error(p):
  print("Syntax error in input!")
  print(p)

parser = yacc.yacc()            # Build the parser

with open(file,'r') as f:
    input_str = f.read()

parser.parse(input_str,debug=0)

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

def make_symbol_table(func_name):
  prev_table = stack[-1]
  local_symbol_table = {}
  prev_table[func_name]['symbol'] = local_symbol_table
  stack.append(local_symbol_table)
  return local_symbol_table

def add_variable_attribute(variable,attribute,value):
    symbol_table = stack[-1]
    try:
        if symbol_table[variable]['exists'] == 0:
            return 0
    except:
        return 0
    symbol_table[variable][attribute] = value
    return 1

def register_variable(variable):
  symbol_table = stack[-1]
  symbol_table[variable]['exists'] = 1
  return

def check_if_variable_declared(variable):
    i = len(stack)-1
    while(i>=0):
        symbol_table = stack[i]
        try:
            if symbol_table[variable]['exists'] == 1:
                return 1
        except:
            return 0
        i = i-1
    return 0


def p_start(p):
  '''start : SourceFile'''


def p_sourcefile(p):
  '''SourceFile : cmtlist PackageClause cmtlist Imports cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist Imports cmtlist
                | cmtlist PackageClause cmtlist'''

def p_packegeclause(p):
  '''PackageClause : PACKAGE IDENTIFIER SEMICOL'''

def p_imports(p):
  '''Imports : Import SEMICOL
           | Imports cmtlist Import SEMICOL'''


def p_import(p):
  '''Import : IMPORT ImportStmt
           | IMPORT LPAREN ImportStmtList OSemi RPAREN
           | IMPORT LPAREN RPAREN'''

def p_importstmt(p):
  '''ImportStmt : ImportHere STRING'''

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
        p[0]['type'] = "void"
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
            if(p[1]['type'] != "int" || p[3]['type'] != "int"):
                print("error!")
                exit(1)
        if(str(p[2]) == "|="):
            op = "|"
            typ = p[1]['type']
            if((p[1]['type'] != "int" || p[3]['type'] != "int") && (p[1]['type'] != "bool" || p[3]['type'] != "bool")):
                print("error!")
                exit(1)
        if(str(p[2]) == "&="):
            op = "&"
            typ = p[1]['type']
            if((p[1]['type'] != "int" || p[3]['type'] != "int") && (p[1]['type'] != "bool" || p[3]['type'] != "bool")):
                print("error!")
                exit(1)
        if(str(p[2]) == "<<="):
            op = "<<"
            typ = p[1]['type']
            if(p[1]['type'] != "int" || p[3]['type'] != "int"):
                print("error!")
                exit(1)

        if(str(p[2]) == ">>="):
            op = ">>"
            typ = p[1]['type']
            if(p[1]['type'] != "int" || p[3]['type'] != "int"):
                print("error!")
                exit(1)

        if(str(p[2]) == "&^="):
            op = ""

        flag = 0
        if(str(p[2]) == "="):
            flag = 1
            if(len(p[1]['exprs']) != len(p[3]['exprs'])):
                print("error!")
                exit(1)
            p[0]['code'] = ""
            for i in range(0,len(p[1]['exprs'])):
                if(p[1]['exprs'][i]['type'] != p[3]['exprs'][i]['type']):
                    p[0]['code'] += p[1]['exprs'][i]['exp'] + " = " + p[3]['exprs'][i]['exp'] + "\n"
                else:
                    print("error!")
                    exit(1)

        if(str(p[2]) == ":="):
            flag = 1
            if(len(p[1]['exprs']) != len(p[3]['exprs'])):
                print("error!")
                exit(1)
            p[0]['code'] = ""
            for i in range(0,len(p[1]['exprs'])):
                p[0]['code'] += p[1]['exprs'][i]['exp'] + " = " + p[3]['exprs'][i]['exp'] + "\n"

        if(flag == 0):
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


def p_elseif(p):
  '''ElseIf : ELSE IF IfHeader LoopBody'''

def p_elseiflist(p):
  '''ElseIfList :
                | ElseIf ElseIfList
                | Else'''


def p_else(p):
  '''Else : ELSE CompoundStmt'''

def p_ntype(p):
  '''NType : FuncType
           |  OtherType
           |  PtrType
           |  DotName
           |  LPAREN NType RPAREN
           |  NewType'''


def p_nonexprtype(p):
  '''NonExprType : FuncType
                 | OtherType
                 | TIMES NonExprType'''


def p_othertype(p):
  '''OtherType : LBRACK OExpr RBRACK NType
               | StructType
               | InterfaceType
               | ChannelType'''


def p_channeltype(p):
  '''ChannelType : CHAN NewType
                 | CHAN LMINUS NewType
                 | LMINUS CHAN NewType'''


def p_structtype(p):
  '''StructType : STRUCT LBRACE StructDeclList OSemi RBRACE
                | STRUCT LBRACE RBRACE'''


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


def p_ptrtype(p):
  '''PtrType : TIMES NType'''

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

def p_onewname(p):
  '''ONewName :
              | NewName'''

def p_oexpr(p):
  '''OExpr :
           | Expr'''

def p_oexprlist(p):
  '''OExprList :
               | ExprList'''

def p_funcliteraldecl(p):
  '''FuncLiteralDecl : FuncType'''

def p_funcliteral(p):
  '''FuncLiteral : FuncLiteralDecl LBRACE cmtlist StmtList cmtlist RBRACE'''

def p_exprlist(p):
  '''ExprList : Expr
              | ExprList COMMA Expr'''

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


def p_stmtlist(p):
  '''StmtList : Stmt SEMICOL
                | StmtList cmtlist Stmt SEMICOL'''

def p_newnamelist(p):
  '''NewNameList : NewName
                   | NewNameList COMMA NewName'''


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

def p_prec2expr_(p):
  '''Prec2Expr_ : Prec3Expr_
                  | Prec2Expr_ AMPAMP Prec3Expr_'''

def p_expr(p):
  '''Expr : Prec2Expr_
            | Expr OROR Prec2Expr_
            | CONSTANTS
            | Chexpr
            | Arrayexp'''

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

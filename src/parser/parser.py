import ply.yacc as yacc
import lexer            # Import lexer information
tokens = lexer.tokens   # Need token list

# Rune part yet to be done
graph="digraph finite_state_machine {ordering=out;rankdir=UD;size=\"8,5\";node [shape = circle];\n"
cnt=0


def make_node(p,label,childs):
    global cnt
    global graph
    cnt+=1
    p[0]=str(cnt)
    graph+=p[0] + " [label=\""+ label+"\"];\n"
    num_childs=len(childs)
    for i in childs:
        if(p[i] != "NULL"):
            graph += p[0] + "->"+ str(p[i])+";\n"

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

def add_child(p,p_index,childs):
  global graph
  for i in childs:
    graph+=p[p_index] + "->" +p[i]+";\n"



def p_start(p):
  '''start : SourceFile'''
  bypass(p,1)
    
def p_sourcefile(p):
  '''SourceFile : cmtlist PackageClause cmtlist Imports cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist Imports cmtlist
                | cmtlist PackageClause cmtlist'''
  if(len(p)==8):
    make_node(p,"source_file",[2,4,6])
  elif (len(p)==6):
    make_node(p,"source_file",[2,4])
  else:
    make_node(p,"source_file",[2])


def p_packegeclause(p):
  '''PackageClause : PACKAGE IDENTIFIER SEMICOL'''
  make_leaf(p,2)
  make_node(p,"package_clause",[1,2])

def p_imports(p):
  '''Imports : Import SEMICOL
           | Imports cmtlist Import SEMICOL'''

  if(len(p)==3):
    make_node(p,"import",[1])
  else:
    bypass(p,1)
    add_child(p,0,[3])

def p_import(p):
  '''Import : IMPORT ImportStmt
           | IMPORT LPAREN ImportStmtList OSemi RPAREN
           | IMPORT LPAREN RPAREN'''
  if(len(p)==3):
    bypass(p,2)
  elif(len(p)==6):
    bypass(p,3)
  else:
    pass_empty(p)

def p_importstmt(p):
  '''ImportStmt : ImportHere STRING'''
  make_leaf(p,2)

def p_importstmtlist(p):
  '''ImportStmtList : ImportStmt
               | ImportStmtList SEMICOL ImportStmt'''
  if(len(p)==2):
    bypass(p,1)
  else:
    bypass(p,1)
    add_child(p,0,[3])

def p_importhere(p):
  '''ImportHere : 
           | IDENTIFIER
           | DOT'''
  pass_empty(p)

def p_declaration(p):
  '''Declaration : CommonDecl
            | FuncDecl
            | NonDeclStmt'''
  make_node(p,"Declaration",[1])


def p_commondecl(p):
  '''CommonDecl : CONSTANT ConstDecl
           | CONSTANT LPAREN ConstDecl OSemi RPAREN
           | CONSTANT LPAREN ConstDecl SEMICOL ConstDeclList OSemi RPAREN
           | CONSTANT LPAREN RPAREN
           | VAR VarDecl
           | VAR LPAREN VarDeclList OSemi RPAREN
           | VAR LPAREN RPAREN
           | TYPE TypeDecl
           | TYPE LPAREN TypeDeclList OSemi RPAREN
           | TYPE LPAREN RPAREN'''
  if(len(p)==3):
    bypass(p,2)
  elif(len(p)==6):
    bypass(p,3)
  elif(len(p)==8):
    bypass(p,3)
    add_child(p,0,[5])
  elif(len(p)==4):
    pass_empty(p)

def p_vardecl(p):
  '''VarDecl   : DeclNameList NType
          | DeclNameList NType EQUAL ExprList
          | DeclNameList EQUAL ExprList'''
  if(len(p)==3):
    #something
    make_node(p,"VAR",[1,2])
  elif(len(p)==4):
    #something
    make_node(p,"VAR",[1,2,3])
  else:
    #something
    make_node(p,"VAR",[1,2,3,4])

def p_constdecl(p):
  '''ConstDecl : DeclNameList NType EQUAL ExprList
          | DeclNameList NType
          | DeclNameList EQUAL ExprList'''
  if(len(p)==4):
    make_node(p,"CONS",[1,2,3])
  elif(len(p)==5):
    make_node(p,"CONS",[1,2,3,4])
  else:
    make_node(p,"CONS",[1,2])

def p_constdecl1(p):
  '''ConstDecl1 : ConstDecl
           | DeclNameList'''
  bypass(p,1)
    

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
  if(len(p)==2):
    
  elif(len(p)==3):
    
  else:

def p_case(p):
  '''Case : CASE ExprOrTypeList COLON
     | CASE ExprOrTypeList EQUAL Expr COLON
     | CASE ExprOrTypeList COLONEQ Expr COLON
     | DEFAULT COLON'''
  if(len(p)==3):

  elif(len(p)==4):

  else:


def p_compoundstmt(p):
  '''CompoundStmt : LBRACE cmtlist StmtList cmtlist RBRACE'''

def p_caseblock(p):
  '''CaseBlock : Case StmtList'''

def p_caseblocklist(p):

  '''CaseBlockList : 
                   | CaseBlockList CaseBlock'''
  if(len(p)==1):

  else:

      
def p_loopbody(p):

  '''LoopBody : LBRACE cmtlist StmtList  cmtlist RBRACE'''

def p_rangestmt(p):

  '''RangeStmt : ExprList EQUAL RANGE Expr
               | ExprList COLONEQ RANGE Expr
               | RANGE Expr'''
  if(len(p)==3):

  else:


def p_forheader(p):

  '''ForHeader : OSimpleStmt SEMICOL OSimpleStmt SEMICOL OSimpleStmt
               | OSimpleStmt
               | RangeStmt'''
  if(len(p)==2):

  else:

              
def p_forbody(p):

  '''ForBody : ForHeader LoopBody'''
        
def p_forstmt(p):

  '''ForStmt : FOR ForBody'''

def p_ifheader(p):
  '''IfHeader : OSimpleStmt
           | OSimpleStmt SEMICOL OSimpleStmt'''
  if(len(p)==2):

  else:


def p_ifstmt(p):
  '''IfStmt : IF IfHeader LoopBody ElseIfList Else'''

def p_elseif(p):
  '''ElseIf : ELSE IF IfHeader LoopBody'''
       
def p_elseiflist(p):
  '''ElseIfList : 
                | ElseIfList ElseIf'''
  if(len(p)==1):

  else:

           
def p_else(p):
  '''Else : 
          | ELSE CompoundStmt'''
  if(len(p)==1):
    
  else:

     
def p_ntype(p):
  '''NType : FuncType
           |  OtherType
           |  PtrType
           |  DotName
           |  LPAREN NType RPAREN
           |  TYPE'''
  if(len(p)==2):

  else:

      
def p_nonexprtype(p):
  '''NonExprType : FuncType
                 | OtherType
                 | TIMES NonExprType'''
  if(len(p)==2):
    
  else:

            
def p_othertype(p):
  '''OtherType : LBRACK OExpr RBRACK NType
               | StructType
               | InterfaceType
               | ChannelType'''
  if(len(p)==2):
    
  else:


def p_channeltype(p):
  '''ChannelType : CHAN TYPE
                 | CHAN LMINUS TYPE
                 | LMINUS CHAN TYPE'''
  if(len(p)==3):

  else:


def p_structtype(p):
  '''StructType : STRUCT LBRACE StructDeclList OSemi RBRACE
                | STRUCT LBRACE RBRACE'''
  if(len(p)==4):

  else:

           
def p_interfacetype(p):
  '''InterfaceType : INTERFACE LBRACE InterfaceDeclList OSemi RBRACE
                   | INTERFACE LBRACE RBRACE'''
              

def p_funcdec1(p):
  '''FuncDecl : FUNCTION FuncDecl_ FuncBody'''
         
def p_funcdec1_(p):
  '''FuncDecl_ : IDENTIFIER ArgList FuncRes
               | LEFT_OR OArgTypeListOComma OR_RIGHT IDENTIFIER ArgList FuncRes'''
  if(len(p)==4):

  else:

          
def p_functype(p):
  '''FuncType : FUNCTION ArgList FuncRes'''
         
def p_arglist(p):
  '''ArgList : LPAREN OArgTypeListOComma RPAREN
             | ArgList LPAREN OArgTypeListOComma RPAREN'''
  if(len(p)==4):

  else:

        
def p_funcbody(p):
  '''FuncBody : 
              | LBRACE  cmtlist StmtList  cmtlist RBRACE'''
  if(len(p)==1):

  else:

         
def p_funcres(p):
  '''FuncRes : 
             | FuncRetType
             | LEFT_OR OArgTypeListOComma OR_RIGHT'''
  if(len(p)==1):
    
  elif(len(p)==2):

  else:
        
def p_structdeclist(p):
  '''StructDeclList : StructDecl
                    | StructDeclList SEMICOL StructDecl'''
  if(len(p)==2):

  else:

               
def p_interfacedec1list(p):
  '''InterfaceDeclList : InterfaceDecl
                       | InterfaceDeclList SEMICOL InterfaceDecl'''
  if(len(p)==2):

  else:

                  
def p_structdec1(p):
  '''StructDecl : NewNameList NType OLiteral
                | Embed OLiteral
                | LPAREN Embed RPAREN OLiteral
                | TIMES Embed OLiteral
                | LPAREN TIMES Embed RPAREN OLiteral
                | TIMES LPAREN Embed RPAREN OLiteral'''
  if(len(p)==3):

  elif(len(p)==4):

  elif(len(p)==5):

  else:

           
def p_interfacedec1(p):
  '''InterfaceDecl : NewName InDecl
                   | IDENTIFIER
                   | LPAREN IDENTIFIER RPAREN'''
  if(len(p)==2):

  elif(len(p)==3):
    
  else:

              
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
                 | TYPE'''
            
def p_dotname(p):
  '''DotName : Name
             | Name DOT IDENTIFIER'''
  if(len(p)==2):

  else:

        
def p_ocomma(p):
  '''OComma : 
            | COMMA'''
  if(len(p)==1):
    
  else:

       
def p_osemi(p):
  '''OSemi : 
           | SEMICOL'''
  if(len(p)==1):

  else:

      
def p_osimplestmt(p):
  '''OSimpleStmt : 
                 | SimpleStmt'''
  if(len(p)==1):
    
  else:

    
def p_onewname(p):
  '''ONewName : 
              | NewName'''
  if(len(p)==1):

  else:
      
def p_oexpr(p):
  '''OExpr : 
           | Expr'''
  if(len(p)==1):

  else:

      
def p_oexprlist(p):
  '''OExprList : 
               | ExprList'''
  if(len(p)==1):
    
  else:

          
def p_funcliteraldecl(p):
  '''FuncLiteralDecl : FuncType'''
                
def p_funcliteral(p):
  '''FuncLiteral : FuncLiteralDecl LBRACE cmtlist StmtList cmtlist RBRACE'''
            
def p_exprlist(p):
  '''ExprList : Expr
              | ExprList COMMA Expr'''
  if(len(p)==2):

  else:

         
def p_exprortypelist(p):
  '''ExprOrTypeList : ExprOrType
                    | ExprOrTypeList COMMA ExprOrType'''
  if(len(p)==2):

  else:

               
def p_oliteral(p):
  '''OLiteral : 
              | Literal'''
  if(len(p)==1):
    
  else:

         
def p_literal(p):
  '''Literal : INTEGER
             | FLOAT
             | STRING'''
        
def p_embed(p):
  '''Embed : IDENTIFIER'''
      
def p_dec1list(p):
  '''DeclList : Declaration SEMICOL
              | DeclList cmtlist Declaration SEMICOL'''
  # if(len(p)==3):
  #   make_node(p,"Declaration",[1])    #check this
  # else:
  #   bypass(p,1)
  #   add_child(p,0,3)

def p_var_dec_list(p):
  '''VarDeclList : VarDecl 
                   | VarDeclList SEMICOL VarDecl'''
  if(len(p)==2):

  else:


def p_const_dec_list(p):
  '''ConstDeclList : ConstDecl1
                     | ConstDeclList SEMICOL ConstDecl1'''
  if(len(p)==2):

  else:


def p_type_decl_list(p): 
  '''TypeDeclList : TypeDecl
                    | TypeDeclList SEMICOL TypeDecl'''
  if(len(p)==2):
    
  else:


def p_decl_name_list(p):
  '''DeclNameList : DeclName
                    | DeclNameList COMMA DeclName'''
  if(len(p)==2):
    
  else:


def p_stmtlist(p):
  '''StmtList : Stmt SEMICOL
                | StmtList cmtlist Stmt SEMICOL'''
  if(len(p)==3):

  else:


def p_newnamelist(p):
  '''NewNameList : NewName
                   | NewNameList COMMA NewName'''
  if(len(p)==2):
    
  else:


def p_keyvallist(p):
  '''KeyvalList : Keyval
                  | BareCompLitExpr
                  | KeyvalList COMMA Keyval
                  | KeyvalList COMMA BareCompLitExpr'''
  if(len(p)==2):

  elif(len(p)==4):

  else:


def p_bracedkeyvallist(p):
  '''BracedKeyvalList : 
                        | KeyvalList OComma'''
  if(len(p)==1):
    
  else:


def p_declname(p):
  '''DeclName : IDENTIFIER'''
  
def p_name(p):
  '''Name : IDENTIFIER'''

def p_argtype(p):
  '''ArgType : NameOrType
               | IDENTIFIER NameOrType
               | IDENTIFIER DotDotDot
               | DotDotDot'''
  if(len(p)==2):
    
  else:


def p_argtypelist(p):
  '''ArgTypeList : ArgType
                   | ArgTypeList COMMA ArgType'''
  if(len(p)==2):

  else:


def p_oargtypelistocomma(p):
  '''OArgTypeListOComma : 
                          | ArgTypeList OComma'''
  if(len(p)==1):

  else:


def p_stmt(p):
  '''Stmt : 
            | CompoundStmt
            | CommonDecl
            | NonDeclStmt'''
  if(len(p)==1):

  else:


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

  elif(len(p)==3):

  else:


def p_dotdotdot(p):
  '''DotDotDot : DDD
                 | DDD NType'''
  if(len(p)==2):
    
  else:


def p_pexpr(p):
  '''PExpr : PExprNoParen
             | LPAREN ExprOrType RPAREN'''
  if(len(p)==2):

  else:


def p_pexprnoparen(p):
  '''PExprNoParen : Literal
                    | Name
                    | PExpr DOT IDENTIFIER
                    | PExpr DOT LPAREN ExprOrType RPAREN
                    | PExpr DOT LPAREN TYPE RPAREN
                    | PExpr LBRACK Expr RBRACK
                    | PExpr LBRACK OExpr COLON OExpr RBRACK
                    | PExpr LBRACK OExpr COLON OExpr COLON OExpr RBRACK
                    | PseudoCall
                    | ConvType LEFT_ANGLE Expr OComma RIGHT_ANGLE
                    | CompType LEFT_LEFT BracedKeyvalList RIGHT_RIGHT
                    | PExpr LEFT_LEFT BracedKeyvalList RIGHT_RIGHT
                    | FuncLiteral
                    | ForCompExpr'''
  if(len(p)==2):

  elif(len(p)==4):
    
  elif(len(p)==5):

  elif(len(p)==6):

  elif(len(p)==7):

  else:
    

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
  if(len(p)==2):

  else:


def p_complitexpr(p):
  '''CompLitExpr : Expr
                   | LEFT_LEFT BracedKeyvalList RIGHT_RIGHT'''
  if(len(p)==2):
    
  else:


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
  if(len(p)==2):
    
  else:


def p_prec4expr_(p):
  '''Prec4Expr_ : Prec5Expr_
                  | Prec4Expr_ PLUS Prec5Expr_
                  | Prec4Expr_ MINUS Prec5Expr_
                  | Prec4Expr_ XOR Prec5Expr_
                  | Prec4Expr_ OR Prec5Expr_'''
  if(len(p)==2):
    
  else:


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
    
  else:


def p_prec2expr_(p):
  '''Prec2Expr_ : Prec3Expr_
                  | Prec2Expr_ AMPAMP Prec3Expr_'''
  if(len(p)==2):

  else:


def p_expr(p):
  '''Expr : Prec2Expr_
            | Expr OROR Prec2Expr_
            | CONSTANTS
            | Chexpr
            | Arrayexp'''
  if(len(p)==2):

  else:


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
  if(len(p)==2):

  else:


def p_forcompexpr(p):
  '''ForCompExpr : LBRACK Expr PIPE RangeStmt RBRACK'''

def p_pseudocall(p):
  '''PseudoCall : PExpr LPAREN RPAREN
                  | PExpr LPAREN ExprOrTypeList OComma RPAREN
                  | PExpr LPAREN ExprOrTypeList DDD OComma RPAREN'''
  if(len(p)==4):

  elif(len(p)==6):

  else:


def p_cmtlist(p):
  '''cmtlist : 
              | cmtlist COMMENT'''
  if(len(p)==1):

  else:
    

def p_error(p):
  print("Syntax error in input!")
  print(p)

parser = yacc.yacc()            # Build the parser

with open('../../tests/parser/test1.go','r') as f:
    input_str = f.read()

parser.parse(input_str,debug=0)


graph+="}"
print(graph)
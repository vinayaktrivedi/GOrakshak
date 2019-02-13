
import ply.yacc as yacc
import sys
import os
# from lexer import tokens, data
from lexer import *
from pprint import pprint


precedence = (
    ('right','ASSIGN', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_ASSIGN'),
    ('left', 'LESSER', 'GREATER','LESS_EQUALS','MORE_EQUALS'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIVIDE','MOD'),
)

# ------------------------START----------------------------
def p_start(p):
    '''start : SourceFile'''
    
# -------------------------------------------------------


# -----------------------TYPES---------------------------
def p_type(p):
    '''Type : TypeName
            | TypeLit
            | LPAREN Type RPAREN'''
    
def p_type_name(p):
    '''TypeName : TypeToken
                | QualifiedIdent'''
    

def p_type_token(p):
    '''TypeToken : INT_T
                 | FLOAT_T
                 | UINT_T
                 | COMPLEX_T
                 | RUNE_T
                 | BOOL_T
                 | STRING_T
                 | TYPE IDENTIFIER'''

def p_type_lit(p):
    '''TypeLit : ArrayType
               | StructType
               | PointerType'''


def p_type_opt(p):
    '''TypeOpt : Type
               | epsilon'''
  
# -------------------------------------------------------





# ------------------- ARRAY TYPE -------------------------
def p_array_type(p):
  '''ArrayType : LSQUARE ArrayLength RSQUARE ElementType'''


def p_array_length(p):
  ''' ArrayLength : Expression '''


def p_element_type(p):
  ''' ElementType : Type '''
 

# --------------------------------------------------------


# ----------------- STRUCT TYPE ---------------------------
def p_struct_type(p):
  '''StructType : STRUCT LCURL FieldDeclRep RCURL'''
 

def p_field_decl_rep(p):
  ''' FieldDeclRep : FieldDeclRep FieldDecl SEMICOLON
                  | epsilon '''


def p_field_decl(p):
  ''' FieldDecl : IdentifierList Type TagOpt'''


def p_TagOpt(p):
  ''' TagOpt : Tag
             | epsilon '''
 

def p_Tag(p):
  ''' Tag : STRING '''
 
# ---------------------------------------------------------


# ------------------POINTER TYPES--------------------------
def p_point_type(p):
    '''PointerType : STAR BaseType'''
  

def p_base_type(p):
    '''BaseType : Type'''
  
# ---------------------------------------------------------


# ---------------FUNCTION TYPES----------------------------
def p_sign(p):
    '''Signature : Parameters ResultOpt'''

def p_result_opt(p):
    '''ResultOpt : Result
                 | epsilon'''

def p_result(p):
    '''Result : Parameters
              | Type'''

def p_params(p):
    '''Parameters : LPAREN ParameterListOpt RPAREN'''

def p_param_list_opt(p):
    '''ParameterListOpt : ParametersList
                             | epsilon'''

def p_param_list(p):
    '''ParametersList : Type
                      | IdentifierList Type
                      | ParameterDeclCommaRep'''

def p_param_decl_comma_rep(p):
    '''ParameterDeclCommaRep : ParameterDeclCommaRep COMMA ParameterDecl
                             | ParameterDecl COMMA ParameterDecl'''

def p_param_decl(p):
    '''ParameterDecl : IdentifierList Type
                     | Type'''
# ---------------------------------------------------------


#-----------------------BLOCKS---------------------------
def p_block(p):
    '''Block : LCURL StatementList RCURL'''

def p_stat_list(p):
    '''StatementList : StatementRep'''

def p_stat_rep(p):
    '''StatementRep : StatementRep Statement SEMICOLON
                    | epsilon'''

# ------------------DECLARATIONS and SCOPE------------------------
def p_decl(p):
  '''Declaration : ConstDecl
                 | TypeDecl
                 | VarDecl'''

def p_toplevel_decl(p):
  '''TopLevelDecl : Declaration
                  | FunctionDecl'''
# -------------------------------------------------------


# ------------------CONSTANT DECLARATIONS----------------
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                 | CONST LPAREN ConstSpecRep RPAREN'''

def p_const_spec_rep(p):
    '''ConstSpecRep : ConstSpecRep ConstSpec SEMICOLON
                    | epsilon'''

def p_const_spec(p):
    '''ConstSpec : IdentifierList TypeExprListOpt'''

def p_type_expr_list(p):
    '''TypeExprListOpt : TypeOpt ASSIGN ExpressionList
                       | epsilon'''

def p_identifier_list(p):
    '''IdentifierList : IDENTIFIER IdentifierRep'''

def p_identifier_rep(p):
    '''IdentifierRep : IdentifierRep COMMA IDENTIFIER
                     | epsilon'''

def p_expr_list(p):
    '''ExpressionList : Expression ExpressionRep'''

def p_expr_rep(p):
    '''ExpressionRep : ExpressionRep COMMA Expression
                     | epsilon'''
# -------------------------------------------------------


# ------------------TYPE DECLARATIONS-------------------
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LPAREN TypeSpecRep RPAREN'''

def p_type_spec_rep(p):
    '''TypeSpecRep : TypeSpecRep TypeSpec SEMICOLON
                   | epsilon'''

def p_type_spec(p):
    '''TypeSpec : AliasDecl
                | TypeDef'''

def p_alias_decl(p):
    '''AliasDecl : IDENTIFIER ASSIGN Type'''
# -------------------------------------------------------


# -------------------TYPE DEFINITIONS--------------------
def p_type_def(p):
    '''TypeDef : IDENTIFIER Type'''
# -------------------------------------------------------


# ----------------VARIABLE DECLARATIONS------------------
def p_var_decl(p):
    '''VarDecl : VAR VarSpec
               | VAR LPAREN VarSpecRep RPAREN'''

def p_var_spec_rep(p):
    '''VarSpecRep : VarSpecRep VarSpec SEMICOLON
                  | epsilon'''

def p_var_spec(p):
    '''VarSpec : IdentifierList Type ExpressionListOpt
               | IdentifierList ASSIGN ExpressionList'''

def p_expr_list_opt(p):
    '''ExpressionListOpt : ASSIGN ExpressionList
                         | epsilon'''

# ----------------SHORT VARIABLE DECLARATIONS-------------
def p_short_var_decl(p):
  ''' ShortVarDecl : IDENTIFIER QUICK_ASSIGN Expression '''
# -------------------------------------------------------



# ----------------FUNCTION DECLARATIONS------------------
def p_func_decl(p):
    '''FunctionDecl : FUNC FunctionName Function
                    | FUNC FunctionName Signature'''

def p_func_name(p):
    '''FunctionName : IDENTIFIER'''

def p_func(p):
    '''Function : Signature FunctionBody'''

def p_func_body(p):
    '''FunctionBody : Block'''
# -------------------------------------------------------


# ----------------------OPERAND----------------------------
def p_operand(p):
    '''Operand : Literal
               | OperandName
               | LPAREN Expression RPAREN'''

def p_literal(p):
    '''Literal : BasicLit'''
               #| CompositeLit'''

def p_basic_lit(p):
    '''BasicLit : INTEGER
                | OCTAL
                | HEX
                | FLOAT
                | IMAGINARY
                | RUNE
                | STRING'''

def p_operand_name(p):
    '''OperandName : IDENTIFIER'''
# ---------------------------------------------------------


# -------------------QUALIFIED IDENTIFIER----------------
def p_quali_ident(p):
    '''QualifiedIdent : IDENTIFIER DOT TypeName'''
# -------------------------------------------------------


# -----------------COMPOSITE LITERALS----------------------
def p_comp_lit(p):
    '''CompositeLit : LiteralType LiteralValue'''

def p_lit_type(p):
    '''LiteralType : ArrayType
                   | ElementType
                   | TypeName'''

def p_lit_val(p):
    '''LiteralValue : LCURL ElementListOpt RCURL'''

def p_elem_list_comma_opt(p):
    '''ElementListOpt : ElementList
                           | epsilon'''

def p_elem_list(p):
    '''ElementList : KeyedElement KeyedElementCommaRep'''

def p_key_elem_comma_rep(p):
    '''KeyedElementCommaRep : KeyedElementCommaRep COMMA KeyedElement
                            | epsilon'''

def p_key_elem(p):
    '''KeyedElement : Key COLON Element
                    | Element'''

def p_key(p):
    '''Key : FieldName
           | Expression
           | LiteralValue'''

def p_field_name(p):
    '''FieldName : IDENTIFIER'''

def p_elem(p):
    '''Element : Expression
               | LiteralValue'''
    p[0] = ["Element", p[1]]
# ---------------------------------------------------------


# ------------------PRIMARY EXPRESSIONS--------------------
def p_prim_expr(p):
    '''PrimaryExpr : Operand
                   | PrimaryExpr Selector
                   | Conversion
                   | PrimaryExpr Index
                   | PrimaryExpr Slice
                   | PrimaryExpr TypeAssertion
                   | PrimaryExpr Arguments'''
    if len(p) == 2:
        p[0] = ["PrimaryExpr", p[1]]
    else:
        p[0] = ["PrimaryExpr", p[1], p[2]]

def p_selector(p):
    '''Selector : DOT IDENTIFIER'''
    p[0] = ["Selector", ".", p[2]]

def p_index(p):
    '''Index : LSQUARE Expression RSQUARE'''
    p[0] = ["Index", "[", p[2], "]"]

def p_slice(p):
    '''Slice : LSQUARE ExpressionOpt COLON ExpressionOpt RSQUARE
             | LSQUARE ExpressionOpt COLON Expression COLON Expression RSQUARE'''
    if len(p) == 6:
        p[0] = ["Slice", "[", p[2], ":", p[4], "]"]
    else:
        p[0] = ["Slice", "[", p[2], ":", p[4], ":", p[6], "]"]

def p_type_assert(p):
    '''TypeAssertion : DOT LPAREN Type RPAREN'''
    p[0] = ["TypeAssertion", ".", "(", p[3], ")"]

def p_argument(p):
    '''Arguments : LPAREN ExpressionListTypeOpt RPAREN'''
    p[0] = ["Arguments", "(", p[2], ")"]

def p_expr_list_type_opt(p):
    '''ExpressionListTypeOpt : ExpressionList
                             | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListTypeOpt", p[1], p[2]]
    else:
        p[0] = ["ExpressionListTypeOpt", p[1]]

#def p_comma_opt(p):
#    '''CommaOpt : COMMA
#                | epsilon'''
#    if p[1] == ",":
#        p[0] = ["CommaOpt", ","]
#    else:
#        p[0] = ["CommaOpt", p[1]]

def p_expr_list_comma_opt(p):
    '''ExpressionListCommaOpt : COMMA ExpressionList
                              | epsilon'''
    if len(p) == 3:
        p[0] = ["ExpressionListCommaOpt", ",", p[2]]
    else:
        p[0] = ["ExpressionListCommaOpt", p[1]]
# ---------------------------------------------------------


#----------------------OPERATORS-------------------------
def p_expr(p):
    '''Expression : UnaryExpr
                  | Expression BinaryOp Expression'''
    if len(p) == 4:
        p[0] = ["Expression", p[1], p[2], p[3]]
    else:
        p[0] = ["Expression", p[1]]

def p_expr_opt(p):
    '''ExpressionOpt : Expression
                     | epsilon'''
    p[0] = ["ExpressionOpt", p[1]]

def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr
                 | UnaryOp UnaryExpr
                 | NOT UnaryExpr'''
    if len(p) == 2:
        p[0] = ["UnaryExpr", p[1]]
    elif p[1] == "!":
        p[0] = ["UnaryExpr", "!", p[2]]
    else:
        p[0] = ["UnaryExpr", p[1], p[2]]

def p_binary_op(p):
    '''BinaryOp : LOGICAL_OR
                | LOGICAL_AND
                | RelOp
                | AddMulOp'''
    if p[1] == "||":
        p[0] = ["BinaryOp", "||"]
    elif p[1] == "&&":
        p[0] = ["BinaryOp", "&&"]
    else:
        p[0] = ["BinaryOp", p[1]]

def p_rel_op(p):
    '''RelOp : EQUALS
             | NOT_ASSIGN
             | LESSER
             | GREATER
             | LESS_EQUALS
             | MORE_EQUALS'''
    if p[1] == "==":
        p[0] = ["RelOp", "=="]
    elif p[1] == "!=":
        p[0] = ["RelOp", "!="]
    elif p[1] == "<":
        p[0] = ["RelOp", "<"]
    elif p[1] == ">":
        p[0] = ["RelOp", ">"]
    elif p[1] == "<=":
        p[0] = ["RelOp", "<="]
    elif p[1] == ">=":
        p[0] = ["RelOp", ">="]

def p_add_mul_op(p):
    '''AddMulOp : UnaryOp
                | OR
                | XOR
                | DIVIDE
                | MOD
                | LSHIFT
                | RSHIFT'''
    if p[1] == "/":
        p[0] = ["AddMulOp", "/"]
    elif p[1] == "%":
        p[0] = ["AddMulOp", "%"]
    elif p[1] == "|":
        p[0] = ["AddMulOp", "|"]
    elif p[1] == "^":
        p[0] = ["AddMulOp", "^"]
    elif p[1] == "<<":
        p[0] = ["AddMulOp", "<<"]
    elif p[1] == ">>":
        p[0] = ["AddMulOp", ">>"]
    else:
        p[0] = ["AddMulOp", p[1]]

def p_unary_op(p):
    '''UnaryOp : PLUS
               | MINUS
               | STAR
               | AND '''
    if p[1] == '+':
        p[0] = ["UnaryOp", "+"]
    elif p[1] == '-':
        p[0] = ["UnaryOp", "-"]
    elif p[1] == '*':
        p[0] = ["UnaryOp", "*"]
    elif p[1] == '&':
        p[0] = ["UnaryOp", "&"]
# -------------------------------------------------------




# -----------------CONVERSIONS-----------------------------
def p_conversion(p):
    '''Conversion : TYPECAST Type LPAREN Expression RPAREN'''
    p[0] = ["Conversion", p[1], p[2],  "(", p[4], ")"]
# ---------------------------------------------------------






# ---------------- STATEMENTS -----------------------
def p_statement(p):
    '''Statement : Declaration
                 | LabeledStmt
                 | SimpleStmt
                 | ReturnStmt
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
                 | Block
                 | IfStmt
                 | SwitchStmt
                 | ForStmt '''
    p[0] = ["Statement", p[1]]



def p_simple_stmt(p):
  ''' SimpleStmt : epsilon
                 | ExpressionStmt
                 | IncDecStmt
                 | Assignment
                 | ShortVarDecl '''
  p[0] = ["SimpleStmt", p[1]]


def p_labeled_statements(p):
  ''' LabeledStmt : Label COLON Statement '''
  p[0] = ["LabeledStmt", p[1], ":", p[3]]

def p_label(p):
  ''' Label : IDENTIFIER '''
  p[0] = ["Label", p[1]]


def p_expression_stmt(p):
  ''' ExpressionStmt : Expression '''
  p[0] = ["ExpressionStmt", p[1]]

def p_inc_dec(p):
  ''' IncDecStmt : Expression INCR
                 | Expression DECR '''
  if p[2] == '++':
    p[0] = ["IncDecStmt", p[1], "++"]
  else:
    p[0] = ["IncDecStmt", p[1], "--"]


def p_assignment(p):
  ''' Assignment : ExpressionList assign_op ExpressionList'''
  p[0] = ["Assignment", p[1], p[2], p[3]]

def p_assign_op(p):
  ''' assign_op : AssignOp'''
  p[0] = ["assign_op", p[1]]

def p_AssignOp(p):
  ''' AssignOp : PLUS_ASSIGN
               | MINUS_ASSIGN
               | STAR_ASSIGN
               | DIVIDE_ASSIGN
               | MOD_ASSIGN
               | AND_ASSIGN
               | OR_ASSIGN
               | XOR_ASSIGN
               | LSHIFT_ASSIGN
               | RSHIFT_ASSIGN
               | ASSIGN '''
  p[0] = ["AssignOp", p[1]]


def p_if_statement(p):
  ''' IfStmt : IF Expression Block ElseOpt '''
  p[0] = ["IfStmt", "if", p[2], p[3], p[4]]

def p_SimpleStmtOpt(p):
  ''' SimpleStmtOpt : SimpleStmt SEMICOLON
                    | epsilon '''
  if len(p) == 3:
    p[0] = ["SimpleStmtOpt", p[1], ";"]
  else :
    p[0] = ["SimpleStmtOpt", p[1]]

def p_else_opt(p):
  ''' ElseOpt : ELSE IfStmt
              | ELSE Block
              | epsilon '''
  if len(p) == 3:
    p[0] = ["ElseOpt", "else", p[2]]
  else:
    p[0] = ["ElseOpt", p[1]]

# ----------------------------------------------------------------





# ----------- SWITCH STATEMENTS ---------------------------------

def p_switch_statement(p):
  ''' SwitchStmt : ExprSwitchStmt
                 | TypeSwitchStmt '''
  p[0] = ["SwitchStmt", p[1]]


def p_expr_switch_stmt(p):
  ''' ExprSwitchStmt : SWITCH ExpressionOpt LCURL ExprCaseClauseRep RCURL'''
  p[0] = ["ExpressionStmt", "switch", p[2], p[3], "{", p[5], "}"]

def p_expr_case_clause_rep(p):
  ''' ExprCaseClauseRep : ExprCaseClauseRep ExprCaseClause
                        | epsilon'''
  if len(p) == 3:
    p[0] = ["ExprCaseClauseRep", p[1], p[2]]
  else:
    p[0] = ["ExprCaseClauseRep", p[1]]

def p_expr_case_clause(p):
  ''' ExprCaseClause : ExprSwitchCase COLON StatementList'''
  p[0] = ["ExprCaseClause", p[1], ":", p[3]]

def p_expr_switch_case(p):
  ''' ExprSwitchCase : CASE ExpressionList
                     | DEFAULT '''
  if len(p) == 3:
    p[0] = ["ExprSwitchCase", "case", p[2]]
  else:
    p[0] = ["ExprSwitchCase", p[1]]

def p_type_switch_stmt(p):
  ''' TypeSwitchStmt : SWITCH SimpleStmtOpt TypeSwitchGuard LCURL TypeCaseClauseOpt RCURL'''
  p[0] = ["TypeSwitchStmt", "switch", p[2], p[3],"{", p[5], "}"]


def p_type_switch_guard(p):
  ''' TypeSwitchGuard : IdentifierOpt PrimaryExpr DOT LPAREN TYPE RPAREN '''

  p[0] = ["TypeSwitchGuard", p[1], p[2], ".", "(", "type", ")"]

def p_identifier_opt(p):
  ''' IdentifierOpt : IDENTIFIER QUICK_ASSIGN
                    | epsilon '''

  if len(p) == 3:
    p[0] = ["IdentifierOpt", p[1], ":="]
  else:
    p[0] = ["IdentifierOpt", p[1]]

def p_type_case_clause_opt(p):
  ''' TypeCaseClauseOpt : TypeCaseClauseOpt TypeCaseClause
                        | epsilon '''
  if len(p) == 3:
    p[0] = ["TypeCaseClauseOpt", p[1], p[2]]
  else:
    p[0] = ["TypeCaseClauseOpt", p[1]]

def p_type_case_clause(p):
  ''' TypeCaseClause : TypeSwitchCase COLON StatementList'''
  p[0] = ["TypeCaseClause", p[1], ":", p[3]]


def p_type_switch_case(p):
  ''' TypeSwitchCase : CASE TypeList
                     | DEFAULT '''
  if len(p) == 3:
    p[0] = ["TypeSwitchCase", p[1], p[2]]
  else:
    p[0] = ["TypeSwitchCase", p[1]]

def p_type_list(p):
  ''' TypeList : Type TypeRep'''
  p[0] = ["TypeList", p[1], p[2]]

def p_type_rep(p):
  ''' TypeRep : TypeRep COMMA Type
              | epsilon '''
  if len(p) == 4:
    p[0] = ["TypeRep", p[1], ",", p[3]]
  else:
    p[0] = ["TypeRep", p[1]]

# -----------------------------------------------------------






# --------- FOR STATEMENTS AND OTHERS (MANDAL) ---------------
def p_for(p):
  '''ForStmt : FOR ConditionBlockOpt Block'''
  p[0] = ["ForStmt", "for", p[2], p[3]]
  print(p[1])

def p_conditionblockopt(p):
  '''ConditionBlockOpt : epsilon
             | Condition
             | ForClause
             | RangeClause'''
  p[0] = ["ConditionBlockOpt", p[1]]

def p_condition(p):
  '''Condition : Expression '''
  p[0] = ["Condition", p[1]]

def p_forclause(p):
  '''ForClause : SimpleStmt SEMICOLON ConditionOpt SEMICOLON SimpleStmt'''
  p[0] = ["ForClause", p[1], ";", p[3], ";", p[5]]

# def p_initstmtopt(p):
#   '''InitStmtOpt : epsilon
#            | InitStmt '''
#   p[0] = ["InitStmtOpt", p[1]]

# def p_init_stmt(p):
#   ''' InitStmt : SimpleStmt'''
#   p[0] = ["InitStmt", p[1]]


def p_conditionopt(p):
  '''ConditionOpt : epsilon
          | Condition '''
  p[0] = ["ConditionOpt", p[1]]

# def p_poststmtopt(p):
#   '''PostStmtOpt : epsilon
#            | PostStmt '''
#   p[0] = ["PostStmtOpt", p[1]]

# def p_post_stmt(p):
#   ''' PostStmt : SimpleStmt '''
#   # p[0] = ["PostStmt", p[1]]

def p_rageclause(p):
  '''RangeClause : ExpressionIdentListOpt RANGE Expression'''
  p[0] = ["RangeClause", p[1], "range", p[3]]

def p_expression_ident_listopt(p):
  '''ExpressionIdentListOpt : epsilon
             | ExpressionIdentifier'''
  p[0] = ["ExpressionIdentListOpt", p[1]]

def p_expressionidentifier(p):
  '''ExpressionIdentifier : ExpressionList ASSIGN'''
  if p[2] == "=":
    p[0] = ["ExpressionIdentifier", p[1], "="]
  else:
    p[0] = ["ExpressionIdentifier", p[1], ":="]

def p_return(p):
  '''ReturnStmt : RETURN ExpressionListPureOpt'''
  p[0] = ["ReturnStmt", "return", p[2]]

def p_expressionlist_pure_opt(p):
  '''ExpressionListPureOpt : ExpressionList
             | epsilon'''
  p[0] = ["ExpressionListPureOpt", p[1]]

def p_break(p):
  '''BreakStmt : BREAK LabelOpt'''
  p[0] = ["BreakStmt", "break", p[2]]

def p_continue(p):
  '''ContinueStmt : CONTINUE LabelOpt'''
  p[0] = ["ContinueStmt", "continue", p[2]]

def p_labelopt(p):
  '''LabelOpt : Label
        | epsilon '''
  p[0] = ["LabelOpt", p[1]]

def p_goto(p):
  '''GotoStmt : GOTO Label '''
  p[0] = ["GotoStmt", "goto", p[2]]
# -----------------------------------------------------------


# ----------------  SOURCE FILE --------------------------------
def p_source_file(p):
    '''SourceFile : PackageClause SEMICOLON ImportDeclRep TopLevelDeclRep'''
    p[0] = ["SourceFile", p[1], ";", p[3], p[4]]

def p_import_decl_rep(p):
  '''ImportDeclRep : epsilon
           | ImportDeclRep ImportDecl SEMICOLON'''
  if len(p) == 4:
    p[0] = ["ImportDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["ImportDeclRep", p[1]]

def p_toplevel_decl_rep(p):
  '''TopLevelDeclRep : TopLevelDeclRep TopLevelDecl SEMICOLON
                     | epsilon'''
  if len(p) == 4:
    p[0] = ["TopLevelDeclRep", p[1], p[2], ";"]
  else:
    p[0] = ["TopLevelDeclRep", p[1]]
# --------------------------------------------------------


# ---------- PACKAGE CLAUSE --------------------
def p_package_clause(p):
    '''PackageClause : PACKAGE PackageName'''
    p[0] = ["PackageClause", "package", p[2]]


def p_package_name(p):
    '''PackageName : IDENTIFIER'''
    p[0] = ["PackageName", p[1]]
# -----------------------------------------------


# --------- IMPORT DECLARATIONS ---------------
def p_import_decl(p):
  '''ImportDecl : IMPORT ImportSpec
          | IMPORT LPAREN ImportSpecRep RPAREN '''
  if len(p) == 3:
    p[0] = ["ImportDecl", "import", p[2]]
  else:
    p[0] = ["ImportDecl", "import", "(", p[3], ")"]

def p_import_spec_rep(p):
  ''' ImportSpecRep : ImportSpecRep ImportSpec SEMICOLON
            | epsilon '''
  if len(p) == 4:
    p[0] = ["ImportSpecRep", p[1], p[2], ";"]
  else:
    p[0] = ["ImportSpecRep", p[1]]

def p_import_spec(p):
  ''' ImportSpec : PackageNameDotOpt ImportPath '''
  p[0] = ["ImportSpec", p[1], p[2]]

def p_package_name_dot_opt(p):
  ''' PackageNameDotOpt : DOT
                        | PackageName
                        | epsilon'''
  if p[1]== '.':
    p[0] = ["PackageNameDotOpt", "."]
  else:
    p[0] = ["PackageNameDotOpt", p[1]]

def p_import_path(p):
  ''' ImportPath : STRING '''
  p[0] = ["ImportPath", p[1]]
# -------------------------------------------------------


def p_empty(p):
  '''epsilon : '''
  p[0] = "epsilon"

# def p_import_decl(p):








# def p_start(p):
#   '''start : expression'''
#   # p[0] = "<start>" + p[1] + "</start>"
#   p[0] = ['start', p[1]]

# def p_expression_plus(p):
#     '''expression : expression PLUS term
#                   | expression MINUS term'''
#     if p[2] == '+':
#         # p[0] = "<expr>" + p[1] + "</expr> + " + p[3]
#         p[0] = ["expression", p[1], '+', p[3]]
#     else:
#         # p[0] = "<expr>" + p[1] + "</expr> - " + p[3]
#         p[0] = ["expression", p[1], '-', p[3]]
#         # p[0] = p[1] - p[3]
# # def p_expression_minus(p):
# #     'expression : '

# def p_expression_term(p):
#     'expression : term'
#     # p[0] = "<term>" + p[1] + "</term>"
#     p[0] = ["expression", p[1]]

# def p_term_times(p):
#     'term : term STAR factor'
#     # p[0] = "<term>" + p[1] + "</term> * " + "<factor>" + p[3] + "</factor>"
#     p[0] = ["term", p[1], "*", p[3]]



# # def p_term_div(p):
# #     'term : term DIVIDE factor'
# #     p[0] = p[1] / p[3]

# def p_term_factor(p):
#     'term : factor'
#     p[0] = ["term", p[1]]

# def p_factor_num(p):
#     'factor : INTEGER'
#     # p[0] = str(p[1])
#     p[0] = ["factor", str(p[1])]

# # def p_factor_expr(p):
# #     'factor : LPAREN expression RPAREN'
# #     p[0] = p[2]



# Error rule for syntax errors


def p_error(p):
  print("Syntax error in input!")
  print(p)


# Build the parser
parser = yacc.yacc()

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
ap.add_argument("-c", "--code",help="name of 3AC output file")
ap.add_argument("-s", "--csv",help="name of csv file")
args = vars(ap.parse_args())

if args["input"] is None:
    args["input"] = "test1.go"

if args["code"] is None:
    args["code"] = "code.txt"

if args["csv"] is None:
    args["csv"] = "symbol_table.csv"

file = args["input"]

offset = 0
# outfile = open(args["output"],"w")

outfile = open(args["code"],"w")
outfile1 = open(args["csv"],"w")

globalsymboltable = {}
globalsymboltable['local_variable_size'] = 0
globalsymboltable["CS335_name"] = "globalsymboltable"
globalsymboltable["CS335_type"] = "global_symbol_table"
globalsymboltable['custom_types'] = {}
globalsymboltable['custom_types']['structures'] = {}
stack = []
stack.append(globalsymboltable)
counter=0
size = {}
size['int'] = 4
size['float'] = 4
size['bool'] = 1
size['char'] = 1

def getlabel():
  global counter
  counter += 1
  return "CS335_"+str(counter)

def make_symbol_table(label,tabletype): #use global keyword
    global stack
    prev_table = stack[-1]
    local_symbol_table = {}
    local_symbol_table['local_variable_size'] = 0
    local_symbol_table["CS335_name"]=label
    if(type != None):
      local_symbol_table["CS335_type"]=tabletype
    if "CS335_childtables" in prev_table.keys():
        pass
    else:
        prev_table["CS335_childtables"] = []
    prev_table["CS335_childtables"].append(local_symbol_table)
    local_symbol_table['CS335_parent'] = prev_table
    # Does making a symbol table always require to set the current symbol table to the new one
    stack.append(local_symbol_table)
    return local_symbol_table

def go_one_level_up():
    global stack
    stack = stack[:-1]

def get_current_func_sym_table():
    global stack
    i = len(stack) - 1
    while(i >= 0):
        if(stack[i]['CS335_type'] != 'function'):
            i = i - 1
        else:
            return stack[i]
    return stack[i+1]

def add_variable_attribute(variable,attribute,value):
    global stack
    symbol_table = stack[-1]
    try:
        if symbol_table[variable]['exists'] == 0:
            return 0
        else:
            symbol_table[variable][attribute] = value
            return 1
    except:
        return 0

def get_variable_attribute(variable,attribute):
    global stack
    global globalsymboltable
    local_symbol_table = stack[-1]
    while 1:

        if variable in local_symbol_table:
          if attribute in local_symbol_table[variable]:
            return local_symbol_table[variable][attribute]
          else:
            return -1
        else:
          if(local_symbol_table == globalsymboltable):
            return -1
          local_symbol_table = local_symbol_table['CS335_parent']

def register_variable(variable):
    if variable in lexer.keywords:
      print("Error in line "+str(p.lineno(2))+" :tried to declare reserved keyword")
      exit(1)
    global stack
    symbol_table = stack[-1]
    symbol_table[variable] = {}
    symbol_table[variable]['exists'] = 1
    return

def add_variable_attribute_api(variable,attribute,value):
    add_variable_attribute(variable,attribute,value)

def check_if_variable_declared(variable):
    global stack
    global globalsymboltable
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

    if 'CS335_childtables' in globalsymboltable:
      child_tables = globalsymboltable['CS335_childtables']
      for childs in child_tables:
        if(childs['CS335_type'] == 'function' and childs['CS335_name'] == variable):
          return 1

    return 0

def increase_local_size(size):
  global stack
  symbol_table = stack[-1]

  #print(size)
  if 'local_variable_size' in symbol_table:
    symbol_table['local_variable_size'] += size
  else:
    symbol_table['local_variable_size'] = size

def get_function_symbol_tables(funcname):
  global globalsymboltable
  child_tables = globalsymboltable['CS335_childtables']
  ret=[]
  for child in child_tables:
    if(child['CS335_type'] == 'function' and child['CS335_name'] == funcname):
      ret.append(child)
  if len(ret)==0:
    return -1
  return ret


def get_size():
  global stack
  symbol_table = stack[-1]
  return symbol_table['local_variable_size']

def bfs():
    symout=""
    global globalsymboltable
    visited, queue = set(), [globalsymboltable]
    while queue:
        current = queue.pop(0)
        if current["CS335_name"] not in visited:
            visited.add(current["CS335_name"])
            #do work
            symout+="Table Info:\n"
            symout+="Name="+current["CS335_name"]+",Type="+current["CS335_type"]+"\n"
            symout+="Table Variables:\n"
            for key, var in current.items():
              if(key=="CS335_childtables" or key=="CS335_show_label" or key=="CS335_update_label" or key=="CS335_loop_label" or key=="CS335_exit_label" or key=="CS335_name" or key=="CS335_type" or key=="local_variable_size" or key=="CS335_parent" or key=="CS335_args" or key=="CS335_response"):
                continue
              symout+="variable name="+str(key)+","
              for attr,val in var.items():
                symout+="attribute="+str(attr)+","+"value="+str(val)+","
              symout+="\n"
            if "CS335_childtables" in current:
              symout+="Child Tables:\n"
              for i,childtable in enumerate(current["CS335_childtables"]):
                queue.append(childtable)
                if((i+1) == len(current["CS335_childtables"])):
                  symout+=childtable["CS335_name"]
                else:
                  symout+=childtable["CS335_name"]+","
              symout+="\n"
            symout+="\n"
    #with open(args['csv'],'wb') as f:
      #f.write(symout)
    dummy = 0


def p_start(p):
  '''start : SourceFile'''
  p[0] = {}
  p[0]['code'] = p[1]['code']
  ir = p[0]['code'].split('\n')
  # ir = [str.strip() for str in p[0]['code'].splitlines()]
  ir = filter(bool, p[0]['code'].splitlines())
  out = ""
  for str in ir:
      out += str + "\n"
  outfile.write(out)
  bfs()

def p_sourcefile(p):
    '''SourceFile : cmtlist PackageClause cmtlist Imports cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist DeclList cmtlist
                | cmtlist PackageClause cmtlist Imports cmtlist
                | cmtlist PackageClause cmtlist'''
    p[0] = {}
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
  p[0] = {}
  p[0]['code'] = 'package ' + str(p[2])

def p_imports(p):
    '''Imports : Import SEMICOL
           | Imports cmtlist Import SEMICOL'''
    p[0] = {}
    if(len(p)==3):
        p[0]['code'] = p[1]['code']
    else:
        p[0]['code'] = p[1]['code'] + "\n" + p[3]['code']

def p_import(p):
    '''Import : IMPORT ImportStmt
           | IMPORT LPAREN ImportStmtList OSemi RPAREN
           | IMPORT LPAREN RPAREN'''
    p[0] = {}
    if(len(p)==3):
        p[0]['code'] = p[2]['code']
    elif(len(p)==6):
        p[0]['code']=""
        for i in range(0,len(p[3])):
            if((i+1)==len(p[3])):
                p[0]['code'] += p[3][i]
            else:
                p[0]['code'] += p[3][i]+"\n"

def p_importstmt(p):
    '''ImportStmt : ImportHere STRING'''
    p[0] = {}
    p[0]['code'] = 'import '+str(p[2])
    register_variable(str(p[2]))
    add_variable_attribute(str(p[2]),"import",1)

def p_importstmtlist(p):
    '''ImportStmtList : ImportStmt
               | ImportStmtList SEMICOL ImportStmt'''
    p[0]=[]
    if(len(p)==2):
        p[0].append(p[1]['code'])
    else:
        p[0].extend(p[1])
        p[0].append(p[3]['code'])

def p_importhere(p):
  '''ImportHere :
           | IDENTIFIER
           | DOT'''

def p_declaration(p):
    '''Declaration : CommonDecl
            | FuncDecl
            | NonDeclStmt'''
    p[0] = {}
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
    # need to do for this
    p[0] = {}
    p[0]['code'] = ""
    if(len(p)==3):
      p[0]['code'] = p[2]['code']


def p_vardecl(p):
    '''VarDecl   : DeclNameList NType
          | DeclNameList NType EQUAL ExprList
          | DeclNameList EQUAL ExprList'''
    p[0] = {}
    p[0]['code'] = ""
    global size
    global offset
    if(len(p)==3):
        for var in p[1]['variable']:
            add_variable_attribute_api(var,'type',p[2]['type'])
            add_variable_attribute_api(var,'offset',offset)
            if(p[2]['type']['val'] == 'array'):
              increase_local_size(size[p[2]['type']['arr_type']]*p[2]['type']['arr_length'])
              offset += size[p[2]['type']['arr_type']]*p[2]['type']['arr_length']
            elif(p[2]['type']['val'][0] == '*'):
              increase_local_size(4)
              offset += 4
            elif p[2]['type']['val'] == 'struct' :
              increase_local_size(p[2]['type']['size'])
              offset += p[2]['type']['size']
            else:
              increase_local_size(size[p[2]['type']['val']])
              offset += size[p[2]['type']['val']]

    elif(len(p)==4):
      i = 0
      if(len(p[1]['variable']) != len(p[3]['exprs'])):
        print("Error in line "+str(p.lineno(2))+" :type mismatch")
        exit(1)

      for j in range(0,len(p[1]['variable'])):
        var = p[1]['variable'][j]
        add_variable_attribute_api(var,'type',p[3]['type'])
        add_variable_attribute_api(var,'value',p[3]['exprs'][i]['value'])
        add_variable_attribute_api(var,'offset',offset)
        p[0]['code'] += var+" = "+p[3]['exprs'][i]['place']+"\n"
        increase_local_size(size[p[3]['type']['val']])
        offset += size[p[3]['type']['val']]
        i = i+1
    else:
      i=0
      if(p[4]['exprs'][0]['type'] != p[2]['type']['val']):
        print("Error in line "+str(p.lineno(3))+" :Type of variable and value assigned type don't match")
        exit(1)
      else:
        if(len(p[1]['variable']) != len(p[4]['exprs'])):
          print("Error in line "+str(p.lineno(3))+" : mismatch in no of variables and no of assignments")
          exit(1)

        for j in range(0,len(p[1]['variable'])):
          var = p[1]['variable'][j]
          add_variable_attribute_api(var,'type',p[2]['type'])
          add_variable_attribute_api(var,'value',p[4]['exprs'][i]['value'])
          add_variable_attribute_api(var,'offset',offset)
          p[0]['code'] += var+" = "+p[4]['exprs'][i]['place']+"\n"
          increase_local_size(size[p[2]['type']['val']])
          offset += size[p[2]['type']['val']]
          i = i+1


def p_constdecl(p):
    '''ConstDecl : DeclNameList NType EQUAL ExprList
          | DeclNameList NType
          | DeclNameList EQUAL ExprList '''
    p[0] = {}
    p[0]['code'] = ""
    global size
    global offset
    if(len(p)==3):
        for var in p[1]['variable']:
            add_variable_attribute_api(var,'type',p[2]['type'])
            add_variable_attribute_api(var,'offset',offset)
            increase_local_size(size[p[2]['type']['val']])
            offset += size[p[2]['type']['val']]
    elif(len(p)==4):
      i = 0
      if(len(p[1]['variable']) != len(p[3]['exprs'])):
        print("Error in line "+str(p.lineno(2))+" :type mismatch")
        exit(1)
      for var in p[1]['variable']:
        add_variable_attribute_api(var,'type',p[3]['type'])
        add_variable_attribute_api(var,'value',p[3]['exprs'][i]['value'])
        add_variable_attribute_api(var,'offset',offset)
        p[0]['code'] += var+" = "+p[3]['exprs'][i]['place']+"\n"
        increase_local_size(size[p[3]['type']['val']])
        offset += size[p[3]['type']['val']]
        i = i+1
    else:
      i=0
      if(p[4]['exprs'][0]['type'] != p[2]['type']['val']):
        print("Error in line "+str(p.lineno(3))+" :Type of variable and value assigned type don't match")
        exit(1)
      else:
        if(len(p[1]['variable']) != len(p[4]['exprs'])):
          print("Error in line "+str(p.lineno(3))+" : mismatch in no. of expressions on lhs and rhs")
          exit(1)

        for var in p[1]['variable']:
          add_variable_attribute_api(var,'type',p[2]['type'])
          add_variable_attribute_api(var,'value',p[4]['exprs'][i]['value'])
          add_variable_attribute_api(var,'offset',offset)
          p[0]['code'] += var+" = "+p[4]['exprs'][i]['place']+"\n"
          increase_local_size(size[p[2]['type']['val']])
          offset += size[p[2]['type']['val']]
          i = i+1


def p_constdecl1(p):
  '''ConstDecl1 : ConstDecl
           | DeclNameList'''


def p_typedeclname(p):
    '''TypeDeclName : IDENTIFIER'''
    p[0] = {}
    p[0]['variable'] = str(p[1])
    p[0]['code'] = str(p[1])

def p_typedecl(p):
    '''TypeDecl : TypeDeclName NType'''
    p[0] = {}
    p[0]['code'] = p[1]['code'] + p[2]['type']['val']
    global globalsymboltable
    if 'val' in p[2]['type']:
      if p[2]['type']['val'] == 'struct':
        globalsymboltable['custom_types']['structures'][p[1]['variable']] = {}
        struct_fields = p[2]['type']['struct_fields']
        globalsymboltable['custom_types']['structures'][p[1]['variable']]['struct_fields'] = struct_fields
        struct_size = 0
        global size
        print(struct_fields)
        for fields in struct_fields:
          for variable in fields:
            struct_size += size[variable['type']['val']]
        globalsymboltable['custom_types']['structures'][p[1]['variable']]['size'] = struct_size



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
    global offset
    p[0] = {}
    if(len(p) == 2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
    if(len(p) == 3):
        typ = p[1]['type']
        p[0]['code'] = p[1]['code'] + "\n"
        if(str(p[2]) == "++"):
            p[0]['code'] += (p[1]['place'] + " = " + p[1]['place'] + " +" + typ + " 1")
        else:
            p[0]['code'] += (p[1]['place'] + " = " + p[1]['place'] + " -" + typ + " 1")
        p[0]['place'] = p[1]['place']
    if(len(p) == 4):
        p[0]['code'] = ""
        if('funccall' in p[3] and str(p[2])!=':='):
          if(len(p[3]['exprs']) == 1):
              func_responses = p[3]['exprs'][0]['func_responses']
              if(len(func_responses)!=len(p[1]['exprs'])):
                print("Error in line "+str(p.lineno(2))+" :length mismatch for function return type")
                exit(1)
          else:
              print("Error in line "+str(p.lineno(2))+" : can't assign multiple functions")
              exit(1)

          i=0
          func_responses = p[3]['exprs'][0]['func_responses']
          p[0]['code'] += p[3]['exprs'][0]['code']
          for exprs in func_responses :
            if(p[1]['exprs'][i]['type']=='float' and exprs['type']=='int'):
              tmp = getlabel()
              register_variable(tmp)
              p[0]['code'] += "\n" + tmp + " = inttofloat " + str(exprs['place'])
              p[0]['code'] += "\n"+str(p[1]['exprs'][i]['place'])+" = "+str(exprs['place'])
            else:
              if(exprs['type']!=p[1]['exprs'][i]['type']):
                print("Error in line "+str(p.lineno(2))+" :type mismatch for function return type")
                exit(1)
              else:
                p[0]['code'] += "\n"+str(p[1]['exprs'][i]['place'])+" = "+str(exprs['place'])
            i = i+1

        else:
          flag = 0
          if(str(p[2]) == "+="):
              op = "+"
              typ = p[1]['type']
              if(p[3]['type'] == "float"):
                  typ = "float"
          if(str(p[2]) == "-="):
              op = "-"
              typ = p[1]['type']
              if(p[3]['type'] == "float"):
                  typ = "float"
          if(str(p[2]) == "*="):
              op = "*"
              typ = p[1]['type']
              if(p[3]['type'] == "float"):
                  typ = "float"
          if(str(p[2]) == "/="):
              # check for divide by zero
              op = "/"
              if(p[3]['value'] == 0):
                print("Error in line "+str(p.lineno(2))+" :can't divide by zero")
                exit(1)
              typ = p[1]['type']
              if(p[3]['type'] == "float"):
                  typ = "float"

          if(str(p[2]) == "%="):
              flag = 1
              op = "%"
              typ = p[1]['type']
              if(p[3]['type'] != "int" or p[3]['type'] != "int"):
                  print("Error in line "+str(p.lineno(2))+" :mod should be used with int types")
                  exit(1)
          if(str(p[2]) == "|="):
              flag = 1
              op = "|"
              typ = p[1]['type']
              if((p[1]['type'] != "int" or p[3]['type'] != "int") and (p[1]['type'] != "bool" or p[3]['type'] != "bool")):
                  print("Error in line "+str(p.lineno(2))+" : bitwise or should be used with int types")
                  exit(1)
          if(str(p[2]) == "&="):
              flag = 1
              op = "&"
              typ = p[1]['type']
              if((p[1]['type'] != "int" or p[3]['type'] != "int") and (p[1]['type'] != "bool" or p[3]['type'] != "bool")):
                  print("Error in line "+str(p.lineno(2))+" : bitwise and should be used with int types")
                  exit(1)
          if(str(p[2]) == "<<="):
              flag = 1
              op = "<<"
              typ = p[1]['type']
              if(p[1]['type'] != "int" or p[3]['type'] != "int"):
                  print("Error in line "+str(p.lineno(2))+" : shift operation should be used with int types")
                  exit(1)

          if(str(p[2]) == ">>="):
              flag = 1
              op = ">>"
              typ = p[1]['type']
              if(p[1]['type'] != "int" or p[3]['type'] != "int"):
                  print("Error in line "+str(p.lineno(2))+" : shift operation should be used with int types")
                  exit(1)

          if(str(p[2]) == "&^="):
              # what to do
              flag = 1
              op = "&^"

          if(str(p[2]) == "="):
              flag = 2
          if(str(p[2]) == ":="):
              flag = 3
              p[0]['code'] = ""
              p3_len = 0

              if('funccall' in p[3]):
                if(len(p[3]['exprs']) == 1):
                    func_responses = p[3]['exprs'][0]['func_responses']
                    p3_len = len(func_responses)
                    if(len(func_responses)!=len(p[1]['exprs'])):
                      print("Error in line "+str(p.lineno(2))+" :length mismatch for function return type")
                      exit(1)
                else:
                    print("Error in line "+str(p.lineno(2))+" : can't assign multiple functions")
                    exit(1)
              else:
                  p3_len = len(p[3]['exprs'])

              if(len(p[1]['exprs']) != p3_len):
                  print("Error in line "+str(p.lineno(2))+" : mismatch in no. of lhs and rhs expressions")
                  exit(1)
              if('funccall' in p[3]):
                  i=0
                  func_responses = p[3]['exprs'][0]['func_responses']
                  p[0]['code'] += p[3]['exprs'][0]['code']
                  for exprs in func_responses :
                    if(check_if_variable_declared(p[1]['exprs'][i]['place'])):
                        if(p[1]['exprs'][i]['type']=='float' and exprs['type']=='int'):
                          tmp = getlabel()
                          register_variable(tmp)
                          p[0]['code'] += "\n" + tmp + " = inttofloat " + str(exprs['place'])
                          p[0]['code'] += "\n"+str(p[1]['exprs'][i]['place'])+" = "+str(exprs['place'])
                        else:
                          if(exprs['type']!=p[1]['exprs'][i]['type']):
                            print("Error in line "+str(p.lineno(2))+" :type mismatch for function return type")
                            exit(1)
                          else:
                            p[0]['code'] += "\n"+str(p[1]['exprs'][i]['place'])+" = "+str(exprs['place'])
                    else:
                        # global offset
                        p[1]['exprs'][i]['type'] = exprs['type']
                        register_variable(p[1]['exprs'][i]['place'])
                        add_variable_attribute(p[1]['exprs'][i]['place'],'type',{'val':exprs['type']})
                        p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + str(exprs['place'])
                        offset += size[exprs['type']]
                        increase_local_size(size[exprs['type']])
                    i = i+1
              else:
                  for i in range(0,len(p[1]['exprs'])):
                      p[0]['code'] += p[1]['exprs'][i]['code'] + "\n" + p[3]['exprs'][i]['code']
                      if(check_if_variable_declared(p[1]['exprs'][i]['place'])):
                          p3_type = ""
                          p3_place = ""
                          if(p[3]['exprs'][i]['type'] == 'functioncall'):
                              p3_type = p[3]['exprs'][i]['func_responses'][0]['type']
                              p3_place = p[3]['exprs'][i]['func_responses'][0]['place']
                              # if(len(p[3]['func_responses']) != 1):
                              #     print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                              #     exit(1)
                          elif ('val' in p[3]['exprs'][i]['type'] and p[3]['exprs'][i]['type']['val'] == 'struct') :
                            if p[3]['exprs'][i]['type']['name'] != p[1]['exprs'][i]['type']['name']:
                              print("Error in line "+str(p.lineno(2))+" : Type mismatch in structure assignment!")
                              exit(1)
                            else:
                              p[0]['code'] = 'todo'
                          else:
                              p3_type = p[3]['exprs'][i]['type']
                              p3_place = p[3]['exprs'][i]['place']
                          if(p[1]['exprs'][i]['type']=='float' and p3_type=='int'):
                              tmp = getlabel()
                              register_variable(tmp)
                              add_variable_attribute_api(p[1]['exprs'][i]['place'],'value',p[3]['exprs'][i]['value'])
                              p[0]['code'] += "\n" + tmp + " = inttofloat " + p3_place
                              p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + tmp
                          elif(p[1]['exprs'][i]['type'] == p3_type):
                              p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + p3_place
                              add_variable_attribute_api(p[1]['exprs'][i]['place'],'value',p[3]['exprs'][i]['value'])
                          else:
                              print("Error in line "+str(p.lineno(2))+" : type mismatch")
                              exit(1)
                      else:
                          p3_type = ""
                          p3_place = ""
                          if(p[3]['exprs'][i]['type'] == 'functioncall'):
                              p3_type = p[3]['exprs'][i]['func_responses'][0]['type']
                              p3_place = p[3]['exprs'][i]['func_responses'][0]['place']
                              # if(len(p[3]['func_responses']) != 1):
                              #     print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                              #     exit(1)
                          elif ('val' in p[3]['exprs'][i]['type'] and p[3]['exprs'][i]['type']['val'] == 'struct') :
                            register_variable(p[1]['exprs'][i]['place'])
                            # global offset
                            x = {}
                            x['val'] = 'struct'
                            x['size'] = p[3]['exprs'][i]['type']['size']
                            x['name'] = p[3]['exprs'][i]['type']['name']
                            x['struct_fields'] = p[3]['exprs'][i]['type']['struct_fields']
                            add_variable_attribute(p[1]['exprs'][i]['place'],'type',x)
                            add_variable_attribute(p[1]['exprs'][i]['place'],'offset',offset)
                            p[0]['code'] = 'todo'
                            offset += x['size']
                            increase_local_size(x['size'])
                          else:
                              p3_type = p[3]['exprs'][i]['type']
                              p3_place = p[3]['exprs'][i]['place']
                          if(check_if_variable_declared(p3_place) or p[3]['exprs'][i]['value']!=""):
                            # global offset
                            p[1]['exprs'][i]['type'] = p3_type
                            register_variable(p[1]['exprs'][i]['place'])
                            add_variable_attribute(p[1]['exprs'][i]['place'],'type',{'val':p3_type})
                            add_variable_attribute_api(p[1]['exprs'][i]['place'],'value',p[3]['exprs'][i]['value'])
                            add_variable_attribute(p[1]['exprs'][i]['place'],'offset',offset)
                            p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + p3_place
                            offset += size[p3_type]
                            increase_local_size(size[p3_type])
                          else:
                            print("Error in line "+str(p.lineno(2))+" : variable "+ p3_place +" not declared")
                            exit(1)
              p[0]['place'] = p[1]['exprs'][0]['place']

          if(flag == 0):
              p[0]['code'] += p[1]['code'] + "\n" + p[3]['code'] + "\n"
              if(check_if_variable_declared(p[1]['place']) and (check_if_variable_declared(p[3]['place']) or p[3]['value']!="")):
                if(p[1]['type'] == 'int' and p[3]['type'] == 'float'):
                    print("Error in line "+str(p.lineno(2))+" : can't assign float to int")
                    exit(1)
                if(p[1]['type'] == 'float' and p[3]['type'] == 'int'):
                    tmp = getlabel()
                    register_variable(tmp)
                    p[0]['code'] += tmp + " = inttofloat " + p[3]['place'] + "\n"
                    p[0]['code'] += p[1]['place'] + " = " + p[1]['place'] + " " + op + "float " + tmp
                    p[0]['place'] = p[1]['place']
                if(p[1]['type'] == p[3]['type']):
                    typ = p[1]['type']
                    if(p[3]['value']!=""):
                        p[0]['code'] += p[1]['place'] + " = " + p[1]['place'] + " " + op + typ + " " + p[3]['place']
                    else:
                        p[0]['code'] += p[1]['place'] + " = " + p[1]['place'] + " " + op + typ + " " + p[3]['place']
              else:
                print("Error in line "+str(p.lineno(2))+" : variable not declared")
                exit(1)
          if(flag == 1):
            if(check_if_variable_declared(p[1]['place']) and (check_if_variable_declared(p[3]['place']) or p[3]['value']!="")):
              p[0]['code'] += p[1]['code'] + "\n" + p[3]['code'] + "\n"
              p[0]['code'] += p[1]['place'] + " = " + p[1]['place'] + " " + op + typ + " " + p[3]['place']
              p[0]['place'] = p[1]['place']
            else:
              print("Error in line "+str(p.lineno(2))+" : variable not declared")
              exit(1)

          if(flag == 2):
              p[0]['code'] = ""
              if(len(p[1]['exprs']) != len(p[3]['exprs'])):
                  print("Error in line "+str(p.lineno(2))+" : mismatch in no. of lhs and rhs expressions")
                  exit(1)
              for i in range(0,len(p[1]['exprs'])):
                  p[0]['code'] += p[1]['exprs'][i]['code'] + "\n" + p[3]['exprs'][i]['code']
                  if(check_if_variable_declared(p[1]['exprs'][i]['place']) and (check_if_variable_declared(p[3]['exprs'][i]['place']) or p[3]['exprs'][i]['value']!="")):
                    if ('val' in p[3]['exprs'][i]['type'] and p[3]['exprs'][i]['type']['val'] == 'struct') :
                        if p[3]['exprs'][i]['type']['name'] != p[1]['exprs'][i]['type']['name']:
                          print("Error in line "+str(p.lineno(2))+" : Type mismatch in structure assignment!")
                          exit(1)
                        else:
                          p[0]['code'] = 'todo'
                    elif(p[1]['exprs'][i]['type']=='float' and p[3]['exprs'][i]['type']=='int'):
                        tmp = getlabel()
                        register_variable(tmp)
                        p[0]['code'] += "\n" + tmp + " = inttofloat " + p[3]['exprs'][i]['place']
                        p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + tmp
                        add_variable_attribute_api(p[1]['exprs'][i]['place'],'value',p[3]['exprs'][i]['value'])

                    elif(p[1]['exprs'][i]['type'] == p[3]['exprs'][i]['type']):
                        p[0]['code'] += "\n" + p[1]['exprs'][i]['place'] + " = " + p[3]['exprs'][i]['place']
                        add_variable_attribute_api(p[1]['exprs'][i]['place'],'value',p[3]['exprs'][i]['value'])
                    else:
                        print("Error in line "+str(p.lineno(2))+" : type mismatch")
                        exit(1)
                  else:
                    print("Error in line "+str(p.lineno(2))+" : variable not declared")
                    exit(1)
              p[0]['place'] = p[1]['exprs'][0]['place']


def p_case(p):
    '''Case : CASE ExprOrTypeList COLON
     | CASE ExprOrTypeList EQUAL Expr COLON
     | CASE ExprOrTypeList COLONEQ Expr COLON
     | DEFAULT COLON'''
    p[0]={}
    if(len(p)==3):
        p[0]['type'] = "default"
        p[0]['value'] =""
    elif(len(p)==4):
        p[0]['type'] = "notdefault"
        p[0]['value']=p[2]['place']




def p_compoundstmt(p):
    '''CompoundStmt : LBRACE compundmarker cmtlist StmtList cmtlist revmarker RBRACE'''
    p[0] = {}
    p[0]['code'] = p[4]['code']

def p_compundmarker(p):
    '''compundmarker :
                '''
    make_symbol_table(getlabel(),"compound statement/else")

def p_revmarker(p):
    '''revmarker :
                '''
    go_one_level_up()

def p_caseblock(p):
    '''CaseBlock : Case StmtList'''
    p[0]={}
    p[0]['code']=p[2]['code']
    p[0]['type']=p[1]['type']
    p[0]['value']=p[1]['value']


def p_caseblocklist(p):

    '''CaseBlockList :
                   | CaseBlockList CaseBlock'''
    p[0] = []
    if(len(p)==3):
        p[0].extend(p[1])
        p[0].append(p[2])

def p_loopbody(p):
    '''LoopBody : LBRACE  cmtlist StmtList  cmtlist RBRACE'''
    p[0] = {}
    p[0]['code'] = p[3]['code']


def p_rangestmt(p):

  '''RangeStmt : ExprList EQUAL RANGE Expr
               | ExprList COLONEQ RANGE Expr
               | RANGE Expr'''

def p_forheader(p):
    '''ForHeader : OSimpleStmt SEMICOL OSimpleStmt SEMICOL OSimpleStmt
               | OSimpleStmt
               | RangeStmt'''
    p[0] = {}
    if(len(p)==6):
        p[0]['extra'] ={}
        p[0]['extra']['update']={}
        p[0]['extra']['initialization'] ={}
        p[0]['extra']['check']={}
        p[0]['extra']['initialization']['code'] = p[1]['code']
        p[0]['extra']['initialization']['place'] = p[1]['place']
        p[0]['extra']['check']['code'] = p[3]['code']
        p[0]['extra']['check']['place'] = p[3]['place']
        p[0]['extra']['update']['code'] = p[5]['code']
        p[0]['extra']['update']['place'] = p[5]['place']

def p_forbody(p):
    '''ForBody : ForHeader formarker LoopBody revmarker'''
    p[0] = {}
    p[0]['extra'] ={}
    p[0]['extra']['ForHeader'] = p[1]['extra']
    p[0]['extra']['loopbody'] = {}
    p[0]['extra']['loopbody']['code']=p[3]['code']
    p[0]['extra']['loop_label'] = p[2]['loop_label']
    p[0]['extra']['exit_label']=p[2]['exit_label']
    p[0]['extra']['update_label']=p[2]['update_label']


def p_forstmt(p):
    '''ForStmt : FOR ForBody'''
    loop_label = p[2]['extra']['loop_label']
    exit_label = p[2]['extra']['exit_label']
    update_label =p[2]['extra']['update_label']
    p[0] = {}
    p[0]['code'] = p[2]['extra']['ForHeader']['initialization']['code'] + "\n" + loop_label+ " :"
    p[0]['code'] += "\n"+ p[2]['extra']['ForHeader']['check']['code']
    p[0]['code'] += "\n"+ "if "+p[2]['extra']['ForHeader']['check']['place'] + " = 0 goto "+exit_label
    p[0]['code'] += "\n"+ p[2]['extra']['loopbody']['code']
    p[0]['code'] += "\n"+ update_label +" :"
    p[0]['code'] += "\n"+ p[2]['extra']['ForHeader']['update']['code']
    p[0]['code'] += "\ngoto "+loop_label
    p[0]['code'] += "\n" + exit_label+" :"

def p_formarker(p):
    '''formarker :
                  '''
    make_symbol_table(getlabel(),"For loop")
    p[0]={}
    p[0]['loop_label']=getlabel()
    p[0]['exit_label']=getlabel()
    p[0]['update_label']=getlabel()
    global stack
    current = stack[-1]
    current["CS335_loop_label"] = p[0]['loop_label']
    current["CS335_exit_label"] = p[0]['exit_label']
    current["CS335_update_label"] = p[0]['update_label']

def p_ifmarker(p):
  '''ifmarker :
                '''
  make_symbol_table(getlabel(),"If/else if")

def p_ifheader(p):
    '''IfHeader : OSimpleStmt
           | OSimpleStmt SEMICOL OSimpleStmt'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']


def p_ifstmt(p):
    '''IfStmt : IF IfHeader ifmarker LoopBody revmarker ElseIfList'''
    nextlabel = getlabel()
    exitlabel = getlabel()
    p[0] = {}
    if(len(p[6]['extra']) == 0):
        p[0]['code'] = p[2]['code'] + "\n" + "if "+p[2]['place'] +"=0 goto "+exitlabel + "\n" + p[4]['code']
    else:
        p[0]['code'] = p[2]['code'] + "\n" + "if "+p[2]['place'] +"=0 goto "+nextlabel + "\n" + p[4]['code'] + "\n" + "goto "+exitlabel
    for i in range(0,len(p[6]['extra'])):
        if((i+1) == len(p[6]['extra'])):
            if(p[6]['extra'][i]['type']=="elseif"):
                p[0]['code'] += "\n" + nextlabel+":" + "\n" + p[6]['extra'][i]['ifheader_code'] + "\n" + "else if "+p[6]['extra'][i]['ifheader_place'] +"=0 goto "+exitlabel + "\n" + p[6]['extra'][i]['body']
            else:
                p[0]['code'] += "\n" + nextlabel+":" + "\n" + "else "+ "\n" + p[6]['extra'][i]['body']
        else:
            nextlabel2= getlabel()
            if(p[6]['extra'][i]['type']=="elseif"):
                p[0]['code'] += "\n" + nextlabel+":" + "\n" + p[6]['extra'][i]['ifheader_code'] + "\n" + "else if "+p[6]['extra'][i]['ifheader_place'] +"=0 goto "+nextlabel2 + "\n" + p[6]['extra'][i]['body'] + "\n" + "goto "+exitlabel
            nextlabel = nextlabel2
    p[0]['code'] += "\n" + exitlabel+":"

def p_elseif(p):
    '''ElseIf : ELSE IF IfHeader ifmarker LoopBody revmarker'''
    p[0] = {}
    p[0]['extra_dict'] = {}
    p[0]['extra_dict']['body'] = p[5]['code']
    p[0]['extra_dict']['type'] = "elseif"
    p[0]['extra_dict']['ifheader_code'] = p[3]['code']
    p[0]['extra_dict']['ifheader_place'] = p[3]['place']


def p_elseiflist(p):
    '''ElseIfList :
                | ElseIf ElseIfList
                | Else'''
    p[0] = {}
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
    p[0] = {}
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
    p[0] = {}
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
    p[0] = {}
    if(len(p) == 2):
        p[0]['type'] = p[1]['type']
    else:
        if(p[2]['type'] == 'int' or p[2]['type'] == 'void'):
          p[0]['type'] = {}
          p[0]['type']['val'] = 'array'
          #print(p[2]['value'])
          p[0]['type']['arr_length'] = p[2]['value']
          p[0]['type']['arr_type'] = p[4]['type']['val']
        else:
          print("Error in line "+str(p.lineno(1))+" : Array definition not good")
          exit(1)


def p_channeltype(p):
  '''ChannelType : CHAN NewType
                 | CHAN LMINUS NewType
                 | LMINUS CHAN NewType'''


def p_structtype(p):
    '''StructType : STRUCT LBRACE StructDeclList OSemi RBRACE
                | STRUCT LBRACE RBRACE'''
    p[0] = {}
    p[0]['type'] = {}
    p[0]['type']['val'] = 'struct'
    p[0]['type']['struct_fields'] = []
    if(len(p) == 6):
        p[0]['type']['struct_fields'] = p[3]['struct_fields']



def p_interfacetype(p):
  '''InterfaceType : INTERFACE LBRACE InterfaceDeclList OSemi RBRACE
                   | INTERFACE LBRACE RBRACE'''


def p_funcdec1(p):
  '''FuncDecl : FUNCTION  funcmarker FuncDecl_  FuncBody'''
  p[0] = {}
  global offset
  p[0]['code'] = p[3]['func_name'] + " : BeginFunc "+ str(offset) +"\n" + "push rbp\n"+"mov rbp rsp\n"+"push rbx\npush r15\npush r14\npush r13\npush r12\n"+ p[4]['code'] + "\nEndFunc"
  offset = 0
def p_funcmarker(p):
    '''funcmarker :
              '''
    global offset
    make_symbol_table("func_unknown",None)
    offset = 8

same_func_count={}
def p_funcdec1_(p):
    '''FuncDecl_ : IDENTIFIER ArgList FuncRes
               | LEFT_OR OArgTypeListOComma OR_RIGHT IDENTIFIER ArgList FuncRes'''

    global globalsymboltable
    global stack
    globalsymboltable[str(p[1])] = {}
    globalsymboltable[str(p[1])]['type'] = {'val' : 'function'}
    globalsymboltable[str(p[1])]['exists']=1
    current = stack[-1]
    p[0] = {}
    if(len(p)==4):
        if(str(p[1]) in same_func_count.keys()):
          same_func_count[str(p[1])]+=1
        else:
          same_func_count[str(p[1])]=1

        p[0]['func_name'] = str(p[1])+str(same_func_count[str(p[1])])
        current['CS335_args'] = p[2]['argList']
        current['CS335_response'] = p[3]['response']
        current['CS335_name']= str(p[1])          #replaces func_unknown by actual func name
        current['CS335_type']= "function"
        current['CS335_show_label']= p[0]['func_name']



def p_functype(p):
  '''FuncType : FUNCTION ArgList FuncRes'''


def p_argList(p):
    '''ArgList : LPAREN OArgTypeListOComma RPAREN
             | ArgList LPAREN OArgTypeListOComma RPAREN'''
    p[0] = {}
    if(len(p)==4):
        p[0]['argList'] = p[2]['argList']

def p_funcbody(p):
    '''FuncBody :
              | LBRACE  cmtlist StmtList  cmtlist funcrevmarker RBRACE'''
    p[0] = {}
    p[0]['code']=p[3]['code']
    p[0]['var_size'] = p[5]['var_size']

def p_funcrevmarker(p):
  '''funcrevmarker :
                    '''
  global offset
  p[0] = {}
  p[0]['var_size'] = offset
  go_one_level_up()


def p_funcres(p):
    '''FuncRes :
             | FuncRetType
             | LEFT_OR OArgTypeListOComma OR_RIGHT'''
    p[0] = {}
    if(len(p)==1):
        p[0]['response'] = 'void'
    else:
        p[0]['response'] = p[1]['response']

######################################################################################################
def p_structdeclist(p):
    '''StructDeclList : StructDecl
                    | StructDeclList SEMICOL StructDecl'''
    p[0] = {}
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
    p[0] = {}
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
  p[0] = {}
  p[0]['names'] = []
  p[0]['names'].append(str(p[1]))


def p_ptrtype(p):
    '''PtrType : TIMES NType'''
    p[0] = {}
    p[0]['type'] = {}
    p[0]['type']['val'] = 'pointer'
    p[0]['type']['pointer_type'] = p[2]['type']['val']

def p_funcrettype(p):
    '''FuncRetType : FuncType
                 | OtherType
                 | PtrType
                 | DotName
                 | myType'''
    p[0] = {}
    p[0]['response'] = p[1]['type']
def p_mytype(p):
  '''myType : NewType
            | myType COMMA NewType'''
  p[0] = {}
  if(len(p)==2):
    p[0]['type'] = []
    p[0]['type'].append(p[1]['type'])
  else:
    p[0]['type'] = p[1]['type']
    p[0]['type'].append(p[3]['type'])

def p_dotname(p):
  '''DotName : Name
             | Name DOT IDENTIFIER'''
  p[0] = {}
  p[0]['type'] = {}
  global globalsymboltable
  if p[1]['place'] in globalsymboltable['custom_types']['structures'] :
    p[0]['type']['val'] = 'struct'
    p[0]['type']['struct_fields'] = globalsymboltable['custom_types']['structures'][p[1]['place']]['struct_fields']
    p[0]['type']['size'] = globalsymboltable['custom_types']['structures'][p[1]['place']]['size']
    p[0]['type']['name'] = p[1]['place']

def p_ocomma(p):
  '''OComma :
            | COMMA'''


def p_osemi(p):
  '''OSemi :
           | SEMICOL'''


def p_osimplestmt(p):
    '''OSimpleStmt :
                 | SimpleStmt'''
    p[0] = {}
    if(len(p)==2):
        p[0]['place'] = p[1]['place']
        p[0]['code'] = p[1]['code']
    else:
        p[0]['code'] = ""

def p_onewname(p):
    '''ONewName :
                | NewName'''
    p[0]={}
    if(len(p)==2):
        pass
    else:
        p[0]['code']=""

def p_oexpr(p):
    '''OExpr :
           | Expr'''
    p[0] = {}
    if(len(p)==2):
        p[0]['type'] = p[1]['type']
        p[0]['value'] = p[1]['value']
    else:
        p[0]['type'] = 'void'
        p[0]['value'] = 0


def p_oexprlist(p):
    '''OExprList :
               | ExprList'''
    p[0] = {}
    if(len(p)==2):
        p[0]['exprs'] = p[1]['exprs']

def p_funcliteraldecl(p):
  '''FuncLiteralDecl : FuncType'''

def p_funcliteral(p):
  '''FuncLiteral : FuncLiteralDecl LBRACE cmtlist StmtList cmtlist RBRACE'''

def p_exprlist(p):
    '''ExprList : Expr
              | ExprList COMMA Expr'''
    p[0] = {}
    p[0]['exprs'] = []
    if(len(p)==2):
        # print("hello")
        # print(p[1])
        p[0]['exprs'].append({'code':p[1]['code'],'type':p[1]['type'],'place':p[1]['place'],'value':p[1]['value']})
        if(p[1]['type'] == "functioncall"):
          # print(p[1])
          # p[0]['func_responses'] = p[1]['func_responses']
          # p[0]['funccall'] = 1
          # p[0]['code'] = p[1]['code']
          p[0]['exprs'][-1]['func_responses'] = p[1]['func_responses']
          p[0]['funccall'] = 1
    else:
        p[0]['exprs'].extend(p[1]['exprs'])
        p[0]['exprs'].append({'code':p[3]['code'],'type':p[3]['type'],'place':p[3]['place'],'value':p[3]['value']})


def p_exprortypelist(p):
  '''ExprOrTypeList : ExprOrType
                    | ExprOrTypeList COMMA ExprOrType'''

  p[0] = {}
  p[0]['exprs'] = []
  if(len(p)==2):
    p[0]['code'] = p[1]['code']
    p[0]['place']=p[1]['place']
    x = {}
    x['place'] = p[1]['place']
    x['type'] = p[1]['type']
    x['value'] = p[1]['value']
    p[0]['exprs'].append(x)
  else:
    p[0]['code'] = p[1]['code']
    p[0]['code'] += "\n"+p[3]['code']
    p[0]['exprs'] = p[1]['exprs']
    x = {}
    x['place'] = p[3]['place']
    x['type'] = p[3]['type']
    x['value'] = p[3]['type']
    p[0]['exprs'].append(x)


def p_oliteral(p):
    '''OLiteral :
              | Literal'''
    p[0] = {}
    if(len(p)==1):
        p[0]['code'] = ""
    else:
        p[0]['value'] = p[1]['value']
        p[0]['code'] = p[1]['code']
        p[0]['type'] = p[1]['type']

def p_literal(p):
    '''Literal : INTEGER
             | FLOAT
             | STRING'''
    a = re.match(r'(0x([0-9A-Fa-f]+))|[0-9]([0-9]+)*([Ee](\+)?[0-9]([0-9]+)*)?',str(p[1]))
    b = re.match(r'(([0-9]([0-9]+)*(\.[0-9]([0-9]+)*)?)[eE]\-[0-9]([0-9]+)*)|([0-9]([0-9]+)*\.[0-9]([0-9]+)*)([eE][\+]?[0-9]([0-9]+)*)?',str(p[1]))
    c = re.match(r'(\"[^\"]*\")|(\'[^\']*\') ',str(p[1]))
    p[0] = {}
    if(b):
        p[0]['value'] = float(str(p[1]))
        p[0]['type'] = 'float'
        p[0]['code'] = ""
    elif(a):
        p[0]['value'] = int(str(p[1]))
        p[0]['type'] = 'int'
        p[0]['code'] = ""
    elif(c):
        p[0]['value'] = str(p[1])
        p[0]['type'] = 'string'
        p[0]['code'] = ""
    p[0]['place'] = str(p[1])

def p_embed(p):
  '''Embed : IDENTIFIER'''

def p_dec1list(p):
    '''DeclList : Declaration SEMICOL
              | DeclList cmtlist Declaration SEMICOL'''
    p[0] = {}
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
    p[0] = {}
    if(len(p)==2):
        p[0]['variable'] = []
        p[0]['variable'].append(p[1]['variable'])
    else:
        p[0]['variable'] = p[1]['variable']
        p[0]['variable'].append(p[3]['variable'])


def p_stmtlist(p):
    '''StmtList : Stmt SEMICOL
                | StmtList cmtlist Stmt SEMICOL'''
    p[0] = {}
    if(len(p)==3):
        p[0]['code']=p[1]['code']
    else:
        p[0]['code']=p[1]['code']+"\n"+p[3]['code']


def p_newnamelist(p):
    '''NewNameList : NewName
                   | NewNameList COMMA NewName'''
    p[0] = {}
    p[0]['names'] = []
    if(len(p)==2):
        p[0]['names'] = p[1]['names']
    else:
        p[0]['names'] = p[1]['names']
        p[0]['names'].append(p[3]['names'])
    print(p[0]['names'])

def p_keyvallist(p):
  '''KeyvalList : Keyval
                  | BareCompLitExpr
                  | KeyvalList COMMA Keyval
                  | KeyvalList COMMA BareCompLitExpr'''
  p[0] = {}
  p[0]['list'] = []
  if len(p) == 2:
    p[0]['list'].append(p[1]['list'])
    #print(p[0]['list'])
  else:

    p[0]['list'] = p[1]['list']
    p[0]['list'].append(p[3]['list'])

def p_bracedkeyvallist(p):
  '''BracedKeyvalList :
                        | KeyvalList OComma'''
  p[0] = {}
  if len(p) == 3:
    p[0]['list'] = p[1]['list']


def p_declname(p):
    '''DeclName : IDENTIFIER'''
    register_variable(str(p[1]))
    p[0] = {}
    p[0]['variable'] = str(p[1])


def p_name(p):
    '''Name : IDENTIFIER'''
    p[0] = {}
    p[0]['value'] = ""
    p[0]['code'] = ""

    x = {}
    if(check_if_variable_declared(str(p[1])) == 0):
        x['val'] = ''
    else:
        x = get_variable_attribute(str(p[1]),"type")
        p[0]['value'] = get_variable_attribute(str(p[1]),'value')

    if(x['val'] == 'array' or x['val'] == 'struct'):
      p[0]['type'] = x
    else:
      p[0]['type'] = x['val']

    p[0]['place'] = str(p[1])

def p_argtype(p):
    '''ArgType : NameOrType
               | IDENTIFIER NameOrType
               | IDENTIFIER DotDotDot
               | DotDotDot'''
    p[0] = {}
    p[0]['args'] = {}
    if(len(p) == 3):
        p[0]['args']['arg_type'] = p[2]['type']
        p[0]['args']['arg_name'] = str(p[1])
        register_variable(str(p[1]))
        add_variable_attribute(str(p[1]),'type',p[2]['type'])

def p_argtypelist(p):
    '''ArgTypeList : ArgType
                   | ArgTypeList COMMA ArgType'''
    p[0] = {}
    p[0]['argList'] = []
    if(len(p) == 2):
        p[0]['argList'].append(p[1]['args'])
    else:
        p[0]['argList'] = p[1]['argList']
        p[0]['argList'].append(p[3]['args'])

def p_oargtypelistocomma(p):
    '''OArgTypeListOComma :
                          | ArgTypeList OComma'''
    p[0] = {}
    p[0]['argList'] = []
    if(len(p) == 3):
        p[0]['argList'] = p[1]['argList']

def p_stmt(p):
    '''Stmt :
            | CompoundStmt
            | CommonDecl
            | NonDeclStmt'''
    p[0] = {}
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
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
    global stack
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
            p[0]['code'] = ""
            # function = stack[-1]["CS335_name"]
            # num = len(get_function_symbol_tables(function)["CS335_response"])
            # num = len(stack[-1]["CS335_response"])
            num = len(get_current_func_sym_table()["CS335_response"])
            try:
              if(num != len(p[2]['exprs'])):
                print("Error in line "+str(p.lineno(1))+" : mismatch in no of returns")
                exit(1)
            except:
              print("Error in line "+str(p.lineno(1))+" : mismatch in no of returns")
              exit(1)
            for i in range(0,len(p[2]['exprs'])):
                if(i==0):
                    p[0]['code'] += p[2]['exprs'][i]['code'] + "\n"
                else:
                    p[0]['code'] += "\n" + p[2]['exprs'][i]['code'] + "\n"
                if(check_if_variable_declared(p[2]['exprs'][i]['place']) == 0 and p[2]['exprs'][i]['value'] == ''):
                  print("Error in line "+str(p.lineno(1))+" : return variable not declared")
                  exit(1)
                p[0]['code'] += "return " + p[2]['exprs'][i]['place']

        if(flag == 0):
            current= stack[-1]
            if (string == "break"):
                p[0]['code'] = "goto "+current["CS335_exit_label"] + "\n" + p[2]['code']
            elif(string == "continue"):
                p[0]['code'] = "goto "+current["CS335_update_label"] + "\n" + p[2]['code']
            else:
                p[0]['code'] = string + " " + p[2]['code']
    if(len(p)==4):
        #
        dummy = 0

def p_dotdotdot(p):
  '''DotDotDot : DDD
                 | DDD NType'''

def p_pexpr(p):
    '''PExpr : PExprNoParen
             | LPAREN ExprOrType RPAREN'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        p[0]['place'] = p[1]['place']
        # print("cc")
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    else:
        p[0]['code'] = p[2]['code']
        p[0]['place'] = p[2]['place']
        p[0]['type'] = p[2]['type']
        p[0]['value'] = p[2]['value']

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
    p[0] = {}
    if(len(p)==2):
        # print(p[1])
        # if 'func_responses' in p[1]:
        #   if(p[1]['func_responses'] == 'void'):
        #     p[0]['type'] = 'void'
        #     p[0]['place'] = 'void'
        #   else:
        #     p[0]['type'] = p[1]['func_responses'][0]['type']
        #     p[0]['place'] = p[1]['place'][0]
        # else:
        #   p[0]['type'] = p[1]['type']
        #   p[0]['place'] = p[1]['place']
        p[0]['code'] = p[1]['code']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        p[0]['place'] = p[1]['place']
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    if(len(p)==4 or len(p)==6):
        # Struct accessing here!!
        p[0] = {}
        struct_name = p[1]['place']
        if len(p)==4 :
          field_name = str(p[3])
        else:
          field_name = p[4]['place']
        if not check_if_variable_declared(struct_name):
          print("Error in line "+str(p.lineno(2))+" : Variable not declared")
          exit(1)

        type_var = get_variable_attribute(struct_name,"type")
        fields = type_var['struct_fields']
        flag = 0
        for temp in fields:
          for temp2 in temp:
            if temp2['name'] == field_name:
              flag = 1
              type_var = temp2['type']['val']
        if flag == 0:
          print("Error in line "+str(p.lineno(2))+" : Struct field invalid")
          exit(1)
        else:
          p[0]['type'] = type_var

        label = getlabel()
        register_variable(label)
        p[0]['place']  = label
        p[0]['value'] = label
        p[0]['code'] = ""

    if(len(p)==5):
      if str(p[2]) == "[(":
        struct_name = p[1]['place']
        global globalsymboltable
        struct_fields = globalsymboltable['custom_types']['structures'][struct_name]['struct_fields']
        for dicts in p[3]['list']:
          key = dicts['key']
          flag = 0
          for fields in struct_fields:
            for variable in fields:
              if key == variable['name'] and dicts['type'] == variable['type']['val']:
                flag = 1
                break
          if flag == 0:
            print("Error in line "+str(p.lineno(2))+" : Struct Assignment type/field not valid")
            exit(1)
        p[0]={}
        label = getlabel()
        register_variable(label)
        p[0]['code'] = 'todo'
        p[0]['type'] = {}
        p[0]['type']['val'] = 'struct'
        p[0]['type']['struct_fields'] = struct_fields
        p[0]['type']['size'] = globalsymboltable['custom_types']['structures'][struct_name]['size']
        p[0]['type']['name'] = struct_name
        p[0]['place'] = label
        p[0]['value'] = label

      else:
        label = getlabel()
        label1 = getlabel()
        register_variable(str(label))
        register_variable(str(label1))
        if(int(p[3]['place']) >= p[1]['type']['arr_length']):
          print("Error in line "+str(p.lineno(2))+" : Array index out of range")
          exit(1)
        p[0]['code'] = p[1]['code']
        p[0]['code'] += "\n"+p[3]['code']
        p[0]['place'] = label
        p[0]['code'] = "\n" + str(label1) + " = BaseAddress(" + p[1]['place'] + ")\n"
        p[0]['code'] += str(label)+" = "+str(label1)+"["+p[3]['place']+"]"
        p[0]['value'] = 1
        p[0]['type'] = p[1]['type']['arr_type']

    if(len(p)==7):
        # what to do
        dummy = 0

def p_NewType(p):
    '''NewType : TYPE'''
    p[0] = {}
    p[0]['type'] = {}
    p[0]['type']['val'] =  str(p[1])


def p_convtype(p):
  '''ConvType : FuncType
                | OtherType'''

def p_comptype(p):
  '''CompType : OtherType'''

def p_keyval(p):
  '''Keyval : Expr COLON CompLitExpr'''
  p[0] = {}
  p[0]['list'] = {}
  p[0]['list']['key'] = p[1]['place']
  p[0]['list']['type'] = p[3]['type']
  p[0]['list']['value'] = p[3]['place']
  #p[0]['code'] = p[1]['code'] + p[3]['code']


def p_barecomplitexpr(p):
  '''BareCompLitExpr : Expr
                       | LEFT_LEFT BracedKeyvalList RIGHT_RIGHT'''

def p_complitexpr(p):
  '''CompLitExpr : Expr
                 | LEFT_LEFT BracedKeyvalList RIGHT_RIGHT'''
  p[0] = {}
  if len(p) == 2:
    p[0]['place'] = p[1]['place']
    p[0]['value'] = p[1]['value']
    p[0]['code'] = p[1]['code']
    p[0]['type'] = p[1]['type']

def p_exportype(p):
    '''ExprOrType : Expr
                  | NonExprType'''

    p[0] = {}
    p[0]['code'] = p[1]['code']
    p[0]['type'] = p[1]['type']
    p[0]['value'] = p[1]['value']
    p[0]['place'] = p[1]['place']


def p_nameortype(p):
    '''NameOrType : NType'''
    p[0] = {}
    p[0]['type'] = p[1]['type']

def p_switchstmt(p):
    '''SwitchStmt : SWITCH IfHeader LBRACE CaseBlockList RBRACE'''
    nextlabel = getlabel()
    exitlabel = getlabel()
    p[0] = {}
    p[0]["code"]= p[2]['code']+"\n"
    dummy = getlabel()
    for i in range(0,len(p[4])):
        if(p[4][i]["type"] == "notdefault"):
            p[0]['code']+= dummy +"= "+p[2]['place']+"=="+p[4][i]["value"] +"\n"
            if((i+1)==len(p[4])):
                p[0]['code']+= "if "+dummy +"= 0 goto "+exitlabel + "\n" + p[4][i]['code']
                break
            else:
                p[0]['code']+= "if "+dummy +"= 0 goto "+nextlabel + "\n" + p[4][i]['code'] + "\n" + "goto "+exitlabel+"\n"

        else:
            p[0]['code']+= p[4][i]['code']
            break
        p[0]['code']+= nextlabel+" :\n"
        nextlabel=getlabel()

    p[0]['code'] += "\n" + exitlabel+" :"

def p_prec5expr_(p):
    '''Prec5Expr_ : UExpr
                  | Prec5Expr_ DIVIDE UExpr
                  | Prec5Expr_ MOD UExpr
                  | Prec5Expr_ SHL UExpr
                  | Prec5Expr_ SHR UExpr
                  | Prec5Expr_ AMPERS UExpr
                  | Prec5Expr_ AMPCAR UExpr
                  | Prec5Expr_ TIMES UExpr'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        p[0]['place'] = p[1]['place']
        # print("e")
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    else:
        p[0]['code'] = p[1]['code'] + "\n" + p[3]['code'] + "\n"
        op = ""
        typ = ""
        p[0]['place'] = getlabel()
        p[0]['value'] = ""
        register_variable(p[0]['place'])
        flag = 0
        if(str(p[2]) == "/"):
            op = "/"
            # can handle divide by zero here
            if(p[1]['value']!="" and p[3]['value']!=""):
                if(p[3]['value']==0):
                  print("Error in line "+str(p.lineno(2))+" :can't divide by zero")
                  exit(1)
                p[0]['value'] = (p[1]['value'] / p[3]['value'])

        if(str(p[2]) == "*"):
            op = "*"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] * p[3]['value'])

        if(str(p[2]) == "%"):
            flag = 1
            op = "%"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] % p[3]['value'])

        if(str(p[2]) == "<<"):
            flag = 1
            op = "<<"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] << p[3]['value'])

        if(str(p[2]) == "&"):
            flag = 1
            op = "%"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] & p[3]['value'])

        if(str(p[2]) == "&^"):
            # what is this
            flag = 2
            op = "&^"

        if(flag == 0):
            ## Error is here, check if type is function call(also check same error in all grammar rules)
            ## Assuming here that functions have only a single return value
            p1_type = ""
            p3_type = ""
            p3_place = ""
            p1_place = ""
            if(p[1]['type'] == 'functioncall'):
                p1_type = p[1]['func_responses'][0]['type']
                p1_place = p[1]['func_responses'][0]['place']
                if(len(p[1]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p1_type = p[1]['type']
                p1_place = p[1]['place']
            if(p[3]['type'] == 'functioncall'):
                p3_type = p[3]['func_responses'][0]['type']
                p3_place = p[3]['func_responses'][0]['place']
                if(len(p[3]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p3_type = p[3]['type']
                p3_place = p[3]['place']
            if(p1_type == 'int' and p3_type == 'float'):
              tmp = getlabel()
              register_variable(tmp)
              p[0]['code'] += tmp + " = inttofloat " + p1_place + "\n"
              p[0]['code'] += p[0]['place'] + " = " + tmp + " " + op + "float " + p3_place
              p[0]['type'] = 'float'
            if(p1_type == 'float' and p3_type == 'int'):
              tmp = getlabel()
              register_variable(tmp)
              p[0]['code'] += tmp + " = inttofloat " + p3_place + "\n"
              p[0]['code'] += p[0]['place'] +  " = " +  p1_place + " " + op + "float " + tmp
              p[0]['type'] = 'float'
            if(p1_type == p3_type):
              typ = p1_type
              p[0]['code'] += p[0]['place'] + " = " + p1_place + " " + op + typ + " " + p3_place
              p[0]['type'] = p1_type
        if(flag == 1):
            if(p[1]['type'] != 'int' or p[3]['type'] != 'int'):
                print("Error in line "+str(p.lineno(2))+" : Both expressions should be of type integer")
                exit(1)
            p[0]['code'] += p[0]['place'] + " = " + p[1]['place'] + " " + op + " " + p[3]['place']
            p[0]['type'] = 'int'

def p_prec4expr_(p):
    '''Prec4Expr_ : Prec5Expr_
                  | Prec4Expr_ PLUS Prec5Expr_
                  | Prec4Expr_ MINUS Prec5Expr_
                  | Prec4Expr_ XOR Prec5Expr_
                  | Prec4Expr_ OR Prec5Expr_'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    else:
        op = ""
        typ = ""
        p[0]['value'] = ""
        p[0]['code'] = p[1]['code'] + "\n" + p[3]['code'] + "\n"
        p[0]['place'] = getlabel()
        register_variable(p[0]['place'])
        flag = 0
        if(str(p[2]) == "+"):
            op = "+"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] + p[3]['value'])

        if(str(p[2]) == "-"):
            op = "-"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] - p[3]['value'])

        if(str(p[2]) == "^"):
            flag = 1
            op = "^"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] ^ p[3]['value'])

        if(str(p[2]) == "|"):
            flag = 1
            op = "|"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] | p[3]['value'])
        if(flag == 0):
            ## Error is here, check if type is function call(also check same error in all grammar rules)
            ## Assuming here that functions have only a single return value
            p1_type = ""
            p3_type = ""
            p3_place = ""
            p1_place = ""
            if(p[1]['type'] == 'functioncall'):
                p1_type = p[1]['func_responses'][0]['type']
                p1_place = p[1]['func_responses'][0]['place']
                if(len(p[1]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p1_type = p[1]['type']
                p1_place = p[1]['place']
            if(p[3]['type'] == 'functioncall'):
                p3_type = p[3]['func_responses'][0]['type']
                p3_place = p[3]['func_responses'][0]['place']
                if(len(p[3]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p3_type = p[3]['type']
                p3_place = p[3]['place']

            if(p1_type == 'int' and p3_type == 'float'):
                tmp = getlabel()
                register_variable(tmp)
                p[0]['code'] += tmp + " = inttofloat " + p1_place + "\n"
                p[0]['code'] += p[0]['place'] + " = " + tmp + " " + op + "float " + p3_place
                p[0]['type'] = 'float'
            if(p1_type == 'float' and p3_type == 'int'):
                tmp = getlabel()
                register_variable(tmp)
                p[0]['code'] += tmp + " = inttofloat " + p3_place + "\n"
                p[0]['code'] += p[0]['place'] + " = " + p1_place +" "+ op + "float " + tmp
                p[0]['type'] = 'float'
            if(p1_type == p3_type):
                typ = p1_type
                p[0]['code'] += p[0]['place'] + " = " + p1_place + " " + op + typ + " " + p3_place
                p[0]['type'] = p1_type
        else:
            p1_type = ""
            p3_type = ""
            p3_place = ""
            p1_place = ""
            if(p[1]['type'] == 'functioncall'):
                p1_type = p[1]['func_responses'][0]['type']
                p1_place = p[1]['func_responses'][0]['place']
                if(len(p[1]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p1_type = p[1]['type']
                p1_place = p[1]['place']
            if(p[3]['type'] == 'functioncall'):
                p3_type = p[3]['func_responses'][0]['type']
                p3_place = p[3]['func_responses'][0]['place']
                if(len(p[3]['func_responses']) != 1):
                    print("Error in line "+str(p.lineno(2))+" : No of return values can be just 1")
                    exit(1)
            else:
                p3_type = p[3]['type']
                p3_place = p[3]['place']

            if(p1_type != 'int' or p3_type != 'int'):
                print("Error in line "+str(p.lineno(2))+" : Both expressions should be of type integer")
                exit(1)
            p[0]['code'] += p[0]['place'] + " = " + p1_place + " " + op + " " + p3_place
            p[0]['type'] = 'int'


def p_prec3expr_(p):
    '''Prec3Expr_ : Prec4Expr_
                  | Prec3Expr_ EQEQ Prec4Expr_
                  | Prec3Expr_ NOTEQ Prec4Expr_
                  | Prec3Expr_ LEQ Prec4Expr_
                  | Prec3Expr_ GEQ Prec4Expr_
                  | Prec3Expr_ GREAT Prec4Expr_
                  | Prec3Expr_ LESS Prec4Expr_
                '''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    else:
        p[0]['code'] = p[1]['code'] + "\n" + p[3]['code'] + "\n"
        op = ""
        if(p[1]['type']!=p[3]['type']):
            print("Error in line "+str(p.lineno(2))+" : Type mismatch")
            exit(1)
        # do this thing for others as well
        p[0]['value'] = ""
        if(str(p[2]) == "=="):
            op = "=="

            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] == p[3]['value'])
        if(str(p[2]) == "!="):
            op = "!="
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] != p[3]['value'])
        if(str(p[2]) == "<="):
            op = "<="
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] <= p[3]['value'])
        if(str(p[2]) == ">="):
            op = ">="
            if(p[1]['value']!="" and p[3]['value']!=""!=""):
                p[0]['value'] = (p[1]['value'] >= p[3]['value'])
        if(str(p[2]) == ">"):
            op = ">"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] > p[3]['value'])
        if(str(p[2]) == "<"):
            op = "<"
            if(p[1]['value']!="" and p[3]['value']!=""):
                p[0]['value'] = (p[1]['value'] < p[3]['value'])
        p[0]['place'] = getlabel()
        register_variable(p[0]['place'])
        p[0]['code'] += p[0]['place'] + " = " + p[1]['place'] + " " + op + " " + p[3]['place']
        p[0]['type'] = 'int'

def p_prec2expr_(p):
    '''Prec2Expr_ : Prec3Expr_
                  | Prec2Expr_ AMPAMP Prec3Expr_'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['place'] = p[1]['place']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        # print("no")
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']
    else:
        p[0]['code'] = p[1]['code'] + "\n" + p[3]['code'] + "\n"
        p[0]['place'] = getlabel()
        register_variable(p[0]['place'])
        if(p[1]['type']!='int' or p[3]['type']!='int'):
            print("Error in line "+str(p.lineno(2))+" : Both expressions should be of type integer")
            exit(1)
        p[0]['code'] += p[0]['place'] + " = " + p[1]['place'] + " && " + p[3]['place']
        p[0]['type'] = p[1]['type']
        if(p[1]['value']!="" and p[3]['value']!=""):
            p[0]['value'] = p[1]['value'] and p[3]['value']

def p_expr(p):
    '''Expr : Prec2Expr_
            | Expr OROR Prec2Expr_
            | CONSTANTS
            | Chexpr
            | Arrayexp'''
    p[0] = {}
    if(len(p)==2):
        z = re.match(r'(((\*)|\ )*true|((\*)|\ )*false|((\*)|\ )*iota)',str(p[1]))
        if(z):
            p[0]['code'] = str(p[1])
        else:
            p[0]['code'] = p[1]['code']
            p[0]['place'] = p[1]['place']
            p[0]['value'] = p[1]['value']
            p[0]['type'] = p[1]['type']
            # print("yo")
            if(p[0]['type'] == "functioncall"):
              p[0]['func_responses'] = p[1]['func_responses']
    else:
        p[0]['place'] = getlabel()
        register_variable(p[0]['place'])
        if(p[1]['type']!='int' or p[3]['type']!='int'):
            print("Error in line "+str(p.lineno(2))+" : Both expressions should be of type integer")
            exit(1)
        p[0]['code'] = p[0]['place'] + " = " + p[1]['place'] + " || " + p[3]['place']
        p[0]['type'] = p[1]['type']
        if(p[1]['value']!="" and p[3]['value']!=""):
            p[0]['value'] = p[1]['value'] or p[3]['value']

def p_chexpr(p):
  '''Chexpr : LMINUS IDENTIFIER'''

def p_arrayexp(p):
  '''Arrayexp : OtherType LBRACE ExprList RBRACE'''
  p[0] = {}
  c_type = p[1]['type']['arr_type']
  i = 0
  global size
  array_label = getlabel()
  p[0]['place'] = array_label
  label2 = getlabel()
  register_variable(str(array_label))
  register_variable(str(label2))
  p[0]['code'] = str(label2)+" = BaseAddress("+str(array_label)+")"
  for objects in p[2]['exprs']:
    if(objects['type']!=c_type):
      print("Error in line "+str(p.lineno(2))+" : Error in array declaration")
      exit(1)
    else:
      temp_label = getlabel()
      p[0]['code'] += "\n" + str(temp_label)+" = "+str(i*size[c_type])
      p[0]['code'] += "\n"+objects['code'] + "\n"
      p[0]['code'] += str(label2)+"["+str(temp_label)+"] = "+str(objects['place'])
    i = i+1

  if(p[1]['type']['arr_length'] != i):
    print("Error in line "+str(p.lineno(2))+" : not enough arguments to initialise array")
    exit(1)

def p_uexpr(p):
    '''UExpr : PExpr
             | AMPERS UExpr
             | NOT UExpr
             | TIMES UExpr
             | PLUS UExpr
             | MINUS UExpr
             | XOR UExpr'''
    p[0] = {}
    if(len(p)==2):
        p[0]['code'] = p[1]['code']
        p[0]['value'] = p[1]['value']
        p[0]['type'] = p[1]['type']
        p[0]['place'] = p[1]['place']
        if(p[0]['type'] == "functioncall"):
          p[0]['func_responses'] = p[1]['func_responses']

    else:
        # will do later
        p[0]['code'] = p[2]['code'] + "\n"
        op = str(p[1])
        p[0]['value'] = ""
        if(op == "&"):
            p[0]['type'] = '*'+p[2]['type']
            p[0]['place'] = getlabel()
            register_variable(p[0]['place'])
            p[0]['code'] += p[0]['place'] + " = " + op + p[2]['place']
            p[0]['value'] = ""
        if(op == "!"):
            p[0]['type'] = 'int'
            p[0]['place'] = getlabel()
            register_variable(p[0]['place'])
            p[0]['code'] += p[0]['place'] + " = " + '!' + p[2]['place']
            if(p[2]['value'] != ""):
                if(p[2]['value']):
                    p[0]['value'] = 0
                else:
                    p[0]['value'] = 1
        if(op == "*"):
            if(p[2]['type'][0] != '*'):
                print("Error in line "+str(p.lineno(1))+" : can't dereference a non pointer")
            p[0]['type'] = p[2]['type'][1:]
            p[0]['place'] = getlabel()
            register_variable(p[0]['place'])
            p[0]['code'] += p[0]['place'] + " = " + op + p[2]['place']
        if(op == "+"):
            p[0]['type'] = p[2]['type']
            p[0]['place'] = p[2]['place']
            if(p[2]['value'] != ""):
                p[0]['value'] = p[2]['value']
        if(op == "-"):
            p[0]['type'] = p[2]['type']
            p[0]['place'] = getlabel()
            register_variable(p[0]['place'])
            p[0]['code'] += p[0]['place'] + " = " + op + p[2]['place']
            if(p[2]['value'] != ""):
                p[0]['value'] = -p[2]['value']
        if(op == "^"):
            dummy = 0

def p_forcompexpr(p):
  '''ForCompExpr : LBRACK Expr PIPE RangeStmt RBRACK'''

def p_pseudocall(p):
  '''PseudoCall : PExpr LPAREN RPAREN
                  | PExpr LPAREN ExprOrTypeList OComma RPAREN
                  | PExpr LPAREN ExprOrTypeList DDD OComma RPAREN'''
  p[0] = {}
  p[0]['place'] = []
  func_symbol_tables = get_function_symbol_tables(str(p[1]['place']))
  if(func_symbol_tables == -1):
    print("Error in line "+str(p.lineno(2))+" : function not defined!")
    exit(1)
  p[0]['func_responses'] = []
  p[0]['type'] = "functioncall"
  p[0]['value'] = ""
  p[0]['code'] = ""
  final_func=None
  for matching_name_func in func_symbol_tables:
    args = matching_name_func['CS335_args']
    response = matching_name_func['CS335_response']
    if(len(p)==4):
      if(len(args)!=0):
        continue
      else:
        final_func=matching_name_func
        break

    exprs = p[3]['exprs']
    if(len(args)!=len(exprs)):
      continue

    i=0
    arg_match=1
    for dicts in args:
      if(exprs[i]['type']!=dicts['arg_type']['val']):
        arg_match=0
        break
      i = i+1
    if(arg_match==0):
      continue
    else:
      final_func=matching_name_func
      break

  if(final_func == None):
      print("Error in line "+str(p.lineno(2))+" : Argument type mismatch")
      exit(1)
  response = final_func['CS335_response']
  args = final_func['CS335_args']

  if(len(p)==4):
    p[0]['code'] = p[1]['code']
    p[0]['code'] += "\ncall "+final_func['CS335_show_label']
    if(response != 'void'):
      for var in response:
        label = getlabel()
        register_variable(label)
        x = {}
        x['place'] = label
        x['type'] = var['val']
        x['value'] = ""

        p[0]['func_responses'].append(x)
        p[0]['code'] += "\npop "+str(label)
        p[0]['place'].append(label)
    else:
      p[0]['func_responses'] = 'void'

  elif(len(p) == 6):
    p[0]['code'] = p[1]['code']
    p[0]['code'] += "\n"+p[3]['code']
    exprs = p[3]['exprs']
    i=0
    for dicts in args:
      p[0]['code'] += "\npush "+str(exprs[i]['place'])
      i = i+1

    p[0]['code'] += "\ncall "+final_func['CS335_show_label']
    if(response != 'void'):
      for var in response:
        label = getlabel()
        register_variable(label)
        x = {}
        x['place'] = label
        x['type'] = var['val']
        x['value'] = ""
        p[0]['func_responses'].append(x)
        p[0]['code'] += "\npop "+str(label)
        p[0]['place'].append(label)
    else:
      p[0]['func_responses'] = 'void'


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


#TODO - Code insertion for struct left

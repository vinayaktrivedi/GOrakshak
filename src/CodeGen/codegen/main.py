#remove footprints of cheating


# import generate
import generateHelper
from parameter import *
import process
import os
import sys
import generate
import pickle


#create blocks
def findAllBlocks():
    ret=[]
    st=0

    for ind, instr in enumerate(ir):
        # print instr.type
        if instr.type == 'if' or instr.type == 'goto' or instr.type == 'EndFunc' or instr.type == 'call' or instr.type=='return'  or instr.type=='printf'  or instr.type=='scanf':
            ret.append([st, ind])
            st = ind + 1

        elif ind > st and instr.type == 'label':
            ret.append([st, ind - 1])
            st = ind

        elif ind == len(ir)-1:
            ret.append([st,ind])
    return ret

#creating next use table for a block
def createTable(x):
    start = x[0]
    end = x[1]
    ret = {}

    for i in range(start, end + 1):
        ret[i] = {}

    listOfSymbols = set([])
    for i in range(start, end + 1):
        if ir[i].type in type_3:
            listOfSymbols.add(ir[i].dst['name'])
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                listOfSymbols.add(ir[i].src1['name'])
            if((ir[i].src2['type'] == "local") or (ir[i].src2['type'] == "temp") or (ir[i].src2['type'] == "global")):
                listOfSymbols.add(ir[i].src2['name'])

        elif ir[i].type in type_2:
            listOfSymbols.add(ir[i].dst['name'])
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                listOfSymbols.add(ir[i].src1['name'])

        elif((ir[i].type in type_5) or (ir[i].type in type_9) or (ir[i].type in type_6)):
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                listOfSymbols.add(ir[i].src1['name'])



    for i in range(start, end + 1):
        for j in listOfSymbols:
            ret[i][j] = {}
            ret[i][j]["live"] = False
            ret[i][j]["nextUse"] = None

    for i in range(end, start - 1, -1):

        #propogates live and nextUse
        if i != end:
            for k in ret[i]:
                ret[i][k] = ret[i + 1][k].copy()

        if ir[i].type in type_3:

            (ret[i])[ir[i].dst['name']]["live"] = False
            (ret[i])[ir[i].dst['name']]["nextUse"] = None

            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                (ret[i])[ir[i].src1['name']]["live"] = True
                (ret[i])[ir[i].src1['name']]["nextUse"] = i

            if((ir[i].src2['type'] == "local") or (ir[i].src2['type'] == "temp") or (ir[i].src2['type'] == "global")):
                (ret[i])[ir[i].src2['name']]["live"] = True
                (ret[i])[ir[i].src2['name']]["nextUse"] = i

        elif ir[i].type in type_2:
            (ret[i])[ir[i].dst['name']]["live"] = False
            (ret[i])[ir[i].dst['name']]["nextUse"] = None
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                (ret[i])[ir[i].src1['name']]["live"] = True
                (ret[i])[ir[i].src1['name']]["nextUse"] = i

        elif ir[i].type in type_5 or ir[i].type in type_6:
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                (ret[i])[ir[i].src1['name']]["live"] = True
                (ret[i])[ir[i].src1['name']]["nextUse"] = i

        elif ir[i].type in type_9:
            if((ir[i].src1['type'] == "local") or (ir[i].src1['type'] == "temp") or (ir[i].src1['type'] == "global")):
                (ret[i])[ir[i].src1['name']]["live"] = False
                (ret[i])[ir[i].src1['name']]["nextUse"] = None


    for i in range(start, end):
        ret[i] = ret[i + 1]

    ## make all live and next Use none for last instruction
    for i in listOfSymbols:
        ret[end][i]["live"] = False
        ret[end][i]["nextUse"] = None

    return ret

#taking input 3ac
if (len(sys.argv) != 2):
    print("Input 3 Address code not given")
    exit(1)

if (not os.path.isfile(str(sys.argv[1]))):
    print("3 AC does not exist")
    exit(1)

lines = tuple(open(str(sys.argv[1]), 'r'))

threeAC=[]
# print(lines)
for x in lines:
    stripped = x.strip().split(" ")
    for i in range(len(stripped)):
        stripped[i] = stripped[i].replace(" ", ",")
    threeAC.append(stripped)

# symboltablesfile = open('examplePickle', 'rb')
# global_symbol_table = pickle.load(symboltablesfile)

#also attach address in stack of variables, assign type based on local, global, temp,constant
ind = 0
for i in threeAC:
    if(i[0] == 'package' or i[0] == 'import'):
        continue
    ir.append(process.IR(i))
    # print ind,
    # print ir[ind].type,
    # print i
    ind = ind + 1
# print(ir[0].type)

#finding blocks
blocks = findAllBlocks()
print(blocks)
#print blocks
#ode gen globals, use global_symbol_table
generateHelper.genGlobals()

#code gen blocks
for block in blocks:
    nextUseTable = createTable(block)
    generate.genCodeForBlock(block,nextUseTable)

#code gen final
generateHelper.close()

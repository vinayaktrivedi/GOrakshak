#remove footprints of cheating

import break_code
import generate
import generateHelper
import infoTable
from parameter import *
import process
import os
import sys
import pickle


#taking input 3ac
if (len(sys.argv) != 2):
    print("Input 3 Address code not given")
    exit(1)

if (not os.path.isfile(str(sys.argv[1]))):
    print("3 AC does not exist")
    exit(1)

lines = tuple(open(str(sys.argv[1]), 'r'))

threeAC=[]
print(lines)
for x in lines:
    stripped = x.strip().split(" ")
    # print stripped
    for i in range(len(stripped)):
        stripped[i] = stripped[i].replace(" ", ",")
    threeAC.append(stripped)
# print threeAC
# a = threeAC[0].split(',')
# #taking global symbol table
# symboltablesfile = open('examplePickle', 'rb')
# global_symbol_table = pickle.load(symboltablesfile)

#also attach address in stack of variables, assign type based on local, global, temp,constant
for i in threeAC:
    if(i[0] == 'package' or i[0] == 'import'):
        continue
    ir.append(process.IR(i))
    # print i
print(ir[0].type)

# #finding blocks
# blocks = blocks.findAllBlocks()

# #code gen globals, use global_symbol_table
# generateHelper.genGlobals()

# #code gen blocks
# for block in blocks:
#     nextUseTable = infoTable.createTable(block)
#     generate.genCodeForBlock(block,nextUseTable)

# #code gen final
# generateHelper.close()

#remove footprints of cheating

import blocks
import generate
import generateHelper
import infoTable
from config import *
import process
import os
import sys
import pickle


#taking input 3ac
if (len(sys.argv) != 2):
    raise LookupError("Provide input 3ac code")

if (not os.path.isfile(str(sys.argv[1]))):
    raise LookupError("3ac code file doesn't exists")

lines = tuple(open(str(sys.argv[1]), 'r'))

threeAC=[]
for x in lines:
    stripped = x.strip().split(",")
    for i in range(len(stripped)):
        stripped[i] = stripped[i].replace(" ", "")
    threeAC.append(stripped)

#taking global symbol table
symboltablesfile = open('examplePickle', 'rb')      
global_symbol_table = pickle.load(symboltablesfile) 

#also attach address in stack of variables, assign type based on local, global, temp,constant
for i in threeAC:
    ir.append(process.IR(i))



#finding blocks
blocks = blocks.findAllBlocks()

#code gen globals, use global_symbol_table
generateHelper.genGlobals()

#code gen blocks
for block in blocks:
    nextUseTable = infoTable.createTable(block)
    generate.genCodeForBlock(block,nextUseTable)

#code gen final
generateHelper.close()

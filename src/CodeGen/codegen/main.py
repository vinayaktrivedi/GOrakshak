import blocks
import generate
import generateHelper
import nextUse
from config import *
import process
import os
import sys


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

for i in threeAC:
    ir.append(process.IR(i))


blocks= blocks.findAllBlocks()

generateHelper.genGlobals()

for block in blocks:
    nextUseTable = nextUse.nextUseTable(block)
    generate.genCodeForBlock(block,nextUseTable)

generateHelper.close()

from config import *

def findAllBlocks():
    ret=[]
    st=0

    for ind, instr in enumerate(ir):
        if instr.type == 'goto' or instr.type == 'ret' or instr.type == 'call':
            ret.append([st, ind])
            st = ind + 1
        
        elif ind > st and instr.type == 'label':
            ret.append([st, ind - 1])
            st = ind

        elif ind == len(ir)-1:
            ret.append((st,ind))

    return ret 
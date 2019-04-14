from parameter import *

def findAllBlocks():
    ret=[]
    st=0

    for ind, instr in enumerate(ir):
        flag = 0
        if instr.type == 'goto' or instr.type == 'ret' or instr.type == 'call':
            ret.append([st, ind])
            flag = 1

        elif ind > st and instr.type == 'label':
            ret.append([st, ind - 1])

        elif ind == len(ir)-1:
            ret.append((st,ind))
            flag = 2

        if flag == 1:
            st = ind + 1
        if flag == 0:
            st = ind

    return ret

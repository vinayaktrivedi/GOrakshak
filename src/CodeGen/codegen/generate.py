from config import *
import generateHelper

def freeAllRegs():
    for regname in regsList:
        regsInfo[regname]=None

def getReg():
    pass


#set up addrDesc which is used to access runtime location of temp and local variables and global variables
def setupAddrDesc(st,end):
    AddrDesc.clear()
    for i in range(st, end + 1):
        if ir[i].type in type_3:  
            if ir[i].dst.type=="local":
                AddrDesc[ir[i].dst.value]= ir[i].dst.addr
            elif ir[i].dst.type=="global":
                AddrDesc[ir[i].dst.value]= ir[i].dst.value 

            if ir[i].src1.type=="local":
                AddrDesc[ir[i].src1.value]= ir[i].src1.addr
            elif ir[i].src1.type=="global":
                AddrDesc[ir[i].src1.value]= ir[i].src1.value
    
            if ir[i].src2.type=="local":
                AddrDesc[ir[i].src2.value]= ir[i].src2.addr
            elif ir[i].src2.type=="global":
                AddrDesc[ir[i].src2.value]= ir[i].src2.value

        elif ir[i].type in type_2:
            if ir[i].dst.type=="local":
                AddrDesc[ir[i].dst.value]= ir[i].dst.addr 
            elif ir[i].dst.type=="global":
                AddrDesc[ir[i].dst.value]= ir[i].dst.value

            if ir[i].src1.type=="local":
                AddrDesc[ir[i].src1.value]= ir[i].src1.addr
            elif ir[i].src1.type=="global":
                AddrDesc[ir[i].src1.value]= ir[i].src1.value
        
        elif((ir[i].type in type_5) or (ir[i].type in type_9) or (ir[i].type in type_6)):
            if((ir[i].src1.type == "local")): 
                AddrDesc[ir[i].src1.value]= ir[i].src1.addr
            elif ir[i].src1.type=="global":
                AddrDesc[ir[i].src1.value]= ir[i].src1.value

def genCodeForBlock(block, infoTable):
    st=block[0]
    end=block[1]
    freeAllRegs()
    setupAddrDesc(st,end)


    for i in range(st,end):
        if ir[i].type in type_1:
            pass
        elif ir[i].type in type_2:
            pass
        elif ir[i].type in type_3:
            #getReg()
            #find address of src1, access address of local and temp variables from AddrDesc, no need for global and constant
            #find address of src2
            #writeInstr
            pass
        elif ir[i].type in type_4:
            pass
        elif ir[i].type in type_5:
            pass
        elif ir[i].type in type_6:
            pass
        elif ir[i].type in type_7:
            pass
        elif ir[i].type in type_8:
            pass
        elif ir[i].type in type_9:
            pass
        elif ir[i].type in type_10:
            pass
    
    #handle last one separately
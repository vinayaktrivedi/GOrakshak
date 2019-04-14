from parameter import *
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
            if(ir[i].src1['type']!='constant'):
                L=getReg(ir[i].src1['name'],infoTable,i)
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1
            else:
                if(AddrDesc[ir[i].dst['name']]['reg'] == None):
                    L=getfreereg(None)
                    generateHelper.writeInstr("mov "+L+", "+ir[i].src1['name'])
                    AddrDesc[ir[i].dst['name']]['reg']=L
                    regsInfo[L]=ir[i].dst['name']
                    AddrDesc[ir[i].dst['name']]['dirty']=1
                else:
                    generateHelper.writeInstr("mov "+AddrDesc[ir[i].dst['name']]['reg']+", "+ir[i].src1['name'])
                    AddrDesc[ir[i].dst['name']]['dirty']=1

        elif ir[i].type in type_3:
            if(ir[i].src1['type']=='constant' and ir[i].src2['type']=='constant'):
                L=getfreereg(None)
                generateHelper.writeInstr("mov "+L+", "+ir[i].src1['name'])
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+L+", "+ir[i].src2['name'])
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+L+", "+ir[i].src2['name'])
                elif(ir[i].type == '<='):            
                    generateHelper.writeInstr("cmp "+L+", "+ir[i].src2['name'])
                    generateHelper.writeInstr("setle al")
                    generateHelper.writeInstr("movbzl eax, al")
                    generateHelper.writeInstr("mov "+ L +", eax")
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1
                    
            elif(ir[i].src1['type']=='constant'):
                L=getfreereg(None)
                generateHelper.writeInstr("mov "+L+", "+ir[i].src1['name'])
                if(AddrDesc[ir[i].src2['name']]['reg']==None):
                    L2=getfreereg(L)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src2['name']]['mem'])
                    AddrDesc[ir[i].src2['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src2['name']
                    AddrDesc[ir[i].src2['name']]['dirty']=0
                    
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                elif(ir[i].type == '<='):            
                    generateHelper.writeInstr("cmp "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                    generateHelper.writeInstr("setle al")
                    generateHelper.writeInstr("movbzl eax, al")
                    generateHelper.writeInstr("mov "+ L +", eax")
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1

            elif(ir[i].src2['type']=='constant'):
                L=getReg(ir[i].src1['name'],infoTable,i)
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+L+", "+ir[i].src2['name'])
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+L+", "+ir[i].src2['name'])
                elif(ir[i].type == '<='):            
                    generateHelper.writeInstr("cmp "+L+", "+ir[i].src2['name'])
                    generateHelper.writeInstr("setle al")
                    generateHelper.writeInstr("movbzl eax, al")
                    generateHelper.writeInstr("mov "+ L +", eax")
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1
            else:
                L=getReg(ir[i].src1['name'],infoTable,i)
                if(AddrDesc[ir[i].src2['name']]['reg']==None):
                    L2=getfreereg(L)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src2['name']]['mem'])
                    AddrDesc[ir[i].src2['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src2['name']
                    AddrDesc[ir[i].src2['name']]['dirty']=0
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                elif(ir[i].type == '<='):            
                    generateHelper.writeInstr("cmp "+L+", "+AddrDesc[ir[i].src2['name']]['reg'])
                    generateHelper.writeInstr("setle al")
                    generateHelper.writeInstr("movbzl eax, al")
                    generateHelper.writeInstr("mov "+ L +", eax")
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1

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
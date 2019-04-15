from parameter import *
import generateHelper
code = ""
AddrDesc = {}
func_offset=-1
def freeAllRegs():
    for regname in regsList:
        regsInfo[regname]=None

def removeFromRegs(var):
    for regname in regsList:
        if(regsInfo[regname]==var):
            regsInfo[regname]=None
def saveDirtyAndClean():
    for i in AddrDesc.items():
        if(AddrDesc[i]['dirty']==1 and AddrDesc[i]['real']==1 and AddrDesc[i]['reg']!=None):
            generateHelper.writeInstr("mov "+AddrDesc[i]['mem']+","AddrDesc[i]['reg'])


def getfreereg(instrcution_number,nextuse,preserve_reg):
    global AddrDesc
    global func_offset
    temp_reg = None
    mini = -1
    for regname in regsList:
        if regsInfo[regname] == None:
            return regname
    for regname in regsList:
        if regname == preserve_reg:
            continue
        info = nextuse[instrcution_number][regsInfo[regname]]
        if info == None:
            return regname
        elif  info > mini:
            mini = info 
            temp_reg = regname

    variable_name = regsInfo[regname]
    if AddrDesc[variable_name]['memory'] == None:
        func_offset += 4
        AddrDesc[variable_name]['memory'] = func_offset 
        generateHelper.writeInstr("push "+regname)
    else:
        generateHelper.writeInstr("mov -"+AddrDesc[variable_name]['memory']+"[ebp] "+regname)
    AddrDesc[variable_name]['reg'] = None
    AddrDesc[variable_name]['dirty'] = 0
    return regname

def getReg(instrcution_number,src1,nextuse):
    
    global AddrDesc
    reg = AddrDesc[src1]['reg'] 
    if reg != None:
        if nextuse[instrcution_number][src1] == None:
            return reg 
        else:
            new_reg = get_free_reg(instrcution_number,nextuse,None)
            generateHelper.writeInstr("mov "+new_reg+" "+reg)
            return new_reg
    else:
        new_reg = get_free_reg(instrcution_number,nextuse,None)
        generateHelper.writeInstr("mov "+new_reg+" -"+AddrDesc[src1['name']]['memory']+"[ebp]")
        return new_reg


#set up addrDesc which is used to access runtime location of temp and local variables and global variables
def setupAddrDesc(st,end):
    global AddrDesc
    AddrDesc = {}
    for i in range(st, end + 1):
        if ir[i].type in type_3:  
            operands = [ir[i].dst,ir[i].src1,ir[i].src2]
        elif ir[i].type in type_2:
            operands = [ir[i].dst,ir[i].src1]
        elif((ir[i].type in type_5) or (ir[i].type in type_9) or (ir[i].type in type_6)):
            operands = [ir[i].src1]

        for variable in operands:
            if variable.type=="local":
                value = variable.value
                AddrDesc[value]= {}
                AddrDesc[value]['memory'] = None
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 0
            elif variable.type=="global":
                value = variable.value
                AddrDesc[value]= {}
                AddrDesc[value]['memory'] = variable.value
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 1
            else:
                value = variable.value
                AddrDesc[value] = {}
                AddrDesc[value]['memory'] = variable.addr
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 1

def genCodeForBlock(block, infoTable):
    st=block[0]
    end=block[1]
    freeAllRegs()
    setupAddrDesc(st,end)


    for i in range(st,end+1):
        if ir[i].type in type_2:
            name = ir[i].dst['name']
            if(ir[i].src1['type']!='constant'):
                L=getReg(i,name,infoTable)
                removeFromRegs(name)
                AddrDesc[name]['reg']=L
                regsInfo[L]=name
                AddrDesc[name]['dirty']=1
            else:
                if(AddrDesc[name]['reg'] == None):
                    L=getfreereg(i,infoTable,None)
                    generateHelper.writeInstr("mov "+L+", "+ir[i].src1['name'])
                    AddrDesc[name]['reg']=L
                    regsInfo[L]=name
                    AddrDesc[name]['dirty']=1
                else:
                    generateHelper.writeInstr("mov "+AddrDesc[name]['reg']+", "+ir[i].src1['name'])
                    AddrDesc[ir[i].dst['name']]['dirty']=1

        elif ir[i].type in type_3:
            name = ir[i].dst['name']
            if(ir[i].src1['type']=='constant' and ir[i].src2['type']=='constant'):
                L=getfreereg(i,infoTable,None)
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
                removeFromRegs(name)
                AddrDesc[name]['reg']=L
                regsInfo[L]=name 
                AddrDesc[name]['dirty']=1
                    
            elif(ir[i].src1['type']=='constant'):
                L=getfreereg(i,infoTable,None)
                generateHelper.writeInstr("mov "+L+", "+ir[i].src1['name'])
                if(AddrDesc[ir[i].src2['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,L)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src2['name']]['memory'])
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
                    L2=getfreereg(i,infoTable,L)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src2['name']]['memory'])
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
            
        elif ir[i].type in type_5:
            if(ir[i].src1['type']=='constant'):   #push registers
                generateHelper.writeInstr("push "+ir[i].src1['name'])
            else:
                if(AddrDesc[ir[i].src1['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,None)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src1['name']]['mem'])
                    AddrDesc[ir[i].src1['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src1['name']
                    AddrDesc[ir[i].src1['name']]['dirty']=0
                    generateHelper.writeInstr("push "+L2)
                else:
                    generateHelper.writeInstr("push "+AddrDesc[ir[i].src1['name']]['reg'])

        elif ir[i].type in type_7:
            generateHelper.writeInstr(ir[i].src1['name']+ ":")
        elif ir[i].type in type_8:
            generateHelper.writeInstr(ir[i].src1['name']+ ":")
            generateHelper.writeInstr("push rbp")
            generateHelper.writeInstr("mov rbp, rsp")
            generateHelper.writeInstr("push eax")
            generateHelper.writeInstr("push ebx")
            generateHelper.writeInstr("push esi")
            generateHelper.writeInstr("push edi")
            generateHelper.writeInstr("push edx")
            global func_offset
            func_offset=int(ir[i].src2['name'])
        elif ir[i].type in type_9:
            if(ir[i].src1['type']=='constant'):   #pop registers
                generateHelper.writeInstr("pop "+ir[i].src1['name'])
            else:
                if(AddrDesc[ir[i].src1['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,None)
                    generateHelper.writeInstr("mov "+L2+","+AddrDesc[ir[i].src1['name']]['mem'])
                    AddrDesc[ir[i].src1['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src1['name']
                    AddrDesc[ir[i].src1['name']]['dirty']=0
                    generateHelper.writeInstr("pop "+L2)
                    AddrDesc[ir[i].src1['name']]['dirty']=1
                else:
                    generateHelper.writeInstr("pop "+AddrDesc[ir[i].src1['name']]['reg'])
                    AddrDesc[ir[i].src1['name']]['dirty']=1    

        #handle last one separately
        if(i==end):
            if ir[i].type in type_1:
                saveDirtyAndClean()
                generateHelper.writeInstr("call "+ir[i].src1['name'])
            elif ir[i].type in type_4:
                saveDirtyAndClean()
                generateHelper.writeInstr(ir[i].src1['name']+":")
            elif ir[i].type in type_6:
                if(AddrDesc[ir[i].src1['name']]['reg']==None):
                    generateHelper.writeInstr("mov eax,"+AddrDesc[ir[i].src1['name']]['mem'])
                else:
                    generateHelper.writeInstr("mov eax,"+AddrDesc[ir[i].src1['name']]['reg'])
                
                saveDirtyAndClean() #clean everything except eax
                generateHelper.writeInstr("cmp 0, eax")
                generateHelper.writeInstr("je "+ir[i].dst['name'])
                
            elif ir[i].type in type_10:
                if(ir[i].src1['type']=='constant'):
                    generateHelper.writeInstr("mov eax, "+ir[i].src1['name'])
                else:
                    if(AddrDesc[ir[i].src1['name']]['reg']==None):
                        generateHelper.writeInstr("mov eax,"+AddrDesc[ir[i].src1['name']]['mem'])
                    else:
                        generateHelper.writeInstr("mov eax,"+AddrDesc[ir[i].src1['name']]['reg'])
                saveDirtyAndClean() #clean everything except eax
                generateHelper.writeInstr("ret")
                
                    
    
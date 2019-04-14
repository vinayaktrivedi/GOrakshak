from parameter import *
import generateHelper
code = ""
AddrDesc = {}
def freeAllRegs():
    for regname in regsList:
        regsInfo[regname]=None

def get_free_reg(instrcution_number,nextuse,preserve_reg):
    global AddrDesc
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
    generateHelper.writeInstr("mov -"+AddrDesc[variable_name]['memory']+"[ebp] "+regname)
    AddrDesc[variable_name]['reg'] = None
    AddrDesc[variable_name]['dirty'] = 0
    return regname

def getReg(instrcution_number,src1,nextuse):
    
    global AddrDesc
    reg = AddrDesc[src1['name']]['reg'] 
    if reg != None:
        if nextuse[instrcution_number][src1['name']] == None:
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
            elif variable.type=="global":
                value = variable.value
                AddrDesc[value]= {}
                AddrDesc[value]['memory'] = variable.value
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
            else:
                value = variable.value
                AddrDesc[value] = {}
                AddrDesc[value]['memory'] = variable.addr
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0

def genCodeForBlock(block, infoTable):
    st=block[0]
    end=block[1]
    freeAllRegs()
    setupAddrDesc(st,end)


    for i in range(st,end):
        if ir[i].type in type_1:
            pass
        elif ir[i].type in type_2:
            if(ir[i].dst['type']=='temp'):
                if(ir[i].src1['type']=='temp'):
                
                elif(ir[i].dst['type']=='local'):

                elif(ir[i].dst['type']=='global'):

            elif(ir[i].dst['type']=='local'):

            elif(ir[i].dst['type']=='global'):


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
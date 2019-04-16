from parameter import *
import generateHelper
from process import *
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
    for i in AddrDesc.keys():
        if(AddrDesc[i]['dirty']==1 and AddrDesc[i]['real']==1 and AddrDesc[i]['reg']!=None):
            generateHelper.writeInstr("mov "+AddrDesc[i]['reg']+", "+AddrDesc[i]['memory']+"(%rbp) ")


def getfreereg(instrcution_number,nextuse,preserve_reg):
    global AddrDesc
    global func_offset
    print("input=", preserve_reg)

    temp_reg = None
    mini = -1
    for regname in regsList:
        if regsInfo[regname] == None:
            if preserve_reg!=None and regname in preserve_reg:
                continue
            return regname

    for regname in regsList:
        if preserve_reg!=None and  regname in preserve_reg:
            continue
        if not (regsInfo[regname] in nextuse[instrcution_number]):
            continue
        info = nextuse[instrcution_number][regsInfo[regname]]
        if info == None:
            AddrDesc[regsInfo[regname]]['reg'] = None
            return regname
        elif  info > mini:
            mini = info
            temp_reg = regname

    regname = temp_reg
    variable_name = regsInfo[regname]
    if AddrDesc[variable_name]['memory'] == None:
        # yha change kiya
        # func_offset += 4
        func_offset += 8
        # print(variable_name,func_offset)
        AddrDesc[variable_name]['memory'] = str(-func_offset)
        generateHelper.writeInstr("push "+temp_reg)
    elif type(AddrDesc[variable_name]['memory']) == dict:
        base = AddrDesc[variable_name]['memory']['base']
        shift = AddrDesc[variable_name]['memory']['offset']
        L = getfreereg(instrcution_number,nextuse,[preserve_reg,temp_reg])
        regsInfo[L] = 'a'
        generateHelper.writeInstr("mov %rbp, "+L)
        generateHelper.writeInstr("sub $"+base+" , "+L)
        L2 = getfreereg(instrcution_number,nextuse,[preserve_reg,temp_reg,L])
        regsInfo[L2] = 'a'
        if int(shift)>=0:
            generateHelper.writeInstr("mov $"+shift+" , "+L2)    
        else:
            temp = AddrDesc[AddrDesc[variable_name]['memory']['val']]['reg']
            if temp != None:
                generateHelper.writeInstr("mov "+temp+" , "+L2)
            else:
                generateHelper.writeInstr("mov "+shift+"(%rbp) , "+L2)
        generateHelper.writeInstr("shl $2 , "+L2)
        generateHelper.writeInstr("sub "+L2+" , "+L)
        generateHelper.writeInstr("mov "+regname+" , "+"("+L+")")
    else:
        # print("hello")
        # print(regname)
        # print(variable_name)
        # print(AddrDesc[variable_name]['memory'])
        generateHelper.writeInstr("mov "+temp_reg+" , "+AddrDesc[variable_name]['memory']+"(%rbp)")
    AddrDesc[variable_name]['reg'] = None
    AddrDesc[variable_name]['dirty'] = 0
    print("ouptut=", regname)
    return regname

def getReg(instrcution_number,src1,nextuse):

    global AddrDesc
    global func_offset
    reg = AddrDesc[src1]['reg']
    if reg != None:
        if nextuse[instrcution_number][src1] == None:
            AddrDesc[src1]['reg'] = None
            return reg
        else:
            new_reg = getfreereg(instrcution_number,nextuse,[reg])
            generateHelper.writeInstr("mov "+reg+", "+new_reg)
            return new_reg
    else:
        
        new_reg = getfreereg(instrcution_number,nextuse,None)
        if AddrDesc[src1]['memory'] == None:
            func_offset += 8
            AddrDesc[src1]['memory'] = str(-func_offset)
            generateHelper.writeInstr("push "+new_reg)
        elif type(AddrDesc[src1]['memory']) == dict:
            base = AddrDesc[src1]['memory']['base']
            shift = AddrDesc[src1]['memory']['offset']
            L = getfreereg(instrcution_number,nextuse,[new_reg])
            regsInfo[L] = 'a'
            generateHelper.writeInstr("mov %rbp, "+L)
            generateHelper.writeInstr("sub $"+base+" , "+L)
            L2 = getfreereg(instrcution_number,nextuse,[new_reg,L])
            regsInfo[L2] = 'a'
            if int(shift)>=0:
                generateHelper.writeInstr("mov $"+shift+" , "+L2)
            else:
                temp = AddrDesc[AddrDesc[src1]['memory']['val']]['reg']
                if temp != None:
                    generateHelper.writeInstr("mov "+temp+" , "+L2)
                else:
                    generateHelper.writeInstr("mov "+shift+"(%rbp) , "+L2)
            generateHelper.writeInstr("shl $2 , "+L2)
            generateHelper.writeInstr("sub "+L2+" , "+L)
            generateHelper.writeInstr("mov "+"("+L+")"+" , "+new_reg)
        else:
            generateHelper.writeInstr("mov  "+AddrDesc[src1]['memory']+"(%rbp) , " + new_reg)
        return new_reg

def array_gen(instrcution_number,nextuse,dictionary,preserve_reg,reg):
    base = dictionary['memory']['base']
    shift = dictionary['memory']['offset']
    L = getfreereg(instrcution_number,nextuse,preserve_reg)
    regsInfo[L] = 'a'
    preserve_reg.append(L)
    generateHelper.writeInstr("mov %rbp, "+L)
    generateHelper.writeInstr("sub $"+base+" , "+L)
    L2 = getfreereg(instrcution_number,nextuse,preserve_reg)
    regsInfo[L2] = 'a'
    if int(shift)>=0:
            generateHelper.writeInstr("mov $"+shift+" , "+L2)
    else:
        temp = AddrDesc[dictionary['memory']['val']]['reg']
        if temp != None:
            generateHelper.writeInstr("mov "+temp+" , "+L2)
        else:
            generateHelper.writeInstr("mov "+shift+"(%rbp) , "+L2)
    generateHelper.writeInstr("shl $2 , "+L2)
    generateHelper.writeInstr("sub "+L2+" , "+L)
    generateHelper.writeInstr("mov "+"("+L+")"+" , "+reg)

#set up addrDesc which is used to access runtime location of temp and local variables and global variables
def setupAddrDesc(st,end):
    global AddrDesc
    AddrDesc = {}
    for i in range(st, end + 1):
        #print(ir[i].type)
        if ir[i].type in type_3:
            operands = [ir[i].dst,ir[i].src1,ir[i].src2]
        elif ir[i].type in type_2:
            operands = [ir[i].dst,ir[i].src1]
        elif((ir[i].type in type_5) or (ir[i].type in type_9) or (ir[i].type in type_6) or (ir[i].type in type_10)):
            operands = [ir[i].src1]
        elif((ir[i].type in type_11) or (ir[i].type in type_12)):
            operands = [ir[i].arg2]
        else:
            continue
        # print(operands)
        for variable in operands:

            if variable['type']=="temp":

                value = variable['name']
                AddrDesc[value]= {}
                AddrDesc[value]['memory'] = None
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 0
            elif variable['type']=="global":
                value = variable['name']
                AddrDesc[value]= {}
                AddrDesc[value]['memory'] = variable['name']
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 1
            else:
                value = variable['name']
                AddrDesc[value] = {}
                a = int(variable['addr'])
                a = a*-1
                a = a*2
                # print(a)
                # AddrDesc[value]['memory'] = variable['addr']
                AddrDesc[value]['memory'] = str(a)
                AddrDesc[value]['reg'] = None
                AddrDesc[value]['dirty'] = 0
                AddrDesc[value]['real'] = 1

def genCodeForBlock(block, infoTable):
    
    nextuse = infoTable
    st=block[0]
    end=block[1]
    freeAllRegs()
    setupAddrDesc(st,end)


    for i in range(st,end+1):
        instrcution_number = i
        if ir[i].type in type_2:
            name = ir[i].dst['name']
            if 'array' in ir[i].src1 and ir[i].src1['array'] == 'True':
                global AddrDesc
                AddrDesc[name]['memory'] = {}
                AddrDesc[name]['memory']['base'] = str(-int(ir[i].src1['addr']))
                AddrDesc[name]['memory']['offset'] = str(-int(ir[i].src1['array_offset']['addr']))
                AddrDesc[name]['memory']['val'] = ir[i].src1['array_offset']['val']

            if ir[i].dst['name'] in rep:
                if(ir[i].src1['type']=='constant'):
                    #generateHelper.writeInstr("hi "+ir[i].src1['name'])
                    base = AddrDesc[name]['memory']['base']
                    shift = AddrDesc[name]['memory']['offset']
                    L = getfreereg(instrcution_number,nextuse,None)
                    regsInfo[L] = 'a'
                    generateHelper.writeInstr("mov %rbp, "+L)
                    generateHelper.writeInstr("sub $"+base+" , "+L)
                    L2 = getfreereg(instrcution_number,nextuse,[L])
                    regsInfo[L2] = 'a'
                    if int(shift)>=0:
                        generateHelper.writeInstr("mov $"+shift+" , "+L2)
                    else:

                        temp = AddrDesc[AddrDesc[name]['memory']['val']]['reg']
                        if temp != None:
                            generateHelper.writeInstr("mov "+temp+" , "+L2)
                        else:
                            generateHelper.writeInstr("mov "+shift+"(%rbp) , "+L2)
                    generateHelper.writeInstr("shl $2 , "+L2)
                    generateHelper.writeInstr("sub "+L2+" , "+L)
                    L3 = getfreereg(instrcution_number,nextuse,[L,L2])
                    generateHelper.writeInstr("mov $"+ir[i].src1['name']+" , "+L3)
                    generateHelper.writeInstr("mov "+L3+" , "+"("+L+")")
                    
                else:
                    base = AddrDesc[name]['memory']['base']
                    shift = AddrDesc[name]['memory']['offset']
                    L = getfreereg(instrcution_number,nextuse,None)
                    regsInfo[L] = 'a'
                    generateHelper.writeInstr("mov %rbp, "+L)
                    generateHelper.writeInstr("sub $"+base+" , "+L)
                    L2 = getfreereg(instrcution_number,nextuse,[L])
                    regsInfo[L2] = 'a'
                    if int(shift)>=0:
                        generateHelper.writeInstr("mov $"+shift+" , "+L2)
                    else:
                        temp = AddrDesc[AddrDesc[name]['memory']['val']]['reg']
                        if temp != None:
                            generateHelper.writeInstr("mov "+temp+" , "+L2)
                        else:
                            generateHelper.writeInstr("mov "+shift+"(%rbp) , "+L2)
                    generateHelper.writeInstr("shl $2 , "+L2)
                    generateHelper.writeInstr("sub "+L2+" , "+L)

                    if AddrDesc[ir[i].src1['name']]['reg'] != None:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['reg']+" , "+"("+L+")")
                    else:
                        L3 = getfreereg(instrcution_number,nextuse,[L,L2])
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['memory']+"(%rbp) , "+L3)
                        generateHelper.writeInstr("mov "+L3+" , "+"("+L+")")

            else:
                if(ir[i].src1['type']!='constant'):
                    #generateHelper.writeInstr("hi "+ir[i].src1['name'])
                    L=getReg(i,ir[i].src1['name'],infoTable)
                    removeFromRegs(name)
                    AddrDesc[name]['reg']=L
                    regsInfo[L]=name
                    AddrDesc[name]['dirty']=1
                else:
                    if(AddrDesc[name]['reg'] == None):
                        L=getfreereg(i,infoTable,None)

                        generateHelper.writeInstr("mov $"+ir[i].src1['name']+","+L)
                        AddrDesc[name]['reg']=L
                        regsInfo[L]=name
                        AddrDesc[name]['dirty']=1
                    else:
                        generateHelper.writeInstr("mov $"+ir[i].src1['name']+", "+AddrDesc[name]['reg'])
                        AddrDesc[ir[i].dst['name']]['dirty']=1

        elif ir[i].type in type_3:
            name = ir[i].dst['name']
            if(ir[i].src1['type']=='constant' and ir[i].src2['type']=='constant'):
                L=getfreereg(i,infoTable,None)
                generateHelper.writeInstr("mov "+ir[i].src1['name']+","+L)
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+ir[i].src2['name']+","+L)
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+ir[i].src2['name']+", "+L)
                elif(ir[i].type == '<='):
                    generateHelper.writeInstr("cmp "+ir[i].src2['name']+", "+L)
                    generateHelper.writeInstr("setle al")
                    generateHelper.writeInstr("movbzl al, %rax")
                    generateHelper.writeInstr("mov %rax ,"+ L)
                removeFromRegs(name)
                AddrDesc[name]['reg']=L
                regsInfo[L]=name
                AddrDesc[name]['dirty']=1

            elif(ir[i].src1['type']=='constant'):
                L=getfreereg(i,infoTable,None)
                generateHelper.writeInstr("mov "++ir[i].src1['name']+", "+L)
                if(AddrDesc[ir[i].src2['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,[L])
                    if type(AddrDesc[ir[i].src2['name']]['memory']) == dict:
                        array_gen(instrcution_number,nextuse,AddrDesc[ir[i].src2['name']],[L,L2],L2)
                    else:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src2['name']]['memory']+"(%rbp), "+L2)

                    AddrDesc[ir[i].src2['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src2['name']
                    AddrDesc[ir[i].src2['name']]['dirty']=0

                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                elif(ir[i].type == '<='):
                    generateHelper.writeInstr("cmp "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                    generateHelper.writeInstr("setle %al")
                    generateHelper.writeInstr("movbzl %al,%rax")
                    generateHelper.writeInstr("mov "+" %rax"+", "+L)
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1

            elif(ir[i].src2['type']=='constant'):
                L=getReg(i,ir[i].src1['name'],infoTable)
                if(ir[i].type == '+int'):
                    generateHelper.writeInstr("add $"+ir[i].src2['name']+", "+L)
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub $"+ir[i].src2['name']+", "+L)
                elif(ir[i].type == '<='):
                    generateHelper.writeInstr("cmp $"+ir[i].src2['name']+", "+L)
                    generateHelper.writeInstr("setle %al")
                    generateHelper.writeInstr("movbz %al, %rax")
                    generateHelper.writeInstr("mov %rax, "+ L)
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1
            else:
                # print(ir[i].src1['name'],"hi")
                print regsInfo
                L=getReg(i,ir[i].src1['name'],infoTable)
                print(ir[i].src1['name'],ir[i].src2['name'])
                print L
                # print(AddrDesc)
                print regsInfo
                if(AddrDesc[ir[i].src2['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,[L])
                    # print i, ir[i].src2['name'], ir[i].src2['type'], ir[i].type
                    # print(L2)

                    # print(ir[i].src2['name'])
                    # print(ir[i].src2)
                    if type(AddrDesc[ir[i].src2['name']]['memory']) == dict:
                        array_gen(instrcution_number,nextuse,AddrDesc[ir[i].src2['name']],[L,L2],L2)
                    else:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src2['name']]['memory']+"(%rbp), "+L2)
                    AddrDesc[ir[i].src2['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src2['name']
                    AddrDesc[ir[i].src2['name']]['dirty']=0
                    print L,L2,"hello",regsInfo
                if(ir[i].type == '+int'):
                    # print(L)
                    # print(AddrDesc[ir[i].src2['name']]['reg'])
                    generateHelper.writeInstr("add "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                elif(ir[i].type == '-int'):
                    generateHelper.writeInstr("sub "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                elif(ir[i].type == '<='):
                    generateHelper.writeInstr("cmp "+AddrDesc[ir[i].src2['name']]['reg']+", "+L)
                    generateHelper.writeInstr("setle %al")
                    generateHelper.writeInstr("movbzl %al, %rax")
                    generateHelper.writeInstr("mov "+"%rax,"+ L )
                removeFromRegs(ir[i].dst['name'])
                AddrDesc[ir[i].dst['name']]['reg']=L
                regsInfo[L]=ir[i].dst['name']
                AddrDesc[ir[i].dst['name']]['dirty']=1

        elif ir[i].type in type_5:
            if(ir[i].src1['type']=='constant'):   #push registers
                generateHelper.writeInstr("push $"+ir[i].src1['name'])
            else:
                if(AddrDesc[ir[i].src1['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,None)
                    if type(AddrDesc[ir[i].src1['name']]['memory']) == dict:
                        array_gen(instrcution_number,nextuse,AddrDesc[ir[i].src1['name']],[L2],L2)
                    else:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['memory']+"(%rbp), "+L2)
                    AddrDesc[ir[i].src1['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src1['name']
                    AddrDesc[ir[i].src1['name']]['dirty']=0
                    generateHelper.writeInstr("push "+L2)
                else:
                    generateHelper.writeInstr("push "+AddrDesc[ir[i].src1['name']]['reg'])

        elif ir[i].type in type_7:
            generateHelper.writeInstr(ir[i].src1['name']+ ":")
        elif ir[i].type in type_8:
            if(ir[i].src1['name'] == "main1"):
                ir[i].src1['name']="main"
            generateHelper.writeInstr(ir[i].src1['name']+ ":")
            generateHelper.writeInstr("push %rbp")
            generateHelper.writeInstr("mov %rsp, %rbp")
            subt = int(ir[i].src2['name'])
            subt = subt*2
            generateHelper.writeInstr("sub $"+str(subt)+ ", %rsp")
            global func_offset
            func_offset=2*int(ir[i].src2['name'])
        elif ir[i].type in type_9:
                if(AddrDesc[ir[i].src1['name']]['reg']==None):
                    L2=getfreereg(i,infoTable,None)
                    generateHelper.writeInstr("mov %rax, "+L2)
                    AddrDesc[ir[i].src1['name']]['reg']=L2
                    regsInfo[L2]=ir[i].src1['name']
                    if(ir[i].src1['type']=="global" or  ir[i].src1['type']=="local"):
                        AddrDesc[ir[i].src1['name']]['dirty']=1
                else:
                    generateHelper.writeInstr("mov %rax, "+AddrDesc[ir[i].src1['name']]['reg'])
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

                    generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['memory']+", %rax")
                else:
                    generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['reg']+", %rax")

                saveDirtyAndClean() #clean everything except eax
                generateHelper.writeInstr("cmp %rax, $0")
                generateHelper.writeInstr("je "+ir[i].dst['name'])

            elif ir[i].type in type_10: #return
                if(ir[i].src1['type']=='constant'):
                    generateHelper.writeInstr("mov $"+ir[i].src1['name']+", %rax")
                else:
                    if(AddrDesc[ir[i].src1['name']]['reg']==None):
                        if type(AddrDesc[ir[i].src1['name']]['memory']) == dict:
                            array_gen(instrcution_number,nextuse,AddrDesc[ir[i].src1['name']],None,'rax')
                        else:
                            generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['memory']+", %rax")
                    else:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].src1['name']]['reg']+", %rax")
                saveDirtyAndClean() #clean everything except eax
                # generateHelper.writeInstr("mov %rbp, %rsp")
                # generateHelper.writeInstr("pop %rbp")
                generateHelper.writeInstr("leave")
                generateHelper.writeInstr("ret")

            elif ir[i].type in type_11: #printf assuming arg1 consist of format string global var name, arg2 consist of var,const to be printed
                # arg to be printed can also be a function
                if(ir[i].arg2['type']=='constant'):
                    generateHelper.writeInstr("mov "+ir[i].arg2['name']+", %rax")
                else:
                    if(AddrDesc[ir[i].arg2['name']]['reg']==None):
                        if type(AddrDesc[ir[i].arg2['name']]['memory']) == dict:
                            array_gen(instrcution_number,nextuse,AddrDesc[ir[i].arg2['name']],None,'rax')
                        else:
                            generateHelper.writeInstr("mov "+AddrDesc[ir[i].arg2['name']]['memory']+"(%rbp) ,%rax")
                    else:
                        generateHelper.writeInstr("mov "+AddrDesc[ir[i].arg2['name']]['reg']+", %rax")
                saveDirtyAndClean() #clean everything except eax
                generateHelper.writeInstr("mov $CS335_format, %rdi")  # this will be global variable format
                generateHelper.writeInstr("mov %rax, %rsi")
                generateHelper.writeInstr("mov $0, %rax")
                generateHelper.writeInstr("call printf")

            elif ir[i].type in type_12: #scanf
                if (ir[i].arg2['type'] == "local"):
                    saveDirtyAndClean() #clean everything except eax
                    generateHelper.writeInstr("mov $CS335_format, %rdi")  # this will be global variable format
                    if type(AddrDesc[ir[i].arg2['name']]['memory']) == dict:
                            array_gen(instrcution_number,nextuse,AddrDesc[ir[i].arg2['name']],None,'rsi')
                    else:
                        generateHelper.writeInstr("lea "+AddrDesc[ir[i].arg2['name']]['memory']+"(%rbp) , %rsi")
                    generateHelper.writeInstr("mov $0, %rax")
                    generateHelper.writeInstr("call scanf")
                else:
                    generateHelper.writeInstr("scanf should be not in local var!")
            else:
                saveDirtyAndClean()

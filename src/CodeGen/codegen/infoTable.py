from parameter import *


def createTable(x):
    start = x[0]
    end = x[1]
    tableToRet = {}

    for i in range(start, end + 1):
        tableToRet[i] = {}

    listOfSymbols = set([])
    for i in range(start, end + 1):
        if ir[i].type in type_3:  
            listOfSymbols.add(ir[i].dst.value)
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                listOfSymbols.add(ir[i].src1)
            if((ir[i].src2.type == "local") or (ir[i].src2.type == "temp") or (ir[i].src2.type == "global")): 
                listOfSymbols.add(ir[i].src2)

        elif ir[i].type in type_2:
            listOfSymbols.add(ir[i].dst.value)
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                listOfSymbols.add(ir[i].src1)
        
        elif((ir[i].type in type_5) or (ir[i].type in type_9) or (ir[i].type in type_6)):
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                listOfSymbols.add(ir[i].src1)
        
        

    for i in range(start, end + 1):
        for j in listOfSymbols:
            tableToRet[i][j] = {}
            tableToRet[i][j]["live"] = False
            tableToRet[i][j]["nextUse"] = None

    for i in range(end, start - 1, -1):

        #propogates live and nextUse
        if i != end:
            for k in tableToRet[i]:
                tableToRet[i][k] = tableToRet[i + 1][k].copy()

        if ir[i].type in type_3:

            (tableToRet[i])[ir[i].dst]["live"] = False
            (tableToRet[i])[ir[i].dst]["nextUse"] = None

            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                (tableToRet[i])[ir[i].src1]["live"] = True
                (tableToRet[i])[ir[i].src1]["nextUse"] = i

            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")):
                (tableToRet[i])[ir[i].src2]["live"] = True
                (tableToRet[i])[ir[i].src2]["nextUse"] = i

        elif ir[i].type in type_2:
            (tableToRet[i])[ir[i].dst]["live"] = False
            (tableToRet[i])[ir[i].dst]["nextUse"] = None
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                (tableToRet[i])[ir[i].src1]["live"] = True
                (tableToRet[i])[ir[i].src1]["nextUse"] = i

        elif ir[i].type in type_5:
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                (tableToRet[i])[ir[i].src1]["live"] = True
                (tableToRet[i])[ir[i].src1]["nextUse"] = i

        elif ir[i].type in type_9:
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                (tableToRet[i])[ir[i].src1]["live"] = False
                (tableToRet[i])[ir[i].src1]["nextUse"] = None
        
        elif ir[i].type in type_6: #if
            if((ir[i].src1.type == "local") or (ir[i].src1.type == "temp") or (ir[i].src1.type == "global")): 
                (tableToRet[i])[ir[i].src1]["live"] = True
                (tableToRet[i])[ir[i].src1]["nextUse"] = i
        

    for i in range(start, end):
        tableToRet[i] = tableToRet[i + 1]

    ## make all live and next Use none for last instruction
    for i in listOfSymbols:
        tableToRet[end][i]["live"] = False
        tableToRet[end][i]["nextUse"] = None

    return tableToRet
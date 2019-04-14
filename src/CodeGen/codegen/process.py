from parameter import *


# Creates IR table

def process_string(x):
    ind = x.find('~')
    name = []
    addr = []
    for i in range(0,ind):
        name.append(x[i])
    for i in range(ind + 1,len(x)):
        addr.append(x[i])
    return "".join(name),"".join(addr)

def find_type(addr):
    if(addr[0] == '-' and addr[1] == '1'):
        return 'global'
    else:
        if(addr[0] == '-' and addr[1] == '2'):
            return 'temp'
        else:
            return 'local'

class IR:
    def __init__(self, instr):
        print instr
        # type
        # src1  # name, type (local, global , temp, constant) , addr, array, array_offset
        # src2
        # dst
        length = len(instr)
        print length

        self.src1 = {}
        self.src2 = {}
        self.dst = {}

        if(instr[0] == 'EndFunc' or instr[0] == 'return' or instr[0] == 'call' or instr[0] == 'goto' or instr[0] == 'push' or instr[0] == 'pop'):
            if(length >= 2):
                self.src1['name'] = instr[1]
            self.type = instr[0]
        if(length <= 2):
            return

        if(instr[0] == 'func'):
            self.type = 'func'
            self.src1['name'] = instr[1]
            self.src2['name'] = instr[4]
            return

        if(instr[1] == ':'):
            self.type == 'label'
            self.src1['name'] = instr[0]
            return

        if((set(type_1) & set(instr)) and (set(['=']) & set(instr))):
            # type is type_1
            
        else:
            self.type = '='
            x = instr[0]
            if(x[0] in ['0','1','2','3','4','5','6','7','8','9']):
                print("Error : can't assign a constant value")
                exit(1)
            name,addr = process_string(x)
            self.dst['name'] = name
            self.dst['type'] = find_type(addr)
            self.dst['addr'] = addr
            if(instr[1] == '='):
                x = instr[2]
                if(not(x[0] in ['0','1','2','3','4','5','6','7','8','9'])):
                    name,addr = process_string(x)
                    self.src1['name'] = name
                    self.src1['type'] = find_type(addr)
                    self.src1['addr'] = addr
                else:
                    self.src1['name'] = x
                    self.src1['type'] = 'constant'
                name,addr = process_string(x)
                self.src1['name'] = name
                self.src1['type'] = find_type(addr)
                self.src1['addr'] = addr

                self.dst['array'] = 'False'

            if(instr[1] == '=' && length == 6):
                # surely src1 is array
                if(self.src1['name'][0] in ['0','1','2','3','4','5','6','7','8','9']):
                    print("Error : array name can't start with integer")
                    exit(1)
                self.src1['array'] = 'True'
                self.src1['array_offset'] = instr[4]
                return
            if(instr[1] == '='):
                self.src1['array'] = 'False'
                return
            # dst is array
            self.dst['array'] = 'True'
            self.dst['array_offset'] = instr[2]
            x = instr[5]
            if(not(x[0] in ['0','1','2','3','4','5','6','7','8','9'])):
                name,addr = process_string(x)
                self.src1['name'] = name
                self.src1['type'] = find_type(addr)
                self.src1['addr'] = addr
            else:
                self.src1['name'] = x
                self.src1['type'] = 'constant'

            if(length == 6):
                # src1 is not array
                self.src1['array'] = 'False'
                return
            else:
                if(self.src1['name'][0] in ['0','1','2','3','4','5','6','7','8','9']):
                    print("Error : array name can't start with integer")
                    exit(1)
                self.src1['array'] = 'True'
                self.src1['array_offset'] = instr[7]
                return

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
    if(addr[0] == '-' and addr[1] == '2'):
        return 'global'
    else:
        if(addr[0] == '-' and addr[1] == '1'):
            return 'temp'
        else:
            return 'local'

class IR:
    def __init__(self, instr):
        # print instr
        # type
        # src1  # name, type (local, global , temp, constant) , addr, array, array_offset
        # src2
        # dst
        length = len(instr)
        # print length

        self.src1 = {}
        self.src2 = {}
        self.dst = {}

        if(instr[0] == 'EndFunc' or instr[0] == 'return' or instr[0] == 'call' or instr[0] == 'goto' or instr[0] == 'push'):
            if(length >= 2):
                self.src1['name'] = instr[1]
            self.type = instr[0]

        if(length < 2):
            return

        if(instr[1] == ':'):
            self.type = 'label'
            self.src1['name'] = instr[0]
            return
        if(instr[0] == 'pop'):
            self.type = 'pop'
            x = instr[1]
            name,addr = process_string(x)
            self.src1['name'] = name
            self.src1['type'] = find_type(addr)
            return
            
        if(length <= 2):
            return

        if(instr[0] == 'func'):
            self.type = 'func'
            self.src1['name'] = instr[1]
            self.src2['name'] = instr[4]
            self.res_length = instr[5]
            return

        if(instr[0] == 'if'):
            self.type = 'if'
            x = instr[1]
            name,addr = process_string(x)
            self.src1['name'] = name
            self.src1['type'] = find_type(addr)
            self.src1['array'] = 'False'
            self.src1['addr'] = addr

            x = instr[5]
            name,addr = process_string(x)
            self.dst['name'] = name
            self.dst['type'] = find_type(addr)
            self.dst['array'] = 'False'
            self.dst['addr'] = addr

            return

        if(instr[0] == 'else'):
            self.type = 'else'
            x = instr[2]
            name,addr = process_string(x)
            self.src1['name'] = name
            self.src1['type'] = find_type(addr)
            self.src1['array'] = 'False'
            self.src1['addr'] = addr

            x = instr[6]
            name,addr = process_string(x)
            self.dst['name'] = name
            self.dst['type'] = find_type(addr)
            self.dst['array'] = 'False'
            self.dst['addr'] = addr

            return

        if((set(type_3) & set(instr)) and (set(['=']) & set(instr))):
            # type is type_1
            dest = 0
            src1 = 0
            src2 = 0
            da = 'False'
            s1a = 'False'
            s2a = 'False'
            if(instr[1] == '='):
                src1 = 2
                if(instr[3] == '['):
                    self.type = instr[6]
                    src2 = 7
                    s1a = 'True'
                else:
                    self.type = instr[3]
                    src2 = 4
            else:
                da = 'True'
                src1 = 5
                if(instr[6] == '['):
                    self.type = instr[9]
                    src2 = 10
                    s1a = 'True'
                else:
                    self.type = instr[6]
                    src2 = 7
            if(length > (src2 + 1)):
                s2a = 'True'
            x = instr[dest]
            name,addr = process_string(x)
            self.dst['name'] = name
            self.dst['type'] = find_type(addr)
            self.dst['addr'] = addr

            self.dst['array'] = da
            self.src1['array'] = s1a
            self.src2['array'] = s2a

            x = instr[src1]
            name,addr = process_string(x)
            self.src1['name'] = name
            self.src1['type'] = find_type(addr)
            self.src1['addr'] = addr

            x = instr[src2]
            name,addr = process_string(x)
            self.src2['name'] = name
            self.src2['type'] = find_type(addr)
            self.src2['addr'] = addr

            if(s1a == 'True'):
                self.src1['array_offset'] = instr[src1 + 2]
            if(s2a == 'True'):
                self.src2['array_offset'] = instr[src2 + 2]
            if(da == 'True'):
                self.dst['array_offset'] = instr[dest + 2]
            return
        else:
            if(not(set(['=']) & set(instr))):
                print "hi"
                return
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
                # print x
                name,addr = process_string(x)
                if(not(x[0] in ['0','1','2','3','4','5','6','7','8','9'])):
                    # self.src1['name'] = name
                    self.src1['type'] = find_type(addr)
                    self.src1['addr'] = addr
                else:
                    # self.src1['name'] = name
                    self.src1['type'] = 'constant'
                self.src1['name'] = name
                self.src1['type'] = find_type(addr)
                self.src1['addr'] = addr

                self.dst['array'] = 'False'

            if((instr[1] == '=') and (length == 6)):
                # surely src1 is array
                u = self.src1['name']
                # print u
                if(u[0] in ['0','1','2','3','4','5','6','7','8','9']):
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
            name,addr = process_string(x)
            if(not(x[0] in ['0','1','2','3','4','5','6','7','8','9'])):
                self.src1['name'] = name
                self.src1['type'] = find_type(addr)
                self.src1['addr'] = addr
            else:
                self.src1['name'] = name
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

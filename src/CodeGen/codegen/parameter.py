'''
a=b+c type 3
a+=c type 2
call foo type 1
goto label type 4
push a type 5
if E=0 goto label  type 6
label: type 7
label: begin func type 8
pop a type 9
ret type 10
'''



ir=[]
global_symbol_table ={}
# Corresponds to 3 operand instructions
# x is multiply and * is dereference
type_3 = ['+', '-', '*', '/', '%', '&', '|', '^', '<<', '>>', '==', '<', '>', '!=', '<=', '>=']

# Corresponds to 2 address instructions
type_2 = ['=', '+=', '-=', '*=', '&=','|=', '^=', '<<=', '>>=']

type_1= ['call']
type_4=['goto']
type_5=['push']
type_6=['if']
type_7=['label']
type_8=['func']
type_9=['pop']
type_10=['ret']

regsList=['rax','rbx','rcx','rdx','rsi','r8','r9','r10','r11','r12','r13','r14','r15']
regsInfo={'rax': None, 'rbx': None, 'rcx': None, 'rdx': None, 'rsi': None, 'rdi': None,'r8':None,'r9':None,'r10':None,'r11':None,'r12':None,'r13':None,'r14':None,'r15':None}
AddrDesc={}

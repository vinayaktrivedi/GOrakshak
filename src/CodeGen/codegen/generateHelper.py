from parameter import *

fil=open('x86.S','w+')

def genGlobals():
    writeInstr("section	.text")
    writeInstr("global _start")
    # writeInstr("section	.data")
    # for key, var in global_symbol_table.items():
    #     if(key=="CS335_childtables" or key=="CS335_show_label" or key=="CS335_update_label" or key=="CS335_loop_label" or key=="CS335_exit_label" or key=="CS335_name" or key=="CS335_type" or key=="local_variable_size" or key=="CS335_parent" or key=="CS335_args" or key=="CS335_response"):
    #         continue

def writeInstr(instr):
    fil.write(instr+"\n")

def close():
    pass
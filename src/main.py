import sys
import csv
import re

import ply.lex as lex
import mylexer
from mylexer import *

with open('../tests/cfg1', mode='r') as infile:
    reader = csv.reader(infile)
    col_spec = {rows[0]:rows[1] for rows in reader}

outfile = open("output.html","w")
outfile.write("<html>\n<title>Generated HTML</title>\n<body>\n")

if (len(sys.argv) == 1):
    file_name =raw_input( "Give a GO file to lexer: ")
else:
    file_name = sys.argv[1]

mapping = {}

try:
    lexer = lex.lex()
    with open(file_name) as f:
        code = f.read()
        code += '\n'
        lexer.input(code)
        for tok in lexer:
            mapping[tok.value] = tok.type
            if tok.type in col_spec:
            	outfile.write("<font color = \"")
            	outfile.write(col_spec[tok.type])
            	outfile.write("\">")
            	outfile.write(str(tok.value))
            	outfile.write("</font>")
            	outfile.write(" ")
            else:
        		outfile.write(str(tok.value))
        		outfile.write(" ")
        outfile.write("<br>")
	outfile.write("</body>\n</html>")

except IOError as e:
    print "I/O error({0}): "+ "Uable to open " + file_name + " . Does the file exist? Check permissions!"

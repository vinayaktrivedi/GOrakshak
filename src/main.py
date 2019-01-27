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
    file =raw_input( "Give a GO file to lexer: ")
else:
    file = sys.argv[1]

mapping = {}
tabs = []


with open(file) as f:
    for line in f:
    	# assuming tabs are given for indentation not spaces
    	tabs.append(len(line) - len(line.lstrip()))

i = 0
lexer = lex.lex()
with open(file) as f:
    code = f.read()
    code += '\n'
    lexer.input(code)
for tok in lexer:
	print tabs[tok.lineno-1]
	if tok.lineno >= (i+1):
		if tok.lineno != 1:
			outfile.write("<br>")
		for k in range(0,tabs[tok.lineno-1]):
			# assuming 4 &nbsp = 1 Tab
			for j in range(0,4):
				outfile.write("&nbsp")
		i = tok.lineno

	mapping[tok.value] = tok.type
	if tok.type in col_spec:
		outfile.write("<font color = \"")
		outfile.write(col_spec[tok.type])
		outfile.write("\">")
		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write(str(tok.value))
		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write("</font>")
		outfile.write(" ")
	else:
		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write(str(tok.value))
		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write(" ")

outfile.write("</body>\n</html>")
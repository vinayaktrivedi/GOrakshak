import sys
import csv
import re
import argparse
import ply.lex as lex
import regex
from regex import *


ap = argparse.ArgumentParser()                                                                                                                                           
ap.add_argument("-c", "--cfg",help="configuration")
ap.add_argument("-i", "--input",help="name of GO input file")
ap.add_argument("-o", "--output",help="name of output file")
args = vars(ap.parse_args())

if args["input"] is None:
    args["input"] = "../../tests/lexer/input/test1.go"

if args["cfg"] is None:
    args["cfg"] = "../../tests/lexer/cfg/cfg1"

if args["output"] is None:
    args["output"] = "../../tests/lexer/output/output1.html"

file = args["input"]
cfgfile = args["cfg"]

with open(cfgfile, mode='r') as infile:
    reader = csv.reader(infile)
    col_spec = {rows[0]:rows[1] for rows in reader}

outfile = open(args["output"],"w")
outfile.write("<html>\n<title>Generated HTML</title>\n<body>\n")

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

num = 0

for tok in lexer:
	flag = 0
	if tok.lineno >= (i+1):
		flag = 1
		if tok.lineno != 1:
			for co in range(0,tok.lineno-i):
				outfile.write("<br>")
				num = num + 1

		for tab in range(0,tabs[tok.lineno-1]):
			# assuming 4 &nbsp = 1 Tab
			outfile.write("&nbsp")
		num = num + tabs[tok.lineno-1]
		i = tok.lineno

	if flag == 1:
		num = tok.lexpos
	for x in range(0,(tok.lexpos - num)):
		if tok.type != "STRING":
			outfile.write("&nbsp")
		else:
			if x != 0:
				outfile.write("&nbsp")
		num = tok.lexpos

	if tok.type in col_spec:
		outfile.write("<font color = \"")
		outfile.write(col_spec[tok.type])
		outfile.write("\">")

		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write(str(tok.value))
		num = num + len(str(tok.value))

		if tok.type == "STRING":
			outfile.write("\"")
			num = num + 2
		outfile.write("</font>")
	else:
		if tok.type == "STRING":
			outfile.write("\"")
		outfile.write(str(tok.value))
		num = num + len(str(tok.value))
		if tok.type == "STRING":
			outfile.write("\"")
			num = num + 2

outfile.write("</body>\n</html>")

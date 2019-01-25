import sys
import csv

with open('../tests/cfg1', mode='r') as infile:
    reader = csv.reader(infile)
    col_spec = {rows[0]:rows[1] for rows in reader}

outfile = open("output.html","w")
outfile.write("<html>\n<title>Generated HTML</title>\n<body>\n")

with open('../tests/inp1','r') as f:
    for line in f:
        for word in line.split():
        	if word in col_spec:
        		outfile.write("<font color = \"")
        		outfile.write(col_spec[word])
        		outfile.write("\">")
        		outfile.write(word)
        		outfile.write("</font>")
        		outfile.write(" ")
        	else:
        		outfile.write(word)
        		outfile.write(" ")
        outfile.write("<br>")
outfile.write("</body>\n</html>")
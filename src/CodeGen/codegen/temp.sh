#!/bin/bash
cd ..
bash temp.sh
cd codegen
python2 main.py ../code.txt
# cat code.txt > "code$i.txt"
# cat symbol_table.csv > "symbol_table$i.csv"
# cat x86.S > "x86.S"
# echo $i

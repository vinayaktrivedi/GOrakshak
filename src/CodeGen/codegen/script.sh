#!/bin/bash
cd ..
./script.sh
cd codegen
for i in {1..26}
do
	python main.py ../code$i.txt
	# cat code.txt > "code$i.txt"
	# cat symbol_table.csv > "symbol_table$i.csv"
	cat x86.S > "x86$i.S"
	echo $i
done

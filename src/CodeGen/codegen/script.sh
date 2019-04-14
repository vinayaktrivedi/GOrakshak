#!/bin/bash
for i in {1..26}
do
	python main.py ../code$i.txt
	# cat code.txt > "code$i.txt"
	# cat symbol_table.csv > "symbol_table$i.csv"
	echo $i
done

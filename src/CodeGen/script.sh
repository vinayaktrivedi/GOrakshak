#!/bin/bash
for i in {1..20}
do
	python parser.py --input="../../tests/Final/test$i.go"
	cat code.txt > "code$i.txt"
	cat symbol_table.csv > "symbol_table$i.csv"
	echo $i
done

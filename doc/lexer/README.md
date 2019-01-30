# GOrakshak
Compiler for Golang implemented in Python

It contains the source code for Lexer of Golang, source code being in src.

The command to run the lexer is -

cd src
cd lexer
python lexer.py [OPTIONS]

OPTIONS include -
--input=location of input Go file. (e.g. test1.go)
--cfg=location of cfg file for html output
--output=location of html file to be saved.

Example-
python lexer.py --input=./my_input.go --cfg=./my_cfg --output=./my_output.html

If not given the values of options, default values of options are-
--input=../../tests/lexer/input/test1.go
--cfg=../../tests/lexer/cfg/cfg1
--output=../../tests/lexer/output1.html



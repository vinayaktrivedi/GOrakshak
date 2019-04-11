import sys
import csv
import re
import argparse
import ply.lex as lex
from tokens import *
from regex import *


keywords = reserved
lexer=lex.lex()

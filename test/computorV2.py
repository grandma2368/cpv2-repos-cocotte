# -*- coding: utf-8 -*-
import sys
import re
from resolve import parsing, print_var
from equation_parser import add_multiplication


while 1:
    input = raw_input('> ')
    input = re.sub(r'[ \t]', '', input).lower()
    input = add_multiplication(input)
    if input == 'quit' or input == 'q' or input == 'exit':
        sys.exit()
    if input == 'vars':
        print_var()
    else:
        try:
            parsing(input)

        except:
            pass

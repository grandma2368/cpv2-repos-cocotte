import sys
import re
import parsing
import utils

data = {"rationel": {}, "complexe": {}, "matrices": {}, "function": {}}

while 1:
    input = raw_input('> ')
    input = re.sub(r'[ \t]', '', input).lower()
    input = utils.add_multiplication(input)

    if input == 'quit' or input == 'q' or input == 'exit':
        sys.exit()
    if input == 'data':
        print("afficher les variables") #A IMPLEMENTER
        # print_var()
    else:
        try:
            parsing.parsing(input, data)
        except:
            pass
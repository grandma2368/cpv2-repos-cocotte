import sys
import re
import parsing
import utils

#affiche toutes les variables dans data
def print_vrb(data):
    for vrb in data["rationel"]:
        print vrb + " :"
        print data["rationel"][vrb]
    for vrb in data["complexe"]:
        print vrb + " :"
        print data["complexe"][vrb]
    for vrb in data["matrices"]:
        print vrb + " :"
        print data["matrices"][vrb]
    for vrb in data["function"]:
        func = data["function"][vrb]
        print vrb + "(" + func.vrb + ") = " + func.func

#contient toutes les variables de la session ouverte
data = {"rationel": {}, "complexe": {}, "matrices": {}, "function": {}}

while 1:
    input = raw_input('> ')
    input = re.sub(r'[ \t]', '', input).lower()
    input = utils.add_multiplication(input)

    if input == 'quit' or input == 'q' or input == 'exit':
        sys.exit()
    if input == 'data':
        print_vrb(data)
    else:
        try:
            parsing.parsing(input, data)
        except:
            pass
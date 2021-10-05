import sys
import re

while 1:
    input = raw_input('> ')
    input = re.sub(r'[ \t]', '', input).lower()

    # input = add_multiplication(input)

    if input == 'quit' or input == 'q' or input == 'exit':
        sys.exit()
    if input == 'data':
        print("afficher les variables") #A IMPLEMENTER
        # print_var()
    else:
        try:
            print("parsing") #A IMPLEMETER
            #parsing(input)

        except:
            pass

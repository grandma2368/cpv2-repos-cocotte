import re
import utils

#calcule l'expression mathematique
def npi_solver(input):
    index = 0
    if len(input) == 1:
        input[0] = types(input[0])
    while len(input) > 1:
        if isinstance(input[index], basestring) and re.match(r'^\*\*|[\-+/^%=*]$', input[index]):
            res = calc(input[index-2], input[index-1], input[index])
            input[index] = res
            input.pop(index - 1)
            input.pop(index - 2)
            index = 0
        index += 1
    return input[0]

#definit si un calcul est prioritaire ou non
def greater_precedence(operator1, operator2):
    if operator2 == '(':
        return False
    elif operator1 == '^':
        if operator2 == '^':
            return True
        else:
            return False
    elif operator1 == '*' or operator1 == '/' or operator1 == '%' or operator1 == '**':
        if operator2 == '+' or operator2 == '-':
            return False
        else:
            return True
    elif operator1 == '-' or operator1 == '+':
            return True

#tri les calculs prioritaires
def sortOut(tokens):
    operator = []
    output = []
    index = 0
    while index < len(tokens):
        if 4 > tokens[index][0] > 0:
            output.append(tokens[index][1])
        elif tokens[index][0] == 0:
            op_index = len(operator)-1
            while len(operator) and greater_precedence(tokens[index][1], operator[op_index]):
                output.append(operator.pop())
                op_index -= 1
            operator.append(tokens[index][1])
        elif tokens[index][0] == 4:
            operator.append('(')
        elif tokens[index][0] == 5:
            op_index = len(operator) - 1
            while len(operator) and operator[op_index] != '(':
                output.append(operator.pop())
                op_index -= 1
            if not len(operator):
                print("\033[91mERREUR: Les parentheses sont mal agencees.\033[0m")
                raise Exception
            else:
                operator.pop()
        index += 1
    while len(operator):
        if operator[-1] == '(':
            print("\033[91mERREUR: Les parentheses sont mal agencees.\033[0m")
            raise Exception
        output.append(operator.pop())
    return output

#resoud une portion d'expression mathematique
def resolve(input):
    if input.endswith("=?"):
        exp = utils.to_tab(input[:-2])
        sorted = sortOut(exp)
        return npi_solver(sorted)
    elif re.match(r'^[a-z]+=', input):
        input = re.sub(r'^[a-z]+=', '', input)
        exp = utils.to_tab(input)
        sorted = sortOut(exp)
        return npi_solver(sorted)
    else:
        print("\033[91mERREUR: Ceci n'est pas une expression mathematique.\033[0m")
        raise Exception
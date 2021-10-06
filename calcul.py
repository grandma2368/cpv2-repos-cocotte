import re
import utils
import type

#reduit l'expression
def reduction(equat):
    if equat.count('=') == 0:
        tab = utils.to_tab(equat)
        sorted = sortOut(tab)
        inp = npi(sorted)
        return inp.to_str()
    else:
        first_part = equat.split('=')[0]
        second_part = equat.split('=')[1]
        tab = utils.to_tab(first_part)
        sorted = sortOut(tab)
        inp = npi(sorted)
        tab2 = utils.to_tab(second_part)
        sorted2 = sortOut(tab2)
        inp2 = npi(sorted2)
        inp_str = inp.to_str() if not isinstance(inp, type.Rationels) else inp.to_str()
        inp2_str = inp2.to_str() if not isinstance(inp2, type.Rationels) else inp2.to_str()
        return inp_str + '=' + inp2_str

#calcul l'image d'une fonction
def resolve_func(func, data):
    fncRgx = re.compile('^([a-z]+)\((.+)\)')
    match = re.match(fncRgx, func)
    if match is not None:
        name = match.group(1)
        calc = match.group(2)
        res = resolve(calc + '=?')
        function = data["function"][name]
        calcul = function.func.replace(function.var, '(' + res.to_str() + ')').replace(' ', '')
        return resolve(calcul + '=?')
    else:
        print("\033[91mERREUR: La fonction n'est pas conforme.\033[0m")
        raise Exception

#calcul matriciel
def calc_mult_matrice(matrice1, matrice2, lign, col, nbr_lign):
    x = 0
    res = type.Rationels(0)
    while x < nbr_lign:
        res = res.add(matrice1[lign][x].mult(matrice2[x][col]))
        x += 1
    return res

#gere les calculs a effectuer selon les symboles
def calc(nbr1, nbr2, operator):
    nbr1 = utils.types(nbr1)
    nbr2 = utils.types(nbr2)
    if operator == '+':
        return nbr1.add(nbr2)
    elif operator == '-':
        return nbr1.sous(nbr2)
    elif operator == '*':
        return nbr1.mult(nbr2)
    elif operator == '/':
        return nbr1.div(nbr2)
    elif operator == '%':
        return nbr1.mod(nbr2)
    elif operator == '^':
        return nbr1.pow(nbr2)
    elif operator == '**':
        return nbr1.m_mult(nbr2)

#calcule l'expression mathematique
def npi(input):
    index = 0
    if len(input) == 1:
        return utils.types(input[0])
    while len(input) > 1:
        if isinstance(input[index], basestring) and re.match(r'^\*\*|[\-+/^%=*]$', input[index]):
            res = calc(input[index-2], input[index-1], input[index])
            input[index] = res
            input.pop(index - 1)
            input.pop(index - 2)
            index = 0
        index += 1
    return input[0]

#calcule l'expression mathematique
def npi_solver(input, data):
    index = 0
    if len(input) == 1:
        input[0] = utils.types(input[0], data)
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
def resolve(input, data):
    if input.endswith("=?"):
        exp = utils.to_tab(input[:-2])
        sorted = sortOut(exp)
        return npi_solver(sorted, data)
    elif re.match(r'^[a-z]+=', input):
        input = re.sub(r'^[a-z]+=', '', input)
        exp = utils.to_tab(input)
        sorted = sortOut(exp)
        return npi_solver(sorted, data)
    else:
        print("\033[91mERREUR: Ceci n'est pas une expression mathematique.\033[0m")
        raise Exception
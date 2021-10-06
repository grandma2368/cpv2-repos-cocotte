import re
import utils
import type
import parsing

#reduit l'expression
def reduction(equat, data):
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
def calc(nbr1, nbr2, operator, data):
    nbr1 = typesSolver(nbr1, data)
    nbr2 = typesSolver(nbr2, data)
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

def calcEqua(nbr1, nbr2, operator):
    nbr1 = types(nbr1)
    nbr2 = types(nbr2)
    if operator == '+':
        if isinstance(nbr2, type.Inconnue):
            return nbr2.add(nbr1)
        return nbr1.add(nbr2)
    elif operator == '-':
        if isinstance(nbr2, type.Inconnue):
            return nbr2.sous(nbr1, 1)
        return nbr1.sous(nbr2)
    elif operator == '*':
        if isinstance(nbr2, type.Inconnue):
            return nbr2.mult(nbr1)
        return nbr1.mult(nbr2)
    elif operator == '/':
        if isinstance(nbr2, type.Inconnue):
            nbr2.div(nbr1, 1)
        return nbr1.div(nbr2)
    elif operator == '%':
        if isinstance(nbr2, type.Inconnue):
            nbr2.mod(nbr1)
        return nbr1.mod(nbr2)
    elif operator == '^':
        if isinstance(nbr2, type.Inconnue):
            nbr2.pow(nbr1, 1)
        return nbr1.pow(nbr2)
    elif operator == '**':
        print("\033[91mError: Can't have ** operator\033[0m")
        raise Exception

#cherche les types pour les equations
def types(nbr):
    nbr_regex = re.compile('^-?[0-9]+(\.[0-9]+)?')
    if isinstance(nbr, type.Rationels) or isinstance(nbr, type.Inconnue):
        return nbr
    if nbr == 'x':
        nbr = type.Inconnue(1, 1)
    elif re.match(nbr_regex, nbr):
        nbr = type.Rationels(float(nbr))
    else:
        print("\033[91mERREUR: Ne reconnait pas la variable.\033[0m")
        raise Exception

    return nbr

#calcule l'expression mathematique
def npi(input):
    index = 0
    if len(input) == 1:
        return types(input[0])
    while len(input) > 1:
        if isinstance(input[index], basestring) and re.match(r'^\*\*|[\-+/^%=*]$', input[index]):
            res = calcEqua(input[index-2], input[index-1], input[index])
            input[index] = res
            input.pop(index - 1)
            input.pop(index - 2)
            index = 0
        index += 1
    return input[0]

#types specifique pour npi_solver
def typesSolver(nbr, data):
    function_regex = re.compile('^[a-z]+\((.+)\)')
    nbr_regex = re.compile('^-?[0-9]+(\.[0-9]+)?')
    matrice_regex = "^\[\[[^],]+(,[^],]+)*\](;\[[^],]+(,[^],]+)*\])*\]"
    if isinstance(nbr, type.Rationels) or isinstance(nbr, type.Complex) or isinstance(nbr, type.Matrice):
        return nbr
    if nbr == 'i':
        nbr = type.Complex(0, 1)
    elif re.match(function_regex, nbr):
        nbr = resolve_func(nbr)
    elif nbr.isalpha():
        nbr = utils.recup_var(nbr)
    elif re.match(nbr_regex, nbr):
        nbr = type.Rationels(float(nbr))
    elif re.match(matrice_regex, nbr):
        nbr = parsing.parse_matrice(nbr, data)
    else:
        print("\033[91mERREUR: Element non reconnu en '" + nbr + "'.\033[0m")
        raise Exception
    return nbr

#calcule l'expression mathematique
def npi_solver(input, data):
    index = 0
    if len(input) == 1:
        input[0] = typesSolver(input[0], data)
    while len(input) > 1:
        if isinstance(input[index], basestring) and re.match(r'^\*\*|[\-+/^%=*]$', input[index]):
            res = calc(input[index-2], input[index-1], input[index], data)
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
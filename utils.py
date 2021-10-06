import parsing
import re
import type
import calcul

#explicite la puissance 1
def add_pow(equat):
    index = 0
    while index < len(equat):
        if equat[index] == 'x':
            if index < len(equat) - 1 and equat[index+1] != "^":
                equat = equat[:index+1] + "^1" + equat[index+1:]
            elif index >= len(equat) - 1:
                equat += "^1"
        if equat[index].isdigit():
            if index -1 < 0 or equat[index-1] != '^':
                while index < len(equat) and (equat[index].isdigit() or equat[index] == "."):
                    index += 1
                if index == len(equat) or equat[index] != "*":
                    equat = equat[:index] + "*x^0" + equat[index:]
        index += 1
    return equat

#checke les parentheses
def parenthesis(equat):
    index = 0
    parenthese = -1
    parentheses_start = 0
    while index < len(equat):
        if equat[index] == ')':
            if parenthese == -1:
                print("\033[91mERREUR: Parenthses non conformes.\033[0m")
                raise Exception
            else:
                parenthese -= 1
                if parenthese == 0:
                    parenthese = -1
                    res = parenthesis(equat[parentheses_start + 1:index])
                    equat = equat.replace(equat[parentheses_start:index+1], res)
                    index = 0
        if equat[index] == '(':
            if parenthese == -1:
                parentheses_start = index
                parenthese = 1
            else:
                parenthese += 1
        index += 1
    return calcul.reduction(equat)

#explicite le 1 des +x et -x
def add_one_before_x(equat):
    expr = ""
    if equat.startswith('x'):
        expr = '1'+equat
    else:
        expr = equat
    return expr.replace('-x', '-1x').replace('+x', '+1x')

#remplace les variables par rapport a data
def replace_var(equat, variables):
    cpxRgx = "[^a-z]i[^a-z]|^i[^a-z]|[^a-z]i$"
    if re.match(cpxRgx, equat):
        print("\033[91mError: Can't have complex in equation\033[0m")
        raise Exception
    index = 0
    while index < len(equat):
        if equat[index].isalpha():
            if parsing.extract_function(equat[index:]):
                func_regex = re.compile('^([a-z]+)\((.+)\)')
                match = re.match(func_regex, equat[index:])
                if match is not None:
                    name = match.group(1)
                    calc = '(' + match.group(2) + ')'

                    function = variables["function"][name]
                    equat = equat.replace(match.group(0), function.func.replace(function.var, calc))
                index = 0
            else:
                var = parsing.extract_var(equat[index:])
                if var != 'x':
                    nbr = ""
                    if var in variables["rationel"]:
                        nbr = variables["rationel"][var]
                        nbr = str(nbr.nbr)
                    elif var in variables["complexe"]:
                        print("\033[91mERREUR: Ne peut resoudre une equation avec un complexe.\033[0m")
                        raise Exception
                    elif var in variables["matrices"]:
                        print("\033[91mERREUR: Ne peut resoudre une equation du second degree avec une matrice.\033[0m")
                        raise Exception
                    else:
                        print("\033[91mERREUR: Variable %s non definie.\033[0m" % var)
                        raise Exception
                    equat = equat.replace(var, nbr).replace(' ', '')
                    index = 0
        index += 1
    return equat

#cherche les variables dans data
def recup_var(var, data):
    if var in data["rationel"]:
        return data["rationel"][var]
    elif var in data["complexe"]:
        return data["complexe"][var]
    elif var in data["matrices"]:
        return data["matrices"][var]
    else:
        print("\033[91mERREUR: Variable '" + var + "' non definie.\033[0m")
        raise Exception

#cherche le type du nombre et resoud le caclul en fonction
def types(nbr, data):
    fncRgx = re.compile('^[a-z]+\((.+)\)')
    nbrRgx = re.compile('^-?[0-9]+(\.[0-9]+)?')
    matrice_regex = "^\[\[[^],]+(,[^],]+)*\](;\[[^],]+(,[^],]+)*\])*\]"
    if isinstance(nbr, type.Rationels) or isinstance(nbr, type.Complex) or isinstance(nbr, type.Matrice):
        return nbr
    if nbr == 'i':
        nbr = type.Complex(0, 1)
    elif re.match(fncRgx, nbr):
        nbr = calcul.resolve_func(nbr, data)
    elif nbr.isalpha():
        nbr = recup_var(nbr, data)
    elif re.match(nbrRgx, nbr):
        nbr = type.Rationels(float(nbr))
    elif re.match(matrice_regex, nbr):
        nbr = parsing.parse_matrice(nbr)
    else:
        print("\033[91mERREUR: Type de '" + nbr + "' non reconnu.\033[0m")
        raise Exception
    return nbr

#explicite les multiplications de variable telles que "3x"
def add_multiplication(input):
    index = 0
    number = False
    while index < len(input):
        if input[index].isalpha() and number:
            input = input[:index] + '*' + input[index:]
        if input[index].isdigit():
            number = True
        else:
            number = False
        index += 1
    return input

#passe les info sous forme de tableau
def to_tab(input):
    nbr = True
    index = 0 #gestion des erreurs un nbr puis un signe etc
    exp = []
    while index < len(input):
        if nbr:
            if parsing.extract_function(input[index:]):
                tmp = parsing.extract_function(input[index:])
                exp.append([3, tmp])
                index += len(tmp)
                nbr = False
            elif parsing.extract_var(input[index:]):
                tmp = parsing.extract_var(input[index:])
                exp.append([2, tmp])
                index += len(tmp)
                nbr = False
            elif parsing.extract_matrice(input[index:]):
                tmp = parsing.extract_matrice(input[index:])
                exp.append([2, tmp])
                index += len(tmp)
                nbr = False
            elif parsing.extract_nbr(input[index:]):
                tmp = parsing.extract_nbr(input[index:])
                exp.append([1, tmp])
                index += len(tmp)
                nbr = False
            elif input[index] == '(':
                exp.append([4, '('])
                index += 1
            else:
                print("\033[91mERREUR: Mauvais symbole proche de %s\033[0m" % input[index-3 if index-3 >= 0 else 0:index+2])
                raise Exception
        else:
            match = re.match(r'^\*\*|^[\-+/^%=*]', input[index:])
            if match is not None:
                exp.append([0, match.group(0)])
                index += len(match.group(0))
                nbr = True
            elif input[index] == ')':
                exp.append([5, ')'])
                index += 1
            elif input[index] == 'i':
                exp.append([0, '*'])
                exp.append([2, 'i'])
                index += 1
                nbr = False
            else:
                print("\033[91mERREUR: Mauvais symbole proche de %s\033[0m" % input[index-3 if index-3 >= 0 else 0:index+2])
                raise Exception
    return exp
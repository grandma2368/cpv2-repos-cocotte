import parsing
import re
import type
import calcul

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
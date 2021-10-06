import re
import assignation
import type
import calcul
import utils
import equation

#parse une equation
def parse_equat(equat, data):
    r = utils.replace_var(equat, data)
    simpler = utils.add_multiplication(utils.add_one_before_x(r))
    res = utils.parenthesis(simpler, data)
    resBis = utils.add_pow(res)
    equation.resolve(resBis)

#parse une matrice
def parse_matrice(matrice_str, data):
    lign = matrice_str.count(';') + 1
    column = matrice_str.split(']')[0].count(',') + 1
    matrice = []
    index = 1
    lign_count = 0
    column_count = 0
    while index < len(matrice_str) - 1:
        if matrice_str[index] == '[':
            lign_count += 1
            matrice.append([])
            index += 1
        elif matrice_str[index] == ']':
            if column_count + 1 != column:
                print("\033[91mERREUR: Matrice non conforme.\033[0m")
                raise Exception
            column_count = 0
            index += 1
        elif matrice_str[index] == ',':
            column_count += 1
            index += 1
        elif matrice_str[index] == ';':
            index += 1
        else:
            i = matrice_str.find(',', index)
            y = matrice_str.find(']', index)
            if y < i or i == -1:
                i = y
            if i >= 0:
                nbr = calcul.resolve(matrice_str[index:i] + "=?", data)
                matrice[lign_count - 1].append(nbr)
                index += i - index
            else:
                print("\033[91mERREUR: Matrice non conforme.\033[0m")
                raise Exception
    if lign_count != lign:
        print("\033[91mERREUR: Matrice non conforme.\033[0m")
        raise Exception
    return type.Matrice(matrice, lign, column)

#retourne une matrice s'il y en a une
def extract_matrice(input):
    rgx = "^\[\[[^],]+(,[^],]+)*\](;\[[^],]+(,[^],]+)*\])*\]"
    match = re.search(rgx, input)
    if match is not None:
        return match.group(0)
    else:
        return None

#retourne un nombre s'il y en a un
def extract_nbr(input):
    rgx = "^\-?[0-9]+(\.[0-9]+)?"
    match = re.search(rgx, input)
    if match is not None:
        return match.group(0)
    else:
        return None

#retourne le nom de la variable s'il est valide
def extract_var(input):
    rgx = "^[a-z]+"
    match = re.search(rgx, input)
    if match is not None:
        return match.group(0)
    else:
        return None

#verifie le nom de la fonction et le renvoie
def extract_function(input):
    rgx = "^[a-z]+\((.+)\)"
    if not re.match(rgx, input):
        return None
    index = input.find('(')
    bracket_count = 0
    while index < len(input):
        if input[index] == '(':
            bracket_count += 1
        elif input[index] == ')':
            bracket_count -= 1
        if bracket_count == 0:
            break
        index += 1
    if bracket_count != 0:
        print("\033[91mERREUR: Les parentheses sont mal agencees.\033[0m")
        raise Exception
    return input[:index + 1]

#parse l'input et verifie s'il s'agit d'une assignation de fonction, de variable ou d'une equation a resoudre
def parse(input):
    #regexp pour chercher des fonctions
    fncRe = re.compile('^([a-z]+)\((.+)\)=')
    tpeInfo = {'assign': False, 'assign_func': False, 'resolve_equat': False}
    if not input:
        print('\033[91mERREUR: La ligne est vide.\033[0m')
        raise Exception
    if input.count("=") == 0:
        print("\033[91mERREUR: Il n'y a pas de '='.\033[0m")
        raise Exception
    if not input.endswith('?'):
        tpeInfo['assign'] = True
        match = re.match(fncRe, input)
        #assigne une fonction
        if match is not None:
            tmp = extract_function(input)
            tpeInfo['assign_func'] = match.group(1)
            tpeInfo['var'] = match.group(2)
            if input[len(tmp)] != "=":
                print("\033[91mERREUR: Nom de la fonction non conforme.\033[0m")
                raise Exception
        #assigne une variable
        elif input[0].isalpha():
            tmp = extract_var(input)
            if tmp == 'i':
                print("\033[91mError: Can't assign \"i\"\033[0m")
                raise Exception
            tpeInfo['assign'] = tmp
            if len(input) == len(tmp) or input[len(tmp)] != "=":
                print("\033[91mERREUR: Nom de la variable non conforme.\033[0m")
                raise Exception
        else:
            print("\033[91mERREUR: Il n'y a pas de variable a assigner.\033[0m")
            raise Exception
    elif not input.endswith('=?'):
        tpeInfo['resolve_equat'] = True
    if input.count("=") > 1:
        print("\033[91mERREUR: Il ne faut qu'un seul '=' dans l'entree.\033[0m")
        raise Exception
    return tpeInfo

#lance le parsing et recupere le type de recherche a faire
def parsing(input, data):
    tpe = parse(input)
    if tpe['assign_func']:
        assignation.assign_func(input, tpe, data)
    elif tpe['assign']:
        assignation.assign_resolve(input, tpe, data)
    elif tpe['resolve_equat']:
        parse_equat(input[:-1], data)
    else:
        res = calcul.resolve(input, data)
        print(res)
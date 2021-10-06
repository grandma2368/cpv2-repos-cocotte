import re
import sys
from type import Rationels, Function, Inconnue
from parse import extract_var, extract_function, to_tab
from equation_solver.computor import resolve


def types(nbr):
    nbr_regex = re.compile('^-?[0-9]+(\.[0-9]+)?')
    if isinstance(nbr, Rationels) or isinstance(nbr, Inconnue):
        return nbr
    if nbr == 'x':
        nbr = Inconnue(1, 1)
    elif re.match(nbr_regex, nbr):
        nbr = Rationels(float(nbr))
    else:
        print "\033[91mError: Can't recognise token\033[0m"
        raise Exception

    return nbr


def calc(nbr1, nbr2, operator):
    nbr1 = types(nbr1)
    nbr2 = types(nbr2)
    if operator == '+':
        if isinstance(nbr2, Inconnue):
            return nbr2.add(nbr1)
        return nbr1.add(nbr2)
    elif operator == '-':
        if isinstance(nbr2, Inconnue):
            return nbr2.sous(nbr1, 1)
        return nbr1.sous(nbr2)
    elif operator == '*':
        if isinstance(nbr2, Inconnue):
            return nbr2.mult(nbr1)
        return nbr1.mult(nbr2)
    elif operator == '/':
        if isinstance(nbr2, Inconnue):
            nbr2.div(nbr1, 1)
        return nbr1.div(nbr2)
    elif operator == '%':
        if isinstance(nbr2, Inconnue):
            nbr2.mod(nbr1)
        return nbr1.mod(nbr2)
    elif operator == '^':
        if isinstance(nbr2, Inconnue):
            nbr2.pow(nbr1, 1)
        return nbr1.pow(nbr2)
    elif operator == '**':
        print("\033[91mError: Can't have ** operator\033[0m")
        raise Exception


def npi(input):
    index = 0
    if len(input) == 1:
        return types(input[0])
    while len(input) > 1:
        if isinstance(input[index], basestring) and re.match(r'^\*\*|[\-+/^%=*]$', input[index]):
            res = calc(input[index-2], input[index-1], input[index])
            input[index] = res
            input.pop(index - 1)
            input.pop(index - 2)
            index = 0
        index += 1
    return input[0]


def reduction(equat):
    from resolve import shunting_yard
    if equat.count('=') == 0:
        tab = to_tab(equat)
        shun = shunting_yard(tab)
        inp = npi(shun)
        return inp.to_str()
    else:
        first_part = equat.split('=')[0]
        second_part = equat.split('=')[1]
        tab = to_tab(first_part)
        shun = shunting_yard(tab)
        inp = npi(shun)
        tab2 = to_tab(second_part)
        shun2 = shunting_yard(tab2)
        inp2 = npi(shun2)
        inp_str = inp.to_str() if not isinstance(inp, Rationels) else inp.to_str()
        inp2_str = inp2.to_str() if not isinstance(inp2, Rationels) else inp2.to_str()
        return inp_str + '=' + inp2_str


def parenthesis(equat):
    index = 0
    parenthese = -1
    parentheses_start = 0
    while index < len(equat):
        if equat[index] == ')':
            if parenthese == -1:
                print "\033[91mError: Wrongly formatted parenthesis\033[0m"
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
    return reduction(equat)


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


def add_one_before_x(equat):
    expr = ""
    if equat.startswith('x'):
        expr = '1'+equat
    else:
        expr = equat
    return expr.replace('-x', '-1x').replace('+x', '+1x')


def replace_var(equat, variables):
    complex_regex = "[^a-z]i[^a-z]|^i[^a-z]|[^a-z]i$"
    function_regex = "([a-z]+)\((.+)\)"
    var_regex = "[a-z]+"
    if re.match(complex_regex, equat):
        print "\033[91mError: Can't have complex in equation\033[0m"
        raise Exception
    index = 0
    while index < len(equat):
        if equat[index].isalpha():
            if extract_function(equat[index:]):
                func_regex = re.compile('^([a-z]+)\((.+)\)')
                match = re.match(func_regex, equat[index:])
                if match is not None:
                    name = match.group(1)
                    calc = '(' + match.group(2) + ')'

                    function = variables["function"][name]
                    equat = equat.replace(match.group(0), function.func.replace(function.var, calc))
                index = 0
            else:
                var = extract_var(equat[index:])
                if var != 'x':
                    nbr = ""
                    if var in variables["rationel"]:
                        nbr = variables["rationel"][var]
                        nbr = str(nbr.nbr)
                    elif var in variables["complexe"]:
                        print "\033[91mError: Can't have complex in equation\033[0m"
                        raise Exception
                    elif var in variables["matrices"]:
                        print "\033[91mError: Can't have matrice in second degree equation\033[0m"
                        raise Exception
                    else:
                        print "\033[91mError: Var not defined %s\033[0m" % var
                        raise Exception
                    equat = equat.replace(var, nbr).replace(' ', '')
                    index = 0
        index += 1
    return equat


def parse_equat(equat, variables):
    r = replace_var(equat, variables)
    simpler = add_multiplication(add_one_before_x(r))
    res = parenthesis(simpler)
    reso = add_pow(res)
    #DEBUG/TEST
    print("pre resolve")
    #DEBUG/TEST
    resolve(reso)
    #DEBUG/TEST
    print("post resolve")
    #DEBUG/TEST


# variables = {"rationel": {"trib": Rationels(21), "ax": Rationels(2)}, "complexe": {}, "matrices": {}, "function": {'f': Function('x^2 + trib', 'x')}}
# print("35x^2+8-25x=ax-trib+x+f(3+5)")
# print(parse_equat("x^2+2x+1=0", variables))


# replace var et fonction par leur valeur tant qu'on en a .
# reduire les parenthese
# resoudre

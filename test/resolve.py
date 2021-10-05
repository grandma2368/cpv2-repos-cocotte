# -*- coding: utf-8 -*-
import re
from parse import to_tab, parse, extract_nbr
from type import Complex, Rationels, Function, Matrice
from equation_parser import parse_equat

variables = {"rationel": {}, "complexe": {}, "matrices": {}, "function": {}}


def parse_matrice(matrice_str):
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
                print "\033[91mError: Matrice not well filled\033[0m"
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
                nbr = resolve(matrice_str[index:i] + "=?")
                matrice[lign_count - 1].append(nbr)
                index += i - index
            else:
                "\033[91mError: Matrice not well filled\033[0m"
                raise Exception
    if lign_count != lign:
        print "\033[91mError: Matrice not well field\033[0m"
        raise Exception
    return Matrice(matrice, lign, column)


def recup_var(var):
    if var in variables["rationel"]:
        return variables["rationel"][var]
    elif var in variables["complexe"]:
        return variables["complexe"][var]
    elif var in variables["matrices"]:
        return variables["matrices"][var]
    else:
        print "\033[91mError: Variable \"" + var + "\" is not defined\033[0m"
        raise Exception


def resolve_func(func):
    function_regex = re.compile('^([a-z]+)\((.+)\)')
    match = re.match(function_regex, func)
    if match is not None:
        name = match.group(1)

        calc = match.group(2)
        res = resolve(calc + '=?')

        function = variables["function"][name]
        calcul = function.func.replace(function.var, '(' + res.to_str() + ')').replace(' ', '')
        return resolve(calcul + '=?')

    else:
        print "\033[91mError: Function not well formated\033[0m"
        raise Exception


def types(nbr):
    function_regex = re.compile('^[a-z]+\((.+)\)')
    nbr_regex = re.compile('^-?[0-9]+(\.[0-9]+)?')
    matrice_regex = "^\[\[[^],]+(,[^],]+)*\](;\[[^],]+(,[^],]+)*\])*\]"
    if isinstance(nbr, Rationels) or isinstance(nbr, Complex) or isinstance(nbr, Matrice):
        return nbr
    if nbr == 'i':
        nbr = Complex(0, 1)
    elif re.match(function_regex, nbr):
        nbr = resolve_func(nbr)
    elif nbr.isalpha():
        nbr = recup_var(nbr)
    elif re.match(nbr_regex, nbr):
        nbr = Rationels(float(nbr))
    elif re.match(matrice_regex, nbr):
        nbr = parse_matrice(nbr)
    else:
        print "\033[91mError: Token not recognized in " + nbr + "\033[0m"
        raise Exception
    return nbr


def calc(nbr1, nbr2, operator):
    nbr1 = types(nbr1)
    nbr2 = types(nbr2)
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


def shunting_yard(tokens):
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
                print("\033[91mError: Wrongly formatted parenthesis\033[0m")
                raise Exception
            else:
                operator.pop()
        index += 1
    while len(operator):
        if operator[-1] == '(':
            print("\033[91mError: Wrongly formatted parenthesis\033[0m")
            raise Exception
        output.append(operator.pop())
    return output


def resolve(input):
    if input.endswith("=?"):
        token_list = to_tab(input[:-2])
        shun = shunting_yard(token_list)
        return npi_solver(shun)
    elif re.match(r'^[a-z]+=', input):
        input = re.sub(r'^[a-z]+=', '', input)
        token_list = to_tab(input)
        shun = shunting_yard(token_list)
        return npi_solver(shun)
    else:
        print "\033[91mError: Not an assignation or a calcul\033[0m"
        raise Exception


def resolve_equat(input):

    parse_equat(input[:-1], variables)


def assign_func(input, parse_info):
    input = re.sub(r'^[a-z]+\((.+)\)=', '', input)
    #if variables[
    if to_tab(input) != 'error':
        variables["function"][parse_info["assign_func"]] = Function(input, parse_info["var"])
        print input


def assign_resolve(input, parse_info):
    var = parse_info["assign"]
    res = resolve(input)
    if var in variables["rationel"]:
        variables["rationel"].pop(var)
    if var in variables["complexe"]:
        variables["complexe"].pop(var)
    if var in variables["matrices"]:
        variables["matrices"].pop(var)
    if isinstance(res, Rationels):
        variables["rationel"][var] = res
    if isinstance(res, Complex):
        variables["complexe"][var] = res
    if isinstance(res, Matrice):
        variables["matrices"][var] = res
    print res


def parsing(input):
    parse_info = parse(input)

    if parse_info['assign_func']:
        assign_func(input, parse_info)
    elif parse_info['assign']:
        assign_resolve(input, parse_info)
    elif parse_info['resolve_equat']:
        resolve_equat(input)
    else:
        res = resolve(input)
        print res


def print_var():
    for var in variables["rationel"]:
        print var + " :"
        print variables["rationel"][var]
    for var in variables["complexe"]:
        print var + " :"
        print variables["complexe"][var]
    for var in variables["matrices"]:
        print var + " :"
        print variables["matrices"][var]
    for var in variables["function"]:
        func = variables["function"][var]
        print var + "(" + func.var + ") = " + func.func

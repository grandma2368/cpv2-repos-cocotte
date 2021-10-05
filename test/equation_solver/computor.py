import sys
import re
from calculs import ft_abs, reduced_form, degree


def is_equat(equat):
    regex = "(\+?\-?[0-9.]+\*[Xx]\^[0-9]+)+=(\+?\-?[0-9.]+\*[Xx]\^[0-9]+)+"
    match = re.search(regex, equat)
    if match is None or match.group(0) != equat:
        print('\033[91mError: Syntaxe error\033[0m')
        raise Exception


def add_int(equat, index, sign, content):
    nbr = ''
    while index < len(equat) and (equat[index].isdigit() or equat[index] == '.' or equat[index] == ','):
        nbr += equat[index]
        index += 1
    content.append(float(nbr) if sign == 1 else -float(nbr))
    return len(nbr)


def parser(equat):
    sign = 1
    index = 0
    content = []
    while index < len(equat):
        if equat[index] == '=':
            content.append('=')
            sign = 1
        if equat[index] == '+' or equat[index] == '-':
            sign = 1 if equat[index] == '+' else 0
        if equat[index].isdigit():
            index += add_int(equat, index, sign, content)
        else:
            index += 1
    return content


def content_to_tab(content):
    eq_tab = {0: 0, 1: 0, 2: 0}
    index = 0
    while index < len(content) and content[index] != '=':
        eq_tab[int(ft_abs(content[index + 1]))] = content[index]
        index += 2
    index += 1
    while index < len(content):
        if eq_tab.has_key(int(ft_abs(content[index + 1]))):
            eq_tab[int(ft_abs(content[index + 1]))] -= content[index]
        else:
            eq_tab[int(ft_abs(content[index + 1]))] = -content[index]
        index += 2
    return eq_tab


def resolve(equat):
    equat = equat.replace(' ', '')

    is_equat(equat)

    content = parser(equat)
    eq_tab = content_to_tab(content)

    for key, value in eq_tab.items():
        if key != 0 and key != 1 and key != 2 and value != 0:
            rForm = "\033[95mReduced form: "
            for key, value in eq_tab.items():
                if value != 0:
                    rForm += "+ " if value > 0 else "- "
                    rForm += str(int(ft_abs(value)) if ft_abs(value) % 1 == 0 else ft_abs(value))
                    rForm += " * X^%d " % key
            rForm += "= 0\033[0m"
            print(rForm)
            print("\033[94mPolynomial degree: %d\033[0m") % (round(key))
            print("\033[91mError : The polynomial degree is stricly greater than 2, I can't solve.\033[0m")
            raise Exception

    eq_tab = reduced_form(eq_tab)
    rForm = "\033[95mReduced form: "
    if eq_tab[0] != 0 or eq_tab[1] == 0 and eq_tab[2] == 0:
        rForm += "- " if eq_tab[0] < 0 else "+ "
        rForm += str(int(ft_abs(eq_tab[0])) if ft_abs(eq_tab[0]) % 1 == 0 else ft_abs(eq_tab[0]))
        rForm += " * X^0 "
    if eq_tab[1] != 0:
        rForm += "+ " if eq_tab[1] > 0 else "- "
        rForm += str(int(ft_abs(eq_tab[1])) if ft_abs(eq_tab[1]) % 1 == 0 else ft_abs(eq_tab[1]))
        rForm += " * X^1 "
    if eq_tab[2] != 0:
        rForm += "+ " if eq_tab[2] > 0 else "- "
        rForm += str(int(ft_abs(eq_tab[2])) if ft_abs(eq_tab[2]) % 1 == 0 else ft_abs(eq_tab[2]))
        rForm += " * X^2 "
    rForm += "= 0\033[0m"

    print(rForm)
    degree(eq_tab)


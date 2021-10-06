import re
import utils

#second degree
def second_degree(eq_tab):
    delta = eq_tab[1] * eq_tab[1] - 4 * eq_tab[2] * eq_tab[0]
    print("\033[94mDegree: 2\033[0m")
    print("\033[94mDelta = %d\033[0m" % delta)
    if delta > 0:
        r1 = (-eq_tab[1] + utils.ft_sqrt(delta)) / (2 * eq_tab[2])
        r2 = (-eq_tab[1] - utils.ft_sqrt(delta)) / (2 * eq_tab[2])
        print("\033[92mDelta positif, il y a donc deux solutions reelles:\033[0m")
        print("\033[93mx1 : %f\033[0m" % r1)
        print("\033[93mx2 : %f\033[0m" % r2)
    elif delta == 0:
        r = -eq_tab[1] / (2 * eq_tab[2])
        print("\033[92mDelta est null, il y a donc une solution:\033[0m")
        print("\033[93mx : %f\033[0m" % r)
    else:
        r1 = (-eq_tab[1]) / (2 * eq_tab[2])
        r1i = (+ utils.ft_sqrt(-delta)) / (2 * eq_tab[2])
        r2 = (-eq_tab[1]) / (2 * eq_tab[2])
        r2i = (- utils.ft_sqrt(-delta)) / (2 * eq_tab[2])
        print("\033[92mDelta negatif, il y a donc deux solutions imaginaires:\033[0m")
        print("\033[93mx1 : %f + i * %f\033[0m" % (r1, r1i))
        print("\033[93mx2 : %f + i * %f\033[0m" % (r2, r2i))

#premier degree
def first_degree(eq_tab):
    print("\033[94mDegree: 1\033[0m")
    if eq_tab[0] == 0:
        print("\033[92mSolution : \033[93mx = 0\033[0m")
    else:
        print("\033[92mSolution : \033[93m x = %f\033[0m" % (-eq_tab[0] / eq_tab[1]))

#degree null
def simple(eq_tab):
    print("\033[94mDegree: 0\033[0m")
    if eq_tab[0] == 0:
        print("\033[92mA tous les reels pour solution.\033[0m")
    else:
        print("\033[92mAucune solution.\033[0m")

#resoud en fonction du degree de l'equation
def degree(eq_tab):
    if eq_tab[2] == 0 and eq_tab[1] == 0:
        simple(eq_tab)
    elif eq_tab[2] == 0:
        first_degree(eq_tab)
    else:
        second_degree(eq_tab)

#renvoie la forme reduite de l'equation
def reduced_form(eq_tab):
    div = abs(eq_tab[0])
    if eq_tab[0] < 0 and eq_tab[1] < 0 and eq_tab[2] < 0:
        eq_tab[0] *= -1
        eq_tab[1] *= -1
        eq_tab[2] *= -1
    while div > 1 and (eq_tab[0] % div != 0 or eq_tab[1] % div != 0 or eq_tab[2] % div != 0):
        div -= 1
    if div > 1:
        eq_tab[0] /= div
        eq_tab[1] /= div
        eq_tab[2] /= div
    return eq_tab

#parse l'equation
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
            index += utils.add_int(equat, index, sign, content)
        else:
            index += 1
    return content

#parse l'egalite de l'equation
def is_equat(equat):
    rgx = "(\+?\-?[0-9.]+\*[Xx]\^[0-9]+)+=(\+?\-?[0-9.]+\*[Xx]\^[0-9]+)+"
    match = re.search(rgx, equat)
    if match is None or match.group(0) != equat:
        print('\033[91mERREUR: Syntaxe.\033[0m')
        raise Exception

#entame la resolution d'equation de polynome de degree 2 max
def resolve(equat):
    equat = equat.replace(' ', '')
    is_equat(equat)
    content = parser(equat)
    eq_tab = utils.content_to_tab(content)
    for key, value in eq_tab.items():
        if key != 0 and key != 1 and key != 2 and value != 0:
            rForm = "\033[95mForme reduite: "
            for key, value in eq_tab.items():
                if value != 0:
                    rForm += "+ " if value > 0 else "- "
                    rForm += str(int(abs(value)) if abs(value) % 1 == 0 else abs(value))
                    rForm += " * X^%d " % key
            rForm += "= 0\033[0m"
            print(rForm)
            print("\033[94mDegree: %d\033[0m") % (round(key))
            print("\033[91mERREUR : Ne peut resoudre des equations de plus de degree 2.\033[0m")
            raise Exception
    eq_tab = reduced_form(eq_tab)
    rForm = "\033[95mForme reduite: "
    if eq_tab[0] != 0 or eq_tab[1] == 0 and eq_tab[2] == 0:
        rForm += "- " if eq_tab[0] < 0 else "+ "
        rForm += str(int(abs(eq_tab[0])) if abs(eq_tab[0]) % 1 == 0 else abs(eq_tab[0]))
        rForm += " * X^0 "
    if eq_tab[1] != 0:
        rForm += "+ " if eq_tab[1] > 0 else "- "
        rForm += str(int(abs(eq_tab[1])) if abs(eq_tab[1]) % 1 == 0 else abs(eq_tab[1]))
        rForm += " * X^1 "
    if eq_tab[2] != 0:
        rForm += "+ " if eq_tab[2] > 0 else "- "
        rForm += str(int(abs(eq_tab[2])) if abs(eq_tab[2]) % 1 == 0 else abs(eq_tab[2]))
        rForm += " * X^2 "
    rForm += "= 0\033[0m"
    print(rForm)
    degree(eq_tab)
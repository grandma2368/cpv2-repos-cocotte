# -*- coding: utf-8 -*-
from sqrt import ft_sqrt


def ft_abs(nbr):
    return nbr if nbr >= 0 else -nbr


def reduced_form(eq_tab):
    div = ft_abs(eq_tab[0])
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


def second_degree(eq_tab):
    delta = eq_tab[1] * eq_tab[1] - 4 * eq_tab[2] * eq_tab[0]
    print("\033[94mPolynomial degree: 2\033[0m")
    print "\033[94mdelta = %d\033[0m" % delta
    if delta > 0:  # x1 = (-b-√Δ)/(2a) et x2= (-b+√Δ)/(2a)
        r1 = (-eq_tab[1] + ft_sqrt(delta)) / (2 * eq_tab[2])
        r2 = (-eq_tab[1] - ft_sqrt(delta)) / (2 * eq_tab[2])
        print("\033[92mDiscriminant is strictly positive, the two solutions are:\033[0m")
        print "\033[93mr1 : %f\033[0m" % r1
        print "\033[93mr2 : %f\033[0m" % r2
    elif delta == 0:  # -b/(2a)
        r = -eq_tab[1] / (2 * eq_tab[2])
        print("\033[92mDiscriminant is strictly equal to 0 , the solution is:\033[0m")
        print "\033[93mr : %f\033[0m" % r
    else:  # x1 = (-b-i√Δ)/(2a) et x2= (-b+i√Δ)/(2a)
        r1 = (-eq_tab[1]) / (2 * eq_tab[2])
        r1i = (+ ft_sqrt(-delta)) / (2 * eq_tab[2])
        r2 = (-eq_tab[1]) / (2 * eq_tab[2])
        r2i = (- ft_sqrt(-delta)) / (2 * eq_tab[2])
        print("\033[92mDiscriminant is strictly negative, the two solutions are:\033[0m")
        print"\033[93mr1 : %f + i * %f\033[0m" % (r1, r1i)
        print"\033[93mr2 : %f + i * %f\033[0m" % (r2, r2i)


def first_degree(eq_tab):
    print "\033[94mPolynomial degree: 1\033[0m"
    if eq_tab[0] == 0:
        print "\033[92mThe solution is \033[93mx = 0\033[0m"
    else:
        print "\033[92mThe solution is\033[93m x = %f\033[0m" % (-eq_tab[0] / eq_tab[1])


def simple(eq_tab):
    print("\033[94mPolynomial degree: 0\033[0m")
    if eq_tab[0] == 0:
        print("\033[92mEvery real are solution\033[0m")
    else:
        print("\033[92mNo solution\033[0m")


def degree(eq_tab):
    if eq_tab[2] == 0 and eq_tab[1] == 0:
        simple(eq_tab)
    elif eq_tab[2] == 0:
        first_degree(eq_tab)
    else:
        second_degree(eq_tab)

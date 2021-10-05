import re
import random


variables = {"rationel": {"a": 25, "po": 12}, "complexe": {"tagada": "pilou"}, "matrices": {}}

class Rationels:
    def __init__(self, nbr):
        self.nbr = nbr
        self.is_positif = True if nbr >= 0 else False

    def __repr__(self):
        return self.nbr

    def __str__(self):
        return str(self.nbr)

nbr = Rationels(23)
nbr2 = 23
print(isinstance(nbr, basestring))
print(isinstance(nbr2, Rationels))



if "a" in variables["rationel"]:
    print("Ok")

if "b" in variables["rationel"]:
    print("Not Ok")

print '----------------------------'


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


print(add_pow("3+4*x+5=5*x^2+1*x-2"))
x= [2, 3, 5]
print(x[-1])
print(x.pop())
print(x[-1])
print(x.pop())
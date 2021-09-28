import parsing
import function
import utils
import math
import calcul

#resoud si delta est null
def deltaNullSolve(a, b):
    print("Delta null donc une solution dans le domaine du reel:")
    res = (-b)/(2 * a)
    print("X = " + str(res))
    return

#resoud si delta est positif
def deltaPositiveSolve(a, b, delta):
    print("Delta positif donc deux solutions dans le domaine du reel:")
    delta = math.sqrt(delta)
    resOne = (-b - delta)/(2 * a)
    resTwo = (-b + delta)/(2 * a)
    print("X1 = " + str(resOne))
    print("X2 = " + str(resTwo))
    return

#resoud si delta est negatif
def deltaNegativeSolve(a, b, delta):
    print("Delta negaitf donc deux solutions dans le domaine imaginaire:")
    delta = -1 * delta
    delta = math.sqrt(delta)
    im = (delta)/(2 * a)
    real = (-b)/(2 * a)
    print("X1 = " + str(im) + ' + ' + str(real))
    print("X2 = " + str(im) + ' - ' + str(real))
    return

#simplifie l'equation
def searchDelta(ptOne, ptTwo):
    #x^2
    a = 0
    #x^1
    b = 0
    #x^0
    c = 0
    i = 0
    lenght = len(ptOne)
    while i < lenght:
        if ptOne[i] == '^' and ptOne[i + 1] == '2' and ptOne[i - 1] == 'x':
            if i - 2 == 0:
                if utils.checkChr(ptOne[i - 2], "-1234567890.") == -1:
                    a = 1
                else:
                    a = -1
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 4 >= 0 and ptOne[i - 4] == '-':
                    a = float(ptOne[i - 3]) * -1
                else:
                    a = float(ptOne[i - 3])
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
                ptOne[i - 3] = 'empty'
            else:
                a = 1
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
        elif (ptOne[i] == 'x' and ptOne[i + 1] == '^' and ptOne[i + 2] == '1') or (ptOne[i] == 'x' and ptOne[i + 1] != '^'):
            if i - 2 == 0:
                if utils.checkChr(ptOne[i - 2], "-1234567890.") == -1:
                    b = 1
                elif ptTwo[i - 1] == '-':
                    res = -1
                elif ptTwo[i - 1] == "empty":
                    res = 1
                else:
                    b = -1
                if ptOne[i + 2] == '1':
                    ptOne[i + 2] = 'empty'
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 >= 0 and ptOne[i - 3] == '-':
                    b = float(ptOne[i - 2]) * -1
                else:
                    b = float(ptOne[i - 2])
                if ptOne[i + 2] == '1':
                    ptOne[i + 2] = 'empty'
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
                ptOne[i - 3] = 'empty'
            else:
                b = 1
                if ptOne[i + 2] == '1':
                    ptOne[i + 2] = 'empty'
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
        i += 1
    i = 0
    while i < lenght:
        if utils.checkString(ptOne[i], "0123456789.") == 0:
            if i - 1 >= 0:
                if ptOne[i - 1] == '-':
                    c = float(ptOne[i]) * -1
                else:
                    c = float(ptOne[i])
        i += 1
    i = 0
    lenght = len(ptTwo)
    while i < lenght:
        res = 0
        if ptTwo[i] == '^' and ptTwo[i + 1] == '2':
            if i - 2 == 0:
                if utils.checkChr(ptTwo[i - 2], "-1234567890.") == -1:
                    res = 1
                else:
                    res = -1
                a = a - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 4 >= 0 and ptTwo[i - 4] == '-':
                    res = float(ptTwo[i - 3]) * -1
                else:
                    res = float(ptTwo[i - 3])
                a = a - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
                ptTwo[i - 3] = 'empty'
            else:
                res = 1
                a = a - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
        elif (ptTwo[i] == 'x' and ptTwo[i + 1] == '^' and ptTwo[i + 2] == '1') or (ptTwo[i] == 'x' and ptTwo[i + 1] != '^'):
            if i - 2 == 0:
                if utils.checkChr(ptTwo[i - 2], "-1234567890.") == -1:
                    res = 1
                else:
                    res = -1
                b = b - res
                if ptTwo[i + 2] == '1':
                    ptTwo[i + 2] = 'empty'
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 >= 0 and ptTwo[i - 3] == '-':
                    res = float(ptTwo[i - 2]) * -1
                elif ptTwo[i - 1] == '-':
                    res = -1
                elif ptTwo[i - 1] == "empty":
                    res = 1
                else:
                    res = float(ptTwo[i - 2])
                b = b - res
                if ptTwo[i + 2] == '1':
                    ptTwo[i + 2] = 'empty'
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
                ptTwo[i - 3] = 'empty'
            else:
                res = 1
                b = b - res
                if ptTwo[i + 2] == '1':
                    ptTwo[i + 2] = 'empty'
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
        i += 1
    i = 0
    while i < lenght:
        res = 0
        if utils.checkString(ptTwo[i], "0123456789.") == 0:
            if i - 1 >= 0:
                if ptTwo[i - 1] == '-':
                    res = float(ptTwo[i]) * -1
                else:
                    res = float(ptTwo[i])
            c = c - res
        i += 1
    delta = b * b - 4 * a * c
    if delta == 0:
        deltaNullSolve(a, b)
    elif delta > 0:
        deltaPositiveSolve(a, b, delta)
    else:
        deltaNegativeSolve(a, b, delta)

#resoud degree 0
def solveNullDegree(partOne, partTwo):
    resOne = calcul.calculate(partOne)
    if resOne == "error":
        return("error")
    resTwo = calcul.calculate(partTwo)
    if resTwo == "error":
        return("error")
    if resTwo == resOne:
        print("L'egalite entre les deux membres de l'equation est bien du type 0 = 0.")
    else:
        print("L'egalite entre les deux membres de l'equation n'est pas du type 0 = 0.")

#resoud degree 1
def solveOneDegree(one, two):
    i = 0
    lenght = len(one)
    a = 0
    b = 0
    while i < lenght:
        if one[i] == 'x' and i - 1 >= 0 and one[i - 1] == '*':
            if i - 3 >= 0 and one[i - 3] == '-':
                a = float(one[i - 2]) * -1
                if i + 1 < lenght and one[i + 1] == '^':
                    one[i + 1] = "empty"
                    one[i + 2] = "empty"
                one[i] = "empty"
                one[i - 1] = "empty"
                one[i - 2] = "empty"
                one[i - 3] = "empty"
            elif i - 2 >= 0 and utils.checkString(one[i - 2], "0123456789.") == 0:
                a = float(one[i -2])
                if i + 1 < lenght and one[i + 1] == '^':
                    one[i + 1] = "empty"
                    one[i + 2] = "empty"
                one[i] = "empty"
                one[i - 1] = "empty"
                one[i - 2] = "empty"
            elif i - 2 >= 0 and utils.checkChr('-', one[i - 2]) == 0:
                a = -1
                if i + 1 < lenght and one[i + 1] == '^':
                    one[i + 1] = "empty"
                    one[i + 2] = "empty"
                one[i] = "empty"
                one[i - 1] = "empty"
                one[i - 2] = "empty"
            else:
                a = 1
                if i + 1 < lenght and one[i + 1] == '^':
                    one[i + 1] = "empty"
                    one[i + 2] = "empty"
                one[i] = "empty"
        i += 1
    i = 0
    while i < lenght:
        if utils.checkString(one[i], "0123456789.") == 0:
            if i - 1 >= 0:
                if one[i - 1] == '-':
                    b = float(one[i]) * -1
                else:
                    b = float(one[i])
        i += 1
    lenght = len(two)
    res = 0
    while i < lenght:
        if two[i] == 'x' and i - 1 >= 0 and two[i - 1] == '*':
            if i - 3 >= 0 and two[i - 3] == '-':
                res = float(two[i - 2]) * -1
                if two[i + 1] == '^':
                    two[i + 1] = "empty"
                    two[i + 2] = "empty"
                two[i] = "empty"
                two[i - 1] = "empty"
                two[i - 2] = "empty"
                two[i - 3] = "empty"
            elif i - 2 >= 0 and utils.checkString(two[i - 2], "0123456789.") == 0:
                res = float(two[i -2])
                if two[i + 1] == '^':
                    two[i + 1] = "empty"
                    two[i + 2] = "empty"
                two[i] = "empty"
                two[i - 1] = "empty"
                two[i - 2] = "empty"
            elif i - 2 >= 0 and utils.checkChr('-', two[i - 2]) == 0:
                res = -1
                if two[i + 1] == '^':
                    two[i + 1] = "empty"
                    two[i + 2] = "empty"
                two[i] = "empty"
                two[i - 1] = "empty"
                two[i - 2] = "empty"
            else:
                res = 1
                if two[i + 1] == '^':
                    two[i + 1] = "empty"
                    two[i + 2] = "empty"
                two[i] = "empty"
        i += 1
    a = a - res
    i = 0
    res = 0
    while i < lenght:
        if utils.checkString(two[i], "0123456789.") == 0:
            if i - 1 >= 0:
                if two[i - 1] == '-':
                    res = float(two[i]) * -1
                else:
                    res = float(two[i])
        i += 1
    b = b - res
    print("Equation de degree 1, une solution dans le domaine du reel :")
    res = (-b)/a
    print("X = " + str(res))

#verifie si bien equation de degre 2 ou inferieur
def checkDegree(partOne, partTwo, data):
    if utils.checkString(partOne, "azertyuiopqsdfghjklmwxcvbn()") == 0:
        if '(' in partOne:
            one = partOne.split('(')
            ukn = one[1].split(')')
            if ukn[0] != 'x':
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
            for vrb in data:
                res = vrb[0].split('(')
                if res[0] == one[0]:
                    expOne = vrb[1]
                    expOne = parsing.parsExpression(expOne)
                    if expOne == "error":
                        return("error")
    else:
        expOne = parsing.parsExpression(partOne)
        if expOne == "error":
            return("error")
    i = 0
    lenght = len(expOne)
    partOne = ''
    while i < lenght:
        partOne = partOne + expOne[i]
        i += 1
    if utils.checkString(partTwo, "azertyuiopqsdfghjklmwxcvbn()") == 0:
        if '(' in partTwo:
            two = partTwo.split('(')
            ukn = two[1].split(')')
            if ukn[0] != 'x':
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
            for vrb in data:
                res = vrb[0].split('(')
                if res[0] == two[0]:
                    expTwo = vrb[1]
                    expTwo = parsing.parsExpression(expTwo)
                    if expTwo == "error":
                        return("error")
    else:
        expTwo = parsing.parsExpression(partTwo)
        if expTwo == "error":
            return("error")
    i = 0
    lenght = len(expTwo)
    partTwo = ''
    while i < lenght:
        partTwo = partTwo + expTwo[i]
        i += 1
    #DEBUG/TEST
    print("avant le remplacement de variable")
    #DEBUG/TEST
    if function.replaceVariablesFunction(expOne, data, 'x') == "error":
        print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
        return("error")
    if function.replaceVariablesFunction(expTwo, data, 'x') == "error":
        print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
        return("error")
    #DEBUG/TEST
    print("apres le remplacement de variable")
    #DEBUG/TEST
    lenghtOne = len(expOne)
    lenghtTwo = len(expTwo)
    degree = 0
    i = 0
    while i < lenghtOne:
        if expOne[i] == '^':
            if float(expOne[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
            if float(expOne[i + 1]) > degree:
                degree = float(expOne[i + 1])
        elif expOne[i] == 'x':
            if 1 > degree:
                degree = 1
        i += 1
    i = 0
    while i < lenghtTwo:
        if expTwo[i] == '^':
            if float(expTwo[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
            if float(expTwo[i + 1]) > degree:
                degree = float(expTwo[i + 1])
        elif expTwo[i] == 'x':
            if 1 > degree:
                degree = 1
        i += 1
    if degree == 2:
        searchDelta(expOne, expTwo)
        return
    elif degree == 1:
        solveOneDegree(expOne, expTwo)
        return
    else:
        solveNullDegree(expOne, expTwo)
        return
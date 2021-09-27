import parsing
import function
import utils

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
        if ptOne[i] == '^' and ptOne[i + 1] == '2':
            if i - 2 == 0:
                if ptOne[i - 2] != '-':
                    a = float(ptOne[i - 2])
                else:
                    a = -1
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 == 0 and ptOne[i - 3] == '-':
                    a = float(ptOne[i - 2]) * -1
                else:
                    a = float(ptOne[i - 2])
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
        elif (ptOne[i] == '^' and ptOne[i + 1] == '1') or (ptOne[i] == 'x' and ptOne[i + 1] != '^'):
            if i - 2 == 0:
                if ptOne[i - 2] != '-':
                    b = float(ptOne[i - 2])
                else:
                    b = -1
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 == 0 and ptOne[i - 3] == '-':
                    b = float(ptOne[i - 2]) * -1
                else:
                    b = float(ptOne[i - 2])
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
                ptOne[i - 2] = 'empty'
                ptOne[i - 3] = 'empty'
            else:
                b = 1
                ptOne[i + 1] = 'empty'
                ptOne[i] = 'empty'
                ptOne[i - 1] = 'empty'
        i += 1
    i = 0
    while i < lenght:
        if ptOne[i] != "empty" and utils.checkString(ptOne, "0123456789.") == 0:
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
                if ptTwo[i - 2] != '-':
                    res = float(ptTwo[i - 2])
                else:
                    res = -1
                a = a - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 == 0 and ptTwo[i - 3] == '-':
                    res = float(ptTwo[i - 2]) * -1
                else:
                    res = float(ptOne[i - 2])
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
        elif (ptTwo[i] == '^' and ptTwo[i + 1] == '1') or (ptTwo[i] == 'x' and ptTwo[i + 1] != '^'):
            if i - 2 == 0:
                if ptTwo[i - 2] != '-':
                    res = float(ptTwo[i - 2])
                else:
                    res = -1
                b = b - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
            elif i - 2 > 0:
                if i - 3 == 0 and ptTwo[i - 3] == '-':
                    res = float(ptTwo[i - 2]) * -1
                else:
                    res = float(ptTwo[i - 2])
                b = b - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
                ptTwo[i - 2] = 'empty'
                ptTwo[i - 3] = 'empty'
            else:
                b = 1
                b = b - res
                ptTwo[i + 1] = 'empty'
                ptTwo[i] = 'empty'
                ptTwo[i - 1] = 'empty'
        i += 1
    i = 0
    while i < lenght:
        res = 0
        if ptTwo[i] != "empty" and utils.checkString(ptTwo, "0123456789.") == 0:
            if i - 1 >= 0:
                if ptTwo[i - 1] == '-':
                    res = float(ptTwo[i]) * -1
                else:
                    res = float(ptTwo[i])
            c = c - res
        i += 1
    delta = b * b - 4 * a * c
    #DEBUG/TEST
    print("a = ", a)
    print("b = ", b)
    print("c = ", c)
    print("delta = ", delta)
    #DEBUG/TEST

#verifie si bien equation de degre 2 ou inferieur
def checkDegree(partOne, partTwo, data):
    lenghtOne = len(partOne)
    lenghtTwo = len(partTwo)
    degree = 0
    i = 0
    while i < lenghtOne:
        if partOne[i] == '^':
            if float(partOne[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
            if float(partOne[i + 1]) > degree:
                degree = float(partOne[i + 1])
        i += 1
    i = 0
    while i < lenghtTwo:
        if partTwo[i] == '^':
            if float(partTwo[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
        i += 1
    expOne = parsing.parsExpression(partOne)
    if expOne == "error":
        return("error")
    expTwo = parsing.parsExpression(partTwo)
    if expTwo == "error":
        return("error")
    if function.replaceVariablesFunction(expOne, data, 'x') == "error":
        print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
        return("error")
    if function.replaceVariablesFunction(expTwo, data, 'x') == "error":
        print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
        return("error")
    if degree == 2:
        searchDelta(expOne, expTwo)
        return
    elif degree == 1:
        print("degree 1")
        return
    else:
        print("degree 0")
        return
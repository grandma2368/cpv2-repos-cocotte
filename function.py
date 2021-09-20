import parsing
import utils
import calcul

#T'ES EN TRAIN DE REVOIR LE PARSING ET LA REDUCTION DES EXPRESSIONS DE FONCTION
#PENSE A CHECKER SI ON TE FILE UNE FONCTION DONT IL FAUT CALCULER L IMAGE OU NON 
#ASSIGNE LA FONCTION DANS DATA APRES LE PARSING DED SA PARTIE CALCULATOIRE

#checke et remplace les variables dans une fonction
def replaceVariablesFunction(exp, data, vrb):
    i = 0
    lenght = len(exp)
    while i < lenght:
        if utils.checkString(exp[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            found = 0
            for el in data:
                if el[0] == exp[i]:
                    exp[i] = el[1]
                    found = 1
            if exp[i] != vrb and found == 0:
                print("Une variable de l'expression n'est pas enregistree dans data.")
                return("error")
        i += 1

#reduit au maximum un calcul avec variable
def reduceCalc(calc):
    while len(calc) > 3:
        vrb = ''
        #va chercher l'index des calculs selon leur ordre de priorite
        if utils.checkChr('*', calc) == 0:
            index = calc.index('*')
            if utils.checkString(calc[index - 1], "0123456789.") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                res = calcul.multiply(calc[index - 1], calc[index + 1])
                calc[index - 1] = res
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            elif utils.checkString(calc[index - 1], "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                calc[index - 1] = calc[index + 1] + calc[index] + calc[index - 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            else:
                calc[index - 1] = calc[index - 1] + calc[index] + calc[index + 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
        if utils.checkChr('/', calc) == 0:
            index = calc.index('/')
            if utils.checkString(calc[index - 1], "0123456789.") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                res = calcul.divide(calc[index - 1], calc[index + 1])
                calc[index - 1] = res
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            elif utils.checkString(calc[index - 1], "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                calc[index - 1] = calc[index + 1] + calc[index] + calc[index - 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            else:
                calc[index - 1] = calc[index - 1] + calc[index] + calc[index + 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
        if utils.checkChr('%', calc) == 0:
            index = calc.index('%')
            if utils.checkString(calc[index - 1], "0123456789.") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                res = calcul.modulo(calc[index - 1], calc[index + 1])
                calc[index - 1] = res
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            elif utils.checkString(calc[index - 1], "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                calc[index - 1] = calc[index + 1] + calc[index] + calc[index - 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            else:
                calc[index - 1] = calc[index - 1] + calc[index] + calc[index + 1]
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
        if utils.checkChr('+', calc) == 0:
            index = calc.index('+')
            if utils.checkString(calc[index - 1], "0123456789.") == 0 and utils.checkString(calc[index + 1], "0123456789.") == 0:
                res = calcul.add(calc[index - 1], calc[index + 1])
                calc[index - 1] = res
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
        if utils.checkChr('-', calc) == 0:
            index = calc.index('-')
            if calc[index - 1] == calc[index + 1] and index + 1 <= len(calc):
                calc[index - 1] = 0
                if index + 1 <= len(calc):
                    calc.pop(index + 1)
                    calc.pop(index)
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            if index + 1 <= len(calc):
                if utils.checkString(calc[index + 1], "0123456789.") == 0:
                    calc[index + 1] = int(calc[index + 1]) * -1
                    calc[index] = '+'
                else:
                    calc[index + 1] = calc[index] + calc[index + 1]
                    calc[index] = '+'
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")

#dernier rempart de reduction de fonction:
def reduceEndFunction(exp):
    i = 0
    while i < len(exp):
        if utils.checkString(str(exp[i]), "*^%/+-") == 0:
            if i < len(exp) and exp[i] == '*':
                if utils.checkString(str(exp[i - 1]), "0123456789.") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    res = calcul.multiply(exp[i - 1], exp[i + 1])
                    exp[i - 1] = res
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                elif utils.checkString(str(exp[i - 1]), "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    exp[i - 1] = str(exp[i + 1]) + str(exp[i]) + str(exp[i - 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                else:
                    exp[i - 1] = str(exp[i - 1]) + str(exp[i]) + str(exp[i + 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
            if i < len(exp) and exp[i] == '/':
                if utils.checkString(str(exp[i - 1]), "0123456789.") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    res = calcul.divide(exp[i - 1], exp[i + 1])
                    exp[i - 1] = res
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                elif utils.checkString(str(exp[i - 1]), "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    exp[i - 1] = str(exp[i + 1]) + str(exp[i]) + str(exp[i - 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                else:
                    exp[i - 1] = str(exp[i - 1]) + str(exp[i]) + str(exp[i + 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
            if i < len(exp) and exp[i] == '%':
                if utils.checkString(str(exp[i - 1]), "0123456789.") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    res = calcul.modulo(exp[i - 1], exp[i + 1])
                    exp[i - 1] = res
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                elif utils.checkString(str(exp[i - 1]), "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    exp[i - 1] = str(exp[i + 1]) + str(exp[i]) + str(exp[i - 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                else:
                    exp[i - 1] = str(exp[i - 1]) + str(exp[i]) + str(exp[i + 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
            if i < len(exp) and exp[i] == '+':
                if utils.checkString(str(exp[i - 1]), "0123456789.") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    res = calcul.add(exp[i - 1], exp[i + 1])
                    exp[i - 1] = res
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                elif utils.checkString(str(exp[i - 1]), "qwertyuiopasdfghjklzxcvbnm") == 0 and utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                    exp[i - 1] = str(exp[i + 1]) + str(exp[i]) + str(exp[i - 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                else:
                    exp[i - 1] = str(exp[i - 1]) + str(exp[i]) + str(exp[i + 1])
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
            if i < len(exp) and exp[i] == '-':
                if exp[i - 1] == exp[i + 1] and i + 1 <= len(exp):
                    exp[i - 1] = 0
                    if i + 1 <= len(exp):
                        exp.pop(i + 1)
                        exp.pop(i)
                    else:
                        print("ERREUR taille tableau dans les calculs")
                        return("error")
                if i + 1 <= len(exp):
                    if utils.checkString(str(exp[i + 1]), "0123456789.") == 0:
                        exp[i + 1] = int(exp[i + 1]) * -1
                        exp[i] = '+'
                    else:
                        exp[i + 1] = exp[i] + exp[i + 1]
                        exp[i] = '+'
                else:
                    print("ERREUR taille tableau dans les calculs")
                    return("error")
            i += 1
        else:
            i += 1

#reduit le contenu entre deux parentheses
def reduceParenthesis(exp, start, end):
    i = start
    found = 0
    calc = []
    while i < end:
        calc.append(exp[i])
        i += 1
    if reduceCalc(calc) == "error":
        return("error")
    lenght = len(calc)
    i = start
    while i < start + lenght:
        exp[i] = calc[i - start]
        i += 1
    index = i
    while i < end:
        exp.pop(index)
        i += 1

#reduit les multiplication par la variable de la fonction
def reduceFunctionExp(exp, start):
    #recupere l'indice de la parenthese ouvrante prioritaire
    prtOpen = 0
    #voit s'il y a une parenthese fermante
    prtClosed = 0
    i = start
    lenght = len(exp)
    while i < lenght:
        if exp[i] == '(':
            prtOpen = i
        if exp[i] == ')':
            prtClosed = i
            #calcule ce qui se trouve entre les deux parentheses
            if reduceParenthesis(exp, prtOpen + 1, prtClosed) == "error":
                return("error")
            if reduceFunctionExp(exp, i + 1) == "error":
                return("error")
        i += 1
    if reduceEndFunction(exp) == "error":
        return("error")
    #lancee une seconde fois pour gerer les nombres negatifs
    if reduceEndFunction(exp) == "error":
        return("error")

#reduit la calcul d'une fonction
def reduceFunction(exp, data, name, vrb):
    if replaceVariablesFunction(exp, data, vrb) == "error":
        return("error")
    if reduceFunctionExp(exp, 0) == "error":
        return("error")
    #TROUVER UN MOYEN DE REDUIRE l'INTERIEUR DES PARENTHESES QUAND C'EST POSSIBLE MAIS NE PAS LES SUPPRIMER

#checke le nom de la fonction et si la fonction a bien une variable
def checkFunction(varName, varValue, data):
    if varName[0] == "i" and varName[1] == "(":
        print("Une fonction ne peut porter le nom de 'i' a cause des nombres imaginaires.")
        return("error")
    res = varName.split('(')
    ukn = res[1].split(')')
    if ukn[0] in varValue:
        exp = parsing.parsExpression(varValue)
        if exp == "error":
            return("error")
        if reduceFunction(exp, data, varName, ukn[0]) == "error":
            return("error")
        #VOIR SI ON GARDE L'ASSIGNATION DANS data ICI
        datum = [varName, varValue]
        data.append(datum)
    else:
        #il n'y a pas de variable dans la fonction
        print("Il n'y a pas de variable dans la fonction.")
        return("error")
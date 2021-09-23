import utils
import show

#puissance
def power(a, b):
    if b < 0:
        print("Ne gere pas les puissances negatives.")
        return("error")
    c = pow(int(a),int(b))
    return(c)

#multiplie deux nombres
def multiply(a, b):
    c = float(a) * float(b)
    return(c)

#divise deux nombres
def divide(a, b):
    if b == 0:
        print("Une division par 0 ne peut etre calcule.")
        return("error")
    c = float(a) / float(b)
    return(c)

#modulo deux nombres
def modulo(a, b):
    if b == 0:
        print("Un modulo par 0 ne peut etre calcule.")
        return("error")
    c = float(a) % float(b)
    return(c)

#additionne deux nombres
def add(a, b):
    c = float(a) + float(b)
    return(c)

#calcule ce qu'il y a dans le tableau
def someCalcul(calc):
    #boucle sur le tableau tant qu'il reste des calculs a faire dedans
    while len(calc) != 1:
        #va chercher l'index des calculs selon leur ordre de priorite
        if utils.checkChr('*', calc) == 0:
            index = calc.index('*')
            res = multiply(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
        if utils.checkChr('^', calc) == 0:
            index = calc.index('^')
            res = power(calc[index - 1], calc[index + 1])
            if res == "error":
                return("error")
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
        if utils.checkChr('/', calc) == 0:
            index = calc.index('/')
            res = divide(calc[index - 1], calc[index + 1])
            if res == "error":
                return("error")
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
        if utils.checkChr('%', calc) == 0:
            index = calc.index('%')
            res = modulo(calc[index - 1], calc[index + 1])
            if res == "error":
                return("error")
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
        if utils.checkChr('+', calc) == 0:
            index = calc.index('+')
            res = add(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
        if utils.checkChr('-', calc) == 0:
            index = calc.index('-')
            if index + 1 <= len(calc):
                calc[index + 1] = int(calc[index + 1]) * -1
                calc[index] = '+'
            else:
                print("ERREUR taille tableau dans les calculs")
                return("error")
    if len(calc) != 1:
        return("error")
    return(calc)

#recupere le calcul prioritaire a faire
def calcParenthesis(start, end, exp):
    calc = []
    i = start + 1
    while i < end:
        calc.append(exp[i])
        i += 1
    #calcule ce qui se trouve dans la portion entre parentheses
    res = someCalcul(calc)
    if res == "error":
        return("error")
    #remplace le calcul entre parentheses par sa valeur
    i = end
    exp[start] = calc[0]
    while i > start:
        exp.pop(i)
        i -= 1

#cherche les parentheses prioritaires
def checkParenthesis(exp):
    #recupere l'indice de la parenthese ouvrante prioritaire
    prtOpen = 0
    #voit s'il y a une parenthese fermante
    prtClosed = 0
    i = 0
    for prt in exp:
        if prt == '(':
            prtOpen = i
        if prt == ')':
            prtClosed = i
            #calcule ce qui se trouve entre les deux parentheses
            if calcParenthesis(prtOpen, prtClosed, exp) == "error":
                return("error")
            if checkParenthesis(exp) == "error":
                return("error")
        i += 1

#calcule une expression pour l'enregistrer dans data, name est a 0 s'il s'agit juste d'un calcul a resoudre
def calculate(exp, data, name):
    #effectue le caclul s'il s'agit de nombres reels
    if checkParenthesis(exp) == "error":
        return("error")
    #calcule ce qui reste dans exp a la fin
    if someCalcul(exp) == "error":
        return("error")
    return(exp[0])
    # #check si c'est un calcul ou variable a assigner
    # if name == 0:
    #     print(exp[0])
    #     return
    # #check pour reassigner ou non une variable
    # reassigned = 0
    # for eachVar in data:
    #     if eachVar[0] == name:
    #         eachVar[1] = exp[0]
    #         reassigned = 1
    #         show.showDatum(data, name)
    # if reassigned == 0:
    #     datum = [name, exp[0]]
    #     data.append(datum)
    #     show.showDatum(data, name)

#checke et remplace les variables par leur valeur dans data
def replaceVariables(exp, data):
    i = 0
    lenght = len(exp)
    while i < lenght:
        if utils.checkString(exp[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            found = 0
            if '(' in exp[i]:
                for eachVar in data:
                    namePb = exp[i].split('(')
                    if utils.checkString(eachVar[0], "qwertyuiopasdfghjklzxcvbnm()") == 0:
                        nameFnc = eachVar[0].split('(')
                        if nameFnc[0] == namePb[0]:
                            found = 1
                            vrb = namePb[1].split(')')
                            vrbFnc = nameFnc[1].split(')')
                            res = function.calculImage(eachVar[1], vrbFnc[0], vrb[0], data, 0)
                            if res == "error":
                                return("error")
                            else:
                                exp[i] = res
                    if found == 0:
                        print("Une variable de l'expression n'est pas enregistree dans data.")
                        return("error")
            else:
                for el in data:
                    if el[0] == exp[i]:
                        exp[i] = el[1]
                        found = 1
                if found == 0:
                    print("Une variable de l'expression n'est pas enregistree dans data.")
                    return("error")
        i += 1

#checke les variables et les remplace si elles sont dans data puis resoud/reduit le calcul
def calculateWithVariables(exp, data, name):
    if replaceVariables(exp, data) == "error":
        return("error")
    res = calculate(exp, data, name)
    if res == "error":
        return("error")
    return(res)

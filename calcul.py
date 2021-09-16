import utils

#multiplie deux nombres
def multiply(a, b):
    c = int(a) * int(b)
    return(c)

#divise deux nombres
def divide(a, b):
    c = int(a) / int(b)
    return(c)

#modulo deux nombres
def modulo(a, b):
    c = int(a) % int(b)
    return(c)

#additionne deux nombres
def add(a, b):
    c = int(a) + int(b)
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
        if utils.checkChr('/', calc) == 0:
            index = calc.index('/')
            res = divide(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('%', calc) == 0:
            index = calc.index('%')
            res = modulo(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('+', calc) == 0:
            index = calc.index('+')
            res = add(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('-', calc) == 0:
            index = calc.index('-')
            if index + 1 <= len(calc):
                calc[index + 1] = int(calc[index + 1]) * -1
                calc[index] = '+'
    if len(calc) != 1:
        return("error")

#recupere le calcul prioritaire a faire
def calcParenthesis(start, end, exp):
    calc = []
    i = start + 1
    while i < end:
        calc.append(exp[i])
        i += 1
    #calcule ce qui se trouve dans la portion entre parentheses
    if someCalcul(calc) == "error":
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
    #vois s'il y a une parenthese fermante
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
    #check si c'est un calcul ou variable a assigner
    if name == 0:
        print(exp[0])
        return
    #check pour reassigner ou non une variable
    reassigned = 0
    for eachVar in data:
        if eachVar[0] == name:
            eachVar[1] = exp[0]
            reassigned = 1
    if reassigned == 0:
        datum = [name, exp[0]]
        data.append(datum)

#checke et remplace les variables par leur valeur dans data
def replaceVariables(exp, data):
    i = 0
    lenght = len(exp)
    while i < lenght:
        if utils.checkString(exp[i], "qwertyuiopasdfghjklzxcvbnm") == 0:
            found = 0
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
    if calculate(exp, data, name) == "error":
        return("error")

#checke et remplace les variables dans une fonction
def replaceVariablesFunction(exp, data, vrb):
    i = 0
    lenght = len(exp)
    while i < lenght:
        if utils.checkString(exp[i], "qwertyuiopasdfghjklzxcvbnm") == 0:
            found = 0
            for el in data:
                if el[0] == exp[i]:
                    exp[i] = el[1]
                    found = 1
            if found == 0 and exp[i] != vrb:
                print("Une variable de l'expression n'est pas enregistree dans data.")
                return("error")
        i += 1

#reduit ce qu'il y a entre deux parentheses dans une expression de fonction
def calcParenthesisFunction(start, end, exp, vrb):
    calc = []
    i = start + 1
    while i < end:
        calc.append(exp[i])
        i += 1
    #calcule ce qui se trouve dans la portion entre parentheses
    if someReduceFunction(calc, vrb) == "error":
        return("error")
    #remplace le calcul entre parentheses par sa valeur
    i = end
    exp[start] = calc[0]
    while i > start:
        exp.pop(i)
        i -= 1

#checke les parentheses dans une fonction
def checkParenthesisFunction(exp, vrb):
    #recupere l'indice de la parenthese ouvrante prioritaire
    prtOpen = 0
    #vois s'il y a une parenthese fermante
    prtClosed = 0
    i = 0
    for prt in exp:
        if prt == '(':
            prtOpen = i
        if prt == ')':
            prtClosed = i
            #calcule ce qui se trouve entre les deux parentheses
            if calcParenthesisFunction(prtOpen, prtClosed, exp, vrb) == "error":
                return("error")
            if checkParenthesisFunction(exp, vrb) == "error":
                return("error")
        i += 1
    return("error")

#REVOIR LA LOGIQUE ICI POUR LA BOUCLE CAR IL PEUT Y A VOIR PLUS D'UNE CASE AU TABLEAU A LA FIN !
#reduit la parcelle de calcul donnee
def someReduceFunction(calc, vrb):
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
        if utils.checkChr('/', calc) == 0:
            index = calc.index('/')
            res = divide(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('%', calc) == 0:
            index = calc.index('%')
            res = modulo(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('+', calc) == 0:
            index = calc.index('+')
            res = add(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            if index + 1 <= len(calc):
                calc.pop(index + 1)
                calc.pop(index)
        if utils.checkChr('-', calc) == 0:
            index = calc.index('-')
            if index + 1 <= len(calc):
                calc[index + 1] = int(calc[index + 1]) * -1
                calc[index] = '+'
    if len(calc) != 1:
        return("error")

#reduit l'expression d'une fonction et l'assigne dans data si tout est correct
def reduceFonctionExp(exp, data, vrb, name):
    #cherche les parentheses
    if checkParenthesisFunction(exp, vrb) == "error":
        return("error")
    #reduit ce qui reste dans exp a la fin
    if someReduceFunction(exp, vrb) == "error":
        return("error")
    return("error")

#reduit la calcul d'une fonction
def reduceFonction(exp, data, name, vrb):
    if replaceVariablesFunction(exp, data, vrb) == "error":
        return("error")
    if reduceFonctionExp(exp, data, vrb, name) == "error":
        return("error")
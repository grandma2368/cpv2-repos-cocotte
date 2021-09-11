import utils

#GROS SOUCIS AVEC LES NOMBRES NEGATIFS A GERER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#multiplie deux nombres
def multiply(a, b):
    c = a * b
    return(c)

#divise deux nombres
def divide(a, b):
    c = a / b
    return(c)

#modulo deux nombres
def modulo(a, b):
    c = a % b
    return(c)

#additionne deux nombres
def add(a, b):
    c = a + b
    return(c)

#soustrait deux nombres
def substract(a, b):
    c = a - b
    return(c)

#recupere le calcul prioritaire a faire
def calcParenthesis(start, end, exp):
    calc = []
    i = start + 1
    while i < end:
        calc.append(exp[i])
        i += 1
    if utils.checkChr('*', calc) == 0:
        index = calc.index('*')
        res = multiply(calc[index - 1], calc[index + 1])
        calc[index - 1] = res
        calc.pop(index + 1)
        calc.pop(index)
    if utils.checkChr('/', calc) == 0:
        index = calc.index('/')
        res = divide(calc[index - 1], calc[index + 1])
        calc[index - 1] = res
        calc.pop(index + 1)
        calc.pop(index)
    if utils.checkChr('%', calc) == 0:
        index = calc.index('%')
        res = modulo(calc[index - 1], calc[index + 1])
        calc[index - 1] = res
        calc.pop(index + 1)
        calc.pop(index)
    if utils.checkChr('+', calc) == 0:
        index = calc.index('+')
        res = add(calc[index - 1], calc[index + 1])
        calc[index - 1] = res
        calc.pop(index + 1)
        calc.pop(index)
    if utils.checkChr('-', calc) == 0:
        index = calc.index('-')
        if index != 0:
            res = substract(calc[index - 1], calc[index + 1])
            calc[index - 1] = res
            calc.pop(index + 1)
            calc.pop(index)

    return("error")

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
            #RENVOYER VERS UNE FONCTION QUI VA CALCULER L'ENTRE DEUX
            calcParenthesis(prtOpen, prtClosed, exp)
            #checkParenthesis(exp)
        i += 1
    if prtClosed != 0:
        print("Une parenthese fermante reste dans l'expression")
        return("error")

#calcule une expression pour l'enregistrer dans data
def calculate(exp, data):
    checkParenthesis(exp)
    #FAIRE UNE FONCTION POUR CALCULER CE QUI RESTE DANS EXP
    return("error")
import parsing
import utils

#T'ES EN TRAIN DE REVOIR LE PARSING ET LA REDUCTION DES EXPRESSIONS DE FONCTION
#PENSE A CHECKER SI ON TE FILE UNE FONCTION DONT IL FAUT CALCULER L IMAGE OU NON 

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
            if exp[i] != vrb and found == 0:
                print("Une variable de l'expression n'est pas enregistree dans data.")
                return("error")
        i += 1

#reduit les multiplication par la variable de la fonction
def reduceFonctionExp(exp, vrb):
    calc = []
    i = 0
    lenght = len(exp)
    while i < lenght:
        if exp[i] in "1234567890" and exp[i + 1] in "*%/" and exp[i + 2] == vrb:
            calc.append(exp[i] + exp[i + 1] + exp[i + 2])
            i += 3
        else:
            calc.append(exp[i])
            i += 1
    i = 0
    lenght = len(calc)
    while i < lenght:
        if calc[i] == exp[i]:
            i += 1
        else:
            exp[i] = calc[i]
            exp.pop(i + 2)
            exp.pop(i + 1)

#reduit la calcul d'une fonction
def reduceFonction(exp, data, name, vrb):
    if replaceVariablesFunction(exp, data, vrb) == "error":
        return("error")
    reduceFonctionExp(exp, vrb)
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
        if reduceFonction(exp, data, varName, ukn[0]) == "error":
            return("error")
        datum = [varName, varValue]
        data.append(datum)
    else:
        #il n'y a pas de variable dans la fonction
        print("Il n'y a pas de variable dans la fonction.")
        return("error")
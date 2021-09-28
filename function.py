import parsing
import utils
import calcul

#calcule l'image d'une fonction existante
def calculImage(fnc, fncVrb, vrb, data, name):
    #si vrb est une variable, verifie dans data qu'elle existe
    if utils.checkString(vrb, "1234567890[].,;i") == -1:
        found = 0
        for datum in data:
            if datum[0] == vrb:
                vrb = datum[1]
                found = 1
                break
        if found == 0:
            print("La variable'" + vrb + "' n'est pas encore enregistree dans data.")
            return("error")
    exp = parsing.parsExpression(fnc)
    if exp == "error":
        print("Une erreur est survenue lors du parsing.")
        return("error")
    i = 0
    lenght = len(exp)
    while i < lenght:
        if exp[i] == fncVrb:
            exp[i] = vrb
        i += 1
    res = calcul.calculate(exp, data, name)
    if res == "error":
        print("Une erreur est surevnue lors du calcul.")
        return("error")
    return(res)

#checke et remplace les variables dans une fonction
def replaceVariablesFunction(exp, data, vrb):
    i = 0
    lenght = len(exp)
    fnc = 0
    while i < lenght:
        if utils.checkString(exp[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            found = 0
            for el in data:
                if el[0] != vrb:
                    if el[0] == exp[i + fnc]:
                        exp[i + fnc] = el[1]
                        found = 1
            if exp[i] != vrb and found == 0:
                print("Une variable de l'expression n'est pas enregistree dans data.")
                return("error")
        i += 1

#reduit la calcul d'une fonction
def reduceFunction(exp, data, name, vrb):
    if replaceVariablesFunction(exp, data, vrb) == "error":
        return("error")
    i = 0
    fnc = ''
    lenght = len(exp)
    while i < lenght:
        fnc = fnc + exp[i]
        i += 1
    datum = [name, fnc]
    return(datum)

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
        res = reduceFunction(exp, data, varName, ukn[0])
        if res == "error":
            return("error")
        return(res)
    else:
        #il n'y a pas de variable dans la fonction
        print("Il n'y a pas de variable dans la fonction.")
        return("error")
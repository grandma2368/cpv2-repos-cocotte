import utils
import calcul

#checke s'il faut remplacer des valeurs dans data et les remplace par leur valeur
def checkVar(exp, data):
    for vrb in exp:
        if utils.checkString(vrb, "qwertyuiopasdfghjklzxcvbnm") == 0:
            #variable pour savoir si la variable a ete trouvee ou non dans data
            found = 0
            for datum in data:
                if datum[0] == vrb:
                    vrb = datum[1]
                    found = 1
            if found == 0:
                print("la variable ", vrb ," n'existe pas encore dans data")
                return("error")
    #calcule l'expression pour rentree le resultat dans data
    calcul.calculate(exp, data)

#parse la partie calcul, fnt determine s'il s'agit du parsing de l'expression d'une fonction ou d'un calcul
def parsExpression(pb, data, fnt):
    i = 0
    lenght = len(pb)
    #contient chaque partie de l'equation
    exp = []
    #verifie que toute parenthese ouverte est fermee plus tard
    prt = 0
    while i < lenght:
        #contient le nombre ou le nom de variable en train d'etre lu
        vrb = ''
        if i == 0 and pb[i] == '-' or i == 0 and pb[i] == '(':
            if pb[i] == '(':
                prt += 1
            exp.append(pb[i])
            i += 1
        #verifie si une donnee a ete trouvee
        found = 0
        while i < lenght and utils.checkChr(pb[i], "0123456789") == 0:
            found = 1
            vrb = vrb + pb[i]
            i += 1
        if found == 1:
            exp.append(vrb)
        else:
            while i < lenght and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm") == 0:
                found = 1
                vrb = vrb + pb[i]
                i += 1
            if found == 1:
                exp.append(vrb)
        if found == 1 and i < lenght :
            if utils.checkChr(pb[i], "^%*+-/)") == 0:
                exp.append(pb[i])
                found = 0
            else:
                #il n'y a pas de symbole de calcul entre deux nombres ou deux variables
                print("il n'y a pas de symbole de calcul entre deux nombres ou deux variables")
                return("error")
        if i < lenght and pb[i] == '(':
            prt += 1
            exp.append(pb[i])
        if i < lenght and pb[i] == ')':
            prt -= 1
        if prt < 0:
            print("une parenthese fermante n'est pas accompagnee d'une ouvrante")
            return("error")
        i += 1
    if prt != 0:
        print("pb de parentheses")
        return("error")
    #renvoie vers le remplacement des varaibles s'il ne s'agit pas de l'expression d'une fonction
    if fnt == 0:
        if checkVar(exp, data) == "error":
            print("Certaines variables sont inconnues")
            return("error")
    else:
        #FAIRE UNE FONCTION POUR REDUIRE L'EXPRESSION DE LA FONCTION
        print("cas ou il faut reduire au maximum l expression de la fonction")

#cherche si le probleme est correcte ou non
def isItAProb(pb, data):
    name = pb.lower()
    for eachVar in data:
        if eachVar[0] == name:
            #renvoie la valeur de la variable trouvee
            print(eachVar[1])
            return
    #IL S'AGIT D'UN CALCUL A RESOUDRE --> A GERER
    #VERIFIER LES PRIORITES DE CALCUL
    if utils.checkString(name, "1234567890+-/.*i%^()") == -1:
        #VERIFIER S'IL Y A UNE FONCTION DANS DATA
        #VERIFIER S'IL Y A DES VARIABLES A REMPLACER PAR LEUR VALEUR DANS DATA
        return("error")
    print("calcul a resoudre")
    return()

#cherche si la variable existe deja dans data et dans ce cas la reassigne
def isReassignated(varName, varValue, data):
    value = varValue.lower()
    name = varName.lower()

    for eachVar in data:
        if eachVar[0] == name:
            #reassigned la nouvelle valeur
            eachVar[1] = value
            print(eachVar[1])
            return("reassigned")

#checke le nom de la fonction et si la fonction a bien une variable
def checkFunction(varName, varValue, data):
    res = varName.split('(')
    ukn = res[1].split(')')
    if ukn[1] in varValue:
        datum = [varName, varValue]
        data.append(datum)
    else:
        #il n'y a pas de variable dans la fonction
        print("il n'y a pas de variable dans la fonction")
        return("error")
    print(varValue)

#cree une nouvelle variable si les donnees sont correctes
def newVarInData(varName, varValue, data):
    value = varValue.lower()
    name = varName.lower()

    #recherche si le nom de variable ne contient que des lettres ou non
    if utils.checkString(name, "azertyuiopqsdfghjklmwxcvbn()") == -1:
        return("error")
    if '(' in name:
        #checke si la fonction est correcte et assigne la fonction
        checkFunction(name, value, data)
        return
    #recherche si la variable est a calculer a partir d'autre ou non ou si matrice
    if utils.checkString(value, "1234567890+-/.*i%^()") == -1:
        #RECHERCHER LES VARIABLES DANS DATA
        #RECHERCHER SI C EST UNE MATRICE
        print("pas un calcul ou une variable de deja donnee")
        return
    #enregistre la variable dans data
    datum = [name, value]
    data.append(datum)
    print(value)
    
#fonction d'entree dans le parsing
def parsing(line, data):
    res = line.split("=")
    if len(res) == 1:
        #verifie s'il s'agit d'une variable a donner ou d'un calcul a resoudre
        if isItAProb(line.replace(" ", ""), data) == "error":
            return("error")
    else:
        #verifie s'il s'agit d'une variable a donner ou d'un calcul a resoudre
        if res[1].replace(" ", "") == "?":
            if isItAProb(res[0].replace(" ", ""), data) == "error":
                return("error")
        else:
            #PHASE DE TEST DE parsExpression
            if parsExpression(res[1].replace(" ", "").lower(), data, 0) == "error":
                print("une erreur est survenue dans le parsing de l expression")
                return("error")
            #verifie s'il s'agit d'une reassignation de variable
            if isReassignated(res[0].replace(" ", ""), res[1].replace(" ", ""), data) != "reassigned":
                #CHECKER S IL Y A UNE VALEUR DEJA DE DONNEE OU S'IL FAUT LA CALCULER
                #VOIR SI C'EST UNE ASSIGNATION PAR RAPPORT A UNE VARIABLE DEJA EXISTANTE
                if newVarInData(res[0].replace(" ", ""), res[1].replace(" ", ""), data) == "error":
                    return("error")
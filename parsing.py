import utils
import calcul
import matrice
import function

#checke s'il faut remplacer des valeurs dans data et les remplace par leur valeur
def checkVar(exp, data, name):
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
    if calcul.calculate(exp, data, name) == "error":
        return("error")

#parse la partie calcul
def parsExpression(pb):
    i = 0
    lenght = len(pb)
    #contient chaque partie de l'equation
    exp = []
    #verifie que toute parenthese ouverte est fermee plus tard
    prt = 0
    #gere les * sous entendus
    found = 0
    while i < lenght:
        #contient le nombre ou le nom de variable en train d'etre lu
        vrb = ''
        #conteneur de matrice
        mtc = []
        if utils.checkChr(pb[i], "-+*^%/[,;") == 0:
            if i == 0:
                if utils.checkChr(pb[i],"-[(") == -1:
                    print("L'expression ne peut commencer par une operation autre que '-'.")
                    return("error")
            if pb[i] == '[':
                #on entre dans la definition d'une matrice
                i = matrice.parseMatrice(mtc, i, pb)
                if i == "error":
                    return("error")
                exp.append(mtc)
            else:
                found = 0
                exp.append(pb[i])
                i += 1
        else:
            if found == 1:
                exp.append('*')
        #verifie les float
        pnt = 0
        #checke les valeurs numerales
        if i < lenght and found > 0 and utils.checkChr(pb[i], "0123456789.") == 0:
            exp.append('*')
            found = 0
        while i < lenght and utils.checkChr(pb[i], "0123456789.") == 0:
            if pb[i] == '.':
                pnt += 1
            found = 1
            vrb = vrb + pb[i]
            i += 1
        if pnt > 1:
            print("Un nombre decimal ne peut contenir qu'un '.'.")
            return("error")
        if found == 1:
            exp.append(vrb)
        #index de depart de la prochaine boucle et checke de parenthese pour le cas d'une fonction
        j = i
        indexPrt = prt
        vrb = ''
        #checke les variables et functions
        if i < lenght and found > 0 and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm(") == 0:
            exp.append('*')
            found = 0
        while i < lenght and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            if pb[i] == '(' and i != j:
                prt += 1
            elif pb[i] == ')' and i != j:
                prt -= 1
            elif pb[i] == '(' and i == j:
                prt += 1
                exp.append(pb[i])
                found = 0
                i += 1
                break
            elif pb[i] == ')' and i == j:
                prt -= 1
                exp.append(pb[i])
                found = 0
                i += 1
                break
            found = 2
            vrb = vrb + pb[i]
            i += 1
        if  prt != 0 and prt != indexPrt and found > 0:
            #gere le cas particulier ou la parenthese ouvrante se trouve a la fin sans qu il n y ait de * entre la variable et la parenthese
            if prt == indexPrt + 1 and pb[i - 1] == '(':
                end = i - 1
                i = j
                vrb = ''
                while i < end:
                    vrb = vrb + pb[i]
                    i += 1
            else:
                print("Toute fonction doit avoir sa variable definie entre deux parentheses, une '(' et une ')'.")
                return("error")
        if found == 2:
            exp.append(vrb)
    return(exp)

#cherche si le probleme est correcte ou non
def isItAProb(pb, data):
    pbm = pb.lower()
    for eachVar in data:
        if eachVar[0] == pbm:
            #FAIRE L'AFFICHAGE PROPRE
            #renvoie la valeur de la donnnee trouvee
            print(eachVar[1])
            return
    if utils.checkString(pbm, "1234567890+-/.*%^()[];,qwertyuiopasdfghjklzxcvbnm") == 0:
        exp = parsExpression(pbm)
        if exp == "error":
            return("error")
        #VERIFIER VERS QUEL CALCUL LE RENVOYER --> MATRICE OU NON / IMAGINAIRE OU NON
        if calcul.calculate(exp, data, 0) == "error":
            return("error")
    else:
        print("Des caracteres ne sont pas propices au calcul.")
        return("error")
    return

#cree une nouvelle variable si les donnees sont correctes
def newVarInData(varName, varValue, data):
    value = varValue.lower()
    name = varName.lower()

    #recherche si le nom de variable ne contient que des lettres ou non
    if utils.checkString(name, "azertyuiopqsdfghjklmwxcvbn()") == -1:
        print("Le nom de la fonction ou de la variable est invalide.")
        return("error")
    if len(name) == 1 and name[0] == 'i':
        print("Une variable ne peut etre nommee 'i' en raison des nombres imaginaires.")
        return("error")

    #checke s'il s'agit d'une definition de fonction ou non
    if '(' in name:
        #checke si la fonction est correcte et assigne la fonction
        if function.checkFunction(name, value, data) == "error":
            return("error")
        return

    #recherche si la variable est a calculer a partir d'autre ou non ou si matrice
    if utils.checkString(value, "1234567890+-/.*%^()[],;") == -1:
        #il s'agit de nombres imaginaires ou variables a aller chercher dans data
        if utils.checkString(value, "1234567890+-/.*i%^()qwertyuiiopasdfghjklzxcvbnm") == 0:
            exp = parsExpression(value)
            if exp == "error":
                return("error")
            if calcul.calculateWithVariables(exp, data, name) == "error":
                return("error")
            else:
                return
        else:
            print("Des caracteres ne sont pas propices au calcul.")
            return("error")
    
    #enregistre la variable dans data
    exp = parsExpression(value)
    if exp == "error":
        return("error")
    if calcul.calculate(exp, data, name) == "error":
        return("error")
    
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
            #ammorce les checks avant enregistrement de la variable
            if newVarInData(res[0].replace(" ", ""), res[1].replace(" ", ""), data) == "error":
                return("error")
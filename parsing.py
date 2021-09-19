import utils
import calcul

#T'ES EN TRAIN DE BOSSER SUR LES MATRICES !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

#verifie une ligne dans une matrice
def parseLigneMatrice(i, pb, ln, lenght):
    lnLocal = 0
    found = 0
    vrb = ''
    ligne = []
    while i < lenght:
        vrb = ''
        pnt = 0
        while utils.checkChr(pb[i], "0123456789.") == 0:
            if pb[i] == '.':
                pnt += 1
            vrb = vrb + pb[i]
            found = 1
        if pnt > 1:
            print("Un nombre decimal ne peut contenir qu'un '.'.")
            return("error")
        if found == 1:
            lnLocal += 1
            if pb[i] == ',':
                ligne.append(vrb)
                i += 1
            elif pb[i] == ']':
                ligne.append(vrb)
                i += 1
                if ln == 0:
                    ln = lnLocal
                else:
                    if lnLocal != ln:
                        print("Les lignes de la matrice doivent toutes avoir le meme nombre de colonnes.")
                        return("error")
                return(ligne)
            else:
                print("Une matrice doit etre definie de la maniere suivante : [[a,b];[c,d]].")
                return("error")
        while utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm") == 0:
            if pb[i] == '.':
                pnt += 1
            vrb = vrb + pb[i]
            found = 1
        if pnt > 1:
            print("Un nombre decimal ne peut contenir qu'un '.'.")
            return("error")
        if found == 1:
            lnLocal += 1
            if pb[i] == ',':
                ligne.append(vrb)
                i += 1
            elif pb[i] == ']':
                ligne.append(vrb)
                i += 1
                if ln == 0:
                    ln = lnLocal
                else:
                    if lnLocal != ln:
                        print("Les lignes de la matrice doivent toutes avoir le meme nombre de colonnes.")
                        return("error")
                return(ligne)
            else:
                print("Une matrice doit etre definie de la maniere suivante : [[a,b];[c,d]].")
                return("error")
#gere les matrices, retourne l'indice de i pour reprendre le fil dans le parsing de l'expression
def parseMatrice(mtc, start, pb):
    if pb[start + 1] != '[':
        print("Une matrice doit etre definie de la maniere suivante : [[a,b];[c,d]].")
        return("error")
    i = start + 1
    lenght = len(pb)
    #garde en memoire la taille d'une ligne
    ln = 0
    while i < lenght:
        if pb[i] != '[':
            return("error")
        i += 1
        ligne = parseLigneMatrice(i, pb, ln, lenght)
        if ligne == "error":
            return("error")
        mtc.append(ligne)
        if pb[i] == ";":
            i += 1
        elif pb[i] == "]":
            i += 1
            return(i)
        else:
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
        #DEBUG/TEST
        print("exp = ", exp)
        print("found = ", found)
        #DEBUG/TEST
        if utils.checkChr(pb[i], "-+*^%/[,;") == 0:
            if i == 0 and (pb[i] != '-' or pb[i] != '[' or pb[i] != '('):
                print("L'expression ne peut commencer par une operation autre que '-'.")
                return("error")
            if pb[i] == '[':
                #on entre dans la definition d'une matrice
                i = parseMatrice(mtc, i, pb)
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
        if i < lenght and found > 0 and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            exp.append('*')
            found = 0
        while i < lenght and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm()") == 0:
            if pb[i] == '(' and i != j:
                prt += 1
            elif pb[i] == ')' and i != j:
                prt -= 1
            found = 2
            vrb = vrb + pb[i]
            i += 1
        if  prt != indexPrt:
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
    #DEBUG/TEST
    print("exp = ", exp)
    return(exp)
        
#parse la partie calcul
# def parsExpression(pb):
#     i = 0
#     lenght = len(pb)
#     #contient chaque partie de l'equation
#     exp = []
#     #verifie que toute parenthese ouverte est fermee plus tard
#     prt = 0
#     while i < lenght:
#         #contient le nombre ou le nom de variable en train d'etre lu
#         vrb = ''
#         #conteneur de matrice
#         mtc = []
#         if i == 0 and pb[i] == '-' or i == 0 and pb[i] == '(':
#             if pb[i] == '(':
#                 prt += 1
#             exp.append(pb[i])
#             i += 1
#         #verifie si une donnee a ete trouvee
#         found = 0
#         while i < lenght and utils.checkChr(pb[i], "0123456789") == 0:
#             found = 1
#             vrb = vrb + pb[i]
#             i += 1
#         if found == 1:
#             exp.append(vrb)
#         else:
#             while i < lenght and utils.checkChr(pb[i], "qwertyuiopasdfghjklzxcvbnm") == 0:
#                 found = 1
#                 vrb = vrb + pb[i]
#                 i += 1
#             if found == 1:
#                 exp.append(vrb)
#         if found == 1 and i < lenght :
#             if utils.checkChr(pb[i], "^%*+-/)") == 0:
#                 exp.append(pb[i])
#                 found = 0
#             else:
#                 #il n'y a pas de symbole de calcul entre deux nombres ou deux variables du coup on suppose une multiplication
#                 exp.append('*')
#                 if pb[i] != '(' and pb[i] != ')':
#                     exp.append(pb[i])
#         if i < lenght and pb[i] == '(':
#             prt += 1
#             exp.append(pb[i])
#         if i < lenght and pb[i] == ')':
#             prt -= 1
#         if prt < 0:
#             print("une parenthese fermante n'est pas accompagnee d'une ouvrante")
#             return("error")
#         i += 1
#     if prt != 0:
#         print("pb de parentheses")
#         return("error")
#     return(exp)

#cherche si le probleme est correcte ou non
def isItAProb(pb, data):
    pbm = pb.lower()
    for eachVar in data:
        if eachVar[0] == pbm:
            #renvoie la valeur de la donnnee trouvee
            print(eachVar[1])
            return
    if utils.checkString(pbm, "1234567890+-/.*%^()") == 0:
        exp = parsExpression(pbm)
        if exp == "error":
            return("error")
        if calcul.calculate(exp, data, 0) == "error":
            return("error")
    else:
        #PEUT ETRE NOMBRE IMAGINAIRE
        #PEUT ETRE MATRICE
        #VERIFIER S'IL Y A UNE FONCTION DANS DATA
        #VERIFIER S'IL Y A DES VARIABLES A REMPLACER PAR LEUR VALEUR DANS DATA
        #DEBUG/TEST
        print("calcul avec des lettres ou une matrice")
        return("error")
    return

#checke le nom de la fonction et si la fonction a bien une variable
def checkFunction(varName, varValue, data):
    if varName[0] == "i" and varName[1] == "(":
        print("Une fonction ne peut porter le nom de 'i' a cause des nombres imaginaires.")
        return("error")
    res = varName.split('(')
    ukn = res[1].split(')')
    if ukn[0] in varValue:
        exp = parsExpression(varValue)
        if exp == "error":
            return("error")
        if calcul.reduceFonction(exp, data, varName, ukn[0]) == "error":
            return("error")
        datum = [varName, varValue]
        data.append(datum)
    else:
        #il n'y a pas de variable dans la fonction
        print("Il n'y a pas de variable dans la fonction.")
        return("error")

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
        if checkFunction(name, value, data) == "error":
            return("error")
        return

    #recherche si la variable est a calculer a partir d'autre ou non ou si matrice
    if utils.checkString(value, "1234567890+-/.*%^()[],;") == -1:
        #RECHERCHER LES VARIABLES DANS DATA
        if utils.checkString(value, "1234567890+-/.*i%^()qwertyuiiopasdfghjklzxcvbnm") == 0:
            exp = parsExpression(value)
            if exp == "error":
                return("error")
            if calcul.calculateWithVariables(exp, data, name) == "error":
                return("error")
            else:
                return
        #RECHERCHER SI C EST UNE MATRICE
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
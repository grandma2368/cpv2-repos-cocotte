import utils

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
    #recherche si la variable est à calculer à partir d'autre ou non ou si matrice
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
            #verifie s'il s'agit d'une reassignation de variable
            if isReassignated(res[0].replace(" ", ""), res[1].replace(" ", ""), data) != "reassigned":
                #CHECKER S IL Y A UNE VALEUR DEJA DE DONNEE OU S'IL FAUT LA CALCULER
                #VOIR SI C'EST UNE ASSIGNATION PAR RAPPORT A UNE VARIABLE DEJA EXISTANTE
                if newVarInData(res[0].replace(" ", ""), res[1].replace(" ", ""), data) == "error":
                    return("error")
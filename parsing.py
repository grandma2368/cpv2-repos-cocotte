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

#check le nom de la fonction et si la fonction a bien une variable
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
    i = 0
    lenght = len(value)
    while i < lenght:
        agree = "azertyuiopqsdfghjklmwxcvbn()"
        if name[i] in agree:
            i += 1
        else:
            #le nom de la variable ne contient pas que des lettres --> cas d'erreur
            return("error")
    if '(' in name:
        #CHECKER LA FONCTION ET FAIRE L'ASSIGNATION DE FONCTION
        checkFunction(name, value, data)
        return
    #recherche si la variable est à calculer à partir d'autre ou non ou si matrice
    i = 0
    lenght = len(value)
    while i < lenght:
        agree = "1234567890+-/*i"
        if value[i] in agree:
            i += 1
        else:
            #RECHERCHER LES VARIABLES DANS DATA
            #RECHERCHER SI C EST UNE MATRICE
            print("pas un calcul ou une variable de deja donnee")
            return
    #enregistre la variable dans data
    datum = [name, value]
    data.append(datum)
    print(value)

#renvoie la valeur de la variable si elle est trouvee dans data
def isAlreadyExist(varName, data):
    name = varName.lower()
    for eachVar in data:
        if eachVar[0] == name:
            #renvoie la valeur de la variable trouvee
            print(eachVar[1])
            return
        else:
            #renvoie une erreur car n'a pas trouve la variable dans data
            print("Cette variable n'a pas encore ete enregistree")
    

def parsing(line, data):
    res = line.split("=")
    if len(res) == 1:
        isAlreadyExist(line.replace(" ", ""), data)
    else:
        #VERIFIER S'IL S'AGIT OU NON D'UNE REASSIGNATION DE VARIABLE
        if isReassignated(res[0].replace(" ", ""), res[1].replace(" ", ""), data) != "reassigned":
            #VERIFIER S IL S'AGIT D UN POLYNOME A RESOUDRE OU D UNE VARIABLE A ASSIGNER
            #CHECKER S IL Y A UNE VALEUR DEJA DE DONNEE OU S'IL FAUT LA CALCULER
            #VOIR SI C'EST UNE ASSIGNATION PAR RAPPORT A UNE VARIABLE DEJA EXISTANTE
            #ENTRER LA VARIABLE DANS DATA
            if newVarInData(res[0].replace(" ", ""), res[1].replace(" ", ""), data) == "error":
                return("error")
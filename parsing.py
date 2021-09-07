def newVarInData(varName, varValue, data):
    varValue.lower()
    varName.lower()
    i = 0
    lenght = len(varValue)
    while i < lenght:
        agree = "1234567890+-/*i"
        if varValue[i] in agree:
            i += 1
        else:
            #RECHERCHER LES VARIABLES DANS DATA
            print("pas un calcul ou une variable de deja donnee")
            return
    datum = [varName, varValue]
    data.append(datum)
    #POUR LE TEST
    print("variable bien enregistree")

def isAlreadyExist(varName, data):
    varName.lower()
    for eachVar in data:
        if eachVar[0] == varName:
            print("existe dans data dans fonction isAlreadyExist")
            print(eachVar[0])
            return
        else:
            print("n existe pas dans Data pour le moment")
    

def parsing(line, data):
    res = line.split("=")
    if len(res) == 1:
        isAlreadyExist(line.replace(" ", ""), data)
        #RECHERCHER SI LA VARIABLE DEMANDEE EXISTE DANS DATA --> SI OUI L AFFICHER --> SINON RENVOYER UN MESSAGE D ERREUR
        #RENVOYER ICI UN INT POUR FAIRE LE TRAITEMENT DE CA DEPUIS DATA DIRECTEMENT DANS cpv2.py
        print(line)
    else:
        #VERIFIER S IL S'AGIT D UN POLYNOME A RESOUDRE OU D UNE VARIABLE A ASSIGNER
        #CHECKER S IL Y A UNE VALEUR DEJA DE DONNEE OU S'IL FAUT LA CALCULER
        #VOIR SI C'EST UNE ASSIGNATION PAR RAPPORT A UNE VARIABLE DEJA EXISTANTE
        #ENTRER LA VARIABLE DANS DATA
        newVarInData(res[0].replace(" ", ""), res[1].replace(" ", ""), data)
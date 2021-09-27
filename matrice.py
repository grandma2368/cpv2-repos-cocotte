import utils

#checke si deux matrices ont bien la meme taille
def checkMatriceSize(a, b):
    if len(a) != len(b):
        print("Les matrices doivent etre de la meme taille pour les calculs.")
        return("error")
    elif len(a[0]) != len(b[0]):
        print("Les matrices doivent etre de la meme taille pour les calculs.")
        return("error")
    else:
        size = []
        #nb de lignes
        size.append(len(a))
        #nb de colonnes
        size.append(len(a[0]))
        return(size)

#addition matricielle
def addMatrice(a, b):
    c = []
    nbMat = 0
    if utils.checkString(str(a), "[]0123456789,;-") == 0:
        nbMat += 1
    if utils.checkString(str(b), "[]0123456789,;-") == 0:
        nbMat += 1
    if nbMat == 2:
        size = checkMatriceSize(a, b)
        if size == "error":
            return("error")
        i = 0
        while i < size[0]:
            lnA = a[i]
            lnB = b[i]
            j = 0
            lnC = []
            while j < size[1]:
                vrbC = float(lnA[j]) + float(lnB[j])
                lnC.append(vrbC)
                j += 1
            c.append(lnC)
            i += 1
        #DEBUG/TEST
        print("c = ", c)
        #DEBUG/TEST
        return(c)
    else:
        #les deux membres du calcul ne sont pas des matrices
        return("calcul")

#multiplication matricielle
def multiplyMatrice(a, b):
    c = []
    nbMat = 0
    if utils.checkString(str(a), "[]0123456789,;-") == 0:
        nbMat += 1
    if utils.checkString(str(b), "[]0123456789,;-") == 0:
        nbMat += 2
    if nbMat == 1:
        nbCol = len(b[0])
        nbLn = len(b)
        i = 0
        while i < nbLn:
            lnC = []
            j = 0
            lnB = b[i]
            while j < nbCol:
                vrbC = float(a) * float(lnB[j])
                lnC.append(vrbC)
                j += 1
            c.append(lnC)
            i += 1
        return(c)
    elif nbMat == 2:
        nbCol = len(a[0])
        nbLn = len(a)
        i = 0
        while i < nbLn:
            lnC = []
            j = 0
            lnA = a[i]
            while j < nbCol:
                vrbC = float(b) * float(lnA[j])
                lnC.append(vrbC)
                j += 1
            c.append(lnC)
            i += 1
        return(c)
    else:
        print("La multiplication entre matrice releve du calcul vectoriel qui est un bonus, il en va de meme pour la division.")
        return("error")

#division matricielle
def divideMatrice(a, b):
    c = []
    nbMat = 0
    if utils.checkString(str(a), "[]0123456789,;-") == 0:
        nbMat += 1
    if utils.checkString(str(b), "[]0123456789,;-") == 0:
        nbMat += 2
    if nbMat == 2:
        if float(a) != 0:
            print("Une division par 0 est impossible")
            return("error")
        a = 1 / float(a)
        nbCol = len(b[0])
        nbLn = len(b)
        i = 0
        while i < nbLn:
            lnC = []
            j = 0
            lnB = b[i]
            while j < nbCol:
                vrbC = float(a) * float(lnB[j])
                lnC.append(vrbC)
                j += 1
            c.append(lnC)
            i += 1
        return(c)
    elif nbMat == 1:
        if float(b) != 0:
            print("Une division par 0 est impossible")
            return("error")
        b = 1 / float(b)
        nbCol = len(a[0])
        nbLn = len(a)
        i = 0
        while i < nbLn:
            lnC = []
            j = 0
            lnA = a[i]
            while j < nbCol:
                vrbC = float(b) * float(lnA[j])
                lnC.append(vrbC)
                j += 1
            c.append(lnC)
            i += 1
        return(c)
    else:
        print("La division entre matrice releve du calcul vectoriel qui est un bonus, il en va de meme pour la multiplication.")
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
        ln = len(ligne)
        mtc.append(ligne)
        while pb[i] != ']':
            i += 1
        i += 1
        if pb[i] == ";":
            i += 1
        elif pb[i] == "]":
            i += 1
            return(i)
        else:
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
            i += 1
        if pnt > 1:
            print("Un nombre decimal ne peut contenir qu'un '.'.")
            return("error")
        if found == 1:
            lnLocal += 1
            if pb[i] == ',':
                found = 0
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
            vrb = vrb + pb[i]
            found = 1
            i += 1
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
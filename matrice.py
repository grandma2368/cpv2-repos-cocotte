import utils

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
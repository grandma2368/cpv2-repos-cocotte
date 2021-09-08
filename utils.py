#check si les elements d'agree sont dans str ou non --> erreur == -1 / succes == 0
def checkString(str, agree):
    i = 0
    lenght = len(str)
    while i < lenght:
        if str[i] in agree:
            i += 1
        else:
            return(-1)
    return(0)
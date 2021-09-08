#cherche les parentheses prioritaires
def checkParenthesis(exp):
    #recupere l'indice de la parenthese ouvrante prioritaire
    prtOpen = 0
    #vois s'il y a une parenthese fermante
    prtClosed = 0
    i = 0
    for prt in exp:
        if prt == '(':
            prtOpen = i
        if prt == ')':
            prtClosed = i
            #RENVOYER VERS UNE FONCTION QUI VA CALCULER L'ENTRE DEUX
        i += i
    if prtClosed != 0:
        checkParenthesis(exp)

#calcule une expression pour l'enregistrer dans data
def calculate(exp, data):
    checkParenthesis(exp)
    #FAIRE UNE FONCTION POUR CALCULER CE QUI RESTE DANS EXP
    return("error")
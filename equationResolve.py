import parsing
import function

#verifie si bien equation de degre 2 ou inferieur
def checkDegree(partOne, partTwo, data):
    lenghtOne = len(partOne)
    lenghtTwo = len(partTwo)
    i = 0
    while i < lenghtOne:
        if partOne[i] == '^':
            if float(partOne[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
        i += 1
    i = 0
    while i < lenghtTwo:
        if partTwo[i] == '^':
            if float(partTwo[i + 1]) > 2:
                print("Ce programme ne peut resoudre que les equations de degree 2 ou inferieur et la variable de l'equation doit etre notee x.")
                return("error")
        i += 1
    expOne = parsing.parsExpression(partOne)
    if expOne == "error":
        return("error")
    expTwo = parsing.parsExpression(partTwo)
    if expTwo == "error":
        return("error")
    if function.replaceVariablesFunction(expOne, data, 'x') == "error":
        return("error")
    if function.replaceVariablesFunction(expTwo, data, 'x') == "error":
        return("error")
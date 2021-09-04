import fileinput
import sys
import parsing

#entree du programme

#initialisation de data qui contiendra toutes les variables pdt le temps d execution du programme
data = []

#boucle pour lire sur stdin
for line in fileinput.input():
    #verifie si l'utilisateur souhaite quitter le programme et agit en consequence
    if line.rstrip() == "exit":
        sys.exit()
    parsing.parsing(line.rstrip(), data)
    #IL FAUT FAIRE DU PARSING ICI --> FAIRE UNE FONCTION DEDIEE
    #IL FAUT CHECKER SI LA VARIABLE EXISTE DEJA --> SI EXISTE REASSIGNER --> SINON CREER ENTREE ET LUI ASSIGNER VALEUR
    for test in data:
        print("varName = ", test[0].replace(" ", ""))
        print("varValue = ", test[1].replace(" ", ""))
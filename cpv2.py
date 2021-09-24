import fileinput
import sys
import parsing
import show

#entree du programme

#initialisation de data qui contiendra toutes les variables pdt le temps d execution du programme
data = []
#boucle pour lire sur stdin
for line in fileinput.input():
    #verifie si l'utilisateur souhaite quitter le programme et agit en consequence
    if line.rstrip() == "exit":
        sys.exit()
    elif line.rstrip() == "data":
        #affiche toutes les donnees de data
        show.showAllData(data)
    elif line.rstrip() == '':
        print("Veuillez entrer une expression mathematique valide.")
    else:
        parsing.parsing(line.rstrip(), data)
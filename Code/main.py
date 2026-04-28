from Jeu.jeu import jeu
from Interface.Interface import interface

def main():
    perso = interface()
    jeu(perso)

if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()
from Jeu.jeu import jeu
from Code.Interface.menu import interface

def main():
    res = interface()
    if res is not False :
        jeu(res)

if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()
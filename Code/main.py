import sys
from Jeu.jeu import jeu
from Interface.menu import interface
from Interface.utilisateur import get_user_name
from Fichiers_variables.gestion_fichiers import ajouter_utilisateur, det_noms

def main():
    running = True
    skip_intro = False
    joueur = None

    while running:
        res = interface(skip_intro=skip_intro, joueur=joueur)

        if res is False:
            running = False
        else:
            perso, joueur = res  # ← dépack les deux
            result = jeu(perso, joueur)

            if result == "menu":
                skip_intro = True
                continue
            elif result == "quit":
                running = False
if __name__ == "__main__":
    main()

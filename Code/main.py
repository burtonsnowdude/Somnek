import sys
from Jeu.jeu import jeu
from Interface.menu import interface

def main():
    running = True
    skip_intro = False
    joueur = None

    while running:
        res = interface(skip_intro=skip_intro, joueur=joueur)

        if res is False:
            running = False
        else:
            perso, map_choisie ,joueur = res  # ← interface retourne (perso, map)
            result = jeu(perso, joueur, map_choisie)

            if result == "menu":
                skip_intro = True
                continue
            elif result == "quit":
                running = False

if __name__ == "__main__":
    main()
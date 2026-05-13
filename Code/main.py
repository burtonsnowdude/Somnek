"""
Main

"""
import sys
from Jeu.jeu import jeu
from Interface.menu import interface
from Interface.video import play_video 

def main():
    running = True
    skip_intro = False
    joueur = None
    play_video("extrait_trailer", 13, 23, 12)
    while running:
        res = interface(skip_intro=skip_intro, joueur=joueur)

        if res is False:
            running = False
        else:
            perso, map_choisie ,joueur = res 
            result = jeu(perso, joueur, map_choisie)

            if result == "menu":
                skip_intro = True
                continue
            elif result == "quit":
                running = False

if __name__ == "__main__":
    main()
import pygame as pyg
from player import *
import time

def draw(player, temp_ecoulé, monster): # dessiner tout
    WIN.blit(BG, (0, 0)) # fond d'ecran

    pyg.draw.rect(WIN, (255, 0, 0), player) # dessiner le joueur (rectangle rouge)
    pyg.draw.rect(WIN, (0, 255, 0), monster) # dessiner le joueur (rectangle rouge)

    if temp_ecoulé < 60: # calculer les minutes et secondes seulement si besoin

        time_text = FONT.render(f"{int(temp_ecoulé)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    else:
        min = temp_ecoulé // 60 # calculer les minutes
        sec = temp_ecoulé % 60 # calculer les secondes

        time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    WIN.blit(time_text, (10, 10)) # afficher le texte du temps ecoulé

    pyg.display.update() # mettre a jour l'affichage


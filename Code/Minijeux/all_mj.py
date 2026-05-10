from Minijeux.minijeu2 import minijeu2 
from Minijeux.minijeu3 import minijeu3
from Minijeux.minijeu1 import minijeu1
import pygame as pyg
from Interface.choix_map import IMAGES_MAPS



def mj(perso, coord_monde, minijeu_fini, p, armes_possedees, armes_joueur, map):
    if map == "Rue" :
        map = pyg.image.load("Images/Maps/map_rue.png")
        if not minijeu_fini :
            if perso == "Fille_populaire":
                coord_monde, minijeu_fini, armes_possedees, armes_joueur = minijeu2(p, coord_monde, minijeu_fini, armes_possedees, armes_joueur, map)
            elif perso == "Nonne":
                coord_monde, minijeu_fini, armes_possedees, armes_joueur = minijeu3(p, coord_monde, minijeu_fini, armes_possedees, armes_joueur, map)
            else :
                coord_monde, minijeu_fini = minijeu1(p, coord_monde, minijeu_fini, map)
    return coord_monde, minijeu_fini, armes_possedees, armes_joueur
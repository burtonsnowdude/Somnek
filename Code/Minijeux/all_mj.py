"""
Gère les mini-jeux
"""
from Minijeux.minijeu2 import minijeu2 
from Minijeux.minijeu3 import minijeu3
from Minijeux.minijeu1 import minijeu1
import pygame as pyg

def mj(perso, coord_monde, minijeu_fini, p, armes_et_items_possedees, armes_possedees, armes_joueur, map):
    """Gestion du mini-jeu de chaque personnage
    
    Parameters
    ----------
    perso : str
        Perso choisi
    coord_monde : tuple(int, int)
        Coordonnées monde du magasin/eglise
    minijeu_fini : bool
        Si le mini-jeu est fini ou pas
    p : Self@Player
        Le joueur
    armes_et_items_possedees : list
        Liste des armes et items possédés
    armes_possedees : list
        Liste des armes possédées
    armes_joueur : list(dict)
        Contenu actualisé du fichier csv des armes
    map : str
        La map actuelle

    Returns
    -------
    quasiment les mêmes choses je vais pas tout recopier
    """
    if map == "Rue" :
        map = pyg.image.load("Images/Maps/map_rue.png")
        if not minijeu_fini :
            if perso == "Fille_populaire":
                coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees,armes_joueur = minijeu2(p, coord_monde, minijeu_fini, armes_et_items_possedees,armes_possedees, armes_joueur, map)
            elif perso == "Nonne":
                coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees,armes_joueur = minijeu3(p, coord_monde, minijeu_fini,  armes_et_items_possedees,armes_possedees, armes_joueur, map)
            else :
                coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees,armes_joueur = minijeu1(p, coord_monde, minijeu_fini,  armes_et_items_possedees,armes_possedees, armes_joueur, map)
    return coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees,armes_joueur
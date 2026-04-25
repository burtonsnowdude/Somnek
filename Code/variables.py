import pygame as pyg
pyg.font.init() # initialiser le module font de pygame
from traitement_images import *
from math import ceil

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre

WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre

pyg.display.set_caption("Somnek") 
FONT = pyg.font.SysFont("Press Start 2P", 24) # definir la police d'ecriture

CENTREx, CENTREy = WIDTH//2, HEIGHT//2 
PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 2 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur

FREQUENCE = 50

CATEGORIE = {}
for i in range(1, 51):
    t = "Type " + str(i)
    CATEGORIE[t] = {"puissance" : i,
                "hp" : 5*i,
                "vitesse" : ceil(i/10),
                "niveau" : i}
    
TYPES_MONSTRES = {

    # NERD
    "Dragon" : { ** CATEGORIE["Type 1"],
                "perso" : "Nerd",
                "anim" : ANIM_DRAGON},
    "Sorcier" : {** CATEGORIE["Type 2"],
                "perso" : "Nerd",
                "image" : SORCIER},
    "Araignée" : {** CATEGORIE["Type 4"],
                "perso" : "Nerd",
                "image" : SPIDER},
    "Creeper" : {** CATEGORIE["Type 6"],
                "perso" : "Nerd",
                "image" : CREEPER},
    "Seau" : {** CATEGORIE["Type 8"],
                "perso" : "Nerd",
                "image" : SEAU},
    "Savon" : {** CATEGORIE["Type 10"],
                "perso" : "Nerd",
                "image" : SAVON},
    "Ballon_basket" : {** CATEGORIE["Type 12"],
                "perso" : "Nerd",
                "image" : BALLON_BASKET},
    "Ballon_foot" : {** CATEGORIE["Type 14"],
                "perso" : "Nerd",
                "anim" : ANIM_BALLON},
    "Grand_mere" : {** CATEGORIE["Type 18"],
                "perso" : "Nerd",
                "anim" : ANIM_GRAND_MERE},
    "Fille_populaire" : {** CATEGORIE["Type 20"],
                "perso" : "Nerd",
                "image" : FILLE_POPULAIRE},
    "Telephone" : {** CATEGORIE["Type 22"],
                "perso" : "Nerd",
                "anim" : ANIM_TELEPHONE},
    "Ecouteur" : {** CATEGORIE["Type 24"],
                "perso" : "Nerd",
                "image" : ECOUTEUR},
    "Prof" : {** CATEGORIE["Type 26"],
                "perso" : "Nerd",
                "anim" : ANIM_PROF},


    # FILLE POPULAIRE           
    "Demaquillant" : {** CATEGORIE["Type 1"],
                "perso" : "Fille_populaire",
                "image" : DEMAQUILLANT},
    "Eval" : {** CATEGORIE["Type 2"],
                "perso" : "Fille_populaire",
                "image" : EVAL},
    "Fond_de_teint" : {** CATEGORIE["Type 4"],
                "perso" : "Fille_populaire",
                "image" : FOND_DE_TEINT},
    "Skinny" : { ** CATEGORIE["Type 6"],
                "perso" : "Fille_populaire",
                "image" : SKINNY}
    
}

TYPES = [type for type in TYPES_MONSTRES]

# Dictionnaire ARMES qui n'a aucun sens juste pour test mon code

ARMES = {}
for i in range(1,61):
    ARMES["nawak"+str(i)] = i

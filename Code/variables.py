import pygame as pyg
pyg.font.init() # initialiser le module font de pygame
from traitement_images import *

# Couleurs
G1 = (0, 255, 120)
G2 = (0, 180, 80)
G3 = (0, 100, 40)
G4 = (0, 20, 0)

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre

WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre

pyg.display.set_caption("Somnek") 
FONT = pyg.font.SysFont("Press Start 2P", 24) # definir la police d'ecriture

CENTREx, CENTREy = WIDTH//2, HEIGHT//2 
PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 2 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur

CATEGORIE = {}
for i in range(1, 51):
    t = "Type " + str(i)
    CATEGORIE[t] = {"puissance" : i,
                "hp" : 5*i,
                "vitesse" : i,
                "niveau" : i}
    
TYPES_MONSTRES = {
    "Dragon" : { ** CATEGORIE["Type 1"],
                "anim" : ANIM_DRAGON},
    "Sorcier" : {** CATEGORIE["Type 1"],
                "image" : SORCIER},
    "Araignée" : {** CATEGORIE["Type 1"],
                "image" : SPIDER},
    "Creeper" : {** CATEGORIE["Type 1"],
                "image" : SORCIER}
}

TYPES = [type for type in TYPES_MONSTRES]

# Dictionnaire ARMES qui n'a aucun sens juste pour test mon code

ARMES = {}
for i in range(1,61):
    ARMES["nawak"+str(i)] = i

import pygame as pyg
pyg.font.init() # initialiser le module font de pygame

PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 5 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur
MONSTER_VIT= 1

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre
CENTREx, CENTREy = WIDTH/2 - PLAYER_WIDTH, HEIGHT/2 - PLAYER_HEIGHT# coordonnees du centre de la fenetre
WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre
pyg.display.set_caption("Player Movement Example") 

BG = pyg.image.load("background.jpg") # charger le fond d'ecran


FONT = pyg.font.SysFont("comicsans", 30) # definir la police d'ecriture
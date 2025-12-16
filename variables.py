import pygame as pyg

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre
WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre
pyg.display.set_caption("Player Movement Example") 

BG = pyg.transform.scale(pyg.image.load("background.jpg"), (WIDTH, HEIGHT)) # charger et redimensionner le fond d'ecran


PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 5 # vitesse de deplacement du joueur
PLAYER_PV = 10 # points de vie du joueur
MONSTER_VIT= 1

FONT = pyg.font.SysFont("comicsans", 30) # definir la police d'ecriture
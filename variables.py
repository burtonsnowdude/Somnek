import pygame as pyg
pyg.font.init() # initialiser le module font de pygame

PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 5 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur

# Couleurs
G1 = (0, 255, 120)
G2 = (0, 180, 80)
G3 = (0, 100, 40)
G4 = (0, 20, 0)
WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre
CENTREx, CENTREy = WIDTH/2 - PLAYER_WIDTH, HEIGHT/2 - PLAYER_HEIGHT# coordonnees du centre de la fenetre
WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre
pyg.display.set_caption("Player Movement Example") 

BG = pyg.image.load("background.jpg") # charger le fond d'ecran

FONT = pyg.font.SysFont("comicsans", 30) # definir la police d'ecriture

TYPES = ["Dragon", "Sorcier", "Araignée", "Creeper"]

TYPES_MONSTRES = {
    "Dragon" : (1, 5, G4, 1),
    "Sorcier" : (1, 3, G2, 1),
    "Araignée" : (1, 2, G1, 2),
    "Creeper" : (1, 4, G3, 2)
}

keys = pyg.key.get_pressed()
UP = keys[pyg.K_UP] or keys[pyg.K_w]
RIGHT = keys[pyg.K_RIGHT] or keys[pyg.K_d]
LEFT = keys[pyg.K_LEFT] or keys[pyg.K_a]
DOWN = keys[pyg.K_DOWN] or keys[pyg.K_s]
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
pyg.display.set_caption("Somnek") 

BG = pyg.image.load("background.jpg") # charger le fond d'ecran
BG = pyg.transform.scale(BG, (800, 600))
FONT = pyg.font.SysFont("comicsans", 20) # definir la police d'ecriture

TYPES_MONSTRES = {
    "Dragon" : {"puissance" : 1,
                "hp" : 5,
                "couleur" : G4, 
                "vitesse" : 1},
    "Sorcier" : {"puissance" : 1,
                "hp" : 3,
                "couleur" : G2, 
                "vitesse" : 1},
    "Araignée" : {"puissance" : 1,
                "hp" : 2,
                "couleur" : G1, 
                "vitesse" : 2},
    "Creeper" : {"puissance" : 1,
                "hp" : 4,
                "couleur" : G3, 
                "vitesse" : 2}
}

TYPES = [type for type in TYPES_MONSTRES]

# Dictionnaire ARMES qui n'a aucun sens juste pour test mon code
ARMES = {}
for i in range(1,61):
    ARMES["nawak"+str(i)] = i
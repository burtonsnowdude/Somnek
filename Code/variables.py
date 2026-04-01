import pygame as pyg
pyg.font.init() # initialiser le module font de pygame

PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 3.5 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur

# Images
PLAYER_IMAGE = pyg.image.load("Images/perso.png")
XP = pyg.image.load("Images/xp.jpg")
BG = pyg.image.load("Images/grass.png") # charger le fond d'ecran
BG = pyg.transform.scale(BG, (800, 600))
FLECHE = pyg.image.load("Images/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/tresor.png")

# Couleurs
G1 = (0, 255, 120)
G2 = (0, 180, 80)
G3 = (0, 100, 40)
G4 = (0, 20, 0)

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre
CENTREx, CENTREy = WIDTH/2 - PLAYER_WIDTH, HEIGHT/2 - PLAYER_HEIGHT# coordonnees du centre de la fenetre
WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre
pyg.display.set_caption("Somnek") 
FONT = pyg.font.SysFont("Press Start 2P", 24) # definir la police d'ecriture


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
"""
Carac_base_arme = {
        "type_arme" : None,
        "dgbase" : 0,
        "prix" : 0,
        "portee" : 0,
        "reduction" : 0,
        "niveau_req" : 0,
        "niveau" : None}
ARMES = {
        "Epee_bleu" : {"dgbase" : 4,
                       "prix" : 0,
                       "niveau_req" : 0,
                        "niveau" : None
                        },
        "Clé_usb" : {"dgbase" : 23,
                     "prix" : 9,
                     "niveau_req" : 4},
        "Epee_enflammee" : {"dgbase" : 10,
                            "prix" : 2,
                            "niveau_req" : 4}
    }
for arme in ARMES : 
         for cle in Carac_base_arme :
            ARMES[arme][cle] = Carac_base_arme[cle]
"""
ARMES = {}
for i in range(1,61):
    ARMES["nawak"+str(i)] = i
"""
Carac_de_base_item = {
    "type_item": None,
    "hp": 0,
    "hp_max": 0,
    "prix": 0,
    "niveau_requis": 0,
    "degat": None,
    "durabilite": None,
    "refroidissement": None,
    "recuperation": None,
    "vitesse_du_j": None,
    "chance": None,
    "cupidite": None,
    "attirance": None,
    "malchance": None,
    "zone": None,
    "resurrection": None,
    "dernier_tir": None,
    "portee_xp": None,
    "refroidir": None,
    "quantite": 5,
    "sante" : None
} 

ITEMS = {
        "Parfum_Dioru": {
            "refroidir": 30,
            "prix": 5
        },
        "Gloss_rose": {
            "attirance": 15,
            "prix": 3
        },
        "Chew_gum": {
            "sante": 0.2,
            "prix": 2
        },
        "Talons_noirs": {
            "vitesse_du_j": 0.2,
            "prix": 7
        },
        "Crop_top_rose": {
            "protection": 0.2,
            "prix": 6
        }
    }

for item in ITEMS : 
         for cle in Carac_de_base_item :
            ITEMS[item][cle] = Carac_de_base_item[cle]
"""
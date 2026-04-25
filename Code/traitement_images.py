import pygame as pyg


PLAYER_IMAGE = pyg.image.load("Images/Persos/perso.png")
XP = pyg.image.load("Images/Autre/xp.jpg")
BG = pyg.image.load("Images/Maps/grass.png") # charger le fond d'ecran
BG = pyg.transform.scale(BG, (800, 600))
FLECHE = pyg.image.load("Images/Coffres/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/Coffres/tresor.png")
ARGENT = pyg.image.load("Images/Coffres/argent.png")

#MONSTRES NERD
SPIDER = pyg.image.load("Images/Monstres/spider.png")
SORCIER = pyg.image.load("Images/Monstres/sorcier.png")
ECOUTEUR = pyg.image.load("Images/Monstres/ecouteur.png")
SEAU = pyg.image.load("Images/Monstres/seau.png")
SAVON = pyg.image.load("Images/Monstres/savon.png")
CREEPER = pyg.image.load("Images/Monstres/creeper.png")

# MONSTRES FILLE POPULAIRE
PALETTE = pyg.image.load("Images/Monstres/palette.png")
FOND_DE_TEINT = pyg.image.load("Images/Monstres/fond_de_teint.png")
EVAL = pyg.image.load("Images/Monstres/eval.png")
DEMAQUILLANT = pyg.image.load("Images/Monstres/demaquillant.png")
SKINNY = pyg.image.load("Images/Monstres/skinny.png")

# MONSTRES NONNE
CHEWING_GUM = pyg.image.load("Images/Monstres/chewing_gum.png")
OSTIE = pyg.image.load("Images/Monstres/ostie.png")

#SPRITESHEET
spritesheet_coffre = pyg.image.load("Images/Coffres/anim_coffre.png")
spritesheet_dragon = pyg.image.load("Images/Monstres/dragon.png")
spritesheet_ballon = pyg.image.load("Images/Monstres/ballon_foot.png")
spritesheet_nonne = pyg.image.load("Images/Monstres/nonne.png")
spritesheet_grand_mere = pyg.image.load("Images/Monstres/grand_mere.png")
spritesheet_harceleur = pyg.image.load("Images/Monstres/harceleur.png")
spritesheet_croix = pyg.image.load("Images/Armes_items/croix.png")

def decouper_image(image, cols, rows, nb_a_enlever):
    sheet_w, sheet_h = image.get_size()
    width = sheet_w // cols
    height = sheet_h // rows

    tableau_images = [[image.subsurface((x * width, y * height, width, height)) for x in range(cols)] for y in range(rows)]
    anim = []
    for i in range(len(tableau_images)-1):
        anim += tableau_images[i]
    for i in range(nb_a_enlever):
        anim.pop(-1)
    return anim

ANIM_COFFRE = decouper_image(spritesheet_coffre, 4, 3, 0)
ANIM_DRAGON = decouper_image(spritesheet_dragon, 3, 4, 3)
ANIM_BALLON = decouper_image(spritesheet_ballon, 2, 2, 0)
ANIM_NONNE = decouper_image(spritesheet_nonne, 5, 5, 4)
ANIM_GRAND_MERE = decouper_image(spritesheet_grand_mere, 1, 2, 0)
ANIM_HARCELEUR = decouper_image(spritesheet_harceleur, 3, 4, 2)
ANIM_CROIX = decouper_image(spritesheet_croix, 2, 2, 0)
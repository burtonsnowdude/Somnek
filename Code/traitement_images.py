import pygame as pyg


PLAYER_IMAGE = pyg.image.load("Images/Persos/perso.png")
XP = pyg.image.load("Images/Autre/xp.jpg")
BG = pyg.image.load("Images/Maps/grass.png") # charger le fond d'ecran
BG = pyg.transform.scale(BG, (800, 600))
FLECHE = pyg.image.load("Images/Coffres/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/Coffres/tresor.png")
ARGENT = pyg.image.load("Images/Coffres/argent.png")

#MONSTRES
SPIDER = pyg.image.load("Images/Monstres/spider.png")
SORCIER = pyg.image.load("Images/Monstres/sorcier.png")
CHEWING_GUM = pyg.image.load("Images/Monstres/chewing_gum.png")
ECOUTEUR = pyg.image.load("Images/Monstres/ecouteur.png")
EVAL = pyg.image.load("Images/Monstres/eval.png")
OSTIE = pyg.image.load("Images/Monstres/ostie.png")
FOND_DE_TEINT = pyg.image.load("Images/Monstres/fond_de_teint.png")
SEAU = pyg.image.load("Images/Monstres/seau.png")
PALETTE = pyg.image.load("Images/Monstres/palette.png")

#SPRITESHEET
spritesheet_coffre = pyg.image.load("Images/Coffres/anim_coffre.png")
spritesheet_dragon = pyg.image.load("Images/Monstres/dragon.png")

def decouper_image(image, cols, rows):
    sheet_w, sheet_h = image.get_size()
    cols = 4
    rows = 3
    width = sheet_w // cols
    height = sheet_h // rows

    tableau_images = [
        [
            image.subsurface(
                (x * width, y * height, width, height)
            )
            for x in range(cols)]
        for y in range(rows)
    ]
    anim = []
    for i in range(len(tableau_images)-1):
        anim += tableau_images[i]
    return anim

ANIM_COFFRE = decouper_image(spritesheet_coffre, 4, 3)
ANIM_DRAGON = decouper_image(spritesheet_dragon, 3, 4)

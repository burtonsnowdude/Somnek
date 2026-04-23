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

#ANIM COFFRE
spritesheet_coffre = pyg.image.load("Images/Coffres/anim_coffre.png")
sheet_w, sheet_h = spritesheet_coffre.get_size()
cols = 4
rows = 3
COFFRE_W = sheet_w // cols
COFFRE_H = sheet_h // rows

tableau_images = [
    [
        spritesheet_coffre.subsurface(
            (x * COFFRE_W, y * COFFRE_H, COFFRE_W, COFFRE_H)
        )
        for x in range(cols)]
    for y in range(rows)
]
ANIM_COFFRE = []
for i in range(len(tableau_images)-1):
    ANIM_COFFRE += tableau_images[i]



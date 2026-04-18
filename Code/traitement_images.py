import pygame as pyg

# Images
PLAYER_IMAGE = pyg.image.load("Images/perso.png")
XP = pyg.image.load("Images/xp.jpg")
BG = pyg.image.load("Images/grass.png") # charger le fond d'ecran
BG = pyg.transform.scale(BG, (800, 600))
FLECHE = pyg.image.load("Images/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/tresor.png")
SPIDER = pyg.image.load("Images/spider.png")
SORCIER = pyg.image.load("Images/sorcier.png")

#anim coffre
spritesheet_coffre = pyg.image.load("Images/anim_coffre.png")

sheet_w, sheet_h = spritesheet_coffre.get_size()

cols = 4
rows = 3

image_width = sheet_w // cols
image_height = sheet_h // rows

ANIM_COFFRE = [
    
        spritesheet_coffre.subsurface(
            (x * image_width, y * image_height, image_width, image_height)
        )
        for x in range(cols)
    
    for y in range(rows)
]



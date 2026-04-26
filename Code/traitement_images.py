import pygame as pyg

################################ IMAGES FIXES ############################

PLAYER_IMAGE = pyg.image.load("Images/Persos/perso.png")
XP = pyg.image.load("Images/Autre/xp.jpg")
BG = pyg.image.load("Images/Maps/grass.png") # charger le fond d'ecran
BGX, BGY = BG.get_size()
FLECHE = pyg.image.load("Images/Coffres/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/Coffres/tresor.png")
ARGENT = pyg.image.load("Images/Coffres/argent.png")

#PERSONNAGES
FILLE_POPULAIRE = pyg.image.load("Images/Persos/fille_populaire.png")

#MONSTRES NERD
SPIDER = pyg.image.load("Images/Monstres/spider.png")
ECOUTEUR = pyg.image.load("Images/Monstres/ecouteur.png")
SEAU = pyg.image.load("Images/Monstres/seau.png")
SAVON = pyg.image.load("Images/Monstres/savon.png")
BALLON_BASKET = pyg.image.load("Images/Monstres/ballon_basket.png")
DARK_VADARO = pyg.image.load("Images/Monstres/dark_vadaro.png")

# MONSTRES FILLE POPULAIRE
PALETTE = pyg.image.load("Images/Monstres/palette.png")
FOND_DE_TEINT = pyg.image.load("Images/Monstres/fond_de_teint.png")
EVAL = pyg.image.load("Images/Monstres/eval.png")
DEMAQUILLANT = pyg.image.load("Images/Monstres/demaquillant.png")


# MONSTRES NONNE
CHEWING_GUM = pyg.image.load("Images/Monstres/chewing_gum.png")
CROIX_ENVERS = pyg.image.load("Images/Monstres/croix_envers.png")
OSTIE_PERIMEE = pyg.image.load("Images/Monstres/ostie_perimee.png")
MONDE = pyg.image.load("Images/Monstres/monde.png")
########################### ANIMS ######################################

#SPRITESHEET
spritesheet_coffre = pyg.image.load("Images/Coffres/anim_coffre.png")

# NERD
spritesheet_dragon = pyg.image.load("Images/Monstres/dragon.png")
spritesheet_ballon = pyg.image.load("Images/Monstres/ballon_foot.png")
spritesheet_grand_mere = pyg.image.load("Images/Monstres/grand_mere.png")
spritesheet_harceleur = pyg.image.load("Images/Monstres/harceleur.png")
spritesheet_telephone = pyg.image.load("Images/Monstres/telephone.png")
spritesheet_prof = pyg.image.load("Images/Monstres/prof.png")
spritesheet_creeper = pyg.image.load("Images/Monstres/creeper.png")
spritesheet_sorcier = pyg.image.load("Images/Monstres/sorcier.png")
spritesheet_ordi_mutant = pyg.image.load("Images/Monstres/ordi_mutant.png")

# FILLE POPULAIRE
spritesheet_chewing_gum_sale = pyg.image.load("Images/Monstres/chewing_gum_sale.png")
spritesheet_skinny = pyg.image.load("Images/Monstres/skinny.png")
spritesheet_avion = pyg.image.load("Images/Monstres/avion.png")
spritesheet_lunettes = pyg.image.load("Images/Monstres/lunettes.png")
spritesheet_out_of_stock = pyg.image.load("Images/Monstres/out_of_stock.png")
spritesheet_caca = pyg.image.load("Images/Monstres/caca.png")

# NONNE
spritesheet_nonne = pyg.image.load("Images/Monstres/nonne.png")
spritesheet_croix = pyg.image.load("Images/Armes_items/croix.png")
spritesheet_homme_mi_demon = pyg.image.load("Images/Monstres/homme_mi_demon.png")
spritesheet_bisous =  pyg.image.load("Images/Monstres/bisous.png")
spritesheet_666 = pyg.image.load("Images/Monstres/666.png")
spritesheet_fruit_defendu = pyg.image.load("Images/Monstres/fruit_defendu.png")
spritesheet_miroir = pyg.image.load("Images/Monstres/miroir.png")

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

# NERD
ANIM_DRAGON = decouper_image(spritesheet_dragon, 3, 4, 3)
ANIM_BALLON = decouper_image(spritesheet_ballon, 2, 2, 0)
ANIM_GRAND_MERE = decouper_image(spritesheet_grand_mere, 1, 2, 0)
ANIM_HARCELEUR = decouper_image(spritesheet_harceleur, 3, 4, 2)
ANIM_TELEPHONE = decouper_image(spritesheet_telephone, 2, 2, 0)
ANIM_PROF = decouper_image(spritesheet_prof, 3, 3, 1)
ANIM_ORDI_MUTANT = decouper_image(spritesheet_ordi_mutant, 2, 2, 0)
ANIM_CREEPER = decouper_image(spritesheet_creeper, 3, 3, 2)
ANIM_SORCIER = decouper_image(spritesheet_sorcier, 2, 3, 0)

# FILLE POPULAIRE
ANIM_SKINNY = decouper_image(spritesheet_skinny, 3, 3, 0)
ANIM_AVION = decouper_image(spritesheet_avion, 3, 3, 2)
ANIM_CHEWING_GUM_SALE = decouper_image(spritesheet_chewing_gum_sale, 2, 2, 0)
ANIM_LUNETTES = decouper_image(spritesheet_lunettes, 3, 3, 0)
ANIM_OUT_OF_STOCK = decouper_image(spritesheet_out_of_stock, 2, 2, 0)
ANIM_CACA = decouper_image(spritesheet_caca, 2, 2, 0)

# NONNE
ANIM_NONNE = decouper_image(spritesheet_nonne, 5, 5, 4)
ANIM_CROIX = decouper_image(spritesheet_croix, 2, 2, 0)
ANIM_HOMME_MI_DEMON = decouper_image(spritesheet_homme_mi_demon, 2, 3, 0)
ANIM_BISOUS = decouper_image(spritesheet_bisous, 3, 3, 0)
ANIM_666 = decouper_image(spritesheet_666, 2, 3, 1)
ANIM_FRUIT_DEFENDU = decouper_image(spritesheet_fruit_defendu, 3, 3, 1)
ANIM_MIROIR = decouper_image(spritesheet_miroir, 3, 4, 0)
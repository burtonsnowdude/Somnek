import pygame as pyg

##############################################################################################################
def decouper_image(image, cols, rows, nb_a_enlever):
    sheet_w, sheet_h = image.get_size()
    width = sheet_w // cols
    height = sheet_h // rows

    tableau_images = [[image.subsurface((x * width, y * height, width, height)) for x in range(cols)] for y in range(rows)]
    anim = []
    for i in range(len(tableau_images)):
        anim += tableau_images[i]
    for i in range(nb_a_enlever):
        anim.pop(-1)
    return anim

################################ IMAGES FIXES ################################################################

XP = pyg.image.load("Images/Autre/xp.jpg")
BG = pyg.image.load("Images/Maps/map_foire.png") # charger le fond d'ecran
BGX, BGY = BG.get_size()
FLECHE = pyg.image.load("Images/Coffres/fleche.png")
FLECHE = pyg.transform.smoothscale(FLECHE, (30, 50))
TRESOR = pyg.image.load("Images/Coffres/tresor.png")
ARGENT = pyg.image.load("Images/Coffres/argent.png")
KILL_SIGN = pyg.image.load("Images/Autre/kill.png")


########################### ARMES ET ITEMS ##########################################################################

# NERD
LUNETTES_CASSEES = pyg.image.load("Images/Armes_items/lunettes_cassees.png")
BERSEK = pyg.image.load("Images/Armes_items/berserk.png")
CAHIER_DE_NSI = pyg.image.load("Images/Armes_items/cahier_de_nsi.png")
NAIN = pyg.image.load("Images/Armes_items/nain.png")
CHAUSSETTES = pyg.image.load("Images/Armes_items/chaussettes.png")
SOURIS = pyg.image.load("Images/Armes_items/souris.png")
CLE_USB = pyg.image.load("Images/Armes_items/cle_usb.png")
PISTOLETS =  pyg.image.load("Images/Armes_items/pistolets.png")
CHARIOT_VIOLET = pyg.image.load("Images/Armes_items/chariot_violet.png")
POMME_SCIENTIFIQUE = pyg.image.load("Images/Armes_items/pomme_scientifique.png")
VODY = pyg.image.load("Images/Armes_items/vody.png")
AMBROISIE = pyg.image.load("Images/Armes_items/ambroisie.png")
NOKIA = pyg.image.load("Images/Armes_items/nokia.png")
TREFLE = pyg.image.load("Images/Armes_items/trefle.png")
ARMURE = pyg.image.load("Images/Armes_items/armure de bronze.png")
CONSOLE = pyg.image.load("Images/Armes_items/console.png")
SERVIETTE = pyg.image.load("Images/Armes_items/serviette_nettoyante.png")
spritesheet_epee_bleue = pyg.image.load("Images/Armes_items/epee_bleue.png")
ANIM_EPEE_BLEUE = decouper_image(spritesheet_epee_bleue, 5, 1, 0)
EPEE_GUTS = pyg.image.load("Images/Armes_items/epee_guts.png")

# FILLE POPULAIRE
GLOSS_ROSE = pyg.image.load("Images/Armes_items/gloss_rose.png")
TICKET =  pyg.image.load("Images/Armes_items/ticket.png")
HIGLIGHTER =  pyg.image.load("Images/Armes_items/highlighter.png")
FAUX_CILS = pyg.image.load("Images/Armes_items/faux_cils.png")
BRACELET_SOEUR = pyg.image.load("Images/Armes_items/bracelet_soeur.png")
CARTE_BLEU = pyg.image.load("Images/Armes_items/carte_bleu.png")
PILULE_VERTE = pyg.image.load("Images/Armes_items/pilule_verte.png")
MOUSSE_VANILLE = pyg.image.load("Images/Armes_items/mousse_vanille.png")
DEMAQUILLANT = pyg.image.load("Images/Armes_items/demaquillant.png")
PARFUM_DIORU = pyg.image.load("Images/Armes_items/parfum_dioru.png")
MINUTEUR = pyg.image.load("Images/Armes_items/minuteur.png")
CHEW_GUM = pyg.image.load("Images/Armes_items/chew_gum.png")
CROP_TOP_ROSE = pyg.image.load("Images/Armes_items/crop_top_rose.png")
TALON_NOIR = pyg.image.load("Images/Armes_items/talon_noir.png")
TALON_LOUBOUTIN = pyg.image.load("Images/Armes_items/talon_louboutin.png")
IPHONE_2000 = pyg.image.load("Images/Armes_items/iphone 2000.png")
PASS_NAVIGO = pyg.image.load("Images/Armes_items/pass navigo.png")
FER_A_LISSER = pyg.image.load("Images/Armes_items/fer_à_lisser.png")
JEAN_STANLEY = pyg.image.load("Images/Armes_items/jean_stanley_cup.png")
CHARGEUR = pyg.image.load("Images/Armes_items/chargeur.png")


# NONNE 
CROIX_DE_BASE = pyg.image.load("Images/Armes_items/croix_de_base.png")
COURONNE =  pyg.image.load("Images/Armes_items/couronne.png")
FEU_SAINT =  pyg.image.load("Images/Armes_items/projectile/feu esprit sain.png")
BOUGIE = pyg.image.load("Images/Armes_items/bougie.png")
BOURSE = pyg.image.load("Images/Armes_items/bourse.png")
OSTIE = pyg.image.load("Images/Armes_items/ostie.png")
BOULE_DENERGIE = pyg.image.load("Images/Armes_items/boule_denergie.png")
EAU_BENITE = pyg.image.load("Images/Armes_items/eau_bénite.png")
MOCASSIN = pyg.image.load("Images/Armes_items/mocassin.png")
HALO_LUMINEUX= pyg.image.load("Images/Armes_items/halo_lumineux.png")
MEDAILLON = pyg.image.load("Images/Armes_items/medaillon.png")
VOILE = pyg.image.load("Images/Armes_items/voile.png")
###################################### PERSONNAGES ##########################################################
# FILLE POPULAIRE
FILLE_POPULAIRE_L = pyg.image.load("Images/Persos/fille_populaire_l.png")
FILLE_POPULAIRE_R = pyg.image.load("Images/Persos/fille_populaire_r.png")
spritesheet_fille_populaire_avant = pyg.image.load("Images/Persos/fille_populaire_avant.png")
spritesheet_fille_populaire_arriere = pyg.image.load("Images/Persos/fille_populaire_arriere.png")
spritesheet_fille_populaire_horizon_r = pyg.image.load("Images/Persos/fille_populaire_horizon_r.png")
spritesheet_fille_populaire_horizon_l = pyg.image.load("Images/Persos/fille_populaire_horizon_l.png")
ANIM_FILLE_POPULAIRE_AVANT = decouper_image(spritesheet_fille_populaire_avant, 16, 1, 0)
ANIM_FILLE_POPULAIRE_ARRIERE = decouper_image(spritesheet_fille_populaire_arriere, 16, 1, 0)
ANIM_FILLE_POPULAIRE_HORIZON_R = decouper_image(spritesheet_fille_populaire_horizon_r, 2, 3, 0)
ANIM_FILLE_POPULAIRE_HORIZON_L = decouper_image(spritesheet_fille_populaire_horizon_l, 2, 3, 0)

#NERD
spritesheet_nerd_avant = pyg.image.load("Images/Persos/nerd_avant.png")
spritesheet_nerd_arriere = pyg.image.load("Images/Persos/nerd_arriere.png")
spritesheet_nerd_horizon_r = pyg.image.load("Images/Persos/nerd_horizon_r.png")
spritesheet_nerd_horizon_l = pyg.image.load("Images/Persos/nerd_horizon_l.png")
ANIM_NERD_AVANT = decouper_image(spritesheet_nerd_avant, 4, 5, 3)
ANIM_NERD_ARRIERE = decouper_image(spritesheet_nerd_arriere, 4, 4, 0)
ANIM_NERD_HORIZON_R = decouper_image(spritesheet_nerd_horizon_r, 3, 3, 0)
ANIM_NERD_HORIZON_L = decouper_image(spritesheet_nerd_horizon_l, 3, 3, 0)

#NONNE
NONNE_R = pyg.image.load("Images/Persos/nonne_r.png")
NONNE_L = pyg.image.load("Images/Persos/nonne_l.png")

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

########################### ANIMS ##########################################################################

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
spritesheet_rouge_a_levre = pyg.image.load("Images/Monstres/rouge_a_levre.png")
spritesheet_ex_amies = pyg.image.load("Images/Monstres/ex_amies.png")
spritesheet_pipi = pyg.image.load("Images/Monstres/pipi.png")
spritesheet_odeurs = pyg.image.load("Images/Monstres/odeurs.png")
spritesheet_ex = pyg.image.load("Images/Monstres/ex.png")

# NONNE
spritesheet_nonne = pyg.image.load("Images/Monstres/nonne.png")
spritesheet_croix = pyg.image.load("Images/Armes_items/croix.png")
spritesheet_homme_mi_demon = pyg.image.load("Images/Monstres/homme_mi_demon.png")
spritesheet_bisous =  pyg.image.load("Images/Monstres/bisous.png")
spritesheet_666 = pyg.image.load("Images/Monstres/666.png")
spritesheet_fruit_defendu = pyg.image.load("Images/Monstres/fruit_defendu.png")
spritesheet_miroir = pyg.image.load("Images/Monstres/miroir.png")
spritesheet_demon = pyg.image.load("Images/Monstres/demon.png")
spritesheet_diablotin = pyg.image.load("Images/Monstres/diablotin.png")
spritesheet_gargouille = pyg.image.load("Images/Monstres/gargouille.png")
spritesheet_lucifer = pyg.image.load("Images/Monstres/lucifer.png")

ANIM_COFFRE = decouper_image(spritesheet_coffre, 4, 6, 0)

# NERD
ANIM_DRAGON = decouper_image(spritesheet_dragon, 3, 4, 6)
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
ANIM_ROUGE_A_LEVRE = decouper_image(spritesheet_rouge_a_levre, 3, 3, 1)
ANIM_EX_AMIES = decouper_image(spritesheet_ex_amies, 3, 3, 0)
ANIM_PIPI = decouper_image(spritesheet_pipi, 3, 3, 0)
ANIM_ODEURS = decouper_image(spritesheet_odeurs, 3, 3, 2)
ANIM_EX = decouper_image(spritesheet_ex, 2, 3, 0)

# NONNE
ANIM_NONNE = decouper_image(spritesheet_nonne, 5, 5, 4)
ANIM_CROIX = decouper_image(spritesheet_croix, 2, 2, 0)
ANIM_HOMME_MI_DEMON = decouper_image(spritesheet_homme_mi_demon, 2, 3, 0)
ANIM_BISOUS = decouper_image(spritesheet_bisous, 3, 3, 0)
ANIM_666 = decouper_image(spritesheet_666, 2, 3, 1)
ANIM_FRUIT_DEFENDU = decouper_image(spritesheet_fruit_defendu, 3, 3, 1)
ANIM_MIROIR = decouper_image(spritesheet_miroir, 3, 4, 0)
ANIM_DEMON = decouper_image(spritesheet_demon, 6, 1, 0)
ANIM_DIABLOTIN = decouper_image(spritesheet_diablotin, 9, 1, 0)
ANIM_GARGOUILLE = decouper_image(spritesheet_gargouille, 8, 1, 0)
ANIM_LUCIFER = decouper_image(spritesheet_lucifer, 8, 1, 0)
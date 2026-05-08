import pygame as pyg
pyg.font.init() # initialiser le module font de pygame
from Fichiers_variables.traitement_images import *
from math import ceil

WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre

WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre

pyg.display.set_caption("Somnek") 
FONT = pyg.font.SysFont("Press Start 2P", 24) # definir la police d'ecriture

CENTREx, CENTREy = WIDTH//2, HEIGHT//2 
PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 2 # vitesse de deplacement du joueur
PLAYER_PV = 50 # points de vie du joueur

FREQUENCE = 50


PERSOS =  {
    "Fille_populaire" : {"image" : 
                            {"horizon_r" : FILLE_POPULAIRE_R,
                            "horizon_l" : FILLE_POPULAIRE_L},
                        "color" : (167, 67, 86, 200)},
    "Nonne" : {"image" :
                {"horizon_r" : NONNE_R,
                "horizon_l" : NONNE_L},
                "color" : (92, 60, 61, 200)},
    "Nerd" : {"anim" : 
                {"avant" : ANIM_NERD_AVANT,
                "arriere" : ANIM_NERD_ARRIERE,
                "horizon_r" : ANIM_NERD_HORIZON_R,
                "horizon_l" : ANIM_NERD_HORIZON_L},
            "color" : (92, 167, 133, 200)}
}

CATEGORIE = {}
for i in range(1, 51):
    t = "Type " + str(i)
    CATEGORIE[t] = {"puissance" : i,
                "hp" : 50*i,
                "vitesse" : ceil(i/10),
                "niveau" : i}
    
TYPES_MONSTRES = {

    # NERD
    "Dragon" : { ** CATEGORIE["Type 1"],
                "perso" : "Nerd",
                "anim" : ANIM_DRAGON},
    "Sorcier" : {** CATEGORIE["Type 2"],
                "perso" : "Nerd",
                "anim" : ANIM_SORCIER},
    "Araignée" : {** CATEGORIE["Type 4"],
                "perso" : "Nerd",
                "image" : SPIDER},
    "Creeper" : {** CATEGORIE["Type 6"],
                "perso" : "Nerd",
                "anim" : ANIM_CREEPER},
    "Seau" : {** CATEGORIE["Type 8"],
                "perso" : "Nerd",
                "image" : SEAU},
    "Savon" : {** CATEGORIE["Type 10"],
                "perso" : "Nerd",
                "image" : SAVON},
    "Ballon_basket" : {** CATEGORIE["Type 12"],
                "perso" : "Nerd",
                "image" : BALLON_BASKET},
    "Ballon_foot" : {** CATEGORIE["Type 14"],
                "perso" : "Nerd",
                "anim" : ANIM_BALLON},
    "Ordi_mutant" : {** CATEGORIE["Type 16"],
                "perso" : "Nerd",
                "anim" : ANIM_ORDI_MUTANT},
    "Grand_mere" : {** CATEGORIE["Type 18"],
                "perso" : "Nerd",
                "anim" : ANIM_GRAND_MERE},
    "Fille_populaire" : {** CATEGORIE["Type 20"],
                "perso" : "Nerd",
                "image" : FILLE_POPULAIRE_R},
    "Telephone" : {** CATEGORIE["Type 22"],
                "perso" : "Nerd",
                "anim" : ANIM_TELEPHONE},
    "Ecouteur" : {** CATEGORIE["Type 24"],
                "perso" : "Nerd",
                "image" : ECOUTEUR},
    "Prof" : {** CATEGORIE["Type 26"],
                "perso" : "Nerd",
                "anim" : ANIM_PROF},


    # FILLE POPULAIRE           
    "Demaquillant" : {** CATEGORIE["Type 1"],
                "perso" : "Fille_populaire",
                "image" : DEMAQUILLANT},
    "Eval" : {** CATEGORIE["Type 2"],
                "perso" : "Fille_populaire",
                "image" : EVAL},
    "Fond_de_teint" : {** CATEGORIE["Type 4"],
                "perso" : "Fille_populaire",
                "image" : FOND_DE_TEINT},
    "Skinny" : { ** CATEGORIE["Type 6"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_SKINNY},
    "Rouge_a_levre" : { ** CATEGORIE["Type 8"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_ROUGE_A_LEVRE},
    "Lunettes" : {** CATEGORIE["Type 10"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_LUNETTES},
    "Out_of_stock" : {** CATEGORIE["Type 14"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_OUT_OF_STOCK},
    "Avion" : { ** CATEGORIE["Type 16"],
               "perso" : "Fille_populaire",
               "anim" : ANIM_AVION},
    "Pipi" : { ** CATEGORIE["Type 18"],
               "perso" : "Fille_populaire",
               "anim" : ANIM_PIPI},
    "Caca" : { ** CATEGORIE["Type 20"],
               "perso" : "Fille_populaire",
               "anim" : ANIM_CACA},
    "Chewing_gum_sale" : { ** CATEGORIE["Type 22"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_CHEWING_GUM_SALE},
    "Odeurs" : { ** CATEGORIE["Type 24"],
                "perso" : "Fille_populaire",
                "anim" : ANIM_ODEURS},

    # NONNE
    "Demon" : { ** CATEGORIE["Type 1"],
            "perso" : "Nonne",
            "anim" : ANIM_DEMON},
    "Diablotin" : { ** CATEGORIE["Type 2"],
            "perso" : "Nonne",
            "anim" : ANIM_DIABLOTIN},
    "Bisous" : { ** CATEGORIE["Type 4"],
                "perso" : "Nonne",
                "anim" : ANIM_BISOUS},
    "666" : { ** CATEGORIE["Type 6"],
                "perso" : "Nonne",
                "anim" : ANIM_666},
    "Fruit_defendu" : { ** CATEGORIE["Type 10"],
                "perso" : "Nonne",
                "anim" : ANIM_FRUIT_DEFENDU},
    "Croix_envers" : { ** CATEGORIE["Type 14"],
                "perso" : "Nonne",
                "image" : CROIX_ENVERS},
    "Monde" : { ** CATEGORIE["Type 18"],
                "perso" : "Nonne",
                "image" : MONDE},   
    "Ostie_perimee" : { ** CATEGORIE["Type 20"],
                "perso" : "Nonne",
                "image" : OSTIE_PERIMEE}, 
    "Miroir" : { ** CATEGORIE["Type 22"],
                "perso" : "Nonne",
                "anim" : ANIM_MIROIR}
}

TYPES = [type for type in TYPES_MONSTRES]

# Dictionnaire ARMES qui n'a aucun sens juste pour test mon code
"""
ARMES = {}
for i in range(1,61):
    ARMES["nawak"+str(i)] = i
"""
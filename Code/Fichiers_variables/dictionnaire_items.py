import pygame as pyg
from Fichiers_variables.traitement_images import *


Items = {

    "Fille populaire": {
    "Parfum_Dioru": {
        
        "effet": "cooldown",
        "max": 0.40,
        "prix": 5
    },
    "Gloss_rose": {
        
        "effet": "attirance",
        "max": 45,
        "prix": 3
    },
    "Chew_gum": {
        
        "effet": "sante",
        
        "max": 2.0,
        "prix": 2
    },
    "Talons_noirs": {
        
        "effet": "vitesse",
        
        "max": 0.50,
        "prix": 7
    },
    "Crop_top_rose": {
        
        "effet": "protection",
        
        "max": 0.40,
        "prix": 6
    },
    "Carte_bleue": {
        
        "effet": "cupidite",
        
        "max": 0.50,
        "prix": 4
    },
    "Sac_main_violet": {
        
        "effet": "quantite",
        "quantite": 8,
        "max": 40,
        "prix": 6
    },
    "Pilule_verte": {
        
        "effet": "sante",
        "max": 2.0,
        "prix": 5
    },
    "Mousse_vanille": {
        
        "effet": "regen",
        "max": 3.0,
        "prix": 6
    }},

    "Nerd": {
    "Lunettes_cassees": {
        
        "effet": "zone",
        
        "max": 0.50,
        "prix": 3
    },
    "Souris_pc": {
       
        "effet": "cupidite",
        
        "max": 0.50,
        "prix": 3
    },
    "Chaussettes_propres": {
        
        "effet": "vitesse",

        "max": 0.50,
        "prix": 2
    },
    "Cahier_NSI": {
        
        "effet": "attirance",
        
        "max": 40,
        "prix": 4
    },
    "Vody_Lemonade": {
        
        "effet": "sante",
        
        "max": 2.0,
        "prix": 5
    },
    "Apple_Watch": {
        
        "effet": "duree",
        
        "max": 2.0,
        "prix": 7
    },
    "Deodorant": {
        
        "effet": "cooldown",
        
        "max": 0.40,
        "prix": 4
    },
    "Pomme_scientifique": {
        
        "effet": "sante",
        
        "max": 2.0,
        "prix": 2
    },
    "Chariot_violet": {
        
        "effet": "quantite",
        
        "max": 40,
        "prix": 6
    },
    "Serviette": {
       
        "effet": "regen",
        
        "max": 3.0,
        "prix": 5
    },
    "Ambroisie": {
        
        "effet": "resurrection",
        
        "max": 1,
        "prix": 10
    }},

    "Nonne": {
    "Eau_benite": {
        
        "effet": "multi",
        "vitesse_du_j": 0.10,
        "sante": 0.12,
        "malchance": 0.10,
        "max": 0.30,
        "prix": 4
    },
    "Chapelet": {
       
        "effet": "chance",
        
        "max": 0.50,
        "prix": 3
    },
    "Mocassin": {
        
        "effet": "vitesse",
        
        "max": 0.50,
        "prix": 2
    },
    "Voile": {
        
        "effet": "protection",
        
        "max": 0.40,
        "prix": 6
    },
    "Bourse": {
        
        "effet": "cupidite",
       
        "max": 0.50,
        "prix": 3
    },
    "Bougie": {
        
        "effet": "attirance",
        
        "max": 40,
        "prix": 3
    },
    "Huile_benie": {
        
        "effet": "cooldown",
        
        "max": 0.40,
        "prix": 4
    },
    "Sac_dos_bleu": {
        
        "effet": "quantite",
        
        "max": 0.40,
        "prix": 5
    },
    "Mousse_vanille": {
        
        "effet": "regen",
        
        "max": 3.0,
        "prix": 5
    },
    "Nokia": {
        
        "effet": "regen",
        
        "max": 3.0,
        "prix": 5
    }}
}

GESTION_NIVEAU_ITEMS = {

    "Nerd": {

        "Niveau 1": {
            "Lunettes_cassees": 0.10,
            "Souris_pc": 0.10,
            "Chaussettes_propres": 0.10
        },

        "Niveau 2": {
            "Lunettes_cassees": 0.05,
            "Souris_pc": 0.05,
            "Chaussettes_propres": 0.05
        },

        "Niveau 3": {
            "Lunettes_cassees": 0.05,
            "Souris_pc": 0.05,
            "Cahier_NSI": 0.08
        },

        "Niveau 4": {
            "Cle_USB": 23,
            "Epée_enflammée": 10
        },

        "Niveau 5": {
            "Pistolets": 15,
            "Berserk" : 0 #à modifier mais j'ai pas capté à quoi servait ce truc
        },

        "Niveau 6": {
            "Petit_nain_roux": 0.07
        },

        "Niveau 7": {
        },

        "Niveau 8": {
            "Souris_pc": 0.05,
            "Cahier_NSI": 0.08
        },

        "Niveau 9": {
            "Vody_Lemonade": 0.20
        },

        "Niveau 10": {
        },

        "Niveau 11": {
            "Apple_watch": 1.5
        },

        "Niveau 12": {
            "Vody_Lemonade": 0.05,
            "Cahier_NSI": 0.06
        },

        "Niveau 13": {
            "Souris_pc": 0.05,
            "Chaussettes_propres": 0.05
        },

        "Niveau 14": {
            "Pomme_scientifique": 0.02,
            "Deodorant": 0.03
        },

        "Niveau 15": {
            "Pistolets": 0.07
        },

        "Niveau 16": {
            "Deodorant": 0.13
        },

        "Niveau 17": {
            "Pomme_scientifique": 0.08,
            "Cahier_NSI": 0.15
        },

        "Niveau 18": {
        },

        "Niveau 19": {
            "Serviette_nettoyante": 0.6
        },

        "Niveau 20": {
            "Mousse_vanille": 0.9
        },

        "Niveau 21": {
            "Chaussettes_propres": 0.05
        },

        "Niveau 22": {
            "Vody_Lemonade": 0.35,
            "Serviette_nettoyante": 3,
            "Ambroisie" : 0.5
        },

        "Niveau 23": {
            "Apple_watch": 1.8
        },

        "Niveau 24": {
            "Epée_de_Guts": 40
        },

        "Niveau 25": {
            "Armure_de_chevalier": 0.50,
            "Pantalon_beige": 0.27
        },

        "Niveau 26": {
        }
    },


    "Fille_populaire": {

        "Niveau 1": {
            "Gloss_rose": 0.15,
            "Faux_cils": 8,
            "Chew_gum": 0.20
        },

        "Niveau 2": {
            "Faux_cils": 0.10,
            "Chew_gum": 0.20,
            "Talons_noirs": 0.10
        },

        "Niveau 3": {
            "Gloss_rose": 0.08
        },

        "Niveau 4": {
            "Faux_ongles_rose": 23,
            "Bracelet_soeur": 10
        },

        "Niveau 5": {
            "Parfum_Dioru": 0.30
        },

        "Niveau 6": {
        },

        "Niveau 7": {
        },

        "Niveau 8": {
            "Carte_bleue": 0.05
        },

        "Niveau 9": {
            "Chargeur": 0.20
        },

        "Niveau 10": {
        },

        "Niveau 11": {
        },

        "Niveau 12": {
        },

        "Niveau 13": {
        },

        "Niveau 14": {
            "Pilule_verte": 0.13
        },

        "Niveau 15": {
            "Parfum_Dioru": 0.13
        },

        "Niveau 16": {
            "Gloss_rose": 0.12
        },

        "Niveau 17": {
        },

        "Niveau 18": {
            "Mousse_vanille": 0.6
        },

        "Niveau 19": {
        },

        "Niveau 20": {
        },

        "Niveau 21": {
        },

        "Niveau 22": {
        },

        "Niveau 23": {
        },

        "Niveau 24": {
            "Ring_light": 0.40
        },

        "Niveau 25": {
            "Ensemble_Juicy": 0.50,
            "Manteau_leopard": 0.27
        },

        "Niveau 26": {
        }
    },


    "Nonne": {

        "Niveau 1": {
            "Eau_benite": 0.10,
            "Chapelet": 0.10,
            "Mocassin": 0.10
        },

        "Niveau 2": {
            "Eau_benite" : 0.10,
            "Tableau_sacre": 0.08,
            "Mocassin" : 0.10
        },

        "Niveau 3": {
            "Voile": 0.20
        },

        "Niveau 4": {
            "Bougie": 0.08,
            "Bourse": 0.05
        },

        "Niveau 5": {
            "Huile_benediction": 0.03
        },

        "Niveau 6": {
        },

        "Niveau 7": {
            "Armure_de_bronze" : 0.1 #jsp modifiez
        },

        "Niveau 8": {
        },

        "Niveau 9": {
            "Bougie": 0.08
        },

        "Niveau 10": {
            "Armure_de_bronze" : 0.10
        },

        "Niveau 11": {
        },

        "Niveau 12": {
        },

        "Niveau 13": {
        },

        "Niveau 14": {
        },

        "Niveau 15": {
            "Armure_de_bronze" : 0.10
        },

        "Niveau 16": {
        },

        "Niveau 17": {
        },

        "Niveau 18": {
            "Ostie": 0.09
        },

        "Niveau 19": {
        },

        "Niveau 20": {
        },

        "Niveau 21": {
        },

        "Niveau 22": {
            "Vin divin": 1
        },

        "Niveau 23": {
        },

        "Niveau 24": {
        },

        "Niveau 25": {
            "lunette": 0.50

        },

        "Niveau 26": {
        }
    }
}

TYPES_ITEMS = {

    "Nerd": {

    "Lunettes_cassees": {
        "image": LUNETTES_CASSEES,
        "texte": "Augmente la zone d'attaque de 10 %."
    },

    "Souris_pc": {
        "image": SOURIS,
        "texte": "Le personnage gagne 10 % de pièces en plus."
    },

    "Chaussettes_propres": {
        "image": CHAUSSETTES,
        "texte": "Le personnage se déplace 10 % plus vite."
    },

    "Cahier_NSI": {
        "image": CAHIER_DE_NSI,
        "texte": "Le personnage gagne 8 % d'attirance en plus."
    },

    "Vody_Lemonade": {
        "image": VODY,
        "texte": "+20 % de santé maximale (max 200 %)"
    },

    "Deodorant": {
        "image": DEMAQUILLANT,#en attente
        "texte": "Le personnage diminue le temps entre les attaques de 3 % (max +40 %)"
    },

    "Pomme_scientifique": {
        "image": POMME_SCIENTIFIQUE,
        "texte": "+2% de santé maximale (max 200 %)"
    },
    "Berserk" : {
        "image" : BERSEK,
        "texte" : "Tome 1 de Berserk : Augmente la puissance des ennemi de 10 % pendant 1 minute et augmente la Puissance du personnage  de 20% pendant 2 minutes."
    },
    "Armure_de_bronze": {
        "image": ARMURE,
        "texte": "Réduit les dégâts des ennemis de 20%"
    },
    "Armure_de_chevalier": {
        "image": ARMURE,
        "texte": "+50 % de santé maximale (max 400 %) et réduit les dégâts des ennemis de 30%."
    },

    "Petit_nain_roux": {
        "image": NAIN,
        "texte": "Le personnage a 7 % de chance de plus à chaque niveau.(max +70%)"
    },

    "Serviette_nettoyante": {
        "image": SERVIETTE,
        "texte": "Le personnage récupère 0,6PV par seconde."
    }
},

    "Fille_populaire": {

    "Gloss_rose": {
        "image": GLOSS_ROSE,
        "texte": "Le personnage gagne 8 % d'attirance en plus. (max +40 %)"
    },

    "Chew_gum": {
        "image": CHEW_GUM,
        "texte": "Augmente la santé maximale de 20 %."
    },

    "Talons_noirs": {
        "image": TALON_NOIR,
        "texte": "Le personnage se déplace 10 % plus vite."
    },

    "Bracelet_soeur": {
        "image": BRACELET_SOEUR,
        "texte": "Tire sur un ennemi aléatoire, inflige de lourds dégâts. Dégât de base : 10PV"
    },

    "Carte_bleue": {
        "image": CARTE_BLEU,
        "texte": "Le personnage gagne 5% de pièces supplémentaire.(max +50 %)"
    },

    "Parfum_Dioru": {
        "image": PARFUM_DIORU,
        "texte": "Le personnage diminue le temps entre les attaques de 30 % (max +40 %)"
    },

    "Pilule_verte": {
        "image": PILULE_VERTE,
        "texte": "+13% de santé maximale (max 200 %)"
    },

    "Crop_top_rose": {
        "image": CROP_TOP_ROSE,
        "texte": "Réduit les dégâts des ennemis de 20%"
    },

    "Coque_trefle": {
        "image": TREFLE,#en attente
        "texte": "Le personnage a 7 % de chance de plus à chaque niveau.(max +70%)"
    },

    "Mousse_vanille": {
        "image": MOUSSE_VANILLE,
        "texte": "Le personnage récupère 0,6PV par seconde."
    },

    "Sac_main_violet": {
        "image": MOUSSE_VANILLE,#en attente
        "texte": "Le personnage augmente la quantité de ses projectiles de 18% (max +40 %)"
    }
    },

    "Nonne": {

    "Croix_marron": {
        "image": CROIX_DE_BASE,
        "texte": "Augmente les dégâts infligés de 15 %(max+60%)"
    },

    "Chapelet": {
        "image": CROIX_DE_BASE,
        "texte": "Le personnage a 10 % de chances supplémentaires."
    },

    "Mocassin": {
        "image": MOCASSIN,
        "texte": "Le personnage se déplace 10 % plus vite."
    },

    "Tableau_sacre": {
        "image": MOCASSIN,
        "texte": "Réduit le temps de recharge des armes de 8 %"
    },

    "Bourse": {
        "image": BOURSE,
        "texte": "Le personnage gagne 5% de pièces supplémentaire.(max +50 %)"
    },

    "Bougie": {
        "image": BOUGIE,
        "texte": "Le personnage gagne 8 % d'attirance en plus. (max +40 %)"
    },

    "Voile": {
        "image": VOILE,
        "texte": "Réduit les dégâts des ennemis de 20%"
    },

    "Huile_benie": {
        "image": EAU_BENITE,#en attente
        "texte": "Le personnage diminue le temps entre les attaques de 3 % (max +40 %)"
    },

    "Ostie": {
        "image": OSTIE,
        "texte": "Augmente la santé maximale de 20 %."
    },

    "Sac_a_dos_bleu": {
        "image": OSTIE,#en attente
        "texte": "Le personnage augmente la quantité de ses projectiles de 18% (max +40 %)"
    },

    "Eau_benite": {
        "image": EAU_BENITE,
        "texte": "Augmente la vitesse + 10%, la santé +12%, la quantité et la fréquence des ennemis de 10 %."
    }
}
}
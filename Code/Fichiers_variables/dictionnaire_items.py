import pygame as pyg
from Fichiers_variables.traitement_images import *
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
    "Lunettes": {
        
        "effet": "zone",
        
        "max": 0.50,
        "prix": 3
    },
    "Souris": {
       
        "effet": "cupidite",
        
        "max": 0.50,
        "prix": 3
    },
    "Chaussettes": {
        
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
    "Huile_benediction": {
        
        "effet": "cooldown",
        
        "max": 0.40,
        "prix": 4
    },
    "Sac_dos_bleu": {
        
        "effet": "quantite",
        
        "max": 0.40,
        "prix": 5
    },
    "Mousse": {
        
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
            "Pistolets": 15
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
            "Serviette_nettoyante": 3
        },

        "Niveau 23": {
            "Apple_watch": 1.8
        },

        "Niveau 24": {
            "Epée_de_Guts": 40
        },

        "Niveau 25": {
            "Armure_chevalier": 0.50,
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
            "Tableau_vierge": 0.08
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
        },

        "Niveau 8": {
        },

        "Niveau 9": {
            "Bougie": 0.08
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
        },

        "Niveau 15": {
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
            "texte": "TEST"
        },

        "Souris_pc": {
            "image": SOURIS,
            "texte": "TEST"
        },

        "Chaussettes_propres": {
            "image": CHAUSSETTES,
            "texte": "TEST"
        },

        "Cahier_NSI": {
            "image": CAHIER_DE_NSI,
            "texte": "TEST"
        },

        "Vody_Lemonade": {
            "image": SOURIS,
            "texte": "TEST"
        },

        "Deodorant": {
            "image": SOURIS,
            "texte": "TEST"
        },

        "Pomme_scientifique": {
            "image": SOURIS,
            "texte": "TEST"
        },

        "Armure_de_bronze": {
            "image": SOURIS,
            "texte": "TEST"
        },

        "Petit_nain_roux": {
            "image": NAIN,
            "texte": "TEST"
        },

        "Serviette_nettoyante": {
            "image": SOURIS,
            "texte": "TEST"
        }
    },

    "Fille_populaire": {

        "Gloss_rose": {
            "image": GLOSS_ROSE,
            "texte": "TEST"
        },

        "Chew_gum": {
            "image": CHEW_GUM,
            "texte": "TEST"
        },

        "Talons_noirs": {
            "image": TALON_NOIR,
            "texte": "TEST"
        },

        "Carte_bleue": {
            "image": CARTE_BLEU,
            "texte": "TEST"
        },

        "Parfum_Dioru": {
            "image": PARFUM_DIORU,
            "texte": "TEST"
        },

        "Pilule_verte": {
            "image": PILULE_VERTE,
            "texte": "TEST"
        },

        "Crop_top_rose": {
            "image": CROP_TOP_ROSE,
            "texte": "TEST"
        },

        "Coque_trefle": {
            "image": CROP_TOP_ROSE,
            "texte": "TEST"
        },

        "Mousse_a_la_vanille": {
            "image": MOUSSE_VANILLE,
            "texte": "TEST"
        },

        "Sac_a_main_violet": {
            "image": MOUSSE_VANILLE,
            "texte": "TEST"
        }
    },

    "Nonne": {

        "Croix_marron": {
            "image": None,
            "texte": "TEST"
        },

        "Chapelet": {
            "image": None,
            "texte": "TEST"
        },

        "Mocassin": {
            "image": None,
            "texte": "TEST"
        },

        "Tableau_sacre": {
            "image": None,
            "texte": "TEST"
        },

        "Bourse": {
            "image": None,
            "texte": "TEST"
        },

        "Bougie": {
            "image": None,
            "texte": "TEST"
        },

        "Voile": {
            "image": None,
            "texte": "TEST"
        },

        "Huile_benie": {
            "image": None,
            "texte": "TEST"
        },

        "Ostie": {
            "image": None,
            "texte": "TEST"
        },

        "Sac_a_dos_bleu": {
            "image": None,
            "texte": "TEST"
        }
    }
}
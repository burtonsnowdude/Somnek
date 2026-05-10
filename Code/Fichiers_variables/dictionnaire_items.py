import pygame as pyg
from Fichiers_variables.traitement_images import *


Items = {
    "Fille_populaire": {
        "Parfum_Dioru": {"effet": "cooldown", "max": 0.40},
        "Chew_gum": {"effet": "sante", "max": 2.0},
        "Talons_noirs": {"effet": "vitesse", "max": 0.50},
        "Crop_top_rose": {"effet": "protection", "max": 0.40},
        "Carte_bleue": {"effet": "cupidite", "max": 0.50},
        "Sac_main_violet": {"effet": "quantite", "max": 40},
        "Pilule_verte": {"effet": "sante", "max": 2.0},
        "Mousse_vanille": {"effet": "regen", "max": 3.0},
        "Coque_trefle": {"effet": "chance", "max": 0.70},
        "Chargeur": {"effet": "duree", "max": 2.0},
        "Ambroisie": {"effet": "resurrection", "max": 1},
        "Iphone_2000": {"effet": "multi", "max": 0.20},
        "Minuteur": {"effet": "duree", "max": 2.0},
        "Ensemble_juicy": {"effet": "protection", "max": 0.50},
        "Manteau_leopard": {"effet": "protection", "max": 0.27}
    },

    "Nerd": {
        "Lunettes_cassees": {"effet": "zone", "max": 0.50},
        "Souris_pc": {"effet": "cupidite", "max": 0.50},
        "Chaussettes_propres": {"effet": "vitesse", "max": 0.50},
        "Cahier_NSI": {"effet": "attirance", "max": 40},
        "Vody_Lemonade": {"effet": "sante", "max": 2.0},
        "Apple_Watch": {"effet": "duree", "max": 2.0},
        "Deodorant": {"effet": "cooldown", "max": 0.40},
        "Pomme_scientifique": {"effet": "sante", "max": 2.0},
        "Serviette_nettoyante": {"effet": "regen", "max": 3.0},
        "Cle_USB": {"effet": "degats", "max": 30},
        "Pistolets": {"effet": "attaque", "max": 2.0},
        "Petit_nain_roux": {"effet": "chance", "max": 0.70},
        "Armure_chevalier": {"effet": "protection", "max": 0.50},
        "Pantalon_beige": {"effet": "vitesse", "max": 0.27},
    },

    "Nonne": {
        "Eau_benite": {
            "effet": "multi",
            "vitesse": 0.10,
            "sante": 0.12,
            "malchance": 0.10,
            "max": 0.30
        },
        "Chapelet": {"effet": "chance", "max": 0.50},
        "Mocassin": {"effet": "vitesse", "max": 0.50},
        "Bourse": {"effet": "cupidite", "max": 0.50},
        "Bougie": {"effet": "attirance", "max": 40},
        "Huile_benediction": {"effet": "cooldown", "max": 0.40},
        "Sac_a_dos_bleu": {"effet": "quantite", "max": 0.40},
        "Nokia": {"effet": "regen", "max": 3.0},
        "Ostie": {"effet": "sante", "max": 2.0},
        "Voile": {"effet": "protection", "max": 0.40},
        "Tableau_sacre": {"effet": "cooldown", "max": 0.30},
        "Boule_energie": {"effet": "attirance", "max": 40},
        "Coeur": {"effet": "attirance", "max": 40},
        "Cape": {"effet": "protection", "max": 0.27},
        "Collant": {"effet": "vitesse", "max": 0.50},
        "Halo": {"effet": "chance", "max": 0.70},
        "Minuteur": {"effet": "duree", "max": 2.0},
    }
}




GESTION_NIVEAU_ITEMS = {

    "Nerd": {
        "Niveau 1": {"Lunettes_cassees": 0.10, "Souris_pc": 0.10, "Chaussettes_propres": 0.10},
        "Niveau 2": {"Lunettes_cassees": 0.05, "Souris_pc": 0.05, "Chaussettes_propres": 0.05},
        "Niveau 3": {"Lunettes_cassees": 0.05, "Souris_pc": 0.05, "Cahier_NSI": 0.08},
        "Niveau 4": {"Cle_USB": 23, "Epee_enflammee": 10},
        "Niveau 5": {"Pistolets": 15},
        "Niveau 6": {"Petit_nain_roux": 0.07},
        "Niveau 7": {},
        "Niveau 8": {"Souris_pc": 0.05, "Cahier_NSI": 0.08},
        "Niveau 9": {"Vody_Lemonade": 0.20},
        "Niveau 10": {},
        "Niveau 11": {"Apple_Watch": 1.5},
        "Niveau 12": {"Vody_Lemonade": 0.05, "Cahier_NSI": 0.06},
        "Niveau 13": {"Souris_pc": 0.05, "Chaussettes_propres": 0.05},
        "Niveau 14": {"Pomme_scientifique": 0.02, "Deodorant": 0.03},
        "Niveau 15": {"Pistolets": 0.07},
        "Niveau 16": {"Deodorant": 0.13},
        "Niveau 17": {"Pomme_scientifique": 0.08, "Cahier_NSI": 0.15},
        "Niveau 18": {},
        "Niveau 19": {"Serviette_nettoyante": 0.6},
        "Niveau 20": {"Mousse_vanille": 0.9},
        "Niveau 21": {"Chaussettes_propres": 0.05},
        "Niveau 22": {"Vody_Lemonade": 0.35, "Serviette_nettoyante": 3},
        "Niveau 23": {"Apple_Watch": 1.8},
        "Niveau 24": {"Epee_de_guts": 40},
        "Niveau 25": {"Armure_chevalier": 0.50, "Pantalon_beige": 0.27},
        "Niveau 26": {}
    },

    "Fille_populaire": {
        "Niveau 1": {"Chew_gum": 0.20, "Talons_noirs": 0.10},
        "Niveau 2": {"Chew_gum": 0.20, "Talons_noirs": 0.10},
        "Niveau 3": {"Chew_gum": 0.8, "Talons_noirs": 0.10},
        "Niveau 4": {"Iphone_2000": (0.10, 0.20)},
        "Niveau 5": {"Talons_noirs": 0.05},
        "Niveau 6": {"Chew_gum": 0.10, "Coque_trefle": 0.07, "Talons_noirs": 0.5},
        "Niveau 7": {"Crop_top_rose": 0.20},
        "Niveau 8": {"Carte_bleue": 0.05},
        "Niveau 9": {"Chargeur": 0.20},
        "Niveau 10": {"Crop_top_rose": 0.01},
        "Niveau 11": {"Chew_gum": 0.09, "Minuteur": 0.5},
        "Niveau 12": {"Chew_gum": 0.05},
        "Niveau 13": {"Carte_bleue": 0.05, "Talons_noirs": 0.10},
        "Niveau 14": {"Pilule_verte": 0.13, "Parfum_Dioru": 0.30, "Sac_main_violet": 0.18},
        "Niveau 15": {"Parfum_Dioru": 0.13, "Crop_top_rose": 0.10},
        "Niveau 16": {"Parfum_Dioru": 0.13},
        "Niveau 17": {"Pilule_verte": 0.08, "Parfum_Dioru": 0.03},
        "Niveau 18": {"Pilule_verte": 0.08, "Mousse_vanille": 0.6},
        "Niveau 19": {"Mousse_vanille": 0.8},
        "Niveau 20": {"Mousse_vanille": 0.9},
        "Niveau 21": {"Talons_noirs": 0.10},
        "Niveau 22": {"Chew_gum": 0.35, "Mousse_vanille": 3, "Ambroisie": 0.50},
        "Niveau 23": {"Chew_gum": 0.15, "Parfum_Dioru": 0.8, "Carte_bleue": 0.2},
        "Niveau 24": {"Chew_gum": 0.15, "Mousse_vanille": 0.8},
        "Niveau 25": {"Ensemble_juicy": 0.50, "Manteau_leopard": 0.27},
        "Niveau 26": {}
    },

    "Nonne": {
        "Niveau 1": {"Eau_benite": 0.10, "Chapelet": 0.10, "Mocassin": 0.10},
        "Niveau 2": {"Eau_benite": 0.10, "Tableau_sacre": 0.08, "Mocassin": 0.10},
        "Niveau 3": {"Eau_benite": 0.08, "Mocassin": 0.08},
        "Niveau 4": {"Nokia": 0.10},
        "Niveau 5": {"Mocassin": 0.05},
        "Niveau 6": {"Tableau_sacre": 0.8, "Chapelet": 0.9, "Mocassin": 0.05},
        "Niveau 7": {"Voile": 0.2},
        "Niveau 8": {"Bourse": 0.05, "Bougie": 0.08},
        "Niveau 9": {"Bougie": 0.08, "Boule_energie": 0.20},
        "Niveau 10": {"Voile": 0.10},
        "Niveau 11": {"Ostie": 0.09},
        "Niveau 12": {"Eau_benite": 0.05, "Bougie": 0.06},
        "Niveau 13": {"Bourse": 0.05, "Mocassin": 0.08},
        "Niveau 14": {"Bourse": 0.15, "Huile_benediction": 0.03, "Sac_a_dos_bleu": 0.18},
        "Niveau 15": {"Huile_benediction": 0.13, "Voile": 0.10},
        "Niveau 16": {"Huile_benediction": 0.13},
        "Niveau 17": {"Pilule_verte": 0.08, "Voile": 0.03, "Coeur": 0.15},
        "Niveau 18": {"Sac_a_dos_bleu": 0.12, "Mousse_vanille": 0.60},
        "Niveau 19": {"Mousse_vanille": 0.80},
        "Niveau 20": {"Mousse_vanille": 0.90},
        "Niveau 21": {"Mocassin": 0.05},
        "Niveau 22": {"Ostie": 0.35, "Mousse_vanille": 3.00},
        "Niveau 23": {"Ostie": 0.15, "Huile_benediction": 1.80, "Bourse": 0.20},
        "Niveau 24": {"Ostie": 0.15, "Minuteur": 0.5},
        "Niveau 25": {"Collant": 0.50, "Cape": 0.27},
        "Niveau 26": {"Halo": 0.40}
    }
}


TYPES_ITEMS = {

    "Nerd": {
        "Lunettes_cassees": {"image": LUNETTES_CASSEES, "texte": "Augmente la zone d'attaque de 10 %."},
        "Souris_pc": {"image": SOURIS, "texte": "Le personnage gagne 10 % de pièces en plus."},
        "Chaussettes_propres": {"image": CHAUSSETTES, "texte": "Le personnage se déplace 10 % plus vite."},
        "Cahier_NSI": {"image": CAHIER_DE_NSI, "texte": "Le personnage gagne 8 % d'attirance en plus."},
        "Vody_Lemonade": {"image": VODY, "texte": "+20 % de santé maximale (max 200 %)"},
        "Deodorant": {"image": DEMAQUILLANT, "texte": "Réduit le cooldown des attaques."},
        "Pomme_scientifique": {"image": POMME_SCIENTIFIQUE, "texte": "+2% de santé maximale"},
        "Petit_nain_roux": {"image": NAIN, "texte": "Augmente la chance de loot."},
        "Serviette_nettoyante": {"image": SERVIETTE, "texte": "Régénération de vie."},
        "Cle_USB": {"image": CLE_USB, "texte": "Augmente les dégâts."},
        "Pistolets": {"image": PISTOLETS, "texte": "Augmente la puissance d'attaque."},
        "Epee_enflammee": {"image": EPEE_ENFLAMMEE, "texte": "Inflige des dégâts de feu."},
        "Epee_de_guts": {"image": EPEE_GUTS, "texte": "Arme légendaire très puissante."},
        "Armure_chevalier": {"image": ARMURE, "texte": "Réduit fortement les dégâts."},
        "Pantalon_beige": {"image": CHAUSSETTES, "texte": "Bonus léger de vitesse."},
        "Apple_Watch": {"image": MOUSSE_VANILLE, "texte": "Augmente la durée des effets."},
    },

    "Fille_populaire": {
        "Chew_gum": {"image": CHEW_GUM, "texte": "Augmente la santé."},
        "Talons_noirs": {"image": TALON_NOIR, "texte": "Augmente la vitesse."},
        "Carte_bleue": {"image": CARTE_BLEU, "texte": "Augmente les gains d'argent."},
        "Parfum_Dioru": {"image": PARFUM_DIORU, "texte": "Réduit le cooldown."},
        "Pilule_verte": {"image": PILULE_VERTE, "texte": "Augmente la santé max."},
        "Crop_top_rose": {"image": CROP_TOP_ROSE, "texte": "Réduit les dégâts."},
        "Coque_trefle": {"image": TREFLE, "texte": "Augmente la chance."},
        "Mousse_vanille": {"image": MOUSSE_VANILLE, "texte": "Régénération de vie."},
        "Sac_main_violet": {"image": MOUSSE_VANILLE, "texte": "Augmente le nombre de projectiles."},
        "Chargeur": {"image": CHARGEUR, "texte": "Augmente la durée des effets."},
        "Iphone_2000": {"image": IPHONE_2000, "texte": "Objet rare multi-effets."},
        "Minuteur": {"image": MINUTEUR, "texte": "Augmente la durée des bonus."},
        "Ambroisie": {"image": AMBROISIE, "texte": "Permet de ressusciter."},
        "Ensemble_juicy": {"image": CROP_TOP_ROSE, "texte": "Bonus global."},
        "Manteau_leopard": {"image": CROP_TOP_ROSE, "texte": "Augmente la résistance."}
    },

    "Nonne": {
        "Eau_benite": {"image": EAU_BENITE, "texte": "Bonus multiples (vitesse, santé, etc.)."},
        "Chapelet": {"image": CROIX_DE_BASE, "texte": "Augmente la chance."},
        "Mocassin": {"image": MOCASSIN, "texte": "Augmente la vitesse."},
        "Tableau_sacre": {"image": CROIX_DE_BASE, "texte": "Réduit le cooldown."},
        "Bourse": {"image": BOURSE, "texte": "Augmente les gains."},
        "Bougie": {"image": BOUGIE, "texte": "Augmente l'attirance."},
        "Voile": {"image": VOILE, "texte": "Réduit les dégâts."},
        "Huile_benediction": {"image": EAU_BENITE, "texte": "Réduit le cooldown."},
        "Ostie": {"image": OSTIE, "texte": "Augmente la santé."},
        "Sac_a_dos_bleu": {"image": SAC_BLEU, "texte": "Augmente les projectiles."},
        "Nokia": {"image": NOKIA, "texte": "Régénération de vie."},
        "Boule_energie": {"image": BOULE_DENERGIE, "texte": "Attaque magique."},
        "Coeur": {"image": MOUSSE_VANILLE, "texte": "Augmente l'attirance."},
        "Cape": {"image": VOILE, "texte": "Augmente la défense."},
        "Collant": {"image": VOILE, "texte": "Bonus vitesse/défense."},
        "Halo": {"image": HALO_LUMINEUX, "texte": "Objet divin très puissant."},
        "Minuteur": {"image": MINUTEUR, "texte": "Augmente la durée des bonus."},
    }
}

ITEMS_PAR_PERSO = Items
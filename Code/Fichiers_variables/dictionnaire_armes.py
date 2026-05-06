from Fichiers_variables.traitement_images import *


TYPES_ARMES = {

    "Nerd": {

        "Epee_bleue": {
            "type_arme": "coup",
            "image": "TEST",
            "texte": "TEST"
        },

        "Cle_USB": {
            "type_arme": "zone",
            "image": CLE_USB,
            "texte": "TEST"
        },

        "Epee_enflammee": {
            "type_arme": "coup",
            "image": PISTOLETS,
            "texte": "TEST"
        },

        "Pistolets": {
            "type_arme": "balle",
            "image": PISTOLETS,
            "texte": "TEST"
        },

        "Ticket_de_metro": {
            "type_arme": "trait",
            "image": TICKET,
            "texte": "TEST"
        },

        "Epee_de_Guts": {
            "type_arme": "coup",
            "image": TICKET,
            "texte": "TEST"
        },

        "Console_allumee": {
            "type_arme": "zone",
            "image": CONSOLE,
            "texte": "TEST"
        }
    },

    "Fille_populaire": {

        "Faux_cils": {
            "type_arme": "trait",
            "image": FAUX_CILS,
            "texte": "TEST"
        },

        "Faux_ongles_roses": {
            "type_arme": "zone",
            "image" : FAUX_CILS,
            "texte": "TEST"
        },

        "Bracelet_de_sa_soeur": {
            "type_arme": "balle",
            "image": BRACELET_SOEUR,
            "texte": "TEST"
        },

        "Fer_a_lisser": {
            "type_arme": "zone_multiples",
            "image": FER_A_LISSER,
            "texte": "TEST"
        },

        "Pass_Navigo": {
            "type_arme": "trait",
            "image": PASS_NAVIGO,
            "texte": "TEST"
        },

        "Ring_light": {
            "type_arme": "zone_multiples",
            "image": PASS_NAVIGO,
            "texte": "TEST"
        }
    },

    "Nonne": {

        "Croix_marron": {
            "type_arme": "poison",
            "image": CROIX_DE_BASE,
            "texte": "TEST"
        },

        "Feu_de_l'Esprit_Saint": {
            "type_arme": "zone",
            "image": FEU_SAINT,
            "texte": "TEST"
        },

        "Medaille_de_bapteme": {
            "type_arme": "balle",
            "image": FEU_SAINT,
            "texte": "TEST"
        },

        "Coiffe_de_rameau": {
            "type_arme": "zone",
            "image": FEU_SAINT,
            "texte": "TEST"
        },

        "Lance_sacree": {
            "type_arme": "trait",
            "image": FEU_SAINT,
            "texte": "TEST"
        },

        "Aura_divine": {
            "type_arme": "poison",
            "image": HALO_LUMINEUX,
            "texte": "TEST"
        }
    }
}

ARMES = {

    "Nerd": {

        "Epee_bleue": {
            **TYPES_ARMES["Nerd"]["Epee_bleue"],
            "niveau_req": 1
        },

        "Cle_USB": {
            **TYPES_ARMES["Nerd"]["Cle_USB"],
            "niveau_req": 4
        },

        "Epee_enflammee": {
            **TYPES_ARMES["Nerd"]["Epee_enflammee"],
            "niveau_req": 4
        },

        "Pistolets": {
            **TYPES_ARMES["Nerd"]["Pistolets"],
            "niveau_req": 5
        },

        "Ticket_de_metro": {
            **TYPES_ARMES["Nerd"]["Ticket_de_metro"],
            "niveau_req": 19
        },

        "Epee_de_Guts": {
            **TYPES_ARMES["Nerd"]["Epee_de_Guts"],
            "niveau_req": 24
        }
    },

    "Fille_populaire": {

        "Faux_cils": {
            **TYPES_ARMES["Fille_populaire"]["Faux_cils"],
            "niveau_req": 1
        },

        "Faux_ongles_roses": {
            **TYPES_ARMES["Fille_populaire"]["Faux_ongles_roses"],
            "niveau_req": 4
        },

        "Bracelet_de_sa_soeur": {
            **TYPES_ARMES["Fille_populaire"]["Bracelet_de_sa_soeur"],
            "niveau_req": 4
        },

        "Fer_a_lisser": {
            **TYPES_ARMES["Fille_populaire"]["Fer_a_lisser"],
            "niveau_req": 5
        },

        "Pass_Navigo": {
            **TYPES_ARMES["Fille_populaire"]["Pass_Navigo"],
            "niveau_req": 19
        },

        "Ring_light": {
            **TYPES_ARMES["Fille_populaire"]["Ring_light"],
            "niveau_req": 24
        }
    },

    "Nonne": {

        "Croix_marron": {
            **TYPES_ARMES["Nonne"]["Croix_marron"],
            "niveau_req": 0
        },

        "Feu_de_l'Esprit_Saint": {
            **TYPES_ARMES["Nonne"]["Feu_de_l'Esprit_Saint"],
            "niveau_req": 4
        },

        "Medaille_de_bapteme": {
            **TYPES_ARMES["Nonne"]["Medaille_de_bapteme"],
            "niveau_req": 4
        },

        "Coiffe_de_rameau": {
            **TYPES_ARMES["Nonne"]["Coiffe_de_rameau"],
            "niveau_req": 5
        },

        "Lance_sacree": {
            **TYPES_ARMES["Nonne"]["Lance_sacree"],
            "niveau_req": 19
        },

        "Aura_divine": {
            **TYPES_ARMES["Nonne"]["Aura_divine"],
            "niveau_req": 24
        }
    }
}

GESTION_DES_NIVEAUX_ARMES = {

    "Nerd": {

        "Niveau 4": {
            "Cle_USB": "23 PV",
            "Epee_enflammee": "10 PV",
            "Pistolets": "15 PV"
        },

        "Niveau 5": {
            "Pistolets": "15 PV"
        },

        "Niveau 7": {
            "Cle_USB": "+20% dégâts",
            "Epee_enflammee": "+10% dégâts"
        },

        "Niveau 10": {
            "Cle_USB": "+20% dégâts",
            "Epee_enflammee": "+10% dégâts"
        },

        "Niveau 11": {
            "Pistolets": "+7% dégâts"
        },

        "Niveau 12": {
            "Epee_enflammee": "+10% dégâts"
        },

        "Niveau 14": {
            "Epee_enflammee": "+3% dégâts"
        },

        "Niveau 15": {
            "Pistolets": "+7% dégâts"
        },

        "Niveau 16": {
            "Pistolets": "+7% dégâts"
        },

        "Niveau 17": {
            "Epee_enflammee": "+10% dégâts"
        },

        "Niveau 18": {
            "Epee_enflammee": "+15% dégâts"
        },

        "Niveau 19": {
            "Ticket_de_metro": "20 PV",
            "Cle_USB": "+10% dégâts"
        },

        "Niveau 20": {
            "Ticket_de_metro": "20 PV",
            "Epee_enflammee": "+15% dégâts"
        },

        "Niveau 21": {
            "Ticket_de_metro": "20 PV",
            "Cle_USB": "+10% dégâts"
        },

        "Niveau 22": {
            "Cle_USB": "+10% dégâts"
        },

        "Niveau 23": {
            "Pistolets": "+7% dégâts"
        },

        "Niveau 24": {
            "Pistolets": "+7% dégâts",
            "Epee_de_Guts": "40 PV"
        },

        "Niveau 26": {
            "Epee_enflammee": "+15% dégâts",
            "Cle_USB": "+20% dégâts"
        }
    },


    "Fille_populaire": {

        "Niveau 1": {
            "Faux_cils": "15 PV",
            "Fer_a_lisser": "19 PV"
        },

        "Niveau 2": {
            "Faux_cils": "+10% dégâts"
        },

        "Niveau 3": {
            "Faux_cils": "+15% dégâts"
        },

        "Niveau 4": {
            "Faux_ongles_roses": "23 PV",
            "Bracelet_de_sa_soeur": "10 PV"
        },

        "Niveau 5": {
            "Bracelet_de_sa_soeur": "+9% dégâts",
            "Fer_a_lisser": "19 PV"
        },

        "Niveau 7": {
            "Faux_ongles_roses": "+20% dégâts",
            "Bracelet_de_sa_soeur": "+7% dégâts"
        },

        "Niveau 8": {
            "Faux_cils": "+10% dégâts"
        },

        "Niveau 9": {
            "Fer_a_lisser": "+10% dégâts"
        },

        "Niveau 10": {
            "Faux_ongles_roses": "+20% dégâts",
            "Bracelet_de_sa_soeur": "+10% dégâts"
        },

        "Niveau 11": {
            "Fer_a_lisser": "+7% dégâts"
        },

        "Niveau 12": {
            "Bracelet_de_sa_soeur": "+10% dégâts",
            "Faux_cils": "+15% dégâts"
        },

        "Niveau 13": {
            "Bracelet_de_sa_soeur": "+10% dégâts"
        },

        "Niveau 15": {
            "Fer_a_lisser": "+7% dégâts"
        },

        "Niveau 16": {
            "Fer_a_lisser": "+7% dégâts"
        },

        "Niveau 17": {
            "Bracelet_de_sa_soeur": "+10% dégâts"
        },

        "Niveau 18": {
            "Bracelet_de_sa_soeur": "+15% dégâts"
        },

        "Niveau 19": {
            "Faux_ongles_roses": "+12% dégâts"
        },

        "Niveau 21": {
            "Faux_cils": "+15% dégâts"
        },

        "Niveau 23": {
            "Fer_a_lisser": "+7% dégâts"
        },

        "Niveau 24": {
            "Fer_a_lisser": "+7% dégâts",
            "Ring_light": "40 PV"
        },

        "Niveau 26": {
            "Bracelet_de_sa_soeur": "+15% dégâts",
            "Faux_ongles_roses": "+20% dégâts"
        }
    },


    "Nonne": {

        "Niveau 1": {
            "Croix_marron": "14 PV",
            "Feu_de_l'Esprit_Saint": "23 PV"
        },

        "Niveau 3": {
            "Croix_marron": "+15% dégâts"
        },

        "Niveau 4": {
            "Feu_de_l'Esprit_Saint": "23 PV",
            "Medaille_de_bapteme": "15 PV"
        },

        "Niveau 7": {
            "Feu_de_l'Esprit_Saint": "+20% dégâts"
        },

        "Niveau 8": {
            "Coiffe_de_rameau": "19 PV"
        },

        "Niveau 10": {
            "Feu_de_l'Esprit_Saint": "+20% dégâts",
            "Medaille_de_bapteme": "+10% dégâts"
        },

        "Niveau 12": {
            "Medaille_de_bapteme": "+10% dégâts"
        },

        "Niveau 13": {
            "Medaille_de_bapteme": "+10% dégâts"
        },

        "Niveau 14": {
            "Feu_de_l'Esprit_Saint": "+20% dégâts"
        },

        "Niveau 17": {
            "Medaille_de_bapteme": "+10% dégâts"
        },

        "Niveau 18": {
            "Medaille_de_bapteme": "+15% dégâts"
        },

        "Niveau 20": {
            "Medaille_de_bapteme": "+15% dégâts"
        },

        "Niveau 24": {
            "Ring_light": "40 PV"
        },

        "Niveau 26": {
            "Medaille_de_bapteme": "+15% dégâts",
            "Feu_de_l'Esprit_Saint": "+20% dégâts"
        }
    }

    }


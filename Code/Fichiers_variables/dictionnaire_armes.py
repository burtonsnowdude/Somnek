from Fichiers_variables.traitement_images import *

GESTION_DES_ARMES = {

    "Nerd": {
        "Cle_USB":        {"effet": "degats", "max": 30},
        "Epee_enflammee": {"effet": "degats", "max": 15},
        "Pistolets":      {"effet": "attaque", "max": 2.0},
        "Ticket_de_metro":{"effet": "degats", "max": 20},
        "Epee_de_Guts":   {"effet": "degats", "max": 40}
    },

    "Fille_populaire": {
        "Gloss_rose":            {"effet": "degats", "max": 45},
        "Faux_cils":             {"effet": "degats", "max": 20},
        "Bracelet_de_sa_soeur":  {"effet": "degats", "max": 19},
        "Faux_ongles_roses":     {"effet": "degats", "max": 23},
        "Fer_a_lisser":          {"effet": "degats", "max": 19},
        "Pass_Navigo":           {"effet": "degats", "max": 20},
        "Ring_light":            {"effet": "degats", "max": 40},
        "Highlighter":           {"effet": "degats", "max": 40}
    },

    "Nonne": {
        "Feu_de_l'Esprit_Saint": {"effet": "degats", "max": 23},
        "Medaille_de_bapteme":   {"effet": "degats", "max": 16},
        "Coiffe_de_rameau":      {"effet": "degats", "max": 19},
        "Croix_marron":          {"effet": "degats", "max": 14},
        "JALAMBAYA":             {"effet": "degats", "max": 20}
    }
}

TYPES_ARMES = {

    "Nerd": {

        "Epee_bleue": {
            "type_arme": "coup",
            "image": EPEE_BLEUE,
            "texte": "Donne +20% de douleur. Dégât de base : 4PV",
            "dgbase": 4
        },

        "Cle_USB": {
            "type_arme": "zone",
            "image": CLE_USB,
            "texte": "Crée une zone dévastatrice en forme de virus dans la direction opposée. Dégât de base : 23PV",
            "dgbase": 23
        },

        "Epee_enflammee": {
            "type_arme": "coup",
            "image": EPEE_ENFLAMMEE,
            "texte": "Tire sur un ennemi aléatoire, inflige de lourds dégâts. Dégât de base : 10PV",
            "dgbase": 10
        },

        "Pistolets": {
            "type_arme": "balle",
            "image": PISTOLETS,
            "texte": "Génère de fines zones de dégâts. Échelle à haute quantité. Dégât de base : 15PV",
            "dgbase": 15
        },

        "Ticket_de_metro": {
            "type_arme": "trait",
            "image": TICKET,
            "texte": "Attaque verticalement, traverse les ennemis. Dégât de base : 20PV",
            "dgbase": 20
        },

        "Epee_de_Guts": {
            "type_arme": "coup",
            "image": EPEE_GUTS,
            "texte": "Tire rapidement dans quatre directions fixes. Dégât de base : 40PV",
            "dgbase": 40
        },

        "Console_allumee": {
            "type_arme": "zone",
            "image": CONSOLE,
            "texte": "Augmente la Puissance des ennemis de 10% pendant 1 minute et augmente la Puissance du personnage de 20% pendant 2 minutes"
        }
    },

    "Fille_populaire": {

        "Gloss_rose": {
            "type_arme": "zone",
            "image": GLOSS_ROSE,
            "texte": "Crée des zones de destruction. Dégâts de base : 10PV.",
            "dgbase": 10
        },

        "Faux_cils": {
            "type_arme": "trait",
            "image": FAUX_CILS,
            "texte": "Attaque horizontalement et traverse les ennemis. Réduit les dégâts entrants. Dégâts de base : 15PV.",
            "dgbase": 15
        },

        "Faux_ongles_roses": {
            "type_arme": "zone",
            "image": FAUX_ONGLE,
            "texte": "Crée une zone dévastatrice derrière le personnage. Dégâts de base : 23PV.",
            "dgbase": 23
        },

        "Bracelet_de_sa_soeur": {
            "type_arme": "balle",
            "image": BRACELET_SOEUR,
            "texte": "Tire sur un ennemi aléatoire et inflige de lourds dégâts. Dégâts de base : 16PV.",
            "dgbase": 16
        },

        "Fer_a_lisser": {
            "type_arme": "zone_multiples",
            "image": FER_A_LISSER,
            "texte": "Génère plusieurs zones de dégâts. Dégâts de base : 19PV.",
            "dgbase": 19
        },

        "Pass_Navigo": {
            "type_arme": "trait",
            "image": PASS_NAVIGO,
            "texte": "Attaque verticalement et traverse les ennemis. Dégâts de base : 20PV.",
            "dgbase": 20
        },

        "Ring_light": {
            "type_arme": "zone_multiples",
            "image": RING_LIGHT,
            "texte": "Tire rapidement dans quatre directions fixes. Dégâts de base : 40PV.",
            "dgbase": 40
        },

        
        "Highlighter": {
            "type_arme": "orbital",
            "image": HIGLIGHTER,
            "texte": "Jette des étoiles trop joliesss. Dégâts de base : 10PV.",
            "dgbase": 10
        }
    },

    "Nonne": {

        "Croix_marron": {
            "type_arme": "poison",
            "image": CROIX_DE_BASE,
            "texte": "Une croix marron qui donne +22% en santé. Dégâts de base : 14PV.",
            "dgbase": 14
        },

        "Feu_de_l'Esprit_Saint": {
            "type_arme": "zone",
            "image": FEU_SAINT,
            "texte": "Crée une zone dévastatrice en forme de virus dans la direction opposée. Dégât de base : 23PV.",
            "dgbase": 23
        },

        "Medaille_de_bapteme": {
            "type_arme": "balle",
            "image": MEDAILLON,
            "texte": "Tire sur un ennemi aléatoire, inflige de lourds dégâts. Dégât de base : 15PV.",
            "dgbase": 15
        },

        "Coiffe_de_rameau": {
            "type_arme": "zone",
            "image": COURONNE,
            "texte": "Génère de fines zones de dégâts. Échelle à haute quantité. Dégât de base : 19PV.",
            "dgbase": 19
        },

        "Lance_sacree": {
            "type_arme": "trait",
            "image": LANCE_SACREE,
            "texte": "Attaque verticalement, traverse les ennemis. Dégât de base : 20PV.",
            "dgbase": 20
        },

        "Aura_divine": {
            "type_arme": "orbital_explosion",
            "image": AURA_DIVINE,
            "texte": "Tourne autour du personnage et inflige des dégâts. Dégât de base : 40PV.",
            "dgbase": 40
        },

        "JALAMBAYA": {
            "type_arme": "balle",
            "image": JALAMBAYA,
            "texte": "Tire rapidement dans quatre directions fixes. Dégât de base : 70PV.",
            "dgbase": 70
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

        "Gloss_rose": {
            **TYPES_ARMES["Fille_populaire"]["Gloss_rose"],
            "niveau_req": 1
        },

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
        },

        "Highlighter": {
            **TYPES_ARMES["Fille_populaire"]["Highlighter"],
            "niveau_req": 10
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

        # CORRECTION : était Ring_light → Aura_divine
        "Aura_divine": {
            **TYPES_ARMES["Nonne"]["Aura_divine"],
            "niveau_req": 24
        },

        "JALAMBAYA": {
            **TYPES_ARMES["Nonne"]["JALAMBAYA"],
            "niveau_req": 28
        }
    }
}


GESTION_DES_NIVEAUX_ARMES = {

    "Nerd": {
        "Niveau 4":  ["Cle_USB", "Epee_enflammee", "Pistolets"],
        "Niveau 5":  ["Pistolets"],
        "Niveau 7":  ["Cle_USB", "Epee_enflammee"],
        "Niveau 10": ["Cle_USB", "Epee_enflammee"],
        "Niveau 11": ["Pistolets"],
        "Niveau 12": ["Epee_enflammee"],
        "Niveau 14": ["Epee_enflammee"],
        "Niveau 15": ["Pistolets"],
        "Niveau 16": ["Pistolets"],
        "Niveau 17": ["Epee_enflammee"],
        "Niveau 18": ["Epee_enflammee"],
        "Niveau 19": ["Ticket_de_metro", "Cle_USB"],
        "Niveau 20": ["Ticket_de_metro", "Epee_enflammee"],
        "Niveau 21": ["Ticket_de_metro", "Cle_USB"],
        "Niveau 22": ["Cle_USB"],
        "Niveau 23": ["Pistolets"],
        "Niveau 24": ["Pistolets", "Epee_de_Guts"],
        "Niveau 26": ["Epee_enflammee", "Cle_USB"]
    },

    "Fille_populaire": {
        "Niveau 1":  ["Faux_cils", "Fer_a_lisser"],
        "Niveau 2":  ["Faux_cils"],
        "Niveau 3":  ["Faux_cils"],
        "Niveau 4":  ["Faux_ongles_roses", "Bracelet_de_sa_soeur"],
        "Niveau 5":  ["Bracelet_de_sa_soeur", "Fer_a_lisser"],
        "Niveau 7":  ["Faux_ongles_roses", "Bracelet_de_sa_soeur"],
        "Niveau 8":  ["Faux_cils"],
        "Niveau 9":  ["Fer_a_lisser", "Gloss_rose"],
        "Niveau 10": ["Faux_ongles_roses", "Bracelet_de_sa_soeur", "Highlighter"],
        "Niveau 11": ["Fer_a_lisser"],
        "Niveau 12": ["Bracelet_de_sa_soeur", "Faux_cils", "Gloss_rose"],
        "Niveau 13": ["Bracelet_de_sa_soeur"],
        "Niveau 15": ["Fer_a_lisser"],
        "Niveau 16": ["Fer_a_lisser", "Gloss_rose"],
        "Niveau 17": ["Bracelet_de_sa_soeur", "Gloss_rose"],
        "Niveau 18": ["Bracelet_de_sa_soeur"],
        "Niveau 19": ["Faux_ongles_roses"],
        "Niveau 21": ["Faux_cils"],
        "Niveau 23": ["Fer_a_lisser"],
        "Niveau 24": ["Fer_a_lisser", "Ring_light"],
        "Niveau 26": ["Bracelet_de_sa_soeur", "Faux_ongles_roses"]
    },

    "Nonne": {
        "Niveau 1":  ["Croix_marron", "Feu_de_l'Esprit_Saint"],
        "Niveau 3":  ["Croix_marron"],
        "Niveau 4":  ["Feu_de_l'Esprit_Saint", "Medaille_de_bapteme"],
        "Niveau 7":  ["Feu_de_l'Esprit_Saint"],
        "Niveau 8":  ["Coiffe_de_rameau"],
        "Niveau 10": ["Feu_de_l'Esprit_Saint", "Medaille_de_bapteme"],
        "Niveau 12": ["Medaille_de_bapteme"],
        "Niveau 13": ["Medaille_de_bapteme"],
        "Niveau 14": ["Feu_de_l'Esprit_Saint"],
        "Niveau 17": ["Medaille_de_bapteme"],
        "Niveau 18": ["Medaille_de_bapteme"],
        "Niveau 20": ["Medaille_de_bapteme"],
        "Niveau 24": ["Aura_divine"],
        "Niveau 26": ["Medaille_de_bapteme", "Feu_de_l'Esprit_Saint"]
    }
}
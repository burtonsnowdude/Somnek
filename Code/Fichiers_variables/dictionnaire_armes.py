from Fichiers_variables.traitement_images import *


TYPES_ARMES = {

    "Nerd": {

        "Epée bleue": {
            "type_arme": "coup",
            "image": None,
            "texte": None
        },

        "Clé USB": {
            "type_arme": "zone",
            "image": CLE_USB,
            "texte": None
        },

        "Epée enflammée": {
            "type_arme": "coup",
            "image": None,
            "texte": None
        },

        "Pistolets": {
            "type_arme": "balle",
            "image": PISTOLETS,
            "texte": None
        },

        "Ticket de métro": {
            "type_arme": "trait",
            "image": None,
            "texte": None
        },

        "Epée de Guts": {
            "type_arme": "coup",
            "image": None,
            "texte": None
        },

        "Console allumée": {
            "type_arme": "zone",
            "image": None,
            "texte": None
        }
    },

    "Fille populaire": {

        "Faux-cils": {
            "type_arme": "trait",
            "image": None,
            "texte": None
        },

        "Faux ongles roses": {
            "type_arme": "zone",
            "image": None,
            "texte": None
        },

        "Bracelet de sa soeur": {
            "type_arme": "balle",
            "image": None,
            "texte": None
        },

        "Fer à lisser": {
            "type_arme": "zone multiples",
            "image": None,
            "texte": None
        },

        "Pass Navigo": {
            "type_arme": "trait",
            "image": None,
            "texte": None
        },

        "Ring light": {
            "type_arme": "zone multiples",
            "image": None,
            "texte": None
        }
    },

    "La soeur": {

        "Croix Marron": {
            "type_arme": "poison",
            "image": None,
            "texte": None
        },

        "Feu de l’Esprit Saint": {
            "type_arme": "zone",
            "image": None,
            "texte": None
        },

        "Médaille de baptême": {
            "type_arme": "balle",
            "image": None,
            "texte": None
        },

        "Coiffe de rameau": {
            "type_arme": "zone",
            "image": None,
            "texte": None
        },

        "Lance sacrée": {
            "type_arme": "trait",
            "image": None,
            "texte": None
        },

        "Aura divine": {
            "type_arme": "poison",
            "image": None,
            "texte": None
        }
    }
}

ARMES = {

    "Nerd": {

        "Epée bleue": {
            **TYPES_ARMES["Nerd"]["Epée bleue"],
            "niveau_req": 1
        },

        "Lunettes cassées": {
            **TYPES_ARMES["Nerd"]["Lunettes cassées"],
            "niveau_req": 1
        },

        "Souris de PC": {
            **TYPES_ARMES["Nerd"]["Souris de PC"],
            "niveau_req": 1
        },

        "Chaussettes propres": {
            **TYPES_ARMES["Nerd"]["Chaussettes propres"],
            "niveau_req": 1
        },

        "Cahier de NSI": {
            **TYPES_ARMES["Nerd"]["Cahier de NSI"],
            "niveau_req": 3
        },

        "Clé USB": {
            **TYPES_ARMES["Nerd"]["Clé USB"],
            "niveau_req": 4
        },

        "Epée enflammée": {
            **TYPES_ARMES["Nerd"]["Epée enflammée"],
            "niveau_req": 4
        },

        "Pistolets": {
            **TYPES_ARMES["Nerd"]["Pistolets"],
            "niveau_req": 5
        },

        "Ticket de métro": {
            **TYPES_ARMES["Nerd"]["Ticket de métro"],
            "niveau_req": 19
        },

        "Epée de Guts": {
            **TYPES_ARMES["Nerd"]["Epée de Guts"],
            "niveau_req": 24
        }
    },

    "Fille populaire": {

        "Faux-cils": {
            **TYPES_ARMES["Fille populaire"]["Faux-cils"],
            "niveau_req": 1
        },

        "Faux ongles roses": {
            **TYPES_ARMES["Fille populaire"]["Faux ongles roses"],
            "niveau_req": 4
        },

        "Bracelet de sa soeur": {
            **TYPES_ARMES["Fille populaire"]["Bracelet de sa soeur"],
            "niveau_req": 4
        },

        "Fer à lisser": {
            **TYPES_ARMES["Fille populaire"]["Fer à lisser"],
            "niveau_req": 5
        },

        "Pass Navigo": {
            **TYPES_ARMES["Fille populaire"]["Pass Navigo"],
            "niveau_req": 19
        },

        "Ring light": {
            **TYPES_ARMES["Fille populaire"]["Ring light"],
            "niveau_req": 24
        }
    },

    "La soeur": {

        "Croix Marron": {
            **TYPES_ARMES["La soeur"]["Croix Marron"],
            "niveau_req": 0
        },

        "Feu de l’Esprit Saint": {
            **TYPES_ARMES["La soeur"]["Feu de l’Esprit Saint"],
            "niveau_req": 4
        },

        "Médaille de baptême": {
            **TYPES_ARMES["La soeur"]["Médaille de baptême"],
            "niveau_req": 4
        },

        "Coiffe de rameau": {
            **TYPES_ARMES["La soeur"]["Coiffe de rameau"],
            "niveau_req": 5
        },

        "Lance sacrée": {
            **TYPES_ARMES["La soeur"]["Lance sacrée"],
            "niveau_req": 19
        },

        "Aura divine": {
            **TYPES_ARMES["La soeur"]["Aura divine"],
            "niveau_req": 24
        }
    }
}

GESTION_DES_NIVEAUX_ARMES = {

"Nerd": {

    "Niveau 4": {
        "Clé USB": "23 PV",
        "Épée enflammée": "10 PV",
        "Pistolets": "15 PV"
    },

    "Niveau 5": {
        "Pistolets": "15 PV"
    },

    "Niveau 7": {
        "Clé USB": "+20% dégâts",
        "Épée enflammée": "+10% dégâts"
    },

    "Niveau 10": {
        "Clé USB": "+20% dégâts",
        "Épée enflammée": "+10% dégâts"
    },

    "Niveau 11": {
        "Pistolets": "+7% dégâts"
    },

    "Niveau 12": {
        "Épée enflammée": "+10% dégâts"
    },

    "Niveau 14": {
        "Épée enflammée": "+3% dégâts"
    },

    "Niveau 15": {
        "Pistolets": "+7% dégâts"
    },

    "Niveau 16": {
        "Pistolets": "+7% dégâts"
    },

    "Niveau 17": {
        "Épée enflammée": "+10% dégâts"
    },

    "Niveau 18": {
        "Épée enflammée": "+15% dégâts"
    },

    "Niveau 19": {
        "Ticket de métro": "20 PV",
        "Clé USB": "+10% dégâts"
    },

    "Niveau 20": {
        "Ticket de métro": "20 PV",
        "Épée enflammée": "+15% dégâts"
    },

    "Niveau 21": {
        "Ticket de métro": "20 PV",
        "Clé USB": "+10% dégâts"
    },

    "Niveau 22": {
        "Clé USB": "+10% dégâts"
    },

    "Niveau 23": {
        "Pistolets": "+7% dégâts"
    },

    "Niveau 24": {
        "Pistolets": "+7% dégâts",
        "Épée de Guts": "40 PV"
    },

    "Niveau 26": {
        "Épée enflammée": "+15% dégâts",
        "Clé USB": "+20% dégâts"
    }
},


"Fille populaire": {

    "Niveau 1": {
        "Faux-cils": "15 PV",
        "Fer à lisser": "19 PV"
    },

    "Niveau 2": {
        "Faux-cils": "+10% dégâts"
    },

    "Niveau 3": {
        "Faux-cils": "+15% dégâts"
    },

    "Niveau 4": {
        "Faux ongles roses": "23 PV",
        "Bracelet": "10 PV"
    },

    "Niveau 5": {
        "Bracelet": "+9% dégâts",
        "Fer à lisser": "19 PV"
    },

    "Niveau 7": {
        "Faux ongles roses": "+20% dégâts",
        "Bracelet": "+7% dégâts"
    },

    "Niveau 8": {
        "Faux-cils": "+10% dégâts"
    },

    "Niveau 9": {
        "Fer à lisser": "+10% dégâts"
    },

    "Niveau 10": {
        "Faux ongles roses": "+20% dégâts",
        "Bracelet": "+10% dégâts"
    },

    "Niveau 11": {
        "Fer à lisser": "+7% dégâts"
    },

    "Niveau 12": {
        "Bracelet": "+10% dégâts",
        "Faux-cils": "+15% dégâts"
    },

    "Niveau 13": {
        "Bracelet": "+10% dégâts"
    },

    "Niveau 15": {
        "Fer à lisser": "+7% dégâts"
    },

    "Niveau 16": {
        "Fer à lisser": "+7% dégâts"
    },

    "Niveau 17": {
        "Bracelet": "+10% dégâts"
    },

    "Niveau 18": {
        "Bracelet": "+15% dégâts"
    },

    "Niveau 19": {
        "Faux ongles roses": "+12% dégâts"
    },

    "Niveau 21": {
        "Faux-cils": "+15% dégâts"
    },

    "Niveau 23": {
        "Fer à lisser": "+7% dégâts"
    },

    "Niveau 24": {
        "Fer à lisser": "+7% dégâts",
        "Ring light": "40 PV"
    },

    "Niveau 26": {
        "Bracelet": "+15% dégâts",
        "Faux ongles roses": "+20% dégâts"
    }
},


"La soeur": {

    "Niveau 1": {
        "Croix marron": "14 PV",
        "Feu de l’Esprit Saint": "23 PV"
    },

    "Niveau 3": {
        "Croix marron": "+15% dégâts"
    },

    "Niveau 4": {
        "Feu de l’Esprit Saint": "23 PV",
        "Médaille de baptême": "15 PV"
    },

    "Niveau 7": {
        "Feu de l’Esprit Saint": "+20% dégâts"
    },

    "Niveau 8": {
        "Coiffe de rameau": "19 PV"
    },

    "Niveau 10": {
        "Feu de l’Esprit Saint": "+20% dégâts",
        "Médaille de baptême": "+10% dégâts"
    },

    "Niveau 12": {
        "Médaille de baptême": "+10% dégâts"
    },

    "Niveau 13": {
        "Médaille de baptême": "+10% dégâts"
    },

    "Niveau 14": {
        "Feu de l’Esprit Saint": "+20% dégâts"
    },

    "Niveau 17": {
        "Médaille de baptême": "+10% dégâts"
    },

    "Niveau 18": {
        "Médaille de baptême": "+15% dégâts"
    },

    "Niveau 20": {
        "Médaille de baptême": "+15% dégâts"
    },

    "Niveau 24": {
        "Ring light": "40 PV"
    },

    "Niveau 26": {
        "Médaille de baptême": "+15% dégâts",
        "Feu de l’Esprit Saint": "+20% dégâts"
    }
}

}


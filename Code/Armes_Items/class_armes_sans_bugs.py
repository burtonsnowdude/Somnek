from Fichiers_variables.dictionnaire_armes import TYPES_ARMES, GESTION_DES_NIVEAUX_ARMES

class Arme:
    Carac_base = {
        "type_arme": None,
        "dgbase": 0,
        "prix": 0,
        "portee": 0,
        "reduction": 0,
        "niveau_req": 0,
        "niveau": 0
    }
    arme_possede = []
    ARMES = {
        "Epee_bleu": {
            **Carac_base,
            "dgbase": 4,
            "prix": 0,
            "niveau_req": 0,
            "niveau": 1
        },
        "Cle_usb": {
            **Carac_base,
            "dgbase": 23,
            "prix": 9,
            "niveau_req": 4,
            "niveau": 1
        },
        "Epee_enflammee": {
            **Carac_base,
            "dgbase": 10,
            "prix": 2,
            "niveau_req": 4,
            "niveau": 1
        },
        "Ticket_de_metro": {
            **Carac_base,
            "dgbase": 10,
            "prix": 2,
            "niveau_req": 4,
            "niveau": 1
        }
    }

    def __init__(self, nom_arme, perso="Nerd"):
        if nom_arme not in self.ARMES:
            raise ValueError(f"Arme '{nom_arme}' inconnue")
        self.nom = nom_arme
        self.perso = perso
        self.caracteristiques = self.ARMES[nom_arme].copy()
        self.attack = self.caracteristiques["dgbase"]

        type_data = TYPES_ARMES.get(perso, {}).get(nom_arme, {})
        self.image = type_data.get("image", None)

    def levelup_depuis_niveau(self, niveau_joueur):
        nv_key = f"Niveau {niveau_joueur}"
        bonus = GESTION_DES_NIVEAUX_ARMES.get(self.perso, {}).get(nv_key, {})
        if self.nom in bonus:
            valeur = bonus[self.nom]
            if isinstance(valeur, str) and "%" in valeur:
                pct = float(valeur.replace("+", "").replace("% dégâts", "").strip()) / 100
                self.caracteristiques["dgbase"] *= (1 + pct)
            elif isinstance(valeur, (int, float)):
                self.caracteristiques["dgbase"] += valeur
        self.attack = self.caracteristiques["dgbase"]

    def calculer_degat(self):
        degat = self.caracteristiques["dgbase"]
        reduction = self.caracteristiques["reduction"]
        return degat - reduction if reduction > 0 else degat
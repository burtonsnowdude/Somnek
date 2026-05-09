from Fichiers_variables.dictionnaire_armes import TYPES_ARMES, GESTION_DES_NIVEAUX_ARMES, ARMES as ARMES_PAR_PERSO

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

    # Construction automatique : on aplatit ARMES_PAR_PERSO en un seul dico {nom_arme: data}
    ARMES = {}
    for _perso, _armes in ARMES_PAR_PERSO.items():
        for _nom, _data in _armes.items():
            ARMES[_nom] = {**Carac_base, **_data}

    def __init__(self, nom_arme, perso="Nerd"):
        if nom_arme not in self.ARMES:
            raise ValueError(f"Arme '{nom_arme}' inconnue")
        self.nom = nom_arme
        self.perso = perso
        self.caracteristiques = self.ARMES[nom_arme].copy()
        self.attack = self.caracteristiques.get("dgbase", 0)

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
        reduction = self.caracteristiqu
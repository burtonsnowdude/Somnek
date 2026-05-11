"""
class_armes_sans_bugs.py — SOMNEK

CORRECTIONS :
- Le check `if dgbase <= 0` est désormais DANS la boucle de construction
  (avant, il ne vérifiait que la dernière arme aplatie → silencieux mais buggy)
- `levelup_depuis_niveau` gère le nouveau format LISTE de
  GESTION_DES_NIVEAUX_ARMES (avant : `bonus[self.nom]` sur une liste → TypeError)
- `calculer_degat` complétée proprement
"""

from Fichiers_variables.dictionnaire_armes import (
    TYPES_ARMES,
    GESTION_DES_NIVEAUX_ARMES,
    ARMES as ARMES_PAR_PERSO,
)


class Arme:
    Carac_base = {
        "type_arme":  None,
        "dgbase":     0,
        "prix":       0,
        "portee":     0,
        "reduction":  0,
        "niveau_req": 0,
        "niveau":     0,
    }
    arme_possede = []

    # ── Construction du dico aplati {nom_arme: data} ───────────────────
    # FIX : check `dgbase <= 0` DANS la boucle (pour chaque arme, pas
    #       seulement la dernière).
    ARMES = {}
    for _perso, _armes in ARMES_PAR_PERSO.items():
        for _nom, _data in _armes.items():
            ARMES[_nom] = {**Carac_base, **_data}
            if ARMES[_nom]["dgbase"] <= 0:
                ARMES[_nom]["dgbase"] = 10

    def __init__(self, nom_arme, perso="Nerd"):
        if nom_arme not in self.ARMES:
            raise ValueError(f"Arme '{nom_arme}' inconnue")
        self.nom              = nom_arme
        self.perso            = perso
        self.caracteristiques = self.ARMES[nom_arme].copy()
        self.attack           = self.caracteristiques.get("dgbase", 10)

        type_data  = TYPES_ARMES.get(perso, {}).get(nom_arme, {})
        self.image = type_data.get("image", None)

    def levelup_depuis_niveau(self, niveau_joueur, bonus_pct: float = 0.20):
        """
        Augmente les dégâts de base si l'arme est listée dans
        GESTION_DES_NIVEAUX_ARMES au niveau donné.

        FIX : `bonus` est une liste de noms d'armes maintenant, pas un dict.
              Si self.nom est listé → on applique `bonus_pct` (+20% par défaut).
        """
        nv_key     = f"Niveau {niveau_joueur}"
        bonus_list = GESTION_DES_NIVEAUX_ARMES.get(self.perso, {}).get(nv_key, [])
        if self.nom in bonus_list:
            self.caracteristiques["dgbase"] *= (1 + bonus_pct)
        self.attack = self.caracteristiques["dgbase"]

    def calculer_degat(self, reduction_ennemi: float = 0.0) -> float:
        """Retourne les dégâts effectifs après réduction éventuelle de l'ennemi."""
        degat = self.caracteristiques["dgbase"]
        return max(0.0, degat * (1.0 - reduction_ennemi))
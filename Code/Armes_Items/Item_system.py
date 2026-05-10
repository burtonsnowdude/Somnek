"""
Système d'items — SOMNEK
Gère l'inventaire d'items d'un joueur et calcule les bonus actifs.
S'intègre avec choix_arme() : equiper_item(nom, niveau) lit la valeur
exacte définie dans GESTION_NIVEAU_ITEMS pour ce niveau.
"""

from Fichiers_variables.dictionnaire_items import GESTION_NIVEAU_ITEMS, ITEMS_PAR_PERSO


class Item:
    def __init__(self, nom: str, perso: str, valeur: float):
        catalogue = ITEMS_PAR_PERSO.get(perso, {})
        if nom not in catalogue:
            raise ValueError(f"Item '{nom}' inconnu pour '{perso}'.")
        self.nom    = nom
        self.perso  = perso
        self.valeur = valeur
        self.config = catalogue[nom]
        self.effet  = self.config["effet"]
        self.max    = self.config["max"]

    @property
    def valeur_plafonnee(self) -> float:
        return min(self.valeur, self.max)

    def __repr__(self):
        return f"<Item {self.nom} | {self.effet} | {self.valeur_plafonnee:.2f}/{self.max}>"




class InventaireItems:
    """
    Inventaire d'items d'UN personnage.

    Flux normal (en jeu) :
        # choix_arme() retourne ("item", "Cle_USB") au niveau 4
        p.inventaire_items.equiper_item("Cle_USB", p.niveau)
        appliquer_stats_items(p, p.inventaire_items.calculer_stats())
    """

    def __init__(self, perso: str):
        if perso not in ITEMS_PAR_PERSO:
            raise ValueError(f"Personnage '{perso}' inconnu.")
        self.perso  = perso
        self._items: dict = {}

    

    def equiper_item(self, nom_item: str, niveau: int):
        """
        Appelé quand choix_arme() retourne ("item", nom_item).
        Cherche la valeur dans GESTION_NIVEAU_ITEMS[perso]["Niveau N"].
        Si absente à ce niveau, remonte aux niveaux précédents.
        """
        valeur = self._valeur_au_niveau(nom_item, niveau)
        if valeur == 0:
            valeur = self._derniere_valeur(nom_item, niveau)
        if isinstance(valeur, tuple):
            valeur = sum(valeur) / len(valeur)
        self._ajouter(nom_item, float(valeur))

    def possede(self, nom_item: str) -> bool:
        return nom_item in self._items

    def lister(self):
        return list(self._items.values())

   

    def calculer_stats(self) -> dict:
        """
        Retourne tous les bonus actifs, plafonnés, prêts à être appliqués.

        Clés retournées :
            cooldown_reduction  [0, 0.90]
            bonus_sante         [0, 2.0]
            bonus_vitesse       [0, 0.50]
            reduction_degats    [0, 0.90]   (multiplicatif)
            bonus_cupidite      [0, 0.50]
            bonus_quantite      int
            regen_par_sec       float
            bonus_chance        [0, 1.00]
            bonus_duree         [0, 2.0]
            resurrection        bool
            bonus_zone          [0, 0.50]
            bonus_attirance     float       (px supplémentaires)
            bonus_degats        float       (dégâts fixes)
            bonus_attaque       float       (multiplicateur, base 1.0)
            multi_effets        dict
        """
        stats = {
            "cooldown_reduction": 0.0,
            "bonus_sante":        0.0,
            "bonus_vitesse":      0.0,
            "reduction_degats":   0.0,
            "bonus_cupidite":     0.0,
            "bonus_quantite":     0,
            "regen_par_sec":      0.0,
            "bonus_chance":       0.0,
            "bonus_duree":        0.0,
            "resurrection":       False,
            "bonus_zone":         0.0,
            "bonus_attirance":    0.0,
            "bonus_degats":       0.0,
            "bonus_attaque":      1.0,
            "multi_effets":       {},
        }

        for item in self._items.values():
            v = item.valeur_plafonnee
            e = item.effet

            if   e == "cooldown":
                stats["cooldown_reduction"] = min(stats["cooldown_reduction"] + v, 0.90)
            elif e == "sante":
                stats["bonus_sante"]       += v
            elif e == "vitesse":
                stats["bonus_vitesse"]     += v
            elif e == "protection":
                stats["reduction_degats"]   = 1 - (1 - stats["reduction_degats"]) * (1 - v)
            elif e == "cupidite":
                stats["bonus_cupidite"]    += v
            elif e == "quantite":
                stats["bonus_quantite"]    += int(v)
            elif e == "regen":
                stats["regen_par_sec"]     += v
            elif e == "chance":
                stats["bonus_chance"]      += v
            elif e == "duree":
                stats["bonus_duree"]       += v
            elif e == "resurrection":
                stats["resurrection"]       = True
            elif e == "zone":
                stats["bonus_zone"]        += v
            elif e == "attirance":
                stats["bonus_attirance"]   += v
            elif e == "degats":
                stats["bonus_degats"]      += v
            elif e == "attaque":
                stats["bonus_attaque"]     += v
            elif e == "multi":
                sous = {k: item.config[k] for k in item.config if k not in ("effet", "max")}
                for k, sv in sous.items():
                    stats["multi_effets"][k] = stats["multi_effets"].get(k, 0) + sv

        stats["reduction_degats"] = min(stats["reduction_degats"], 0.90)
        stats["bonus_chance"]     = min(stats["bonus_chance"],      1.00)
        return stats

    

    def _ajouter(self, nom_item: str, valeur: float):
        if nom_item in self._items:
            self._items[nom_item].valeur += valeur
        else:
            self._items[nom_item] = Item(nom_item, self.perso, valeur)

    def _valeur_au_niveau(self, nom_item: str, niveau: int):
        return GESTION_NIVEAU_ITEMS.get(self.perso, {}).get(f"Niveau {niveau}", {}).get(nom_item, 0)

    def _derniere_valeur(self, nom_item: str, jusqu_a: int):
        prog = GESTION_NIVEAU_ITEMS.get(self.perso, {})
        for n in range(jusqu_a, 0, -1):
            val = prog.get(f"Niveau {n}", {}).get(nom_item)
            if val is not None:
                return val
        return 0.0




def appliquer_stats_items(joueur, stats: dict):
    """
    Recalcul complet des stats à partir des valeurs BASE du joueur.
    À appeler après chaque equiper_item().

    Le joueur doit avoir (définis dans Player.__init__) :
        hp_max_base, vitesse_base, zone_base, portee_xp_base
    """
    joueur.hp_max          = int(joueur.hp_max_base * (1 + stats["bonus_sante"]))
    joueur.hp              = min(joueur.hp, joueur.hp_max)
    joueur.vitesse         = joueur.vitesse_base * (1 + stats["bonus_vitesse"])

    # Bonus stockés sur le joueur, utilisés par les armes et la boucle de jeu
    joueur.bonus_degats      = stats["bonus_degats"]
    joueur.attaque_mult      = stats["bonus_attaque"]
    joueur.cooldown_reduction= stats["cooldown_reduction"]
    joueur.argent_bonus      = stats["bonus_cupidite"]
    joueur.nb_projectiles    = max(1, 1 + stats["bonus_quantite"])
    joueur.regen             = stats["regen_par_sec"]
    joueur.chance            = stats["bonus_chance"]
    joueur.duree_effets      = 1.0 + stats["bonus_duree"]
    joueur.resurrection      = stats["resurrection"]
    joueur.zone_attaque      = joueur.zone_base * (1 + stats["bonus_zone"])
    joueur.portee_xp         = joueur.portee_xp_base + stats["bonus_attirance"]
    joueur.reduction_degats  = stats["reduction_degats"]

    for k, v in stats["multi_effets"].items():
        if k == "vitesse":
            joueur.vitesse  *= (1 + v)
        elif k == "sante":
            joueur.hp_max    = int(joueur.hp_max * (1 + v))
            joueur.hp        = min(joueur.hp, joueur.hp_max)
"""
Item_system.py — SOMNEK


"""

from Fichiers_variables.dictionnaire_items import GESTION_NIVEAU_ITEMS, ITEMS_PAR_PERSO

CADENCE_BASE = 30


class Item:
    def __init__(self, nom: str, perso: str, valeur: float):
        catalogue = ITEMS_PAR_PERSO.get(perso, {})
        if nom not in catalogue:
            raise ValueError(
                f"[Item] '{nom}' inconnu pour '{perso}'. "
                f"Items disponibles : {list(catalogue.keys())}"
            )
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
        return (f"<Item {self.nom} | {self.effet} | "
                f"{self.valeur_plafonnee:.2f}/{self.max}>")




class InventaireItems:
    """
    Inventaire d'items d'UN personnage.

    Si un nom d'ARME est passé par erreur, on logge un warning et on ignore
    proprement — le jeu ne plante pas.
    """

    def __init__(self, perso: str):
        if perso not in ITEMS_PAR_PERSO:
            raise ValueError(f"[InventaireItems] Personnage '{perso}' inconnu.")
        self.perso  = perso
        self._items: dict[str, Item] = {}

    

    def equiper_item(self, nom_item: str, niveau: int):
        catalogue = ITEMS_PAR_PERSO.get(self.perso, {})
        if nom_item not in catalogue:
            print(f"[InventaireItems] WARN: '{nom_item}' ignoré "
                  f"(pas un item de '{self.perso}').")
            return

        valeur = self._valeur_au_niveau(nom_item, niveau)
        if valeur == 0:
            valeur = self._derniere_valeur(nom_item, niveau)

        if isinstance(valeur, (tuple, list)):
            valeur = sum(valeur) / len(valeur)

        valeur = float(valeur)
        if valeur == 0.0:
            valeur = catalogue[nom_item]["max"] / 10
            print(f"[InventaireItems] WARN: valeur 0 pour '{nom_item}' "
                  f"au niveau {niveau}. Fallback={valeur:.3f}")

        self._ajouter(nom_item, valeur)

    def possede(self, nom_item: str) -> bool:
        return nom_item in self._items

    def lister(self) -> list:
        return list(self._items.values())

    

    def calculer_stats(self) -> dict:
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
                stats["cooldown_reduction"] = min(
                    stats["cooldown_reduction"] + v, 0.90)
            elif e == "sante":
                stats["bonus_sante"]     += v
            elif e == "vitesse":
                stats["bonus_vitesse"]   += v
            elif e == "protection":
                # Empilement multiplicatif correct
                stats["reduction_degats"] = 1 - (
                    1 - stats["reduction_degats"]) * (1 - v)
            elif e == "cupidite":
                stats["bonus_cupidite"]  += v
            elif e == "quantite":
                stats["bonus_quantite"]  += int(v)
            elif e == "regen":
                stats["regen_par_sec"]   += v
            elif e == "chance":
                stats["bonus_chance"]    += v
            elif e == "duree":
                stats["bonus_duree"]     += v
            elif e == "resurrection":
                stats["resurrection"]     = True
            elif e == "zone":
                stats["bonus_zone"]      += v
            elif e == "attirance":
                stats["bonus_attirance"] += v
            elif e == "degats":
                stats["bonus_degats"]    += v
            elif e == "attaque":
                stats["bonus_attaque"]   += v
            elif e == "multi":
                sous = {
                    k: item.config[k]
                    for k in item.config
                    if k not in ("effet", "max")
                }
                for k, sv in sous.items():
                    stats["multi_effets"][k] = (
                        stats["multi_effets"].get(k, 0) + sv)

        # Plafonds globaux
        stats["reduction_degats"] = min(stats["reduction_degats"], 0.90)
        stats["bonus_chance"]     = min(stats["bonus_chance"],     1.00)
        return stats

    

    def _ajouter(self, nom_item: str, valeur: float):
        catalogue = ITEMS_PAR_PERSO.get(self.perso, {})
        if nom_item not in catalogue:
            print(f"[InventaireItems] _ajouter ignoré: '{nom_item}' "
                  f"absent du catalogue de '{self.perso}'.")
            return
        if nom_item in self._items:
            self._items[nom_item].valeur += valeur
        else:
            self._items[nom_item] = Item(nom_item, self.perso, valeur)

    def _valeur_au_niveau(self, nom_item: str, niveau: int):
        return (GESTION_NIVEAU_ITEMS
                .get(self.perso, {})
                .get(f"Niveau {niveau}", {})
                .get(nom_item, 0))

    def _derniere_valeur(self, nom_item: str, jusqu_a: int):
        prog = GESTION_NIVEAU_ITEMS.get(self.perso, {})
        for n in range(jusqu_a - 1, 0, -1):
            val = prog.get(f"Niveau {n}", {}).get(nom_item)
            if val is not None:
                return val
        return 0.0




def appliquer_stats_items(joueur, stats: dict):
    """
    Recalcul COMPLET des stats à partir des valeurs BASE du joueur.
    À appeler après chaque equiper_item().

    Le joueur doit avoir (dans Player.__init__) :
        hp_max_base, vitesse_base, zone_base, portee_xp_base
    """
    # On retient l'ancien max pour soigner du delta s'il augmente
    ancien_hp_max  = getattr(joueur, "hp_max", joueur.hp_max_base)
    nouveau_hp_max = int(joueur.hp_max_base * (1 + stats["bonus_sante"]))

    # Multi-effets 
    multi_sante = stats["multi_effets"].get("sante", 0)
    if multi_sante:
        nouveau_hp_max = int(nouveau_hp_max * (1 + multi_sante))

    delta = nouveau_hp_max - ancien_hp_max
    if delta > 0:
        joueur.hp += delta

    joueur.hp_max  = nouveau_hp_max
    joueur.hp      = min(joueur.hp, joueur.hp_max)
    joueur.vitesse = joueur.vitesse_base * (1 + stats["bonus_vitesse"])

    joueur.bonus_degats       = stats["bonus_degats"]
    joueur.attaque_mult       = stats["bonus_attaque"]
    joueur.cooldown_reduction = stats["cooldown_reduction"]
    joueur.argent_bonus       = stats["bonus_cupidite"]
    joueur.nb_projectiles     = max(1, 1 + stats["bonus_quantite"])
    joueur.regen              = stats["regen_par_sec"]
    joueur.chance             = stats["bonus_chance"]
    joueur.duree_effets       = 1.0 + stats["bonus_duree"]
    joueur.resurrection       = stats["resurrection"]
    joueur.zone_attaque       = joueur.zone_base * (1 + stats["bonus_zone"])
    joueur.portee_xp          = joueur.portee_xp_base + stats["bonus_attirance"]
    joueur.reduction_degats   = stats["reduction_degats"]

   
    joueur.projectile_cadence = max(
        5,
        int(CADENCE_BASE * (1.0 - stats["cooldown_reduction"]))
    )

    
    for k, v in stats["multi_effets"].items():
        if k == "vitesse":
            joueur.vitesse = joueur.vitesse * (1 + v)
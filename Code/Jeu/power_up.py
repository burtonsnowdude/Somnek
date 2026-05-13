"""
power_up.py
Applique les bonus de l'inventaire sur les stats du joueur.
 appeler : après chaque achat, après un level-up, au chargement de la partie.
"""

import Interface.variable_power_up as data


BASE_VITESSE       = 2
BASE_CADENCE       = 30      
BASE_HP_MAX        = 400
BASE_PROTECTION    = 0.0
BASE_QUANTITE      = 1
BASE_ZONE          = 1.0
BASE_DUREE         = 1.0
BASE_CHANCE        = 0
BASE_ATTIRANCE     = 50      # portée XP en pixels
BASE_CROISSANCE_XP = 1.0


def _niveau(power: str) -> int:
    return data.playerInventory.get(power, 0)


def _bonus_multiplicatif(power: str) -> float:
    niveau = _niveau(power)
    if niveau == 0:
        return 1.0
    _, effets = data.liste_power_up[power]
    return 1.0 + sum(effets[:niveau])


def _bonus_additif(power: str):
    niveau = _niveau(power)
    if niveau == 0:
        return 0
    _, effets = data.liste_power_up[power]
    return sum(effets[:niveau])




def apply_powerups(player):
    """
    Recalcule toutes les stats du joueur depuis les bases + inventaire.
    Appeler à chaque achat et au démarrage.
    """
    player.vitesse              = BASE_VITESSE * _bonus_multiplicatif("vitesse_du_j")
    player.projectile_cadence   = max(5, int(BASE_CADENCE / _bonus_multiplicatif("refroidissement")))
    player.hp_max               = BASE_HP_MAX + int(_bonus_additif("sante"))
    player.protection           = min(0.75, _bonus_additif("Protection"))
    player.quantite_projectiles = BASE_QUANTITE + int(_bonus_additif("quantite"))
    player.zone_bonus           = _bonus_multiplicatif("zone")
    player.duree_bonus          = _bonus_multiplicatif("durabilite")
    player.chance               = BASE_CHANCE + int(_bonus_additif("chance") * 10)
    player.portee_xp            = BASE_ATTIRANCE + int(_bonus_additif("attirance"))
    player.croissance_xp        = BASE_CROISSANCE_XP * _bonus_multiplicatif("croissance")
    player.degats_bonus         = _bonus_multiplicatif("Pouvoir")

    # Clamp HP
    if player.hp > player.hp_max:
        player.hp = player.hp_max

    #  Répercute le bonus Pouvoir sur chaque arme possédée
    for arme_instance in player.armes:
        _appliquer_degats_arme(arme_instance, player.degats_bonus)



def _appliquer_degats_arme(arme_instance, multiplicateur: float):
    """
    Met à jour arme_instance.damage en partant du dgbase propre à chaque arme
    (ex : Epee_bleue=4)
    puis applique le multiplicateur Pouvoir du joueur.

    Si l'arme a déjà gagné des niveaux (levelup_depuis_niveau),
    on utilise _dgbase_apres_levelup pour ne pas perdre ces bonus.
    """
    from Armes_Items.class_armes_sans_bugs import Arme  

    nom = getattr(arme_instance, "nom", None)
    if nom is None:
        return

    arme_data = Arme.ARMES.get(nom)
    if arme_data is None:
        return

    #dgbase post-levelup stocké sur l'instance ArmeBase
    # sinon : dgbase initial du dictionnaire
    dgbase = getattr(arme_instance, "_dgbase_apres_levelup", arme_data.get("dgbase", 10))
    arme_instance.damage = dgbase * multiplicateur






def calculer_degats_recus(player, degats_bruts: float) -> float:
    """
    Retourne les dégâts réels subis après réduction par la Protection.
    À appeler dans player.degats() :
        self.hp -= calculer_degats_recus(self, degats)
    """
    protection = getattr(player, "protection", 0.0)
    return max(0.0, degats_bruts * (1.0 - protection))


def calculer_xp_gagne(player, xp_base: float) -> float:
    """
    Retourne l'XP réellement gagné après bonus Croissance.
    """
    return xp_base * getattr(player, "croissance_xp", 1.0)
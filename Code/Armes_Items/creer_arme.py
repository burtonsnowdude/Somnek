import pygame as pyg
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
from Armes_Items.Classe_par_type_darme import (
    ArmeProjectile,
    ArmeEpee,
    ArmeMultiDirection,
    ArmeZone,
    ArmeExplosion,
    ArmePoison
)

TYPE_VERS_CLASSE = {
    "balle":          ArmeProjectile,
    "zone":           ArmeZone,
    "coup":           ArmeEpee,
    "trait":          ArmeMultiDirection,
    "zone_multiples": ArmeExplosion,
    "poison":         ArmePoison
}

def creer_arme(player, nom_arme, perso):
    try:
        data = TYPES_ARMES[perso][nom_arme]
    except KeyError:
        print("ERREUR ARME:", nom_arme, "pour perso:", perso)
        print("Armes disponibles:", TYPES_ARMES[perso].keys())
        raise

    type_arme = data.get("type_arme")
    classe = TYPE_VERS_CLASSE.get(type_arme)

    if classe is None:
        raise ValueError(f"Type d'arme inconnu : '{type_arme}' pour {nom_arme}")

    return classe(player, nom_arme)
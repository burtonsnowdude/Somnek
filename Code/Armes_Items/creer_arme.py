"""
creer_arme.py — SOMNEK
Instancie la bonne class d'arme en fonction du type défini dans le dictionaire.
"""

import pygame as pyg
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
from Armes_Items.Classe_par_type_darme import (
    ArmeProjectile,
    ArmeEpee,
    ArmeMultiDirection,
    ArmeZone,
    ArmeExplosion,
    ArmePoison,
    ArmeOrbitale,
    ArmeOrbitaleExplosion,
)

# correspondance entre le type_arme du dico et la classe python
TYPE_VERS_CLASSE = {
    "balle":             ArmeProjectile,
    "zone":              ArmeZone,
    "coup":              ArmeEpee,
    "trait":             ArmeMultiDirection,
    "zone_multiples":    ArmeExplosion,
    "poison":            ArmePoison,
    "orbital":           ArmeOrbitale,
    "orbital_explosion": ArmeOrbitaleExplosion,
}


def creer_arme(player, nom_arme, perso):
    """Crée et retourne l'instance d'arme correspondant au nom donné.

    Parameters
    ----------
    player : Player
        L'instance du joueur qui posède l'arme
    nom_arme : str
        Le nom de l'arme à créer (doit exister dans TYPES_ARMES[perso])
    perso : str
        Le perso actif — utilisé pour chercher les données dans le dico

    Returns
    -------
    ArmeBase
        Une instance de la sous-classe correspondant au type_arme

    Raises
    ------
    KeyError
        Si l'arme n'existe pas pour ce perso
    ValueError
        Si le type_arme est inconnu dans TYPE_VERS_CLASSE
    """
    try:
        data = TYPES_ARMES[perso][nom_arme]
    except KeyError:
        # arme introuvable, on affiche les armes dispo pour debugger facilement
        print("ERREUR ARME:", nom_arme, "pour perso:", perso)
        print("Armes disponibles:", list(TYPES_ARMES[perso].keys()))
        raise

    type_arme = data.get("type_arme")
    classe    = TYPE_VERS_CLASSE.get(type_arme)

    if classe is None:
        raise ValueError(f"Type d'arme inconnu : '{type_arme}' pour {nom_arme}")

    # instanciation de la classe avec le joueur et le nom de l'arme
    return classe(player, nom_arme)
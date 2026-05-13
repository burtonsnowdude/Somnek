"""
class_items_sans_bugs.py — SOMNEK
Ancienne classe Items et fonctions utilitaires liées aux items.
Ce fichier est gardé pour compatibilité mais le vrai système d'items
est dans Item_system.py — ne pas utiliser Items directement en jeu.
"""

import pygame as pyg
import time
from random import *
import math
import random
import pygame


class Items:
    """Ancienne classe item — gardée pour compatibilité.
    
    Contient les carac de base de chaque item et les méthodes
    pour appliquer leurs effets sur le joueur.
    """

    # carac par défaut partagées par tous les items
    Carac_base__item = {
        "type_item": None,
        "hp": 0,
        "hp_max": 0,
        "prix": 0,
        "niveau_requis": 0,
        "degat": 0,
        "durabilite": None,
        "refroidissement": None,
        "recuperation": None,
        "vitesse_du_j": None,
        "chance": None,
        "cupidite": None,
        "attirance": None,
        "malchance": None,
        "zone": None,
        "resurrection": None,
        "dernier_tir": 0,
        "portee_xp": None,
        "refroidir": None,
        "quantite": 5,
        "sante": None,
        "protection": 0
    }

    # catalogue des items avec leurs stats spécifiques
    Items = {
        "Parfum_Dioru": {
            **Carac_base__item,
            "refroidir": 30,
            "prix": 5
        },
        "Gloss_rose": {
            **Carac_base__item,
            "attirance": 15,
            "prix": 3
        },
        "Chew_gum": {
            **Carac_base__item,
            "sante": 0.2,
            "prix": 2
        },
        "Talons_noirs": {
            **Carac_base__item,
            "vitesse_du_j": 0.2,
            "prix": 7
        },
        "Crop_top_rose": {
            **Carac_base__item,
            "protection": 0.2,
            "prix": 6
        }
    }

    def __init__(self, nom_item):
        """Initialise un item à partir de son nom.

        Parameters
        ----------
        nom_item : str
            Nom de l'item à instancier
        
        Raises
        ------
        ValueError
            Si le nom n'existe pas dans le catalogue
        """
        if nom_item not in self.Items:
            raise ValueError(f"Item '{nom_item}' non trouvé")

        self.nom = nom_item
        # copie pour pas modifier le dico de base
        self.caracteristiques = self.Items[nom_item].copy()

    def refroidissement(self):
        """Reduit le temps entre les attaques.

        Returns
        -------
        int
            Nouveau cooldown après réduction
        """
        refroidissement_base = 100
        refroidir = self.caracteristiques.get("refroidir")

        if refroidir is None:
            return refroidissement_base

        nv_reduction = refroidissement_base - refroidir
        return max(nv_reduction, 0)

    def vitesse(self):
        """Augmenter la vitesse du joueur.

        Returns
        -------
        float
            Nouvelle vitesse calculée
        """
        vitesse_base = 20
        vitesse_j = self.caracteristiques.get("vitesse_du_j")

        if vitesse_j is None:
            return vitesse_base

        nv_vitesse = vitesse_base * (1 + vitesse_j)
        return nv_vitesse

    def chance(self):
        """Augmente la chance du joueur.

        Returns
        -------
        float
            Nouvelle valeur de chance
        """
        chance_base = 10
        chance_val = self.caracteristiques.get("chance")

        if chance_val is None:
            return chance_base

        nv_chance = chance_base * (1 + chance_val)
        return nv_chance

    def cupidite(self, somme):
        """Augmenter l'argent récolté.

        Parameters
        ----------
        somme : float
            Montant de base à multiplier

        Returns
        -------
        float
            Montant après bonus cupidité
        """
        cupidite_val = self.caracteristiques.get("cupidite")

        if cupidite_val is None:
            return somme

        argent_final = somme * (1 + cupidite_val)
        return argent_final

    def attirance_xp(self, xp_base, distance, portee_xp):
        """Collecte de l'xp à distance selon l'attirance.

        Parameters
        ----------
        xp_base : float
            Xp de base de l'orbe
        distance : float
            Distance entre le joueur et l'orbe
        portee_xp : float
            Portée max d'attirance

        Returns
        -------
        float
            Xp collecté (0 si hors portée)
        """
        attirance_val = self.caracteristiques.get("attirance")

        if attirance_val is None or portee_xp is None:
            return 0

        if distance <= portee_xp:
            xp_collecte = xp_base * (1 + attirance_val * 0.01)
            return xp_collecte

        return 0

    def malchance(self, dg_ennemis, frequence):
        """Applique les effets de malchance sur les dégats et la fréquence.

        Parameters
        ----------
        dg_ennemis : float
            Dégâts de base des ennemis
        frequence : float
            Fréquence d'apparition des ennemis

        Returns
        -------
        tuple(float, float)
            Dégâts et fréquence augmentés
        """
        malchance_val = self.caracteristiques.get("malchance")

        if malchance_val is None:
            return dg_ennemis, frequence

        dg_supp = dg_ennemis + malchance_val
        nv_frequence = frequence + malchance_val
        return dg_supp, nv_frequence

    def protection(self, dg_ennemis):
        """Reduire les degats reçus.

        Parameters
        ----------
        dg_ennemis : float
            Dégâts bruts entrants

        Returns
        -------
        float
            Dégâts après réduction
        """
        protection_val = self.caracteristiques.get("protection")

        if protection_val == 0:
            return dg_ennemis

        dg_reduit = dg_ennemis * (1 - protection_val)
        return max(dg_reduit, 0)

    def augmentation_sante(self, sante_base):
        """Améliore la santé de base du joueur.

        Parameters
        ----------
        sante_base : float
            HP max de base

        Returns
        -------
        float
            Nouveaux HP max après bonus
        """
        sante_val = self.caracteristiques.get("sante")

        if sante_val is None or sante_val <= 0:
            return sante_base

        nv_sante = sante_base * (1 + sante_val)
        return nv_sante

    def equiper_item(self, item):
        """Equiper un item dans l'inventaire.

        Parameters
        ----------
        item : Items
            L'item à équiper
        """
        if isinstance(item, Items):
            self.equipe_items.append(item)

    def prendre_degat(self, degat):
        """Subir les degats et clamp les hp à 0.

        Parameters
        ----------
        degat : float
            Dégâts à infliger
        """
        self.hp -= degat
        if self.hp < 0:
            self.hp = 0

    def gagner_xp(self, xp):
        """Gagner de l experience.

        Parameters
        ----------
        xp : float
            Quantité d'xp gagnée
        """
        self.xp += xp

    def gagner_argent(self, montant):
        """Gagner de l'argent.

        Parameters
        ----------
        montant : float
            Montant à ajouter
        """
        self.argent += montant


def calculer_application_refroidissement(dernier_tir, refroidissement):
    """Vérifie si le temps requis est passé depuis le dernier tir.

    Parameters
    ----------
    dernier_tir : float
        Timestamp du dernier tir (time.time())
    refroidissement : float
        Délai requis entre deux tirs en secondes

    Returns
    -------
    tuple(bool, float)
        True si on peut tirer + le nouveau timestamp
    """
    maintenant = time.time()

    # premier tir, on initialise le timer
    if dernier_tir == 0:
        dernier_tir = maintenant
        return True, maintenant

    if maintenant - dernier_tir >= refroidissement:
        dernier_tir = maintenant
        return True, dernier_tir

    return False, dernier_tir


def durabilite_effect(player, durabilite_val, damage_per_tick=5, interval=2):
    """Diminue les HP du joueur à intervale régulier selon la durabilité.

    Parameters
    ----------
    player : Player
        Instance du joueur
    durabilite_val : int or None
        Nombre de ticks de dégâts
    damage_per_tick : int
        Dégâts par tick (défaut 5)
    interval : int
        Secondes entre chaque tick (défaut 2)
    """
    if durabilite_val is None:
        return

    for _ in range(durabilite_val):
        time.sleep(interval)
        player.hp -= damage_per_tick

    pyg.quit()


pygame.init()
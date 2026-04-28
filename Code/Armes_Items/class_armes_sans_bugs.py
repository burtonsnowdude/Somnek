import pygame as pyg 
import time

from random import *
import math
import random
import pygame as pyg

class Arme:
    """Class arme"""

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
        }
    }
    
    def __init__(self, nom_arme):
        """Initialise une arme
        
        Parameters
        ----------
        nom_arme : str
            Le nom de l'arme à créer
        """
        if nom_arme not in self.ARMES:
            raise ValueError(f"Arme '{nom_arme}' non trouvée")
        
        self.nom = nom_arme
        self.caracteristiques = self.ARMES[nom_arme].copy()
        self.attack = self.ARMES[nom_arme]["dgbase"]

    def equiper_arme(self, arme):
        """Equiper l'arme"""
        if isinstance(arme, Arme):
            self.arme_possede.append(arme)

    def ameliorer_arme(self, nv_degat):
        niveau_req = self.caracteristiques["niveau_req"]
        niveau_actuel = self.caracteristiques["niveau"]
        
        if niveau_actuel >= niveau_req:
            self.caracteristiques["dgbase"] += nv_degat
            self.caracteristiques["niveau"] += 1
            return True
        return False

    def est_a_portee(self, distance_monstre):
        return distance_monstre <= self.caracteristiques["portee"]

    def calculer_degat(self):
        degat = self.caracteristiques["dgbase"]
        reduction = self.caracteristiques["reduction"]
        
        return degat - reduction if reduction > 0 else degat

    def get_prix(self):
        return self.caracteristiques["prix"]
    """def afficher_arme_map(self): focntion pour afficher les armes en haut à gauche"""



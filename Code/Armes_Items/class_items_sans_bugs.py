import pygame as pyg 
import time

from random import *
import math
import random
import pygame

class Items:
    """Class items"""
    
    Carac_base__item= {
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
        """Initialisez les items"""
        if nom_item not in self.Items:
            raise ValueError(f"Item '{nom_item}' non trouvé")
        
        self.nom = nom_item
        self.caracteristiques = self.Items[nom_item].copy()
    
    
    def acheter_item(self,solde_j, prix):
        """Acheter un item"""
        if solde_j >= prix:
            solde_j -= prix
            return solde_j
        return solde_j
    
    def refroidissement(self):
        """Reduit le temps entre les attaques"""
        refroidissement_base = 100
        refroidir = self.caracteristiques.get("refroidir")
        
        if refroidir is None:
            return refroidissement_base
        
        nv_reduction = refroidissement_base - refroidir
        return max(nv_reduction, 0)  
    
    def vitesse(self):
        """Augmenter la vitesse du joueur"""
        vitesse_base = 20
        vitesse_j = self.caracteristiques.get("vitesse_du_j")
        
        if vitesse_j is None:
            return vitesse_base
        
        nv_vitesse = vitesse_base * (1 + vitesse_j)
        return nv_vitesse
    
    def chance(self):
        """Increase player chance"""
        chance_base = 10
        chance_val = self.caracteristiques.get("chance")
        
        if chance_val is None:
            return chance_base
        
        nv_chance = chance_base * (1 + chance_val)
        return nv_chance
    
    def cupidite(self, somme):
        """Augmenter l'argent récolté"""
        cupidite_val = self.caracteristiques.get("cupidite")
        
        if cupidite_val is None:
            return somme
        
        argent_final = somme * (1 + cupidite_val)
        return argent_final
    
    def attirance_xp(self, xp_base, distance, portee_xp):
        """Collect XP at distance based on attraction"""
        attirance_val = self.caracteristiques.get("attirance")
        
        if attirance_val is None or portee_xp is None:
            return 0
        
        if distance <= portee_xp:
            xp_collecte = xp_base * (1 + attirance_val * 0.01)
            return xp_collecte
        
        return 0
    
    def malchance(self, dg_ennemis, frequence):
        """Effets malchance"""
        malchance_val = self.caracteristiques.get("malchance")
        
        if malchance_val is None:
            return dg_ennemis, frequence
        
        dg_supp = dg_ennemis + malchance_val
        nv_frequence = frequence + malchance_val
        return dg_supp, nv_frequence
    
    def protection(self, dg_ennemis):
        """Reduire les degats"""
        protection_val = self.caracteristiques.get("protection")
        
        if protection_val == 0:
            return dg_ennemis
        
        dg_reduit = dg_ennemis * (1 - protection_val)
        return max(dg_reduit, 0) 
    
    def augmentation_sante(self, sante_base):
        """Améliore la santé de base"""
        sante_val = self.caracteristiques.get("sante")
        
        if sante_val is None or sante_val <= 0:
            return sante_base
        
        nv_sante = sante_base * (1 + sante_val)
        return nv_sante


    def equiper_item(self, item):
        """Equiper un item"""
        if isinstance(item, Items):
            self.equipe_items.append(item)
    
    def prendre_degat(self, degat):
        """Subir les degats"""
        self.hp -= degat
        if self.hp < 0:
            self.hp = 0
    
    def gagner_xp(self, xp):
        """Gagner de l experience"""
        self.xp += xp
    
    def gagner_argent(self, montant):
        """gagner l'argent"""
        self.argent += montant


def calculer_application_refroidissement(dernier_tir, refroidissement):
    """Vérifie si le temps requis est passé"""
    maintenant = time.time()
    if dernier_tir == 0:
        dernier_tir = maintenant
        return True, maintenant
    
    if maintenant - dernier_tir >= refroidissement:
        dernier_tir = maintenant
        return True, dernier_tir
    
    return False, dernier_tir


def regen_hp(player, recuperation, interval=1):
    """Regenere les points de vies par seconde"""
    if recuperation is None or recuperation <= 0:
        return
    
    while player.hp < player.hp_max:
        time.sleep(interval)
        player.hp += recuperation
        if player.hp > player.hp_max:
            player.hp = player.hp_max


def durabilite_effect(player, durabilite_val, damage_per_tick=5, interval=2):
    """Decrease HP based on item durability"""
    if durabilite_val is None:
        return
    
    for _ in range(durabilite_val):
        time.sleep(interval)
        player.hp -= damage_per_tick

    pyg.quit() 

pygame.init()
import pygame as pyg
from variables import * 
import math
from random import *

class Monstre:
    """Class Monstre"""
    def __init__(self, type):
        """Initialise un monstre en fonction de son type et choisit ses coordonnées d'apparition
        
        Parameters
        ----------
        type : str
            Le type de monstre
        """
        self.puissance = TYPES_MONSTRES[type]["puissance"]
        self.hp = TYPES_MONSTRES[type]["hp"]
        self.couleur = TYPES_MONSTRES[type]["couleur"]
        self.vitesse = TYPES_MONSTRES[type]["vitesse"]
        self.all_monsters = pyg.sprite.Group() 
        
        # Choisit un endroit aléatoire sur un bord pour apparaitre
        bord = randint(1,4)
        if bord == 1 :
            x, y = 0, randint(0, HEIGHT)
        elif bord == 2 :
            x, y = randint(0, WIDTH), 0
        elif bord == 3 :
            x, y = WIDTH, randint(0, HEIGHT)
        else :
            x, y = randint(0, WIDTH), HEIGHT
        self.pos = pyg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def show(self):
        """Dessine le monstre tant qu'il est en vie
        
        Returns
        -------
        bool 
        """
        if self.hp > 0 :
            pyg.draw.rect(WIN, self.couleur, self.pos)
            return True
        else :
            self.death_place = (self.pos.x, self.pos.y)
            self.rect = XP.get_rect()
            self.rect.topleft = self.death_place
            return False
    
    def show_xp(self):
        WIN.blit(XP, (self.pos.x, self.pos.y))
        self.valeur = self.puissance

    def degats(self, degats):
        """Inflige des dégâts au monstre

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats

    def follow(self, p):
        """Suivre le joueur
        
        Parameters
        ----------
        p : Self@Player
        """

        # Calculate direction vector from monster to player
        dx = p.pos.centerx - self.pos.centerx
        dy = p.pos.centery - self.pos.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move 
            self.pos.x += (dx / distance) * self.vitesse
            self.pos.y += (dy / distance) * self.vitesse

# Gestion des ennemis
def ajouter_monstre(monstres_presents):
    """Crée un nouveau monstre et l'ajoute à la liste des monstres presents
    
    Parameters
    ----------
    monstres_presents : list
        La liste des monstres presents
    
    Returns
    -------
    list 
        La liste des monstres presents"""
    monstres_presents.append(Monstre(choice(TYPES))) # crée un nouveau monstre de type aléatoire
    return monstres_presents

def gestion_monstres_presents(monstres_presents, frame, p, xp_dispo):
    """Gère l'affichage, le déplacement des monstres presents et les collisions avec le joueur
    
    Parameters
    ----------
    monstres_presents : list
        La liste des monstres presents
    frame : int
        Le numéro de la frame actuelle
    p : Self@Player
        Le joueur
    
    Returns
    -------
    list 
        La liste des monstres presents
    """
    kill_count = p.kill_count
    for m in monstres_presents[:]:
        existe = m.show() # affiche tous les monstres existant
        if existe :
            m.follow(p) # monstres suivant le joueur
            if p.pos.colliderect(m.pos) and frame%10 == 0:
                p.degats(m.puissance) # dégâts en cas de collision
        else :
            kill_count += 1
            monstres_presents.remove(m)
            xp_dispo.append(m)
    return monstres_presents, kill_count

def gestion_xp_fenetre(xp_dispo, p, xp_attendu):
    obtenu = 0
    for xp in xp_dispo[:]:
        xp.show_xp()
        if p.pos.colliderect(xp.pos):
            obtenu += xp.puissance
            p.update_xp(xp.valeur, xp_attendu)
            xp_dispo.remove(xp)
    return xp_dispo, obtenu
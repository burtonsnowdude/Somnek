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
        self.vitesse = TYPES_MONSTRES[type]["vitesse"]
        self.all_monsters = pyg.sprite.Group() 
        self.image = TYPES_MONSTRES[type]["image"]
        
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
        self.pos = pyg.Rect(x, y, self.image.get_width(), self.image.get_height())

    def choix_coord(self, coord):
        x, y = coord
        self.pos = pyg.Rect(x, y, self.image.get_width(), self.image.get_height())

    def show(self):
        """Dessine le monstre tant qu'il est en vie
        
        Returns
        -------
        bool 
        """
        if self.hp > 0 :
            WIN.blit(self.image, self.pos)
            return True
        else :
            return False
    
    def show_xp(self):
        WIN.blit(XP, self.pos)
        self.valeur = self.puissance

    def degats(self, degats):
        """Inflige des dégâts au monstre

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats

    def follow(self, coord):
        """Suivre le joueur
        
        Parameters
        ----------
        p : Self@Player
        """

        # Calculate direction vector from monster to player
        dx = coord.centerx - self.pos.centerx
        dy = coord.centery - self.pos.centery
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
            m.follow(p.pos) # monstres suivant le joueur
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

def gestion_vague(derniere_vague, niveau):
    if derniere_vague > 600 and randint(1, 10):
        nb_monstres = randint(5, 10)
        monstres_dispos = [monstre for monstre in TYPES_MONSTRES if TYPES_MONSTRES[monstre]["niveau"] <= niveau]
        type = choice(monstres_dispos)
        coin = randint(1,4)
        if coin == 1 :
            x, y = 0, 0
        if coin == 2 :
            x, y = WIDTH, 0
        if coin == 3 :
            x, y = 0, HEIGHT
        if coin == 4 : 
            x, y = WIDTH, HEIGHT
        monstres_vague = []
        for i in range(nb_monstres) : 
            m = Monstre(type)
            m.vitesse += 7
            m.choix_coord((x, y))
            if choice((True, False)) :
                x += randint(-60,60)
            else : 
                y += randint(-60, 60)
            monstres_vague.append(m)
        return 0, monstres_vague, coin
    return False
    
def traverser_ecran(monstres_vague, coin, p, frame, xp_dispo, kill_count):
    coin_a_atteindre = 5 - coin # le coin en diagonale
    if coin_a_atteindre == 1:
        coord = (-25,-25)
    if coin_a_atteindre == 2 :
        coord = (WIDTH+25, -25)
    if coin_a_atteindre == 3 :
        coord = (-25, HEIGHT+25)
    if coin_a_atteindre == 4 :
        coord = (WIDTH+25, HEIGHT+25)
    coord = pyg.Rect(coord[0], coord[1], 1, 1)
    for m in monstres_vague[:]:
        existe = m.show() # affiche tous les monstres existant
        if existe :
            m.follow(coord) # monstres suivant le joueur
            if p.pos.colliderect(m.pos) and frame%10 == 0:
                p.degats(m.puissance) # dégâts en cas de collision
        else :
            kill_count += 1
            monstres_vague.remove(m)
            xp_dispo.append(m)
    return monstres_vague, kill_count
        
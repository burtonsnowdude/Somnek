import pygame as pyg
from variables import * 
import math
from random import randint

class Monstre:
    """Class Monstre"""
    def __init__(self, type):

        self.puissance = TYPES_MONSTRES[type]["puissance"]
        self.hp = TYPES_MONSTRES[type]["hp"]
        self.couleur = TYPES_MONSTRES[type]["couleur"]
        self.vitesse = TYPES_MONSTRES[type]["vitesse"]

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
            return False

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

class Player:
    """Class Player"""
    def __init__(self):
        self.hp = PLAYER_PV
        self.pos = pyg.Rect(CENTREx, CENTREy, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vitesse = PLAYER_VIT
        self.xp = 0
        self.niveau = 1
        self.x_suppose = CENTREx
        self.y_suppose = CENTREy

    def draw_player(self):
        """Dessine le joueur"""
        pyg.draw.rect(WIN, (255, 0, 0), self.pos)

    def move_bg(self, bg, monstres):
        """Déplace le fond pour donner l'illusion que le joueur se déplace
        
        Parameters
        ----------
        bg : Rect
        monstres : list
        """
        keys = pyg.key.get_pressed()
        up = keys[pyg.K_UP] or keys[pyg.K_w]
        right = keys[pyg.K_RIGHT] or keys[pyg.K_d]
        left = keys[pyg.K_LEFT] or keys[pyg.K_a]
        down = keys[pyg.K_DOWN] or keys[pyg.K_s]
        
        # Déplacement pour chaque touche appuyée, adapté en diagonale pour que le joueur n'aille pas plus vite
        if left:
            if up or down : 
                bg.x += 1/(math.sqrt(2)) * self.vitesse
                self.x_suppose -= 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.x += 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.x += self.vitesse
                self.x_suppose -= self.vitesse
                for m in monstres:
                    m.pos.x += self.vitesse

        if right:
            if up or down : 
                bg.x -= 1/(math.sqrt(2)) * self.vitesse
                self.x_suppose += 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.x -= 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.x -= self.vitesse
                self.x_suppose += self.vitesse
                for m in monstres:
                    m.pos.x -= self.vitesse

        if up:
            if right or left : 
                bg.y += 1/(math.sqrt(2)) * self.vitesse
                self.y_suppose -= 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.y += 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.y += self.vitesse
                self.y_suppose -= self.vitesse
                for m in monstres:
                    m.pos.y += self.vitesse

        if down:
            if right or left :
                bg.y -= 1/(math.sqrt(2)) * self.vitesse
                self.y_suppose += 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.y -= 1/(math.sqrt(2)) * self.vitesse
            else :
                bg.y -= self.vitesse
                self.y_suppose += self.vitesse
                for m in monstres:
                    m.pos.y -= self.vitesse

    def degats(self, degats):
        """Prendre des dégâts

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats
        if self.hp <= 0 :
            pyg.quit() #à remplacer plus tard

    def update_xp(self, xp, xp_attendu):
        self.xp += xp
        if self.xp >= xp_attendu :
            self.xp -= xp_attendu
            self.niveau += 1
            return True
        return False
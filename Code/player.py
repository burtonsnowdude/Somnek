import pygame as pyg
from variables import * 
import math
from random import randint
from classe_projectile import Projectile
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
        self.all_projectiles = pyg.sprite.Group()   
        self.projectile_cooldown = 0
        self.projectile_cadence = 10 

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
            #pyg.quit() #à remplacer plus tard
            pass # car ça fait buguer

    def update_xp(self, xp, xp_attendu):
        self.xp += xp
        if self.xp >= xp_attendu :
            self.xp -= xp_attendu
            self.niveau += 1
            return True
        return False
    def lancer_projectile(self):
        """Créer un projectile avec cooldown"""
        # Vérifier si l'on peut tirer 
        if self.projectile_cooldown <= 0:
            projectile = Projectile(self)
            self.all_projectiles.add(projectile)
            self.projectile_cooldown = self.projectile_cadence  # Reset cooldown
    
    def update_cooldown(self):
        """À appeler chaque frame pour réduire le cooldown"""
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1
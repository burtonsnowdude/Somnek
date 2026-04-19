import pygame as pyg
from variables import * 
import math
from random import randint
from classe_projectile import Projectile
class Player:
    """Class Player"""
    def __init__(self):
        self.hp = PLAYER_PV
        self.pos = pyg.Rect(CENTREx-PLAYER_WIDTH/2, CENTREy - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vitesse = PLAYER_VIT
        self.xp = 0
        self.niveau = 1
        self.kill_count = 0
        
        self.x_suppose = CENTREx
        self.y_suppose = CENTREy

        self.x_suppose = CENTREx-PLAYER_WIDTH/2
        self.y_suppose = CENTREy - PLAYER_HEIGHT
        #Liste spéciale pygame

        self.all_projectiles = pyg.sprite.Group()   
        self.projectile_cooldown = 0
        self.projectile_cadence = 30

    def draw_player(self):
        """Dessine le joueur"""
        WIN.blit(PLAYER_IMAGE, (CENTREx-PLAYER_WIDTH/2, CENTREy - PLAYER_HEIGHT/2))

    def move_bg(self, bg, monstres, xp, monstres_vague):
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
        obj_a_deplacer = monstres+xp
        if monstres_vague is not None :
            obj_a_deplacer += monstres_vague 
        # Déplacement pour chaque touche appuyée, adapté en diagonale pour que le joueur n'aille pas plus vite
        dx, dy = 0, 0
        
        if left :
            dx -=1 * self.vitesse
        if right :
            dx += 1 * self.vitesse
        if up :
            dy -= 1 * self.vitesse
        if down :
            dy += 1* self.vitesse
        
        """if dx != 0 and dy != 0 :
            dx *= 1/(math.sqrt(2)) 
            dy *= 1/(math.sqrt(2))
        """
        self.x_suppose += dx
        self.y_suppose += dy
        for objet in obj_a_deplacer :
            objet.pos.x -= dx
            objet.pos.y -= dy
        

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

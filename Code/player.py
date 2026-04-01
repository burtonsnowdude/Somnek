import pygame as pyg
from variables import * 
import math
from random import randint



class Player:
    """Class Player"""
    def __init__(self):
        self.hp = PLAYER_PV
        self.pos = pyg.Rect(CENTREx-PLAYER_WIDTH/2, CENTREy - PLAYER_HEIGHT/2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vitesse = PLAYER_VIT
        self.xp = 0
        self.niveau = 1
        self.x_suppose = CENTREx-PLAYER_WIDTH/2
        self.y_suppose = CENTREy - PLAYER_HEIGHT
        #Liste spéciale pygame
        self.all_projectiles = pyg.sprite.Group()   

    def draw_player(self):
        """Dessine le joueur"""
        WIN.blit(PLAYER_IMAGE, (CENTREx-PLAYER_WIDTH/2, CENTREy - PLAYER_HEIGHT/2))

    def move_bg(self, bg, monstres, xp):
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
                for x in xp:
                    x.pos.x += 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.x += self.vitesse
                self.x_suppose -= self.vitesse
                for m in monstres:
                    m.pos.x += self.vitesse
                for x in xp:
                    x.pos.x += self.vitesse

        if right:
            if up or down : 
                bg.x -= 1/(math.sqrt(2)) * self.vitesse
                self.x_suppose += 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.x -= 1/(math.sqrt(2)) * self.vitesse
                for x in xp:
                    x.pos.x -= 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.x -= self.vitesse
                self.x_suppose += self.vitesse
                for m in monstres:
                    m.pos.x -= self.vitesse
                for x in xp:
                    x.pos.x -= self.vitesse

        if up:
            if right or left : 
                bg.y += 1/(math.sqrt(2)) * self.vitesse
                self.y_suppose -= 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.y += 1/(math.sqrt(2)) * self.vitesse
                for x in xp:
                    x.pos.y += 1/(math.sqrt(2)) * self.vitesse
            else : 
                bg.y += self.vitesse
                self.y_suppose -= self.vitesse
                for m in monstres:
                    m.pos.y += self.vitesse
                for x in xp:
                    x.pos.y += self.vitesse


        if down:
            if right or left :
                bg.y -= 1/(math.sqrt(2)) * self.vitesse
                self.y_suppose += 1/(math.sqrt(2)) * self.vitesse
                for m in monstres:
                    m.pos.y -= 1/(math.sqrt(2)) * self.vitesse
                for x in xp:
                    x.pos.y -= 1/(math.sqrt(2)) * self.vitesse
            else :
                bg.y -= self.vitesse
                self.y_suppose += self.vitesse
                for m in monstres:
                    m.pos.y -= self.vitesse
                for x in xp:
                    x.pos.y -= self.vitesse

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

import pygame as pyg
from variables import * 
import math
from random import randint

class Monstre:

    def __init__(self, type):
        self.puissance = TYPES_MONSTRES[type][0]
        self.hp = TYPES_MONSTRES[type][1]
        bord = randint(1,4)
        if bord == 1 :
            x, y = 0, randint(0, 600)
        elif bord == 2 :
            x, y = randint(0, 800), 0
        elif bord == 3 :
            x, y = 800, randint(0, 600)
        else :
            x, y = randint(0, 800), 600
        self.pos = pyg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.couleur = TYPES_MONSTRES[type][2]

    def spawn(self):
        if self.hp > 0 :
            pyg.draw.rect(WIN, self.couleur, self.pos)
            return True
        else :
            return False

    def degats(self, degats):
        self.hp -= degats

    def follow(self, p):
        # Calculate direction vector from monster to player
        dx = p.pos.centerx - self.pos.centerx
        dy = p.pos.centery - self.pos.centery
        
        distance = math.sqrt(dx**2 + dy**2)
        
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move at MONSTER_VIT speed
            self.pos.x += (dx / distance) * MONSTER_VIT
            self.pos.y += (dy / distance) * MONSTER_VIT

class player:
    def __init__(self):
        self.hp = PLAYER_PV
        self.pos = pyg.Rect(CENTREx, CENTREy, PLAYER_WIDTH, PLAYER_HEIGHT)

    def draw_player(self):
        pyg.draw.rect(WIN, (255, 0, 0), self.pos)

    def move_bg(self, bg, monstres):
        keys = pyg.key.get_pressed()

        if keys[pyg.K_LEFT] or keys[pyg.K_a]:
            bg.x += PLAYER_VIT
            for m in monstres:
                m.pos.x += PLAYER_VIT

        if keys[pyg.K_RIGHT] or keys[pyg.K_d]:
            bg.x -= PLAYER_VIT
            for m in monstres:
                m.pos.x -= PLAYER_VIT

        if keys[pyg.K_UP] or keys[pyg.K_w]:
            bg.y += PLAYER_VIT
            for m in monstres:
                m.pos.y += PLAYER_VIT

        if keys[pyg.K_DOWN] or keys[pyg.K_s]:
            bg.y -= PLAYER_VIT
            for m in monstres:
                m.pos.y -= PLAYER_VIT

    def degats(self, degats):
        self.hp -= degats
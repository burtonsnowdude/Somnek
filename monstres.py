import pygame as pyg
from variables import * 
import math

class monstre:
    def __init__(self, type):
        monstre.hp = 50
        monstre.pos = pyg.Rect(20, 20, PLAYER_WIDTH, PLAYER_HEIGHT)
        monstre.existe = True

    def spawn(self):
        if monstre.existe :
            pyg.draw.rect(WIN, (0, 255, 0), monstre.pos)

    def degats(self, degats):
        monstre.hp -= degats

    def follow(self, player):
            # Calculate direction vector from monster to player
        dx = player.pos.centerx - monstre.pos.centerx
        dy = player.pos.centery - monstre.pos.centery
        
        distance = math.sqrt(dx**2 + dy**2)
        
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move at MONSTER_VIT speed
            monstre.pos.x += (dx / distance) * MONSTER_VIT
            monstre.pos.y += (dy / distance) * MONSTER_VIT

class player:
    def __init__(self):
        player.hp = PLAYER_PV
        player.pos = pyg.Rect(CENTREx, CENTREy, PLAYER_WIDTH, PLAYER_HEIGHT)

    def draw_player(self):
        pyg.draw.rect(WIN, (255, 0, 0), player.pos)

    def move_bg(self, bg):
        # controle du joueur (avec les fleches ou les touches WASD)
        keys = pyg.key.get_pressed()
        
        if (keys[pyg.K_LEFT] or keys[pyg.K_a]):                       # gauche
            bg.x += PLAYER_VIT
            monstre.pos.x += PLAYER_VIT

        if (keys[pyg.K_RIGHT] or keys[pyg.K_d]) and (player.pos.x + PLAYER_VIT + PLAYER_WIDTH) <= WIDTH:   # droite
            bg.x -= PLAYER_VIT
            monstre.pos.x -= PLAYER_VIT

        if (keys[pyg.K_UP] or keys[pyg.K_w]) and (player.pos.y - PLAYER_VIT) >= 0:                         # haut
            bg.y += PLAYER_VIT
            monstre.pos.y += PLAYER_VIT

        if (keys[pyg.K_DOWN] or keys[pyg.K_s]) and (player.pos.y + PLAYER_VIT + PLAYER_HEIGHT) <= HEIGHT:  # bas
            bg.y -= PLAYER_VIT
            monstre.pos.y -= PLAYER_VIT
    
    def degats(self, degats):
        player.hp -= degats
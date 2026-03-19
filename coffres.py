from random import *
from math import *
import pygame as pyg
from variables import *

DISTANCE_MIN = -2000
DISTANCE_MAX = 2000

class Coffre :

    def __init__(self, player):
        """Crée un objet Coffre et détermine ses coordonnées en fonction de la position du joueur
        
        Parameters
        ----------
        player 
            Self@Player
        """
        # Coordonnées du coffre
        self.x_coffre = randint(DISTANCE_MIN + int(player.x_suppose), DISTANCE_MAX + int(player.x_suppose))
        self.y_coffre = randint(DISTANCE_MIN + int(player.y_suppose), DISTANCE_MAX + int(player.y_suppose))
        # Image de la flèche
        self.fleche = pyg.image.load("fleche.jpg").convert_alpha()
        self.fleche = pyg.transform.smoothscale(self.fleche, (30, 50))
        self.rectangle_existe = False

    def pointer_coffre(self, player):
        """Dessine une flèche qui pointe vers le coffre, dessine le coffre s'il est dans la zone visible
        
        Parameters
        ----------
        player
            Self@Player
        """

        # Calcul de l'angle
        angle = atan2((self.x_coffre - player.x_suppose), (self.y_coffre - player.y_suppose))
        angle = degrees(angle) - 180

        # Rotation de la flèche
        fleche_orientee = pyg.transform.rotate(self.fleche, angle)
        WIN.blit(fleche_orientee, (400, 200))

        # Calcul des coordonnées couvertes par l'écran affiché
        position_min_en_x = player.x_suppose - CENTREx
        position_max_en_x = player.x_suppose + CENTREx
        position_min_en_y = player.y_suppose - CENTREy
        position_max_en_y = player.y_suppose + CENTREy

        # On dessine le coffre s'il se situe parmi ces coordonnées
        if position_min_en_x <= self.x_coffre <= position_max_en_x and position_min_en_y <= self.y_coffre <= position_max_en_y:
            x_screen_coffre = CENTREx - (player.x_suppose - self.x_coffre)
            y_screen_coffre = CENTREy - (player.y_suppose - self.y_coffre)
            
            self.coffre = pyg.Rect(x_screen_coffre, y_screen_coffre, 10, 10)
            if player.pos.colliderect(self.coffre) :
                return
            pyg.draw.rect(WIN, (255, 0, 0), self.coffre)
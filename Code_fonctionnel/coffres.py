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
        
        self.coffre_sur_lecran = False
        self.coffre = None

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
        fleche_orientee = pyg.transform.rotozoom(FLECHE, angle, 1)
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
            self.coffre_sur_lecran = True
            
            self.coffre = TRESOR
            

            if self.coffre_sur_lecran :
                WIN.blit(TRESOR, (x_screen_coffre, y_screen_coffre))
                self.rect = self.coffre.get_rect()
                self.rect.topleft = (x_screen_coffre, y_screen_coffre)
    
    def determiner_recompense(self, armes_possedees, seuil) :
        
        armes_dispo = [arme for arme in ARMES if ARMES[arme] < seuil]
        for arme in armes_dispo[:]:
            if arme in armes_possedees :
                armes_dispo.remove(arme)
        argent_dispo = int(seuil * randint(1, seuil))
        choix_aleat = choice((True, False))
        if choix_aleat :
            return argent_dispo
        else : 
            return choice(armes_dispo)
        

        
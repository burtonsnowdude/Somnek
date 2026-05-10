from random import *
from math import *
import pygame as pyg
from Fichiers_variables.variables import *
from Affichage.fonctionnement_divers import remplir_fond
from Fichiers_variables.dictionnaire_armes import GESTION_DES_NIVEAUX_ARMES
from Fichiers_variables.dictionnaire_items import GESTION_NIVEAU_ITEMS
from Jeu.passage_niveau import scroll_gemme

FONT_COFFRE = pyg.font.SysFont("Press Start 2P", 50) 
DISTANCE_MIN = -2000
DISTANCE_MAX = 2000
ARGENT_W = ARGENT.get_width()
ARGENT_H = ARGENT.get_height()
COFFRE_W = TRESOR.get_width()
COFFRE_H = TRESOR.get_height()

class Coffre :

    def __init__(self, player):
        """Crée un objet Coffre et détermine ses coordonnées en fonction de la position du joueur
        
        Parameters
        ----------
        player 
            Self@Player
        """
        # Coordonnées du coffre
        self.rect = TRESOR.get_rect()
        self.x_coffre = randint(DISTANCE_MIN + int(player.x_monde), DISTANCE_MAX + int(player.x_monde))
        self.y_coffre = randint(DISTANCE_MIN + int(player.y_monde), DISTANCE_MAX + int(player.y_monde))
        

    def pointer_coffre(self, player):
        """Dessine une flèche qui pointe vers le coffre, dessine le coffre s'il est dans la zone visible
        
        Parameters
        ----------
        player
            Self@Player
        """

        # Calcul de l'angle
        angle = atan2((self.x_coffre - player.x_monde), (self.y_coffre - player.y_monde))
        angle = degrees(angle) - 180

        # Rotation de la flèche
        fleche_orientee = pyg.transform.rotozoom(FLECHE, angle, 1)
        WIN.blit(fleche_orientee, (400, 200))
        x_screen_coffre = CENTREx - (player.x_monde - self.x_coffre)
        y_screen_coffre = CENTREy - (player.y_monde - self.y_coffre)
        WIN.blit(TRESOR, (x_screen_coffre, y_screen_coffre))
        self.rect.topleft = (x_screen_coffre, y_screen_coffre)
    
    def determiner_recompense(self, armes_et_items_possedees, p) :
        """Détermine la récompense obtenue par le joueur quand il atteint un coffre

        Parameters
        ----------
        armes_possedees : list
            La liste des armes détenues par le joueur
        seuil : int
            Le seuil de valeur maximale pour une arme (en fonction du niveau atteint)
        
        Returns
        -------
        int
            L'argent récolté
        ou
        str
            L'arme récupérée
        """
        rect = ANIM_COFFRE[0].get_rect()
        rect.center = (CENTREx, CENTREy)
        frame = 0
        i = 0
        violet = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        violet.fill((102, 62, 86, 150))
        while i < len(ANIM_COFFRE) -1 :
            remplir_fond(p)
            WIN.blit(violet, (0, 0))
            scroll_gemme(frame)
            WIN.blit(ANIM_COFFRE[i], rect)
            frame += 1
            if frame % 10 == 0 :
                i += 1
            pyg.display.flip()
        armes_dispo = []
        items_dispo = []
        niveau = 1
        while niveau < p.niveau :
            for item in GESTION_NIVEAU_ITEMS[p.perso]["Niveau "+str(niveau)]:
                items_dispo.append(item)
            niveau += 1
        niveau = 1
        while niveau < p.niveau :
            if "Niveau "+str(niveau) in GESTION_DES_NIVEAUX_ARMES[p.perso] :
                for arme in GESTION_DES_NIVEAUX_ARMES[p.perso]["Niveau "+str(niveau)]:
                    if niveau != 1 :
                        armes_dispo.append(arme)
            niveau += 1
        dispo = items_dispo+armes_dispo
        armes_deja_enlevees = []
        for arme in dispo[:]:
            if arme in armes_et_items_possedees or arme in armes_deja_enlevees :
                dispo.remove(arme)
                armes_deja_enlevees.append(arme)
        argent_dispo = randint(p.niveau*50, p.niveau*200)
        choix_aleat = choice((True, False))
        if choix_aleat or len(dispo) == 0 :
            rect = ARGENT.get_rect()
            rect.center = (CENTREx, CENTREy)
            WIN.blit(ARGENT, rect)
            txt = FONT_COFFRE.render(str(argent_dispo), 1, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.center = CENTREx, 100
            frame = 0
            fade = 255
            while frame < 180 : 
                remplir_fond(p)
                scroll_gemme(frame)
                txt.set_alpha(fade)
                if frame%2 == 0:
                    fade -= 1
                rect.center = (CENTREx, CENTREy)
                WIN.blit(ARGENT, rect)
                frame += 1
                WIN.blit(txt, txt_rect)
                pyg.display.flip()
            return argent_dispo
        else : 
            choix = choice(dispo)
            if choix in armes_dispo : 
                type_objet = "arme"
            else :
                type_objet = "item"
            return type_objet, choix
    

def ajout_coffre(dernier_coffre_apparu, coffre_existant, p):
    if randint(1,100) == 1 and dernier_coffre_apparu > 100 and not coffre_existant:
            nouveau_coffre = Coffre(p)
            dernier_coffre_apparu = 0 
            coffre_existant = True
            return nouveau_coffre, dernier_coffre_apparu, coffre_existant
    else :
        return False
import pygame as pyg
from Fichiers_variables.variables import * 
import math
from random import choice, randint
from Affichage.fonctionnement_divers import screen_to_world

class Monstre:
    """Class Monstre"""
    def __init__(self, type, p):
        """Initialise un monstre en fonction de son type et choisit ses coordonnées d'apparition
        
        Parameters
        ----------
        type : str
            Le type de monstre
        """
        self.type = type
        self.puissance = TYPES_MONSTRES[type]["puissance"]
        self.hp = TYPES_MONSTRES[type]["hp"]
        self.vitesse = TYPES_MONSTRES[type]["vitesse"]
        self.all_monsters = pyg.sprite.Group() 
        if "image" in TYPES_MONSTRES[type]:
            self.image = TYPES_MONSTRES[type]["image"]
            self.rect = self.image.get_rect()
        elif "anim" in TYPES_MONSTRES[type]:
            self.anim = TYPES_MONSTRES[type]["anim"]
            self.index = 0
            self.rect = self.anim[0].get_rect()
        # Choisit un endroit aléatoire sur un bord pour apparaitre
        bord = randint(1,4)
        if bord == 1 :
            self.x_screen, self.y_screen = 0, randint(0, HEIGHT)
        elif bord == 2 :
            self.x_screen, self.y_screen = randint(0, WIDTH), 0
        elif bord == 3 :
            self.x_screen, self.y_screen = WIDTH, randint(0, HEIGHT)
        else :
            self.x_screen, self.y_screen = randint(0, WIDTH), HEIGHT
        self.x_monde, self.y_monde = screen_to_world(self.x_screen, self.y_screen, p)
        
        

    def choix_coord(self, coord):
        self.x_monde, self.y_monde = coord
        self.x_screen, self.y_screen = coord

    def show(self, frame):
        """Dessine le monstre"""
        self.rect.center = (self.x_screen, self.y_screen)
        if "image" in TYPES_MONSTRES[self.type]:
            img = self.image.copy()
            WIN.blit(img, self.rect)
        elif frame % 4 == 0:
            WIN.blit(self.anim[self.index], self.rect)
            self.index += 1
            self.index = self.index % len(self.anim)
        else:
            WIN.blit(self.anim[self.index], self.rect)

        if getattr(self, "est_empoisonne", False):
            img = self.image.copy() if "image" in TYPES_MONSTRES[self.type] else self.anim[self.index].copy()
            vert = pyg.Surface(img.get_size(), pyg.SRCALPHA)
            vert.fill((0, 200, 0, 100))
            img.blit(vert, (0, 0))
            WIN.blit(img, self.rect)
    
    def show_xp(self):
        self.rect.center = (self.x_screen, self.y_screen)
        WIN.blit(XP, self.rect)
        self.valeur = self.puissance
    

    def empoisonner(self, duree, degats, tick):  # ← dans la classe
        self.est_empoisonne = True
        self.poison_duree = duree
        self.poison_degats = degats
        self.poison_tick = tick
        self.poison_timer = 0

    def update_poison(self):
        if not getattr(self, "est_empoisonne", False):
            return
        self.poison_timer += 1
        self.poison_duree -= 1
        if self.poison_timer >= self.poison_tick:
            self.degats(self.poison_degats)
            self.poison_timer = 0
        if self.poison_duree <= 0:
            self.est_empoisonne = False
    def degats(self, degats):
        """Inflige des dégâts au monstre

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats

    def follow(self, x,y):
        """Suivre le joueur
        
        Parameters
        ----------
        p : Self@Player
        """

        # Calculate direction vector from monster to player
        dx = x - self.x_monde
        dy = y - self.y_monde
        distance = math.sqrt(dx**2 + dy**2)
        
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move 
            self.x_monde += (dx / distance) * self.vitesse
            self.y_monde += (dy / distance) * self.vitesse

# Gestion des ennemis
def ajouter_monstre(monstres_presents, p, perso):
    """Crée un nouveau monstre et l'ajoute à la liste des monstres presents
    
    Parameters
    ----------
    monstres_presents : list
        La liste des monstres presents
    
    Returns
    -------
    list 
        La liste des monstres presents"""
    choix_possibles = [monstre for monstre in TYPES_MONSTRES if TYPES_MONSTRES[monstre]["niveau"] <= p.niveau and TYPES_MONSTRES[monstre]["perso"] == perso]
    if not choix_possibles:
        choix_possibles = [m for m in TYPES_MONSTRES 
                           if TYPES_MONSTRES[m]["perso"] == perso]
        choix_possibles = [min(choix_possibles, 
                           key=lambda m: TYPES_MONSTRES[m]["niveau"])]
    monstres_presents.append(Monstre(choice(choix_possibles), p)) # crée un nouveau monstre de type aléatoire
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
        m.show(frame) # affiche tous les monstres existant
        m.update_poison()
        if m.hp > 0 :
            m.follow(p.x_monde, p.y_monde) # monstres suivant le joueur
            if p.pos.colliderect(m.rect) and frame%10 == 0:
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
        if p.pos.colliderect(xp.rect):
            obtenu += xp.valeur
            p.xp += xp.valeur  
            xp_dispo.remove(xp)
    return xp_dispo, obtenu
def empoisonner(self, duree, degats, tick):
    self.est_empoisonne = True
    self.poison_duree = duree
    self.poison_degats = degats
    self.poison_tick = tick
    self.poison_timer = 0

def update_poison(self):
    if not getattr(self, "est_empoisonne", False):
        return
    self.poison_timer += 1
    self.poison_duree -= 1
    if self.poison_timer >= self.poison_tick:
        self.degats(self.poison_degats)
        self.poison_timer = 0
    if self.poison_duree <= 0:
        self.est_empoisonne = False


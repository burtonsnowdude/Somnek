import pygame as pyg
from Fichiers_variables.variables import * 
import math
from Armes_Items.classe_projectile import Projectile
from Affichage.fonctionnement_divers import camera

class Player:
    """Class Player"""
    def __init__(self, perso):
        self.hp = PLAYER_PV
        if "image" in PERSOS[perso] :
            self.image_r = PERSOS[perso]["image"]["horizon_r"]
            self.image_l = PERSOS[perso]["image"]["horizon_l"]
            self.image = self.image_r
            self.pos = self.image.get_rect()
        else :
            self.index = 0
            self.anim_avant = PERSOS[perso]["anim"]["avant"]
            self.anim_arriere = PERSOS[perso]["anim"]["arriere"]
            self.anim_horizon_r = PERSOS[perso]["anim"]["horizon_r"]
            self.anim_horizon_l = PERSOS[perso]["anim"]["horizon_l"]
            self.anim = self.anim_avant
            self.pos = self.anim[0].get_rect()
        
        self.pos.center = CENTREx, CENTREy
        self.vitesse = PLAYER_VIT
        self.xp = 0
        self.niveau = 1
        self.kill_count = 0
        self.perso = perso
        
        self.x_monde = CENTREx
        self.y_monde = CENTREy
        #Liste spéciale pygame

        self.all_projectiles = pyg.sprite.Group()   
        self.projectile_cooldown = 0
        self.projectile_cadence = 30

    def draw_player(self, frame):
        """Dessine le joueur"""
        if "anim" in PERSOS[self.perso] :
            if frame%4 == 0 : 
                self.index += 1
                self.index = self.index%len(self.anim)
            WIN.blit(self.anim[self.index], self.pos)
        else:
            WIN.blit(self.image, self.pos)


    def move_bg(self, monstres, xp, monstres_vague, boss, boss_present):
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
        if boss_present :
            obj_a_deplacer.append(boss)
        # Déplacement pour chaque touche appuyée, adapté en diagonale pour que le joueur n'aille pas plus vite
        dx, dy = 0, 0
        
        if left :
            dx -=1 * self.vitesse
            if "anim" in PERSOS[self.perso] :
                if self.anim != self.anim_horizon_l :
                    self.index = 0
                self.anim = self.anim_horizon_l
                
            else : 
                self.image = self.image_l
        if right :
            dx += 1 * self.vitesse
            if "anim" in PERSOS[self.perso] :
                if self.anim != self.anim_horizon_r :
                    self.index = 0
                self.anim = self.anim_horizon_r
            else : 
                self.image = self.image_r
        if up :
            dy -= 1 * self.vitesse
            if "anim" in PERSOS[self.perso] :
                if self.anim != self.anim_arriere :
                    self.index = 0
                self.anim = self.anim_arriere

        if down :
            dy += 1* self.vitesse
            if "anim" in PERSOS[self.perso] :
                if self.anim != self.anim_avant :
                    self.index = 0
                self.anim = self.anim_avant
        
        if dx != 0 and dy != 0 :
            dx *= 1/(math.sqrt(2)) 
            dy *= 1/(math.sqrt(2))
        self.x_monde += dx
        self.y_monde += dy
        for objet in obj_a_deplacer :
            objet.x_screen, objet.y_screen = camera(objet.x_monde, objet.y_monde, self)

        

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

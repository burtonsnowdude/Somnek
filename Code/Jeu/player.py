import pygame as pyg
from Fichiers_variables.variables import * 
import math
from Armes_Items.class_items_sans_bugs import Items 
from Armes_Items.classe_projectile import Projectile
from Affichage.fonctionnement_divers import camera
from Interface.Game_over import game_over
from Armes_Items.creer_arme import creer_arme
from Fichiers_variables.dictionnaire_armes import ARMES
from Armes_Items.Classe_par_type_darme import ArmeProjectile, ArmeEpee, ArmeMultiDirection, ArmeZone, ArmeExplosion, ArmePoison
from Jeu.power_up import apply_powerups
from Armes_Items.class_armes_sans_bugs import Arme


TYPE_VERS_CLASSE = {
    "balle":         ArmeProjectile,
    "zone":          ArmeZone,
    "coup":          ArmeEpee,   
    "trait":         ArmeMultiDirection,
    "zone_multiples": ArmeExplosion,
    "poison":         ArmePoison
}
class Player:
    """Class Player"""
    def __init__(self, perso, nom):
        self.hp = PLAYER_PV
        self.nom = nom
        if "image" in PERSOS[perso] :
            self.image_r = PERSOS[perso]["image"]["horizon_r"]
            self.image_l = PERSOS[perso]["image"]["horizon_l"]
            self.image = self.image_r
            self.hp_max = PLAYER_PV
            
            self.pos = self.image.get_rect()

            
        else :
            self.index = 0
            self.anim_avant = PERSOS[perso]["anim"]["avant"]
            self.anim_arriere = PERSOS[perso]["anim"]["arriere"]
            self.anim_horizon_r = PERSOS[perso]["anim"]["horizon_r"]
            self.anim_horizon_l = PERSOS[perso]["anim"]["horizon_l"]
            self.anim = self.anim_avant
            self.pos = self.anim[0].get_rect()
        
        self.arme_active = 0
        self.armes = []          # toutes les armes actives
        self.armes_unlock = set()  # armes déjà ajoutées
        self.arme_active = 0
        self.all_zones = pyg.sprite.Group() 
        self.pos.center = CENTREx, CENTREy
        self.vitesse = PLAYER_VIT
        self.xp = 0
        self.niveau = 1
        self.kill_count = 0
        self.alive = True
        self.perso = perso
        self.armes_data = Arme.arme_possede
        
        self.color = PERSOS[perso]["color"]
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
    
    def update_armes(self):
        for arme in self.armes:
            arme.update()
            arme.trigger()

    def ajouter_arme(self, nom_arme):
        if nom_arme in self.armes_unlock:
            return

        self.armes_unlock.add(nom_arme)

        arme = creer_arme(self, nom_arme, self.perso)
        self.armes.append(arme) # arme par défaut

    def equiper_arme(self, nom_arme):
        """Ajoute une arme en cours de partie (niveau-up, shop)"""
        arme_obj = Arme(nom_arme)
        Arme.arme_possede.append(arme_obj)
        self.armes = self._construire_armes() 


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
        if not self.alive:
            return
        self.hp -= degats
        if self.hp <= 0 :
            self.alive = False

    def update_xp(self, xp, xp_attendu):
        self.xp += xp
        if self.xp >= xp_attendu :
            self.xp -= xp_attendu
            self.niveau += 1
            return True
        return False
    
   
    def ajouter_item(self, nom_item):
         
        item_obj = Items(nom_item)
    
        carac = item_obj.caracteristiques

        if carac.get("vitesse_du_j"):
            self.vitesse *= (1 + carac["vitesse_du_j"])
        if carac.get("attirance"):
            self.attirance = getattr(self, "attirance", 0) + carac["attirance"]
        if carac.get("protection"):
            self.protection = getattr(self, "protection", 0) + carac["protection"]
    # ajoute d'autres effets selon tes besoins
    def update_cooldown(self):
        """À appeler chaque frame pour réduire le cooldown"""
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

    def get_direction(self):
        if "anim" in PERSOS[self.perso]:
            if self.anim == self.anim_horizon_r:
                return (1, 0)   # droite
            elif self.anim == self.anim_horizon_l:
             return (-1, 0)  # gauche
            elif self.anim == self.anim_arriere:
                return (0, -1)  # haut
            else:
                return (0, 1)   # bas (anim_avant = direction par défaut)
        else:
            if self.image == self.image_r:
                return (1, 0)
            else:
                return (-1, 0)
import pygame as pyg
from Fichiers_variables.variables import * 
import math
from Armes_Items.class_items_sans_bugs import Items 
from Armes_Items.classe_projectile import Projectile
from Affichage.fonctionnement_divers import camera
from Interface.Game_over import game_over
from Armes_Items.creer_arme import creer_arme
from Fichiers_variables.dictionnaire_armes import ARMES
from Armes_Items.Classe_par_type_darme import ArmeProjectile, ArmeEpee, ArmeMultiDirection, ArmeZone, ArmeExplosion
from Jeu.power_up import apply_powerups
from Armes_Items.class_armes_sans_bugs import Arme
from Armes_Items.Item_system import InventaireItems, appliquer_stats_items


TYPE_VERS_CLASSE = {
    "balle":          ArmeProjectile,
    "zone":           ArmeZone,
    "coup":           ArmeEpee,
    "trait":          ArmeMultiDirection,
    "zone_multiples": ArmeExplosion,
}


class Player:
    """Class Player"""

    def __init__(self, perso, nom):
        self.nom   = nom
        self.perso = perso

        
        if "image" in PERSOS[perso]:
            self.image_r = PERSOS[perso]["image"]["horizon_r"]
            self.image_l = PERSOS[perso]["image"]["horizon_l"]
            self.image   = self.image_r
            self.pos     = self.image.get_rect()
        else:
            self.index         = 0
            self.anim_avant    = PERSOS[perso]["anim"]["avant"]
            self.anim_arriere  = PERSOS[perso]["anim"]["arriere"]
            self.anim_horizon_r= PERSOS[perso]["anim"]["horizon_r"]
            self.anim_horizon_l= PERSOS[perso]["anim"]["horizon_l"]
            self.anim          = self.anim_avant
            self.pos           = self.anim[0].get_rect()

        self.pos.center = CENTREx, CENTREy

        # Stats de base
        self.hp_max_base    = PLAYER_PV
        self.vitesse_base   = PLAYER_VIT
        self.zone_base      = 1.0
        self.portee_xp_base = 100.0

        
        self.hp              = PLAYER_PV
        self.hp_max          = PLAYER_PV
        self.vitesse         = PLAYER_VIT

        # Bonus items (valeur 0 / 1.0 = aucun bonus)
        self.bonus_degats       = 0.0
        self.attaque_mult       = 1.0
        self.cooldown_reduction = 0.0
        self.argent_bonus       = 0.0
        self.nb_projectiles     = 1
        self.regen              = 0.0
        self.chance             = 0.0
        self.duree_effets       = 1.0
        self.resurrection       = False
        self.zone_attaque       = 1.0
        self.portee_xp          = 100.0
        self.reduction_degats   = 0.0

       
        self.arme_active  = 0
        self.armes        = []
        self.armes_unlock = set()
        self.all_zones    = pyg.sprite.Group()
        self.armes_data   = Arme.arme_possede

        
        self.inventaire_items = InventaireItems(perso)

        
        self.xp          = 0
        self.niveau      = 1
        self.kill_count  = 0
        self.alive       = True
        self.color       = PERSOS[perso]["color"]
        self.x_monde     = CENTREx
        self.y_monde     = CENTREy

        self.all_projectiles    = pyg.sprite.Group()
        self.projectile_cooldown= 0
        self.projectile_cadence = 30

    

    def draw_player(self, frame):
        if "anim" in PERSOS[self.perso]:
            if frame % 4 == 0:
                self.index += 1
                self.index  = self.index % len(self.anim)
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
        self.armes.append(arme)

    def equiper_arme(self, nom_arme):
        """Ajoute une arme en cours de partie (niveau-up, coffre)."""
        self.ajouter_arme(nom_arme)

    

    def ajouter_item(self, nom_item):
        """
        Équipe un item et recalcule immédiatement toutes les stats.
        Utilisé au démarrage (items de départ) et en cours de partie.
        """
        self.inventaire_items.equiper_item(nom_item, self.niveau)
        appliquer_stats_items(self, self.inventaire_items.calculer_stats())

    

    def move_bg(self, monstres, xp, monstres_vague, boss, boss_present):
        keys  = pyg.key.get_pressed()
        up    = keys[pyg.K_UP]    or keys[pyg.K_w]
        right = keys[pyg.K_RIGHT] or keys[pyg.K_d]
        left  = keys[pyg.K_LEFT]  or keys[pyg.K_a]
        down  = keys[pyg.K_DOWN]  or keys[pyg.K_s]

        obj_a_deplacer = monstres + xp
        if monstres_vague is not None:
            obj_a_deplacer += monstres_vague
        if boss_present:
            obj_a_deplacer.append(boss)

        dx, dy = 0, 0

        if left:
            dx -= 1 * self.vitesse
            if "anim" in PERSOS[self.perso]:
                if self.anim != self.anim_horizon_l:
                    self.index = 0
                self.anim = self.anim_horizon_l
            else:
                self.image = self.image_l

        if right:
            dx += 1 * self.vitesse
            if "anim" in PERSOS[self.perso]:
                if self.anim != self.anim_horizon_r:
                    self.index = 0
                self.anim = self.anim_horizon_r
            else:
                self.image = self.image_r

        if up:
            dy -= 1 * self.vitesse
            if "anim" in PERSOS[self.perso]:
                if self.anim != self.anim_arriere:
                    self.index = 0
                self.anim = self.anim_arriere

        if down:
            dy += 1 * self.vitesse
            if "anim" in PERSOS[self.perso]:
                if self.anim != self.anim_avant:
                    self.index = 0
                self.anim = self.anim_avant

        if dx != 0 and dy != 0:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        self.x_monde += dx
        self.y_monde += dy

        for objet in obj_a_deplacer:
            objet.x_screen, objet.y_screen = camera(objet.x_monde, objet.y_monde, self)

   

    def degats(self, degats_bruts):
        """Subit des dégâts en tenant compte de la réduction (items protection)."""
        if not self.alive:
            return
        degats_reels = degats_bruts * (1.0 - self.reduction_degats)
        self.hp -= degats_reels
        if self.hp <= 0:
            self.hp    = 0
            self.alive = False

    def update_xp(self, xp, xp_attendu):
        self.xp += xp
        if self.xp >= xp_attendu:
            self.xp -= xp_attendu
            self.niveau += 1
            return True
        return False

    def update_cooldown(self):
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

    def get_direction(self):
        if "anim" in PERSOS[self.perso]:
            if self.anim == self.anim_horizon_r:
                return (1, 0)
            elif self.anim == self.anim_horizon_l:
                return (-1, 0)
            elif self.anim == self.anim_arriere:
                return (0, -1)
            else:
                return (0, 1)
        else:
            if self.image == self.image_r:
                return (1, 0)
            else:
                return (-1, 0)
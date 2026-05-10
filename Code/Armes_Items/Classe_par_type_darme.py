"""
Classe_par_type_darme.py — SOMNEK

Corrections :
- ArmeExplosion : ne tire PLUS de Projectile visible, crée l'Explosion directement
- ArmeOrbitale  : nouvelle classe — les armes orbitent autour du joueur
- draw()        : l'arme d'index 0 (arme de départ) s'affiche en main,
                  les autres tournent en orbite
- Aura_divine   : type "orbital_explosion" → orbite + explosion à l'impact
"""

import pygame as pyg
import random
import math

from Armes_Items.classe_projectile import Projectile, ProjectilePoison

ZONES_IMAGES = {
    "Cle_USB":           "Images/Armes_items/projectile/proj_cleusb.png",
    "Console_allumee":   "Images/Armes_items/projectile/proj_console.png",
    "Gloss_rose":        "Images/Armes_items/projectile/proj_gloss_rose.png",
    "Faux_ongles_roses": "Images/Armes_items/projectile/proj_faux_ongles_roses.png",
    "Coiffe_de_rameau":  "Images/Armes_items/projectile/proj_couronne.png",
    "Feu_de_l'Esprit_Saint": "Images/Armes_items/projectile/feu esprit sain.png",
}

_ZONE_FALLBACK = "Images/Armes_items/projectile/proj_couronne.png"


# ─────────────────────────────────────────────
#  Base
# ─────────────────────────────────────────────

class ArmeBase:
    def __init__(self, player, nom_arme: str = None):
        from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
        self.player   = player
        self.cooldown = 60
        self.timer    = 0
        self.nom      = nom_arme
        self.damage   = 10

        data           = TYPES_ARMES.get(player.perso, {}).get(nom_arme, {})
        self.proj_type = data.get("type_arme", "balle")
        self.damage    = data.get("dgbase", 10)

        image = data.get("image")
        if image:
            self.image   = pyg.transform.scale(image, (40, 40))
            self.visible = True
        else:
            self.image   = None
            self.visible = False

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def trigger(self):
        if self.timer <= 0:
            self.tirer()
            self.timer = self.cooldown

    def tirer(self):
        pass

    def _est_arme_de_base(self) -> bool:
        """Retourne True si cette arme est la première du joueur (index 0)."""
        return bool(self.player.armes) and self.player.armes[0] is self

    def draw(self, win):
        if not self.image:
            return
        if self._est_arme_de_base():
        # Arme de départ : en main
            direction = self.player.get_direction()
            px, py    = self.player.pos.x, self.player.pos.y
            offsets   = {
            (1,  0): (35, 10),
            (-1, 0): (-20, 10),
            (0, -1): (10, -20),
            (0,  1): (10, 35),
            }
            ox, oy = offsets.get(direction, (35, 10))
            win.blit(self.image, (px + ox, py + oy))
        else:
        # Armes secondaires : orbite simple
            idx = self.player.armes.index(self)  # position dans la liste
            angle_base = (idx * 90) % 360        # espacement à 90° entre armes
            # l'angle tourne avec le temps via un compteur global frame
            angle = (angle_base + pyg.time.get_ticks() * 0.1) % 360
            rad   = math.radians(angle)
            cx    = self.player.pos.centerx + math.cos(rad) * 80
            cy    = self.player.pos.centery + math.sin(rad) * 80
            rotated  = pyg.transform.rotate(self.image, -angle)
            rot_rect = rotated.get_rect(center=(int(cx), int(cy)))
            win.blit(rotated, rot_rect)

class ArmeProjectile(ArmeBase):
    """Tire un projectile dans la direction du joueur."""
    def tirer(self):
        proj = Projectile(
            self.player,
            proj_type=self.proj_type,
            nom_arme=self.nom
        )
        self.player.all_projectiles.add(proj)


# ─────────────────────────────────────────────
#  Explosion directe (SANS projectile visible)
# ─────────────────────────────────────────────

class ArmeExplosion(ArmeBase):
    """
    Crée une explosion directement à portée aléatoire.
    N'instancie AUCUN Projectile visible — élimine le double-sprite.
    """
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.cooldown = 90
        self.rayon    = 300

    def tirer(self):
        from Armes_Items.Explosions import Explosion
        angle    = random.uniform(0, 360)
        distance = random.uniform(50, self.rayon)
        rad      = math.radians(angle)
        x = self.player.x_monde + math.cos(rad) * distance
        y = self.player.y_monde + math.sin(rad) * distance
        exp = Explosion(x, y, self.player, degats=self.damage)
        # On ajoute dans la liste globale d'explosions via le player
        if hasattr(self.player, "explosions"):
            self.player.explosions.append(exp)


# ─────────────────────────────────────────────
#  Multi-direction (8 projectiles)
# ─────────────────────────────────────────────

class ArmeMultiDirection(ArmeBase):
    """Tire dans 8 directions simultanément."""
    def tirer(self):
        for angle in range(0, 360, 45):
            proj = Projectile(
                self.player,
                proj_type=self.proj_type,
                nom_arme=self.nom
            )
            proj.set_direction(angle)
            self.player.all_projectiles.add(proj)


# ─────────────────────────────────────────────
#  Poison
# ─────────────────────────────────────────────

class ArmePoison(ArmeBase):
    """Projectile empoisonné."""
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.cooldown = 80

    def tirer(self):
        proj = ProjectilePoison(
            self.player,
            nom_arme=self.nom
        )
        self.player.all_projectiles.add(proj)


# ─────────────────────────────────────────────
#  Zone ponctuelle (spawn aléatoire autour du joueur)
# ─────────────────────────────────────────────

class ZoneAttaque(pyg.sprite.Sprite):
    def __init__(self, pos, player, nom_arme: str = None, duration: int = 150):
        super().__init__()
        self.player = player

        image_path = ZONES_IMAGES.get(nom_arme, _ZONE_FALLBACK)
        self.image = pyg.image.load(image_path).convert_alpha()
        self.image = pyg.transform.scale(self.image, (120, 120))

        self.x_monde = pos[0]
        self.y_monde = pos[1]
        self.rect    = self.image.get_rect()
        self.timer   = duration

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            return
        from Affichage.fonctionnement_divers import camera
        sx, sy           = camera(self.x_monde, self.y_monde, self.player)
        self.rect.center = (sx, sy)


class ArmeZone(ArmeBase):
    """Crée une zone d'attaque à portée aléatoire autour du joueur."""
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.cooldown = 200
        self.rayon    = 400

    def tirer(self):
        angle    = random.uniform(0, 360)
        distance = random.uniform(20, self.rayon)
        rad      = math.radians(angle)
        x = self.player.x_monde + math.cos(rad) * distance
        y = self.player.y_monde + math.sin(rad) * distance
        zone = ZoneAttaque((x, y), self.player, nom_arme=self.nom)
        self.player.all_zones.add(zone)


# ─────────────────────────────────────────────
#  Épée (zone de coup au contact)
# ─────────────────────────────────────────────

class ZoneCoup(pyg.sprite.Sprite):
    def __init__(self, player, nom_arme: str, duration: int = 15):
        super().__init__()
        from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
        data  = TYPES_ARMES.get(player.perso, {}).get(nom_arme, {})
        image = data.get("image")
        if image:
            self.image = pyg.transform.scale(image, (50, 50))
        else:
            self.image = pyg.Surface((50, 50), pyg.SRCALPHA)
            self.image.fill((255, 255, 0, 180))

        self.rect   = self.image.get_rect()
        self.player = player
        self.timer  = duration

        dx, dy = player.get_direction()
        self.rect.centerx = player.pos.centerx + dx * 50
        self.rect.centery = player.pos.centery + dy * 50

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class ArmeEpee(ArmeBase):
    """Arme de mêlée : crée une zone de coup devant le joueur. Pas de Projectile."""
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.offset   = (20, 10)
        self.cooldown = 40

    def tirer(self):
        zone = ZoneCoup(self.player, self.nom)
        self.player.all_zones.add(zone)

    def draw(self, win):
        # L'épée de base s'affiche en main via ArmeBase.draw()
        super().draw(win)


# ─────────────────────────────────────────────
#  Orbitale — tourne autour du joueur en continu
# ─────────────────────────────────────────────

class ArmeOrbitale(ArmeBase):
    """
    L'arme tourne en orbite autour du joueur.
    Chaque tick elle vérifie les collisions avec les ennemis.
    Pas de Projectile tiré — le sprite orbital EST l'arme.

    Usage : Highlighter (Fille populaire), Aura_divine (Nonne)
    """
    RAYON_ORBITE  = 80      # pixels écran
    VITESSE_DEG   = 2.5     # degrés par frame

    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.cooldown = 1      # trigger chaque frame pour update_angle
        self.angle    = 0.0    # angle courant en degrés
        # Décalage de phase pour ne pas empiler toutes les orbitales au même endroit
        idx = len([a for a in player.armes if isinstance(a, ArmeOrbitale)])
        self.angle = idx * (360 / max(1, 4))   # répartition initiale

    def update(self):
        super().update()
        self.angle = (self.angle + self.VITESSE_DEG) % 360

    def tirer(self):
        # Pas de projectile — les dégâts sont gérés dans jeu.py via all_zones
        # On crée un sprite orbital pour la hitbox et l'affichage
        pass

    def get_pos_ecran(self):
        """Retourne la position écran du centre de l'orbitale."""
        rad = math.radians(self.angle)
        cx  = self.player.pos.centerx + math.cos(rad) * self.RAYON_ORBITE
        cy  = self.player.pos.centery + math.sin(rad) * self.RAYON_ORBITE
        return int(cx), int(cy)

    def get_rect_ecran(self):
        """Retourne le rect écran pour la détection de collision."""
        cx, cy = self.get_pos_ecran()
        if self.image:
            r = self.image.get_rect(center=(cx, cy))
        else:
            r = pyg.Rect(0, 0, 40, 40)
            r.center = (cx, cy)
        return r

    def draw(self, win):
        if not self.image:
            return
        cx, cy = self.get_pos_ecran()
        rect   = self.image.get_rect(center=(cx, cy))
        # Rotation de l'image selon l'angle pour un effet plus vivant
        rotated = pyg.transform.rotate(self.image, -self.angle)
        rot_rect = rotated.get_rect(center=(cx, cy))
        win.blit(rotated, rot_rect)


class ArmeOrbitaleExplosion(ArmeOrbitale):
    """
    Variante orbitale qui déclenche une explosion quand elle touche un ennemi.
    Utilisée par Aura_divine.
    """
    RAYON_ORBITE = 90
    VITESSE_DEG  = 3.0

    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self._explosion_cooldown = 0

    def update(self):
        super().update()
        if self._explosion_cooldown > 0:
            self._explosion_cooldown -= 1

    def declencher_explosion(self):
        """Appelé depuis jeu.py quand la hitbox touche un ennemi."""
        if self._explosion_cooldown > 0:
            return
        from Armes_Items.Explosions import Explosion
        cx, cy = self.get_pos_ecran()
        # Convertir position écran → monde
        x_monde = self.player.x_monde + (cx - self.player.pos.centerx)
        y_monde = self.player.y_monde + (cy - self.player.pos.centery)
        exp = Explosion(x_monde, y_monde, self.player, degats=self.damage)
        if hasattr(self.player, "explosions"):
            self.player.explosions.append(exp)
        self._explosion_cooldown = 45   # ~0.75 s à 60 fps entre deux explosions
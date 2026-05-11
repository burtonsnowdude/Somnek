"""
Classe_par_type_darme.py — SOMNEK

CORRECTIONS :
- Nouvelle méthode ArmeBase.calculer_degats_finaux() qui combine :
    arme.damage × (1 + player.bonus_degats) × player.attaque_mult
- Tous les .tirer() propagent ces dégâts au Projectile / Explosion / Zone
  (avant, Projectile.damage restait hardcodé à 10 dans son __init__)
- ZoneAttaque et ZoneCoup stockent leur damage pour que la collision
  dans jeu.py puisse le lire via `zone.damage`
"""

import pygame as pyg
import random
import math

from Armes_Items.classe_projectile import Projectile, ProjectilePoison

ZONES_IMAGES = {
    "Cle_USB":               "Images/Armes_items/projectile/proj_cleusb.png",
    "Console_allumee":       "Images/Armes_items/projectile/proj_console.png",
    "Gloss_rose":            "Images/Armes_items/projectile/proj_gloss_rose.png",
    "Faux_ongles_roses":     "Images/Armes_items/projectile/proj_faux_ongles_roses.png",
    "Coiffe_de_rameau":      "Images/Armes_items/projectile/proj_couronne.png",
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

    # ── NOUVEAU : centralise le calcul de dégâts incluant les bonus joueur
    def calculer_degats_finaux(self) -> float:
        """
        Dégâts de base de l'arme × bonus du joueur (items 'degats' et 'attaque').
        À utiliser dans CHAQUE tirer() pour propager au projectile/zone/explosion.
        """
        bonus_degats = getattr(self.player, "bonus_degats", 0.0)
        attaque_mult = getattr(self.player, "attaque_mult", 1.0)
        return float(self.damage) * (1.0 + bonus_degats) * attaque_mult

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
        return bool(self.player.armes) and self.player.armes[0] is self

    def draw(self, win):
        if not self.image:
            return
        if self._est_arme_de_base():
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
            idx        = self.player.armes.index(self)
            angle_base = (idx * 90) % 360
            angle      = (angle_base + pyg.time.get_ticks() * 0.1) % 360
            rad        = math.radians(angle)
            cx         = self.player.pos.centerx + math.cos(rad) * 80
            cy         = self.player.pos.centery + math.sin(rad) * 80
            rotated    = pyg.transform.rotate(self.image, -angle)
            rot_rect   = rotated.get_rect(center=(int(cx), int(cy)))
            win.blit(rotated, rot_rect)


# ─────────────────────────────────────────────
#  Projectile simple
# ─────────────────────────────────────────────

class ArmeProjectile(ArmeBase):
    """Tire un projectile dans la direction du joueur."""
    def tirer(self):
        proj = Projectile(
            self.player,
            proj_type=self.proj_type,
            nom_arme=self.nom,
        )
        proj.damage = self.calculer_degats_finaux()   # FIX
        self.player.all_projectiles.add(proj)


# ─────────────────────────────────────────────
#  Explosion directe (sans projectile visible)
# ─────────────────────────────────────────────

class ArmeExplosion(ArmeBase):
    """Crée une explosion à portée aléatoire."""
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
        exp = Explosion(
            x, y, self.player,
            degats=self.calculer_degats_finaux(),     # FIX
        )
        if hasattr(self.player, "explosions"):
            self.player.explosions.append(exp)


# ─────────────────────────────────────────────
#  Multi-direction (8 projectiles)
# ─────────────────────────────────────────────

class ArmeMultiDirection(ArmeBase):
    """Tire dans 8 directions simultanément."""
    def tirer(self):
        degats = self.calculer_degats_finaux()        # FIX : une seule fois
        for angle in range(0, 360, 45):
            proj = Projectile(
                self.player,
                proj_type=self.proj_type,
                nom_arme=self.nom,
            )
            proj.damage = degats
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
        proj = ProjectilePoison(self.player, nom_arme=self.nom)
        proj.damage = self.calculer_degats_finaux()   # FIX
        self.player.all_projectiles.add(proj)


# ─────────────────────────────────────────────
#  Zone ponctuelle (spawn autour du joueur)
# ─────────────────────────────────────────────

class ZoneAttaque(pyg.sprite.Sprite):
    def __init__(self, pos, player, nom_arme: str = None,
                 duration: int = 150, damage: float = 10.0):
        super().__init__()
        self.player = player
        self.damage = damage                          # FIX : exposé pour jeu.py

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
    """Crée une zone d'attaque à portée aléatoire."""
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
        zone = ZoneAttaque(
            (x, y), self.player,
            nom_arme=self.nom,
            damage=self.calculer_degats_finaux(),     # FIX
        )
        self.player.all_zones.add(zone)


# ─────────────────────────────────────────────
#  Épée (zone de coup au contact)
# ─────────────────────────────────────────────

class ZoneCoup(pyg.sprite.Sprite):
    def __init__(self, player, nom_arme: str,
                 duration: int = 15, damage: float = 10.0):
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
        self.damage = damage                          # FIX

        dx, dy            = player.get_direction()
        self.rect.centerx = player.pos.centerx + dx * 50
        self.rect.centery = player.pos.centery + dy * 50

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class ArmeEpee(ArmeBase):
    """Mêlée : crée une zone de coup devant le joueur."""
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.offset   = (20, 10)
        self.cooldown = 40

    def tirer(self):
        zone = ZoneCoup(
            self.player, self.nom,
            damage=self.calculer_degats_finaux(),     # FIX
        )
        self.player.all_zones.add(zone)

    def draw(self, win):
        super().draw(win)


# ─────────────────────────────────────────────
#  Orbitales
# ─────────────────────────────────────────────

class ArmeOrbitale(ArmeBase):
    """L'arme tourne autour du joueur. Hitbox = self.get_rect_ecran()."""
    RAYON_ORBITE = 80
    VITESSE_DEG  = 2.5

    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, nom_arme)
        self.cooldown = 1
        self.angle    = 0.0
        idx = len([a for a in player.armes if isinstance(a, ArmeOrbitale)])
        self.angle = idx * (360 / max(1, 4))

    def update(self):
        super().update()
        self.angle = (self.angle + self.VITESSE_DEG) % 360

    def tirer(self):
        # Pas de projectile. La hitbox orbite et les dégâts sont gérés via jeu.py
        pass

    def get_pos_ecran(self):
        rad = math.radians(self.angle)
        cx  = self.player.pos.centerx + math.cos(rad) * self.RAYON_ORBITE
        cy  = self.player.pos.centery + math.sin(rad) * self.RAYON_ORBITE
        return int(cx), int(cy)

    def get_rect_ecran(self):
        cx, cy = self.get_pos_ecran()
        if self.image:
            return self.image.get_rect(center=(cx, cy))
        r = pyg.Rect(0, 0, 40, 40)
        r.center = (cx, cy)
        return r

    def draw(self, win):
        if not self.image:
            return
        cx, cy   = self.get_pos_ecran()
        rotated  = pyg.transform.rotate(self.image, -self.angle)
        rot_rect = rotated.get_rect(center=(cx, cy))
        win.blit(rotated, rot_rect)


class ArmeOrbitaleExplosion(ArmeOrbitale):
    """Variante orbitale : déclenche une explosion au contact."""
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
        """Appelé depuis jeu.py au contact avec un ennemi."""
        if self._explosion_cooldown > 0:
            return
        from Armes_Items.Explosions import Explosion
        cx, cy  = self.get_pos_ecran()
        x_monde = self.player.x_monde + (cx - self.player.pos.centerx)
        y_monde = self.player.y_monde + (cy - self.player.pos.centery)
        exp = Explosion(
            x_monde, y_monde, self.player,
            degats=self.calculer_degats_finaux(),     # FIX
        )
        if hasattr(self.player, "explosions"):
            self.player.explosions.append(exp)
        self._explosion_cooldown = 45                 # ~0.75s à 60 fps
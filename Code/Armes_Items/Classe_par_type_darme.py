import pygame as pyg
from Armes_Items.classe_projectile import Projectile, ProjectilePoison
import random
import math

ZONES_IMAGES = {
    # Nerd
    "Cle_USB":          "Images/Armes_items/projectile/proj_cleusb.png",
    "Console_allumee":  "Images/Armes_items/projectile/proj_console.png",

    # Fille populaire
    "Gloss_rose":       "Images/Armes_items/projectile/proj_gloss_rose.png",
    "Faux_ongles_roses":"Images/Armes_items/projectile/proj_faux_ongles_roses.png",

    # Nonne
    "Coiffe_de_rameau": "Images/Armes_items/projectile/proj_couronne.png",
}
class ArmeBase:
    def __init__(self, player, nom_arme=None):
        from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
        self.player = player
        self.cooldown = 60
        self.timer = 0
        self.nom = nom_arme
        self.damage = 10

        data = TYPES_ARMES.get(player.perso, {}).get(nom_arme, {})  # ← data AVANT proj_type
        self.proj_type = data.get("type_arme", "balle")             # ← maintenant data existe

        image = data.get("image")
        if image:
            self.image = pyg.transform.scale(image, (40, 40))
            self.visible = True
        else:
            self.image = None
            self.visible = False

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def trigger(self):
        if self.timer <= 0:
            self.tirer()            # ← ne pas oublier self.tirer()
            self.timer = self.cooldown

    def tirer(self):
        pass

    def draw(self, win):
        if not self.image:
            return
        direction = self.player.get_direction()
        px, py = self.player.pos.x, self.player.pos.y
        offsets = {
            (1, 0):  (35, 10),
            (-1, 0): (-20, 10),
            (0, -1): (10, -20),
            (0, 1):  (10, 35),
        }
        ox, oy = offsets.get(direction, (35, 10))
        win.blit(self.image, (px + ox, py + oy))


class ArmeProjectile(ArmeBase):
    def tirer(self):
        proj = Projectile(self.player, proj_type=self.proj_type)
        self.player.all_projectiles.add(proj)


class ArmeExplosion(ArmeBase):
    def __init__(self, player, nom_arme=None):
        super().__init__(player, nom_arme)
        self.cooldown = 90
        self.has_explosion = True

    def tirer(self):
        proj = Projectile(self.player, proj_type=self.proj_type, explode=True)
        self.player.all_projectiles.add(proj)


class ZoneAttaque(pyg.sprite.Sprite):
    def __init__(self, pos, player, nom_arme=None, duration=150):
        super().__init__()
        self.player = player

        image_path = ZONES_IMAGES.get(nom_arme, "Images/Armes_items/projectile/proj_couronne.png")
        self.image = pyg.image.load(image_path).convert_alpha()
        self.image = pyg.transform.scale(self.image, (120, 120))  # ← augmente ces valeurs

        self.x_monde = pos[0]
        self.y_monde = pos[1]
        self.rect = self.image.get_rect()
        self.timer = duration

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            return
        from Affichage.fonctionnement_divers import camera
        sx, sy = camera(self.x_monde, self.y_monde, self.player)
        self.rect.center = (sx, sy)


class ArmeZone(ArmeBase):
    def __init__(self, player, nom_arme=None):
        super().__init__(player, nom_arme)
        self.cooldown = 200
        self.rayon = 400

    def tirer(self):
        angle = random.uniform(0, 360)
        distance = random.uniform(20, self.rayon)
        rad = math.radians(angle)
        x = self.player.x_monde + math.cos(rad) * distance
        y = self.player.y_monde + math.sin(rad) * distance
        zone = ZoneAttaque((x, y), self.player, nom_arme=self.nom)  # ← passe self.nom
        self.player.all_zones.add(zone)

class ArmeMultiDirection(ArmeBase):
    def __init__(self, player, nom_arme=None):
        super().__init__(player, nom_arme)

    def tirer(self):
        for angle in range(0, 360, 45):
            proj = Projectile(self.player, proj_type=self.proj_type)
            proj.set_direction(angle)
            self.player.all_projectiles.add(proj)


class ZoneCoup(pyg.sprite.Sprite):
    def __init__(self, player, nom_arme, duration=15):  # ← nom_arme en paramètre
        super().__init__()
        from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
        data = TYPES_ARMES.get(player.perso, {}).get(nom_arme, {})  # ← nom_arme direct
        image = data.get("image")
        if image:
            self.image = pyg.transform.scale(image, (50, 50))
        else:
            self.image = pyg.Surface((50, 50), pyg.SRCALPHA)
            self.image.fill((255, 255, 0, 180))
        self.rect = self.image.get_rect()
        self.player = player
        self.timer = duration
        dx, dy = player.get_direction()
        self.rect.centerx = player.pos.centerx + dx * 50
        self.rect.centery = player.pos.centery + dy * 50

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()


class ArmeEpee(ArmeBase):
    def __init__(self, player, nom_arme=None):
        super().__init__(player, nom_arme)
        self.offset = (20, 10)
        self.cooldown = 40

    def tirer(self):
        zone = ZoneCoup(self.player, self.nom)  # ← passe self.nom
        self.player.all_zones.add(zone)
    def draw(self, win):
        if self.image:
            pos = self.player.pos.copy()
            pos.x += self.offset[0]
            pos.y += self.offset[1]
            win.blit(self.image, pos)


class ArmePoison(ArmeBase):
    def __init__(self, player, nom_arme=None):
        super().__init__(player, nom_arme)
        self.cooldown = 80

    def tirer(self):
        proj = ProjectilePoison(self.player)
        self.player.all_projectiles.add(proj)
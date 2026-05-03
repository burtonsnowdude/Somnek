import pygame as pyg
from Armes_Items.classe_projectile import Projectile


# =========================
# BASE WEAPON
# =========================
class ArmeBase:
    def __init__(self, player):
        self.player = player
        self.cooldown = 30
        self.timer = 0
        self.visible = False
        self.damage = 10

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def trigger(self):
        if self.timer <= 0:
            self.tirer()
            self.timer = self.cooldown

    def tirer(self):
        pass

    def draw(self, win):
        pass


# =========================
# PROJECTILE WEAPON
# =========================
class ArmeProjectile(ArmeBase):
    def tirer(self):
        projectile = Projectile(self.player)
        self.player.all_projectiles.add(projectile)


# =========================
# ZONE D'ATTAQUE
# =========================
class ZoneAttaque(pyg.sprite.Sprite):
    def __init__(self, pos, player, duration=150):
        super().__init__()  # ← SANS arguments

        self.player = player  # ← pour accéder à la caméra

        self.image = pyg.image.load(
            "Images/Armes_items/projectile/proj_couronne.png"
        ).convert_alpha()
        self.image = pyg.transform.scale(self.image, (200, 300))

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
        sx, sy = camera(self.x_monde, self.y_monde, self.player)  # ← self.player, pas de paramètre
        self.rect.center = (sx, sy)



class ArmeZone(ArmeBase):
    def __init__(self, player):
        super().__init__(player)
        self.cooldown = 120

    def tirer(self):
        x = self.player.x_monde + 150
        y = self.player.y_monde

        zone = ZoneAttaque((x, y), self.player)  # ← on passe le player
        self.player.all_zones.add(zone)


# =========================
# MULTI DIRECTION
# =========================
class ArmeMultiDirection(ArmeBase):
    def tirer(self):
        for angle in range(0, 360, 45):
            proj = Projectile(self.player, proj_type="slash")
            proj.set_direction(angle)
            self.player.all_projectiles.add(proj)


# =========================
# EPEE / ORBITE
# =========================
class ArmeEpee(ArmeBase):
    def __init__(self, player):
        super().__init__(player)
        self.visible = True
        self.offset = (20, 10)

        image = pyg.image.load("Images/Armes_items/ticket.png").convert_alpha()
        self.image = pyg.transform.scale(image, (20, 20))

    def draw(self, win):
        pos = self.player.pos.copy()
        pos.x += self.offset[0]
        pos.y += self.offset[1]
        win.blit(self.image, pos)
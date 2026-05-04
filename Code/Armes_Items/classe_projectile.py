import math
import pygame as pyg

PROJECTILES = { "bullet": "Images/Armes_items/projectile/feu esprit sain.png",
    "fireball" : "Images/Armes_items/projectile/proj_highliter.png",
    "slash": "Images/Armes_items/projectile/proj_ticket.png"
}


class Projectile(pyg.sprite.Sprite):
    """Projectile générique"""

    def __init__(self, player, proj_type="bullet", explode=False):
        super().__init__()

        self.player = player
        self.type = proj_type

        self.speed = 7
        self.damage = 10
        self.piercing = 1
        self.explode = explode 

        self.image = pyg.image.load(PROJECTILES[self.type]).convert_alpha()
        if self.type == "bullet":
            self.image = pyg.transform.scale(self.image, (30, 30))
        elif self.type == "fireball":
            self.image = pyg.transform.scale(self.image, (50, 50)) 
        self.rect = self.image.get_rect(center=player.pos.center)

        dx, dy = player.get_direction()
        self.dx = dx
        self.dy = dy
    def set_direction(self, angle):
        rad = math.radians(angle)
        self.dx = math.cos(rad)
        self.dy = math.sin(rad)

        length = math.sqrt(self.dx**2 + self.dy**2)
        if length != 0:
            self.dx /= length
            self.dy /= length

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        self.check_bounds()

    def check_bounds(self):
        if (
            self.rect.right < 0 or
            self.rect.left > 1920 or
            self.rect.bottom < 0 or
            self.rect.top > 1080
        ):
            self.kill()

    def hit(self, enemy):
        enemy.degats(self.damage)
        self.piercing -= 1
        if self.piercing <= 0:
            self.kill()
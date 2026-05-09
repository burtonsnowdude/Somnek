import math
import pygame as pyg

from Fichiers_variables.traitement_images import decouper_image

PROJECTILES = {
    # Nerd
      "Epee_bleue":
          "Images/Armes_items/projectile/proj_epee.png",
    
    "Epee_enflammee" :  {
        "path":    "Images/Armes_items/Epee enflamee.png",
        "cols":    4,
        "rows":    1,
        "enlever": 0,
        "taille":  (30, 30)
    },
    "Cle_USB":          "Images/Armes_items/projectile/proj_cleusb.png",
    "Pistolets":        "Images/Armes_items/projectile/proj_pistolets.png",
    "Ticket_de_metro":  "Images/Armes_items/projectile/proj_ticket.png",

    # Fille populaire
    "Gloss_rose":           "Images/Armes_items/projectile/proj_gloss_rose.png",
    "Faux_cils":            "Images/Armes_items/projectile/proj_faux_cils.png",
    "Faux_ongles_roses":    "Images/Armes_items/projectile/proj_ongles.png",
    "Bracelet_de_sa_soeur": { "path" : "Images/Armes_items/projectile/proj_bracelet.png"
      ,
        "cols":    7,
        "rows":    1,
        "enlever": 0,
        "taille":  (30, 30)},
    "Fer_a_lisser":  {"path" :     "Images/Armes_items/projectile/proj_fer_a_lisser.png",
      "cols":    4,
        "rows":    1,
        "enlever": 0,
        "taille":  (30, 30)},
    "Pass_Navigo":          "Images/Armes_items/projectile/proj_ticket.png",
    "Ring_light":           "Images/Armes_items/projectile/proj_ring.png",
    "Highlighter" : "Images/Armes_items/projectile/proj_highliter.png",

    # Nonne
    "Croix_marron":   {"path" :   "Images/Armes_items/projectile/proj_croix.png",  "cols":    4,
        "rows":    1,
        "enlever": 0,
        "taille":  (30, 30)},
    "Feu_de_l'Esprit_Saint":"Images/Armes_items/projectile/feu esprit sain.png",
    "Medaille_de_bapteme":  "Images/Armes_items/projectile/proj_medaille.png",
    "Coiffe_de_rameau":     "Images/Armes_items/projectile/proj_couronne.png",
    "Lance_sacree":         "Images/Armes_items/projectile/proj_lance.png",
    "Aura_divine":          "Images/Armes_items/projectile/aura divine.png",
    "JALAMBAYA":          {"path" : "Images/Armes_items/projectile/proj_jalambaya.png",  "cols":    13,
        "rows":    1,
        "enlever": 0,
        "taille":  (30, 30)},
}

class Projectile(pyg.sprite.Sprite):
    def __init__(self, player, proj_type="balle", explode=False):
        super().__init__()
        self.player = player
        self.type = proj_type
        self.speed = 7
        self.damage = 10
        self.piercing = 1
        self.explode = explode
        self.anime = False

        nom_arme = player.armes[player.arme_active].nom
        image_data = PROJECTILES.get(nom_arme)

        if image_data is None:
            self.image = pyg.image.load("Images/Armes_items/projectile/feu esprit sain.png").convert_alpha()
            self.image = pyg.transform.scale(self.image, (30, 30))
        elif isinstance(image_data, dict):
            self.anim = self._charger_anim(image_data)
            self.anim_index = 0
            self.anim_timer = 0
            self.anim_speed = 6
            self.image = self.anim[0]
            self.anime = True
        elif isinstance(image_data, str):
            self.image = pyg.image.load(image_data).convert_alpha()
            self.image = pyg.transform.scale(self.image, (30, 30))
        else:
            self.image = pyg.transform.scale(image_data, (30, 30))

        self.rect = self.image.get_rect(center=player.pos.center)
        dx, dy = player.get_direction()
        self.dx = dx
        self.dy = dy

    def _charger_anim(self, data):
        sheet = pyg.image.load(data["path"]).convert_alpha()
        frames = decouper_image(sheet, data["cols"], data["rows"], data.get("enlever", 0))
        taille = data.get("taille", (30, 30))
        return [pyg.transform.scale(f, taille) for f in frames]

    def set_direction(self, angle):
        rad = math.radians(angle)
        self.dx = math.cos(rad)
        self.dy = math.sin(rad)
        length = math.sqrt(self.dx**2 + self.dy**2)
        if length != 0:
            self.dx /= length
            self.dy /= length

    def update(self):
        if self.anime:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_index = (self.anim_index + 1) % len(self.anim)
                self.image = self.anim[self.anim_index]
                self.anim_timer = 0
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


class ProjectilePoison(Projectile):
    def __init__(self, player):
        super().__init__(player, proj_type="poison")
        self.poison = True
        self.duree_poison = 180
        self.degats_poison = 2
        self.tick = 30
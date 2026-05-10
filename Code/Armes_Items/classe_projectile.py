"""
classe_projectile.py — SOMNEK
- Epee_bleue retiré de PROJECTILES (ArmeEpee ne tire pas de Projectile)
- Cle_USB : image statique (c'est une ArmeZone, pas de projectile visible)
- Fer_a_lisser retiré (ArmeExplosion ne crée pas de Projectile visible)
- Ring_light retiré (idem)
- Croix_marron : poison animé, conservé
"""

import math
import pygame as pyg

from Fichiers_variables.traitement_images import decouper_image

PROJECTILES = {
    # ── Nerd ──────────────────────────────────────────────────────────────
    # Epee_bleue : RETIRÉ — ArmeEpee crée une ZoneCoup, pas un Projectile
    "Epee_enflammee": {
        "path":    "Images/Armes_items/Epee enflamee.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    # Cle_USB : statique — c'est une ArmeZone, pas de projectile tiré
    "Pistolets":            "Images/Armes_items/projectile/proj_pistolet.png",
    "Ticket_de_metro":      "Images/Armes_items/projectile/proj_ticket.png",

    # ── Fille populaire ───────────────────────────────────────────────────
    # Gloss_rose : ArmeZone → pas de projectile visible
    "Faux_cils":            "Images/Armes_items/projectile/proj_faux_cils.png",
    "Faux_ongles_roses":    "Images/Armes_items/projectile/proj_ongles.png",
    "Bracelet_de_sa_soeur": {
        "path":    "Images/Armes_items/projectile/proj_bracelet.png",
        "cols":    7, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    # Fer_a_lisser : RETIRÉ — ArmeExplosion ne tire pas de Projectile visible
    # Ring_light   : RETIRÉ — idem ArmeExplosion
    "Pass_Navigo":          "Images/Armes_items/projectile/proj_ticket.png",
    "Highlighter":          "Images/Armes_items/projectile/proj_highliter.png",

    # ── Nonne ─────────────────────────────────────────────────────────────
    "Croix_marron": {
        "path":    "Images/Armes_items/projectile/proj_croix.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Feu_de_l'Esprit_Saint": "Images/Armes_items/projectile/feu esprit sain.png",
    "Medaille_de_bapteme":   "Images/Armes_items/projectile/proj_medaille.png",
    # Coiffe_de_rameau : ArmeZone → pas de projectile visible
    "Lance_sacree":          "Images/Armes_items/projectile/proj_lance.png",
    # Aura_divine : ArmeOrbitale → gère son propre affichage
    "JALAMBAYA": {
        "path":    "Images/Armes_items/projectile/proj_jalambaya.png",
        "cols":    13, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
}

_FALLBACK_PATH = "Images/Armes_items/projectile/feu esprit sain.png"


def _charger_image_projectile(nom_arme: str):
    """
    Retourne (image_ou_frames, est_anime).
    """
    image_data = PROJECTILES.get(nom_arme)

    if image_data is None:
        img = pyg.image.load(_FALLBACK_PATH).convert_alpha()
        return pyg.transform.scale(img, (30, 30)), False

    if isinstance(image_data, dict):
        sheet  = pyg.image.load(image_data["path"]).convert_alpha()
        frames = decouper_image(
            sheet,
            image_data["cols"],
            image_data["rows"],
            image_data.get("enlever", 0)
        )
        taille = image_data.get("taille", (30, 30))
        frames = [pyg.transform.scale(f, taille) for f in frames]
        return frames, True

    img = pyg.image.load(image_data).convert_alpha()
    return pyg.transform.scale(img, (30, 30)), False


class Projectile(pyg.sprite.Sprite):
    """
    Paramètre `nom_arme` (str) : le nom de l'arme qui tire CE projectile.
    Toujours le passer explicitement depuis ArmeBase.tirer().
    """

    def __init__(self, player, proj_type: str = "balle",
                 explode: bool = False, nom_arme: str = None):
        super().__init__()
        self.player   = player
        self.type     = proj_type
        self.speed    = 7
        self.damage   = 10
        self.piercing = 1
        self.explode  = explode
        self.anime    = False

        if nom_arme is None:
            if player.armes:
                nom_arme = player.armes[player.arme_active].nom
            else:
                nom_arme = ""
        self.nom_arme = nom_arme

        result, self.anime = _charger_image_projectile(nom_arme)

        if self.anime:
            self.anim        = result
            self.anim_index  = 0
            self.anim_timer  = 0
            self.anim_speed  = 6
            self.image       = self.anim[0]
        else:
            self.image = result

        self.rect = self.image.get_rect(center=player.pos.center)
        dx, dy    = player.get_direction()
        self.dx   = float(dx)
        self.dy   = float(dy)

    def set_direction(self, angle: float):
        rad     = math.radians(angle)
        self.dx = math.cos(rad)
        self.dy = math.sin(rad)
        length  = math.hypot(self.dx, self.dy)
        if length:
            self.dx /= length
            self.dy /= length

    def update(self):
        if self.anime:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_index = (self.anim_index + 1) % len(self.anim)
                self.image      = self.anim[self.anim_index]
                self.anim_timer = 0

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        self._check_bounds()

    def _check_bounds(self):
        if (self.rect.right  < 0    or self.rect.left > 1920 or
                self.rect.bottom < 0 or self.rect.top  > 1080):
            self.kill()

    def hit(self, enemy):
        enemy.degats(self.damage)
        self.piercing -= 1
        if self.piercing <= 0:
            self.kill()


class ProjectilePoison(Projectile):
    def __init__(self, player, nom_arme: str = None):
        super().__init__(player, proj_type="poison", nom_arme=nom_arme)
        self.poison        = True
        self.duree_poison  = 180
        self.degats_poison = 2
        self.tick          = 30
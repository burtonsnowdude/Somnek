"""
classe_projectile.py — SOMNEK
Correction clé : le nom de l'arme est passé EXPLICITEMENT au Projectile.
On ne se fie plus à player.arme_active (qui peut avoir changé entre temps).
"""

import math
import pygame as pyg

from Fichiers_variables.traitement_images import decouper_image

PROJECTILES = {
    # Nerd
    "Epee_bleue":           "Images/Armes_items/projectile/proj_epee.png",
    "Epee_enflammee": {
        "path":    "Images/Armes_items/Epee enflamee.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Cle_USB":              "Images/Armes_items/projectile/proj_cleusb.png",
    "Pistolets":            "Images/Armes_items/projectile/proj_pistolets.png",
    "Ticket_de_metro":      "Images/Armes_items/projectile/proj_ticket.png",

    # Fille populaire
    "Gloss_rose":           "Images/Armes_items/projectile/proj_gloss_rose.png",
    "Faux_cils":            "Images/Armes_items/projectile/proj_faux_cils.png",
    "Faux_ongles_roses":    "Images/Armes_items/projectile/proj_ongles.png",
    "Bracelet_de_sa_soeur": {
        "path":    "Images/Armes_items/projectile/proj_bracelet.png",
        "cols":    7, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Fer_a_lisser": {
        "path":    "Images/Armes_items/projectile/proj_fer_a_lisser.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Pass_Navigo":          "Images/Armes_items/projectile/proj_ticket.png",
    "Ring_light":           "Images/Armes_items/projectile/proj_ring.png",
    "Highlighter":          "Images/Armes_items/projectile/proj_highliter.png",

    # Nonne
    "Croix_marron": {
        "path":    "Images/Armes_items/projectile/proj_croix.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Feu_de_l'Esprit_Saint": "Images/Armes_items/projectile/feu esprit sain.png",
    "Medaille_de_bapteme":   "Images/Armes_items/projectile/proj_medaille.png",
    "Coiffe_de_rameau":      "Images/Armes_items/projectile/proj_couronne.png",
    "Lance_sacree":          "Images/Armes_items/projectile/proj_lance.png",
    "Aura_divine":           "Images/Armes_items/projectile/aura divine.png",
    "JALAMBAYA": {
        "path":    "Images/Armes_items/projectile/proj_jalambaya.png",
        "cols":    13, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
}

# Image de fallback si l'arme n'a pas de projectile défini
_FALLBACK_PATH = "Images/Armes_items/projectile/feu esprit sain.png"


def _charger_image_projectile(nom_arme: str):
    """
    Charge et retourne (image_ou_frames, est_anime).
    Centralisé ici pour éviter la duplication entre Projectile et sous-classes.
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

    # Chemin simple (str)
    img = pyg.image.load(image_data).convert_alpha()
    return pyg.transform.scale(img, (30, 30)), False


class Projectile(pyg.sprite.Sprite):
    """
    Paramètre `nom_arme` (str) : le nom de l'arme qui tire CE projectile.
    Toujours le passer explicitement depuis ArmeBase.tirer().
    Ne jamais se fier à player.arme_active.
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

        # ── Résolution du nom d'arme ──────────────────────────────────────
        # On utilise le paramètre en priorité, jamais arme_active seul.
        if nom_arme is None:
            # Fallback de sécurité : prendre l'arme active actuelle
            if player.armes:
                nom_arme = player.armes[player.arme_active].nom
            else:
                nom_arme = ""
        self.nom_arme = nom_arme

        # ── Chargement image / animation ──────────────────────────────────
        result, self.anime = _charger_image_projectile(nom_arme)

        if self.anime:
            self.anim        = result
            self.anim_index  = 0
            self.anim_timer  = 0
            self.anim_speed  = 6
            self.image       = self.anim[0]
        else:
            self.image = result

        # ── Position et direction ─────────────────────────────────────────
        self.rect    = self.image.get_rect(center=player.pos.center)
        dx, dy       = player.get_direction()
        self.dx      = float(dx)
        self.dy      = float(dy)

    # ── Helpers ───────────────────────────────────────────────────────────

    def set_direction(self, angle: float):
        rad      = math.radians(angle)
        self.dx  = math.cos(rad)
        self.dy  = math.sin(rad)
        length   = math.hypot(self.dx, self.dy)
        if length:
            self.dx /= length
            self.dy /= length

    # ── Update / Draw ─────────────────────────────────────────────────────

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
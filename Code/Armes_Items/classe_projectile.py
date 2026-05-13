"""
classe_projectile.py :
Projectiles tirés par les armes — chargement d'images statiques ou animées,
déplacement, détection de sortie d'écran et application des dégâts aux ennemis
"""

import math
import pygame as pyg

from Fichiers_variables.traitement_images import decouper_image

# catalogue des images de projectiles par arme 
PROJECTILES = {
    "Epee_enflammee": {
        "path":    "Images/Armes_items/Epee enflamee.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Epee_bleue" :  
        "Images/Armes_items/epee_bleue_img.png",
    
    "Pistolets":            "Images/Armes_items/projectile/proj_pistolet.png",
    "Ticket_de_metro":      "Images/Armes_items/projectile/proj_ticket.png",

    
    "Faux_cils":            "Images/Armes_items/projectile/proj_faux_cils.png",
    "Faux_ongles_roses":    "Images/Armes_items/projectile/proj_ongles.png",
    "Bracelet_de_sa_soeur": {
        "path":    "Images/Armes_items/projectile/proj_bracelet.png",
        "cols":    7, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
   
    "Pass_Navigo":          "Images/Armes_items/projectile/proj_ticket.png",
    "Highlighter":          "Images/Armes_items/projectile/proj_highliter.png",

    # Nonne 
    "Croix_marron": {
        "path":    "Images/Armes_items/projectile/proj_croix.png",
        "cols":    4, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
    "Feu_de_l'Esprit_Saint": "Images/Armes_items/projectile/feu esprit sain.png",
    "Medaille_de_bapteme":   "Images/Armes_items/projectile/proj_medaille.png",
    
    "Lance_sacree":          "Images/Armes_items/projectile/proj_lance.png",
    
    "JALAMBAYA": {
        "path":    "Images/Armes_items/projectile/proj_jalambaya.png",
        "cols":    13, "rows": 1, "enlever": 0, "taille": (30, 30)
    },
}

_FALLBACK_PATH = "Images/Armes_items/projectile/feu esprit sain.png"


def _charger_image_projectile(nom_arme: str):
    """Charge l'image ou les frames d'animation du projectile pour une arme donnée

    Retourne une image statique si l'arme utilise un simple PNG,
    une liste de frames si elle utilise un spritesheet animé.
    Utilise une image de secours si l'arme est absente du catalogue.

    Parameters
    ----------
    nom_arme : str
        Nom de l'arme dont on charge le projectile

    Returns
    -------
    tuple(pygame.Surface | list[pygame.Surface], bool)
        (image_ou_frames, est_anime) — est_anime vaut True si c'est une liste de frames
    """
    image_data = PROJECTILES.get(nom_arme)

    if image_data is None:
        # Arme absente du catalogue → image de secours
        img = pyg.image.load(_FALLBACK_PATH).convert_alpha()
        return pyg.transform.scale(img, (30, 30)), False

    if isinstance(image_data, dict):
        # Spritesheet animé : découpage en frames
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

    # Image statique simple
    img = pyg.image.load(image_data).convert_alpha()
    return pyg.transform.scale(img, (30, 30)), False


class Projectile(pyg.sprite.Sprite):
    """
    Class Projectile :
    Projectile tiré par une arme — se déplace en ligne droite,
    supporte les animations, le piercing et les effets à l'impact
    """

    def __init__(self, player, proj_type: str = "balle",
                 explode: bool = False, nom_arme: str = None):
        """Initialise le projectile depuis la position du joueur dans la direction visée

        Si nom_arme est None, l'arme active du joueur est utilisée.
        Toujours passer nom_arme explicitement depuis ArmeBase.tirer().

        Parameters
        ----------
        player : Player
            Le joueur qui tire le projectile
        proj_type : str, optional
            Type du projectile ("balle", "poison", etc.) (défaut "balle")
        explode : bool, optional
            True si le projectile déclenche une explosion à l'impact (défaut False)
        nom_arme : str, optional
            Nom de l'arme source pour charger la bonne image (défaut None)
        """
        super().__init__()
        self.player   = player
        self.type     = proj_type
        self.speed    = 7
        self.damage   = 10
        self.piercing = 1      # nombre d'ennemis traversables avant destruction
        self.explode  = explode
        self.anime    = False

        # Résolution du nom d'arme si non fourni
        if nom_arme is None:
            if player.armes:
                nom_arme = player.armes[player.arme_active].nom
            else:
                nom_arme = ""
        self.nom_arme = nom_arme

        result, self.anime = _charger_image_projectile(nom_arme)

        if self.anime:
            self.anim       = result
            self.anim_index = 0
            self.anim_timer = 0
            self.anim_speed = 6   # frames entre chaque changement d'image
            self.image      = self.anim[0]
        else:
            self.image = result

        self.rect = self.image.get_rect(center=player.pos.center)
        dx, dy    = player.get_direction()
        self.dx   = float(dx)
        self.dy   = float(dy)

    def set_direction(self, angle: float):
        """Définit la direction du projectile à partir d'un angle en degrés

        Parameters
        ----------
        angle : float
            Angle en degrés (0° = droite, sens horaire)
        """
        rad     = math.radians(angle)
        self.dx = math.cos(rad)
        self.dy = math.sin(rad)
        length  = math.hypot(self.dx, self.dy)
        if length:
            self.dx /= length
            self.dy /= length

    def update(self):
        """Met à jour la position et l'animation du projectile à chaque frame

        Avance selon la direction et la vitesse, anime le sprite si nécessaire,
        et supprime le projectile s'il sort des limites de l'écran.
        """
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
        """Supprime le projectile s'il sort du rectangle 1920x1080"""
        if (self.rect.right  < 0    or self.rect.left > 1920 or
                self.rect.bottom < 0 or self.rect.top  > 1080):
            self.kill()

    def hit(self, enemy):
        """Applique les dégâts à un ennemi et détruit le projectile si le piercing est épuisé

        Parameters
        ----------
        enemy : Enemy
            L'ennemi touché par le projectile
        """
        enemy.degats(self.damage)
        self.piercing -= 1
        if self.piercing <= 0:
            self.kill()


class ProjectilePoison(Projectile):
    """
    Class ProjectilePoison :
    Projectile qui applique un effet de poison sur les ennemis touchés
    """

    def __init__(self, player, nom_arme: str = None):
        """Initialise un projectile poison avec ses paramètres de dégâts sur la durée

        Parameters
        ----------
        player : Player
            Le joueur qui tire le projectile
        nom_arme : str, optional
            Nom de l'arme source (défaut None)
        """
        super().__init__(player, proj_type="poison", nom_arme=nom_arme)
        self.poison        = True
        self.duree_poison  = 180   # durée du poison en frames 
        self.degats_poison = 2     # dégâts par tick
        self.tick          = 30    # intervalle entre deux ticks en frames
"Code des Explosions"

import pygame as pyg

def charger_explosion(path, cols, rows, nb_a_enlever=0, taille=None):
    """
    Charge une sprite sheet d'explosion et la découpe en frames.

    Args:
        path (str): chemin vers l'image de la sprite sheet
        cols (int): nombre de colonnes dans la sprite sheet
        rows (int): nombre de lignes dans la sprite sheet
        nb_a_enlever (int, optional): nombre de frames à retirer à la fin
        taille (tuple, optional): taille (width, height) pour redimensionner chaque frame

    Returns:
        list: liste des surfaces pygame correspondant aux frames de l'animation
    """
    image = pyg.image.load(path).convert_alpha()
    sheet_w, sheet_h = image.get_size()
    width = sheet_w // cols
    height = sheet_h // rows

    tableau_images = [
        [image.subsurface((x * width, y * height, width, height)) for x in range(cols)]
        for y in range(rows)
    ]

    frames = []
    for ligne in tableau_images:
        frames += ligne

    for i in range(nb_a_enlever):
        frames.pop(-1)

    if taille:
        frames = [pyg.transform.scale(f, taille) for f in frames]

    return frames


class Explosion:
    """
    Gère une animation d'explosion avec dégâts.

    Attributes:
        frames (list): frames de l'animation (chargées une seule fois)
        index (int): frame actuelle
        x_monde (int): position x dans le monde
        y_monde (int): position y dans le monde
        player (Player): référence au joueur (pour la caméra)
        rect (pygame.Rect): rectangle d'affichage
        timer (int): compteur pour gérer la vitesse d'animation
        frame_speed (int): temps entre chaque frame (ms)
        degats (int): dégâts infligés par l'explosion
        a_fait_degats (bool): indique si les dégâts ont déjà été appliqués
    """

    frames = None  # chargé une seule fois via init_frames()

    @classmethod
    def init_frames(cls):
        """
        Initialise les frames de l'explosion (appelée une seule fois).
        """
        cls.frames = charger_explosion(
            "Images/Armes_items/projectile/explosion.png",
            cols=14,
            rows=1,
            nb_a_enlever=0,
            taille=(100, 100)
        )

    def __init__(self, x_monde, y_monde, player, degats=30):
        """
        Initialise une explosion.

        Args:
            x_monde (int): position x dans le monde
            y_monde (int): position y dans le monde
            player (Player): joueur pour le calcul caméra
            degats (int, optional): dégâts infligés
        """
        self.index = 0
        self.x_monde = x_monde
        self.y_monde = y_monde
        self.player = player
        self.rect = self.frames[0].get_rect()
        self.timer = 0
        self.frame_speed = 80
        self.degats = degats
        self.a_fait_degats = False

    def update(self, dt):
        """
        Met à jour la position écran et l'animation.

        Args:
            dt (int): temps écoulé depuis la dernière frame (ms)
        """
        from Affichage.fonctionnement_divers import camera

        sx, sy = camera(self.x_monde, self.y_monde, self.player)
        self.rect.center = (sx, sy)

        self.timer += dt
        if self.timer >= self.frame_speed:
            self.index += 1
            self.timer = 0

    def draw(self, surface):
        """
        Dessine l'explosion sur l'écran.

        Args:
            surface (pygame.Surface): surface d'affichage
        """
        if self.index < len(self.frames):
            surface.blit(self.frames[self.index], self.rect)

    def finished(self):
        """
        Indique si l'animation est terminée.

        Returns:
            bool: True si toutes les frames ont été jouées
        """
        return self.index >= len(self.frames)
    
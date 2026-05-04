import pygame as pyg

def charger_explosion(path, cols, rows, nb_a_enlever=0, taille=None):
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
    frames = None  # chargé une seule fois via init_frames()

    @classmethod
    def init_frames(cls):
        cls.frames = charger_explosion(
                "Images/Armes_items/projectile/explosion.png",
                cols=14,   # ← 14 colonnes
                rows=1,    # ← 1 ligne
                nb_a_enlever=0,  # ← 14 frames, rien à enlever
                taille=(100, 100))

    def __init__(self, x_monde, y_monde, player, degats=30):
        self.index = 0
        self.x_monde = x_monde
        self.y_monde = y_monde
        self.player = player  # ← nécessaire pour la caméra
        self.rect = self.frames[0].get_rect()
        self.timer = 0
        self.frame_speed = 80
        self.degats = degats
        self.a_fait_degats = False
    def update(self, dt):
        from Affichage.fonctionnement_divers import camera
        sx, sy = camera(self.x_monde, self.y_monde, self.player)
        self.rect.center = (sx, sy)  # ← recalcul écran chaque frame

        self.timer += dt
        if self.timer >= self.frame_speed:
            self.index += 1
            self.timer = 0
    
    def draw(self, surface):
        if self.index < len(self.frames):
            surface.blit(self.frames[self.index], self.rect)

    def finished(self):
        return self.index >= len(self.frames)
    
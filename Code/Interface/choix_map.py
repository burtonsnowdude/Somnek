"""
Choix de la map — SOMNEK
Affiche les 5 maps. Les maps non débloquées sont grisées 
et ne sont pas cliquables.
"""

import pygame
from Fichiers_variables.variables import WIDTH, HEIGHT, WIN
from Fichiers_variables.progression import (
    ORDRE_MAPS, maps_debloquees, temps_limite
)
from Interface.Class_Button import Button

pygame.init()

try:
    FONT_TITRE = pygame.font.Font("assets/pixels.ttf", 36)
except Exception:
    FONT_TITRE = pygame.font.SysFont("Impact", 44, bold=True)

try:
    FONT_NOM = pygame.font.Font("assets/pixels.ttf", 16)
except Exception:
    FONT_NOM = pygame.font.SysFont(None, 28)

try:
    FONT_INFO = pygame.font.Font("assets/pixels.ttf", 12)
except Exception:
    FONT_INFO = pygame.font.SysFont(None, 22)

FONT_BUTTON = pygame.font.SysFont(None, 24)


VIOLET_FONCE = (45,  20,  65)
OR_CLAIR     = (255, 215, 100)
BLANC        = (255, 255, 255)
GRIS         = (90,   90,  95)


# ─────────────────────────────────────────────
#  IMAGES DES MAPS (avec fallback couleur)
# ─────────────────────────────────────────────

def _try_load(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except Exception:
        # Fallback : carré coloré uni
        s = pygame.Surface(size)
        s.fill((70, 50, 90))
        return s


CARTE_W, CARTE_H = 180, 110

IMAGES_MAPS = {
    "Cour":   _try_load("Images/Interface/img_map_cour.png",   (CARTE_W, CARTE_H)),
    "Rue":    _try_load("Images/Interface/img_map_rue.png",    (CARTE_W, CARTE_H)),
    "Ruelle": _try_load("Images/Interface/img_map_ruelle.png", (CARTE_W, CARTE_H)),
    "Foire":  _try_load("Images/Interface/img_map_foire.png",  (CARTE_W, CARTE_H)),
    "Metro":  _try_load("Images/Interface/img_map_metro.png",  (CARTE_W, CARTE_H)),
}


# ─────────────────────────────────────────────
#  CADENAS
# ─────────────────────────────────────────────

def draw_lock(surface, rect):
    cx, cy = rect.center
    body = pygame.Rect(cx - 16, cy - 5, 32, 24)
    pygame.draw.rect(surface, (40, 40, 40), body, border_radius=4)
    pygame.draw.rect(surface, OR_CLAIR,     body, 2, border_radius=4)
    pygame.draw.arc(surface, OR_CLAIR,
                    (cx - 12, cy - 22, 24, 22), 0, 3.14, 4)


def img_grisee(img):
    s = img.copy()
    s.fill((50, 50, 60), special_flags=pygame.BLEND_RGB_MULT)
    return s


# ─────────────────────────────────────────────
#  CARTE D'UNE MAP
# ─────────────────────────────────────────────

class CarteMap:
    def __init__(self, nom, x, y):
        self.nom      = nom
        self.rect     = pygame.Rect(x, y, CARTE_W, CARTE_H + 30)
        self.img_rect = pygame.Rect(x, y, CARTE_W, CARTE_H)
        self.base_img = IMAGES_MAPS.get(nom)
        self.unlocked = False
        self.hovered  = False

    def refresh_unlock(self, debloquees):
        self.unlocked = self.nom in debloquees

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos) and self.unlocked

    def is_clicked(self, events):
        if not self.unlocked:
            return False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def draw(self, surface):
        # Image (grisée si verrouillée)
        img = self.base_img if self.unlocked else img_grisee(self.base_img)
        surface.blit(img, self.img_rect)

        # Bordure
        couleur_bord = BLANC if self.unlocked else GRIS
        pygame.draw.rect(surface, couleur_bord, self.img_rect, 2)

        # Nom + temps
        nom_txt = FONT_NOM.render(self.nom, True, BLANC if self.unlocked else GRIS)
        surface.blit(nom_txt,
                     nom_txt.get_rect(center=(self.rect.centerx, self.rect.bottom - 18)))

        if self.unlocked:
            temps_min = temps_limite(self.nom) // 60
            t_txt = FONT_INFO.render(f"{temps_min} min", True, OR_CLAIR)
            surface.blit(t_txt, t_txt.get_rect(midright=(self.img_rect.right - 6,
                                                          self.img_rect.bottom - 12)))


# ─────────────────────────────────────────────
#  ENTRÉE PRINCIPALE
# ─────────────────────────────────────────────

def open_choix_map(joueur: str):
    """
    Affiche un écran plein-écran de sélection de map. Bloque jusqu'à choix.
    Retourne le nom de la map choisie, ou None si l'utilisateur annule (Echap).
    """
    clock = pygame.time.Clock()

    # Crée les cartes en grille (3 + 2)
    margin_x = 30
    margin_y = 150
    espace_x = (WIDTH - 3 * CARTE_W - 2 * margin_x) // 2
    espace_y = 50
    cartes   = []
    for i, nom in enumerate(ORDRE_MAPS):
        col = i % 3
        row = i // 3
        x = margin_x + col * (CARTE_W + espace_x)
        y = margin_y + row * (CARTE_H + 30 + espace_y)
        cartes.append(CarteMap(nom, x, y))

    btn_retour = Button("RETOUR", "back",
                        WIDTH // 2 - 80, HEIGHT - 70,
                        160, 50, FONT_BUTTON)

    while True:
        clock.tick(60)
        mouse_pos     = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        events        = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

        # ─── Maj statut maps depuis le CSV ──────────────────────────────
        debloquees = maps_debloquees(joueur)
        for c in cartes:
            c.refresh_unlock(debloquees)
            c.update(mouse_pos)

        # ─── Détection clic ─────────────────────────────────────────────
        for c in cartes:
            if c.is_clicked(events):
                return c.nom

        # ─── Rendu ──────────────────────────────────────────────────────
        WIN.fill(VIOLET_FONCE)

        # Titre
        titre = FONT_TITRE.render("CHOISIS TA MAP", True, BLANC)
        WIN.blit(titre, titre.get_rect(center=(WIDTH // 2, 70)))

        # Cartes
        for c in cartes:
            c.draw(WIN)

        # Bouton retour
        btn_retour.draw(WIN, mouse_pos)
        if btn_retour.is_clicked(mouse_pos, mouse_pressed):
            return None

        pygame.display.flip()
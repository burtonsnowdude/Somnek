"""
Écran de victoire — affiché quand le joueur termine une map.
Annonce les déblocages (nouvelle map / nouveau perso).
"""

import pygame as pyg
from Fichiers_variables.variables import *

try:
    FONT_TITRE = pyg.font.Font("assets/pixels.ttf", 48)
except Exception:
    FONT_TITRE = pyg.font.SysFont("Impact", 56, bold=True)

try:
    FONT_SOUS = pyg.font.Font("assets/pixels.ttf", 18)
except Exception:
    FONT_SOUS = pyg.font.SysFont(None, 30)

try:
    FONT_INFO = pyg.font.Font("assets/pixels.ttf", 14)
except Exception:
    FONT_INFO = pyg.font.SysFont(None, 24)


VIOLET_FONCE = (45,  20,  65)
OR_CLAIR     = (255, 215, 100)
BLANC        = (255, 255, 255)


# ─────────────────────────────────────────────
#  IMAGE TITRE VICTOIRE
# ─────────────────────────────────────────────

try:
    IMG_VICTOIRE = pyg.image.load("Images/Interface/victoire.png").convert_alpha()
    # Adapte la taille (max 500px de large)
    iw, ih = IMG_VICTOIRE.get_size()
    if iw > 500:
        ratio = 500 / iw
        IMG_VICTOIRE = pyg.transform.smoothscale(
            IMG_VICTOIRE, (int(iw * ratio), int(ih * ratio))
        )
except Exception:
    IMG_VICTOIRE = None    # fallback sur le texte si l'image n'existe pas


def victoire(map_terminee_nom: str,
              nouvelle_map: str = None,
              nouveau_perso: str = None) -> str:
    """
    Affiche l'écran de victoire en plein écran.
    Retourne 'menu' ou 'quit' selon le choix du joueur.
    """
    clock   = pyg.time.Clock()
    running = True

    overlay = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    overlay.fill((*VIOLET_FONCE, 230))

    btn_w, btn_h = 220, 60
    btn_menu = pyg.Rect(CENTREx - btn_w - 20, HEIGHT - 130, btn_w, btn_h)
    btn_quit = pyg.Rect(CENTREx + 20,         HEIGHT - 130, btn_w, btn_h)

    while running:
        clock.tick(60)
        mouse_pos = pyg.mouse.get_pos()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "quit"
            if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                if btn_menu.collidepoint(event.pos):
                    return "menu"
                if btn_quit.collidepoint(event.pos):
                    return "quit"
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_RETURN or event.key == pyg.K_ESCAPE:
                    return "menu"

        # ─── Rendu ───────────────────────────────────────────────────────
        WIN.blit(overlay, (0, 0))

        # Image VICTOIRE (ou texte si image absente)
        if IMG_VICTOIRE is not None:
            rect = IMG_VICTOIRE.get_rect(center=(CENTREx, 150))
            WIN.blit(IMG_VICTOIRE, rect)
        else:
            titre = FONT_TITRE.render("VICTOIRE", True, OR_CLAIR)
            WIN.blit(titre, titre.get_rect(center=(CENTREx, 130)))

        # Map terminée
        sous = FONT_SOUS.render(
            f"Map terminee : {map_terminee_nom}", True, BLANC
        )
        WIN.blit(sous, sous.get_rect(center=(CENTREx, 270)))

        # Annonces de déblocage
        y = 340
        if nouvelle_map:
            txt = FONT_INFO.render(
                f"Nouvelle map debloquee : {nouvelle_map}", True, OR_CLAIR
            )
            WIN.blit(txt, txt.get_rect(center=(CENTREx, y)))
            y += 40

        if nouveau_perso:
            txt = FONT_INFO.render(
                f"Nouveau personnage : {nouveau_perso}", True, OR_CLAIR
            )
            WIN.blit(txt, txt.get_rect(center=(CENTREx, y)))
            y += 40

        if not nouvelle_map and not nouveau_perso:
            txt = FONT_INFO.render(
                "Tu as tout debloque, bravo !", True, OR_CLAIR
            )
            WIN.blit(txt, txt.get_rect(center=(CENTREx, y)))

        # Boutons
        for rect, label in [(btn_menu, "MENU"), (btn_quit, "QUITTER")]:
            hover = rect.collidepoint(mouse_pos)
            color = OR_CLAIR if hover else (180, 140, 70)
            pyg.draw.rect(WIN, color,        rect, border_radius=8)
            pyg.draw.rect(WIN, VIOLET_FONCE, rect, 3, border_radius=8)
            t = FONT_SOUS.render(label, True, VIOLET_FONCE)
            WIN.blit(t, t.get_rect(center=rect.center))

        pyg.display.flip()
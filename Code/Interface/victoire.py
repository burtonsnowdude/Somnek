"""
victoire.py :
Écran de victoire ,
avec le titre VICTOIRE, un tableau de statistiques et des boutons de navigation
"""

import pygame as pyg
from Fichiers_variables.variables import WIDTH, HEIGHT, WIN, CENTREx, CENTREy



try:
    FONT_TITRE  = pyg.font.Font("assets/pixels.ttf", 52)
    FONT_LABEL  = pyg.font.Font("assets/pixels.ttf", 13)
    FONT_VALEUR = pyg.font.Font("assets/pixels.ttf", 18)
    FONT_BTN    = pyg.font.Font("assets/pixels.ttf", 14)
    FONT_UNLOCK = pyg.font.Font("assets/pixels.ttf", 12)
except Exception:
    FONT_TITRE  = pyg.font.SysFont("Impact",  64, bold=True)
    FONT_LABEL  = pyg.font.SysFont(None, 22)
    FONT_VALEUR = pyg.font.SysFont(None, 30)
    FONT_BTN    = pyg.font.SysFont(None, 26)
    FONT_UNLOCK = pyg.font.SysFont(None, 20)


OR          = (255, 215,  80)
OR_FONCE    = (200, 160,  40)
BLANC       = (255, 255, 255)
GRIS_CLAIR  = (200, 200, 210)
VIOLET_BTN  = ( 70,  30, 100)
VIOLET_HOV  = (110,  50, 150)
VIOLET_BORD = (140,  80, 200)
NOIR_SEMI   = ( 10,   5,  20, 180)
TABLEAU_BG  = ( 20,   8,  35, 200)
LIGNE_SEP   = ( 90,  50, 130)


try:
    _img = pyg.image.load("Images/Interface/victoire.png").convert_alpha()
    iw, ih = _img.get_size()
    if iw > 420:
        ratio = 420 / iw
        _img  = pyg.transform.smoothscale(_img, (int(iw * ratio), int(ih * ratio)))
    IMG_VICTOIRE = _img
except Exception:
    IMG_VICTOIRE = None   # fallback texte si l'image est absente


def _fmt_temps(secondes):
    """Formate un nombre de secondes en chaîne MM:SS

    Parameters
    ----------
    secondes : float
        Durée à formater

    Returns
    -------
    str
        Durée formatée sous la forme "MM:SS"
    """
    m = int(secondes) // 60
    s = int(secondes) % 60
    return f"{m:02d}:{s:02d}"


def _draw_panel(surface, rect, bg_color, border_color, radius=10):
    """Dessine un panneau arrondi semi-transparent sur une surface

    Parameters
    ----------
    surface : pygame.Surface
        Surface de destination
    rect : pygame.Rect
        Position et dimensions du panneau
    bg_color : tuple
        Couleur de fond RGBA
    border_color : tuple
        Couleur de la bordure RGB ou RGBA
    radius : int, optional
        Rayon des coins arrondis (défaut 10)
    """
    panel = pyg.Surface((rect.width, rect.height), pyg.SRCALPHA)
    pyg.draw.rect(panel, bg_color,    (0, 0, rect.width, rect.height), border_radius=radius)
    pyg.draw.rect(panel, border_color, (0, 0, rect.width, rect.height), 2, border_radius=radius)
    surface.blit(panel, rect.topleft)


def _draw_button(surface, rect, label, hovered):
    """Dessine un bouton violet avec effet de survol doré

    Parameters
    ----------
    surface : pygame.Surface
        Surface de destination
    rect : pygame.Rect
        Position et dimensions du bouton
    label : str
        Texte affiché sur le bouton
    hovered : bool
        True pour appliquer le style de survol (fond plus clair, texte doré)
    """
    color = VIOLET_HOV if hovered else VIOLET_BTN
    _draw_panel(surface, rect, (*color, 230), VIOLET_BORD, radius=8)
    txt = FONT_BTN.render(label, True, OR if hovered else BLANC)
    surface.blit(txt, txt.get_rect(center=rect.center))


def victoire(
    map_terminee_nom: str,
    nouvelle_map:  str   = None,
    nouveau_perso: str   = None,
    temps_survie:  float = 0,
    argent_recolte: int  = 0,
    monstres_tues:  int  = 0,
    armes_debloquees: int = 0,
) -> str:
    """Affiche l'écran de victoire par-dessus le dernier frame du jeu

    Présente un tableau de statistiques avec animation d'entrée,
    les éventuels déblocages (map/personnage) et deux boutons de navigation.

    Parameters
    ----------
    map_terminee_nom : str
        Nom de la map que le joueur vient de terminer
    nouvelle_map : str, optional
        Nom d'une nouvelle map débloquée (None si aucune)
    nouveau_perso : str, optional
        Nom d'un nouveau personnage débloqué (None si aucun)
    temps_survie : float, optional
        Durée de la partie en secondes (défaut 0)
    argent_recolte : int, optional
        Argent total ramassé durant la partie (défaut 0)
    monstres_tues : int, optional
        Nombre de monstres éliminés, correspond à p.kill_count (défaut 0)
    armes_debloquees : int, optional
        Nombre d'armes/items possédés, correspond à len(armes_et_items_possedees) (défaut 0)

    Returns
    -------
    str
        "menu" pour retourner au menu principal, "quit" pour quitter le jeu
    """
    clock = pyg.time.Clock()

    # capture le dernier frame du jeu comme fond de l'écran de victoire
    fond_jeu = WIN.copy()

    
    overlay = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    overlay.fill((30, 10, 55, 175))

    # données du tableau de statistiques
    stats = [
        ("TEMPS DE SURVIE",    _fmt_temps(temps_survie)),
        ("ARGENT RECOLTE",     f"{argent_recolte} $"),
        ("MONSTRES TUES",      str(monstres_tues)),
        ("ARMES / ITEMS",      str(armes_debloquees)),
    ]

    # calcul des dimensions et positions
    TABLEAU_W  = 420
    LIGNE_H    = 52
    TITRE_H    = 90    # hauteur réservée au titre dans le panneau
    UNLOCK_H   = 50 if (nouvelle_map or nouveau_perso) else 0
    TABLEAU_H  = TITRE_H + len(stats) * LIGNE_H + UNLOCK_H + 20

    tableau_rect = pyg.Rect(
        CENTREx - TABLEAU_W // 2,
        CENTREy - TABLEAU_H // 2 - 30,
        TABLEAU_W,
        TABLEAU_H,
    )

    BTN_W, BTN_H = 180, 48
    btn_menu = pyg.Rect(CENTREx - BTN_W - 16, tableau_rect.bottom + 20, BTN_W, BTN_H)
    btn_quit = pyg.Rect(CENTREx + 16,         tableau_rect.bottom + 20, BTN_W, BTN_H)

    # animation 
    ANIM_FRAMES = 22
    for frame in range(ANIM_FRAMES + 1):
        t = frame / ANIM_FRAMES
        ease = 1 - (1 - t) ** 3          # ease-out cubique
        offset_y = int((1 - ease) * (-HEIGHT // 2))

        WIN.blit(fond_jeu, (0, 0))

        # Overlay dont l'opacité augmente progressivement
        ov_alpha = int(175 * ease)
        ov_tmp = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        ov_tmp.fill((30, 10, 55, ov_alpha))
        WIN.blit(ov_tmp, (0, 0))

        # Panneau décalé vers le haut pendant l'animation
        tr = tableau_rect.move(0, offset_y)
        _draw_panel(WIN, tr, TABLEAU_BG, VIOLET_BORD, radius=12)

        pyg.display.flip()
        clock.tick(60)

    # boucle principale
    while True:
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
                if event.key in (pyg.K_RETURN, pyg.K_ESCAPE):
                    return "menu"

        
        WIN.blit(fond_jeu, (0, 0))
        WIN.blit(overlay, (0, 0))

        # panneau principal
        _draw_panel(WIN, tableau_rect, TABLEAU_BG, VIOLET_BORD, radius=12)

        # Titre 
        if IMG_VICTOIRE is not None:
            ir = IMG_VICTOIRE.get_rect(center=(CENTREx, tableau_rect.top + 45))
            WIN.blit(IMG_VICTOIRE, ir)
        else:
            titre_surf = FONT_TITRE.render("VICTOIRE !", True, OR)
            WIN.blit(titre_surf, titre_surf.get_rect(center=(CENTREx, tableau_rect.top + 48)))

       
        sep_y = tableau_rect.top + TITRE_H - 6
        pyg.draw.line(WIN, LIGNE_SEP,
                      (tableau_rect.left + 20,  sep_y),
                      (tableau_rect.right - 20, sep_y), 1)

        for i, (label, valeur) in enumerate(stats):
            row_y = sep_y + 10 + i * LIGNE_H

            # Fond alterné légèrement plus clair sur les lignes paires
            if i % 2 == 0:
                row_rect = pyg.Rect(tableau_rect.left + 4, row_y + 2,
                                    tableau_rect.width - 8, LIGNE_H - 4)
                row_bg = pyg.Surface((row_rect.width, row_rect.height), pyg.SRCALPHA)
                row_bg.fill((255, 255, 255, 12))
                WIN.blit(row_bg, row_rect.topleft)

            #label à gauche
            lbl = FONT_LABEL.render(label, True, GRIS_CLAIR)
            WIN.blit(lbl, (tableau_rect.left + 22, row_y + LIGNE_H // 2 - lbl.get_height() // 2))

           
            val = FONT_VALEUR.render(valeur, True, OR)
            WIN.blit(val, val.get_rect(midright=(tableau_rect.right - 22,
                                                  row_y + LIGNE_H // 2)))

            # séparateur entre lignes 
            if i < len(stats) - 1:
                ly = row_y + LIGNE_H - 1
                pyg.draw.line(WIN, LIGNE_SEP,
                              (tableau_rect.left + 20,  ly),
                              (tableau_rect.right - 20, ly), 1)

        # section éblocages ouvelle map et nouveau personnage
        if nouvelle_map or nouveau_perso:
            unlock_y = sep_y + 10 + len(stats) * LIGNE_H + 8
            pyg.draw.line(WIN, LIGNE_SEP,
                          (tableau_rect.left + 20,  unlock_y),
                          (tableau_rect.right - 20, unlock_y), 1)
            unlock_y += 10
            if nouvelle_map:
                t = FONT_UNLOCK.render(f"Nouvelle map débloquée : {nouvelle_map}", True, OR)
                WIN.blit(t, t.get_rect(center=(CENTREx, unlock_y)))
                unlock_y += 22
            if nouveau_perso:
                t = FONT_UNLOCK.render(f"Nouveau personnage : {nouveau_perso}", True, OR)
                WIN.blit(t, t.get_rect(center=(CENTREx, unlock_y)))

        #boutons de navigation
        _draw_button(WIN, btn_menu, "MENU PRINCIPAL", btn_menu.collidepoint(mouse_pos))
        _draw_button(WIN, btn_quit, "QUITTER",         btn_quit.collidepoint(mouse_pos))

        pyg.display.flip()
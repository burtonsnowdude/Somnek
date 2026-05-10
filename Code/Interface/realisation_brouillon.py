import pygame
import Interface.pygameui as pygameui
from Fichiers_variables.variables import *
from Fichiers_variables.gestion_fichiers import contenu_fichier_quetes

# ─────────────────────────────────────────────
#  DÉFINITION DES QUÊTES
# ─────────────────────────────────────────────

QUETES = {
    "histoire": {
        "scene1": [
            "trouver quelqu'un",
            "survie aux vagues de creatures",
            "inspecte le livre mysterieux",
            "cherche l'exterieur",
        ],
        "scene2": ["trouve ton (objet spécial)", "survie aux vagues de créatures"],
        "scene3": [],
        "scene4": [],
        "scene5": [
            "Elimine (nom de boss)",
            "rentre chez toi",
            "sauve le civil",
            "survie aux monstres",
            "entre dans le metro",
        ],
        "scene6": ["élimine les monstres", "prend le metro"],
        "scene7": ["tue (nom du boss)"],
    },
    "kill": {
        10: "tue 10 ennemis",
        20: "tue 20 ennemis",
        50: "tue 50 ennemis",
        100: "tue 100 ennemis",
        500: "tue 500 ennemis",
        1000: "tue 1000 ennemis",
        5000: "tue 5000 ennemis",
        10000: "tue 10000 ennemis",
    },
    "aquerir": [
        "aquerir ton premier arme",
        "aquerir 5 armes",
        "aquerir 10 armes",
        "aquerir 20 armes",
        "aquerir 50 armes",
        "aquerir 100 armes",
        "aquerir 200 armes",
        "aquerir 500 armes",
    ],
}


def verif_q(nb_armes):
    if   nb_armes >= 500: return QUETES["aquerir"][7]
    elif nb_armes >= 200: return QUETES["aquerir"][6]
    elif nb_armes >= 100: return QUETES["aquerir"][5]
    elif nb_armes >= 50:  return QUETES["aquerir"][4]
    elif nb_armes >= 20:  return QUETES["aquerir"][3]
    elif nb_armes >= 10:  return QUETES["aquerir"][2]
    elif nb_armes >= 5:   return QUETES["aquerir"][1]
    elif nb_armes >= 1:   return QUETES["aquerir"][0]
    return False


def verif_k(p):
    n = p.kill_count
    if n == 10:    return QUETES["kill"][10]
    if n == 20:    return QUETES["kill"][20]
    if n == 50:    return QUETES["kill"][50]
    if n == 100:   return QUETES["kill"][100]
    if n == 500:   return QUETES["kill"][500]
    if n == 1000:  return QUETES["kill"][1000]
    if n == 5000:  return QUETES["kill"][5000]
    if n == 10000: return QUETES["kill"][10000]
    return False


# ─────────────────────────────────────────────
#  ÉTAT DES QUÊTES (lecture CSV)
# ─────────────────────────────────────────────

def quete_realisee(joueur_nom: str, quete_id: str) -> bool:
    try:
        contenu = contenu_fichier_quetes()
        for row in contenu:
            if row.get("Type") == quete_id:
                return str(row.get(joueur_nom, "0")) == "1"
    except Exception as e:
        print(f"[Quetes] Lecture impossible : {e}")
    return False


# ─────────────────────────────────────────────
#  PARAMÈTRES VISUELS
# ─────────────────────────────────────────────

fond     = (245, 245, 235)
croix    = (220,  40,  50)
blanc    = (255, 255, 255)
or_clair = (255, 215, 100)

POPUP_W, POPUP_H = 500, 500
HEADER_H = 90                # Zone titre sticky
POPUP_X  = (WIDTH  - POPUP_W) // 2
POPUP_Y  = (HEIGHT - POPUP_H) // 2

fond_realisation_full = pygame.image.load("Images/Interface/fond_realisation.png")

# Police titre — Press Start 2P si dispo, sinon fallback stylé
try:
    FONT_TITRE = pygame.font.Font("assets/pixels.ttf", 38)
except Exception:
    FONT_TITRE = pygame.font.SysFont("Impact", 44, bold=True)

try:
    FONT_SCORE = pygame.font.Font("assets/pixels.ttf", 16)
except Exception:
    FONT_SCORE = pygame.font.SysFont(None, 28)


def draw_title(surface, text, center_x, center_y):
    """Titre simple avec la police pixel."""
    texte = FONT_TITRE.render(text, True, blanc)
    texte_rect = texte.get_rect(center=(center_x, center_y))
    surface.blit(texte, texte_rect)


# ─────────────────────────────────────────────
#  SCROLLBAR CUSTOM (coords écran absolues)
# ─────────────────────────────────────────────

class ScrollBar:
    def __init__(self, x_local: int, y_local: int,
                 width: int, height: int,
                 content_height: int, view_height: int):
        self.x_local        = x_local
        self.y_local        = y_local
        self.width          = width
        self.height         = height
        self.content_height = content_height
        self.view_height    = view_height
        self.offset         = 0.0
        self._dragging      = False
        self._drag_offset_y = 0

    @property
    def max_offset(self) -> float:
        return max(0, self.content_height - self.view_height)

    @property
    def handle_height(self) -> int:
        if self.content_height <= self.view_height:
            return self.height
        h = int(self.height * self.view_height / self.content_height)
        return max(30, h)

    def track_rect_screen(self) -> pygame.Rect:
        return pygame.Rect(POPUP_X + self.x_local, POPUP_Y + self.y_local,
                           self.width, self.height)

    def handle_rect_screen(self) -> pygame.Rect:
        if self.max_offset == 0:
            handle_y = POPUP_Y + self.y_local
        else:
            ratio    = self.offset / self.max_offset
            handle_y = (POPUP_Y + self.y_local
                        + int(ratio * (self.height - self.handle_height)))
        return pygame.Rect(POPUP_X + self.x_local, handle_y,
                           self.width, self.handle_height)

    def track_rect_local(self) -> pygame.Rect:
        return pygame.Rect(self.x_local, self.y_local, self.width, self.height)

    def handle_rect_local(self) -> pygame.Rect:
        if self.max_offset == 0:
            return pygame.Rect(self.x_local, self.y_local,
                               self.width, self.handle_height)
        ratio = self.offset / self.max_offset
        y     = self.y_local + int(ratio * (self.height - self.handle_height))
        return pygame.Rect(self.x_local, y, self.width, self.handle_height)

    def _set_offset_from_screen_y(self, screen_y: int, drag_y_offset: int = 0):
        track_top = POPUP_Y + self.y_local
        target    = screen_y - drag_y_offset - track_top
        space     = self.height - self.handle_height
        if space <= 0:
            return
        ratio       = target / space
        self.offset = max(0, min(ratio * self.max_offset, self.max_offset))

    def update(self, events):
        popup_rect = pygame.Rect(POPUP_X, POPUP_Y, POPUP_W, POPUP_H)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.handle_rect_screen().collidepoint(event.pos):
                        self._dragging      = True
                        self._drag_offset_y = (event.pos[1]
                                                - self.handle_rect_screen().y)
                    elif self.track_rect_screen().collidepoint(event.pos):
                        self._set_offset_from_screen_y(
                            event.pos[1], self.handle_height // 2
                        )
                elif event.button == 4 and popup_rect.collidepoint(event.pos):
                    self.offset = max(0, self.offset - 40)
                elif event.button == 5 and popup_rect.collidepoint(event.pos):
                    self.offset = min(self.max_offset, self.offset + 40)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._dragging = False
            elif event.type == pygame.MOUSEMOTION and self._dragging:
                self._set_offset_from_screen_y(event.pos[1], self._drag_offset_y)

    def get_value(self) -> int:
        return int(self.offset)

    def draw_on_popup(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (215, 215, 210),
                         self.track_rect_local(), border_radius=6)
        pygame.draw.rect(surface, (180, 180, 175),
                         self.track_rect_local(), 1, border_radius=6)
        couleur = (90, 90, 90) if self._dragging else (130, 130, 130)
        pygame.draw.rect(surface, couleur,
                         self.handle_rect_local(), border_radius=6)


# ─────────────────────────────────────────────
#  CHECKBOX D'AFFICHAGE (lecture seule)
# ─────────────────────────────────────────────

class QuestCheckbox(pygameui.Checkbox):
    def __init__(self, x: int, y: int, taille: int, quete_id: str):
        super().__init__(
            position=(x, y), width=taille, height=taille,
            style="cross", color=croix, background_color=fond
        )
        self.disable()
        self.quete_id = quete_id

    def refresh(self, joueur_nom: str):
        self.set_checked(quete_realisee(joueur_nom, self.quete_id))


# ─────────────────────────────────────────────
#  CONFIGURATION DES QUÊTES
# ─────────────────────────────────────────────

QUETES_AFFICHEES = [
    ("Avoir retrouvé quelqu'un",       "trouver_quelquun"),
    ("Inspecter le livre mystérieux",  "inspecter_livre"),
    ("Trouver ton objet mystérieux",   "trouver_objet"),
    ("Éliminer le boss final",         "boss_final"),
    ("Entrer dans le métro",           "Entrer_metro"),
    ("Tuer 10 ennemis",                "kill_10"),
    ("Tuer 50 ennemis",                "kill_50"),
    ("Tuer 100 ennemis",               "kill_100"),
    ("Tuer 500 ennemis",               "kill_500"),
    ("Acquérir ta première arme",      "acquerir_1"),
    ("Acquérir 5 armes",               "acquerir_5"),
    ("Acquérir 10 armes",              "acquerir_10"),
    ("Acquérir 50 armes",              "acquerir_50"),
]

checkboxes   = []
instructions = []
_DEPART_Y    = 30           # y dans le world (pas dans la popup)
_ESPACE_Y    = 65
for i, (libelle, qid) in enumerate(QUETES_AFFICHEES):
    y = _DEPART_Y + i * _ESPACE_Y
    checkboxes.append(QuestCheckbox(80, y, 40, qid))
    instructions.append(pygameui.Text((140, y + 8), libelle, blanc, font_size=22))

# Hauteur du contenu scrollable
WORLD_H   = max(POPUP_H - HEADER_H,
                _DEPART_Y + len(QUETES_AFFICHEES) * _ESPACE_Y + 50)
VIEW_H    = POPUP_H - HEADER_H        # zone visible scrollable
world     = pygame.Surface((POPUP_W, WORLD_H))

fond_realisation = pygame.transform.scale(fond_realisation_full, (POPUP_W, WORLD_H))

# Scrollbar (placée dans la zone scrollable uniquement)
sb_v = ScrollBar(
    x_local=POPUP_W - 22, y_local=HEADER_H + 5,
    width=12, height=VIEW_H - 10,
    content_height=WORLD_H,
    view_height=VIEW_H,
)


# ─────────────────────────────────────────────
#  RENDU
# ─────────────────────────────────────────────

def calcul_score():
    return sum(1 for cb in checkboxes if cb.is_checked())


def realisation_brouillon(events, joueur_nom: str = "test", *_, **__):
    """
    Rend la popup des réalisations (500x500) avec un titre "LES QUÊTES" sticky.
    """
    surface = pygame.Surface((POPUP_W, POPUP_H))
    surface.fill(fond)

    # Scrollbar
    sb_v.update(events)
    offset = sb_v.get_value()

    # Mise à jour des checkboxes
    for cb in checkboxes:
        cb.refresh(joueur_nom)

    # Rendu du contenu scrollable
    world.blit(fond_realisation, (0, 0))
    for cb in checkboxes:
        cb.draw(world)
    for text in instructions:
        text.draw(world)

    # Découpe la zone scrollable visible (sous le header)
    visible_zone = surface.subsurface(pygame.Rect(0, HEADER_H, POPUP_W, VIEW_H))
    visible_zone.blit(world, (0, -offset))

    # ── HEADER (titre sticky) ────────────────────────────────────────────
    # Fond violet foncé derrière le titre
    pygame.draw.rect(surface, (45, 20, 65),
                     pygame.Rect(0, 0, POPUP_W, HEADER_H))

    draw_title(surface, "LES QUÊTES", POPUP_W // 2, HEADER_H // 2 - 8)

    # Score en dessous du titre
    score_surf = FONT_SCORE.render(
        f"Complete : {calcul_score()}/{len(checkboxes)}", True, blanc
    )
    score_rect = score_surf.get_rect(center=(POPUP_W // 2, HEADER_H - 14))
    surface.blit(score_surf, score_rect)

    # Scrollbar par-dessus tout
    sb_v.draw_on_popup(surface)

    return surface
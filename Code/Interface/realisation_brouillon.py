"""
realisation_brouillon.py :
Interface des quêtes/réalisations — popup scrollable avec titre sticky,
checkboxes en lecture seule et compteur de progression
"""

import pygame
import Interface.pygameui as pygameui
from Fichiers_variables.variables import *
from Fichiers_variables.gestion_fichiers import contenu_fichier_quetes


POPUP_W, POPUP_H = 500, 400
WORLD_H = 1000   # hauteur initiale du contenu scrollable (recalculée plus bas)

world = pygame.Surface((POPUP_W, WORLD_H))

fond_realisation = pygame.image.load("Images/Interface/fond_realisation.png")
fond_realisation = pygame.transform.scale(fond_realisation, (POPUP_W, WORLD_H))

# Données brutes des quêtes (histoires, kills, acquisitions)
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
        10:    "tue 10 ennemis",
        20:    "tue 20 ennemis",
        50:    "tue 50 ennemis",
        100:   "tue 100 ennemis",
        500:   "tue 500 ennemis",
        1000:  "tue 1000 ennemis",
        5000:  "tue 5000 ennemis",
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
    """Retourne le libellé de la quête d'acquisition correspondant au nombre d'armes possédées

    Parameters
    ----------
    nb_armes : int
        Nombre d'armes actuellement possédées par le joueur

    Returns
    -------
    str or False
        Libellé de la quête atteinte, ou False si aucune quête n'est déclenchée
    """
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
    """Retourne le libellé de la quête de kills si le joueur atteint un palier exact

    Parameters
    ----------
    p : object
        Objet joueur possédant l'attribut kill_count

    Returns
    -------
    str or False
        Libellé de la quête si un palier est atteint exactement, sinon False
    """
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



#  ÉTAT DES QUÊTES 


def quete_realisee(joueur_nom: str, quete_id: str) -> bool:
    """Vérifie si une quête est marquée comme réalisée pour un joueur dans le CSV

    Parameters
    ----------
    joueur_nom : str
        Nom du joueur à vérifier
    quete_id : str
        Identifiant de la quête (colonne "Type" dans le CSV)

    Returns
    -------
    bool
        True si la quête est réalisée (valeur "1"), False sinon ou en cas d'erreur
    """
    try:
        contenu = contenu_fichier_quetes()
        for row in contenu:
            if row.get("Type") == quete_id:
                return str(row.get(joueur_nom, "0")) == "1"
    except Exception as e:
        print(f"[Quetes] Lecture impossible : {e}")
    return False




fond     = (245, 245, 235)   # couleur de fond de la popup
croix    = (220,  40,  50)   # couleur des checkboxes cochées
blanc    = (255, 255, 255)
or_clair = (255, 215, 100)

POPUP_W, POPUP_H = 500, 500
HEADER_H = 90                 # hauteur de la zone titre sticky
POPUP_X  = (WIDTH  - POPUP_W) // 2
POPUP_Y  = (HEIGHT - POPUP_H) // 2

fond_realisation_full = pygame.image.load("Images/Interface/fond_realisation.png")

# Police pixel avec fallback
try:
    FONT_TITRE = pygame.font.Font("assets/pixels.ttf", 38)
except Exception:
    FONT_TITRE = pygame.font.SysFont("Impact", 44, bold=True)

try:
    FONT_SCORE = pygame.font.Font("assets/pixels.ttf", 16)
except Exception:
    FONT_SCORE = pygame.font.SysFont(None, 28)


def draw_title(surface, text, center_x, center_y):
    """Dessine un titre centré avec la police pixel

    Parameters
    ----------
    surface : pygame.Surface
        Surface sur laquelle dessiner le titre
    text : str
        Texte du titre
    center_x, center_y : int
        Coordonnées du centre du titre
    """
    texte = FONT_TITRE.render(text, True, blanc)
    texte_rect = texte.get_rect(center=(center_x, center_y))
    surface.blit(texte, texte_rect)


class ScrollBar:
    """
    Class ScrollBar :
    Barre de défilement verticale personnalisée avec gestion du drag
    et du scroll molette, positionnée en coordonnées écran absolues
    """

    def __init__(self, x_local: int, y_local: int,
                 width: int, height: int,
                 content_height: int, view_height: int):
        """Initialise la scrollbar avec ses dimensions et son contenu

        Parameters
        ----------
        x_local, y_local : int
            Position locale dans la popup (sans offset POPUP_X/Y)
        width, height : int
            Dimensions de la piste de la scrollbar
        content_height : int
            Hauteur totale du contenu scrollable
        view_height : int
            Hauteur de la zone visible
        """
        self.x_local        = x_local
        self.y_local        = y_local
        self.width          = width
        self.height         = height
        self.content_height = content_height
        self.view_height    = view_height
        self.offset         = 0.0    # défilement actuel en pixels
        self._dragging      = False
        self._drag_offset_y = 0

    @property
    def max_offset(self) -> float:
        """Offset maximum atteignable (quand le contenu dépasse la vue)

        Returns
        -------
        float
            Valeur maximale du défilement en pixels
        """
        return max(0, self.content_height - self.view_height)

    @property
    def handle_height(self) -> int:
        """Hauteur de la poignée proportionnelle au rapport vue/contenu

        Returns
        -------
        int
            Hauteur de la poignée en pixels (minimum 30)
        """
        if self.content_height <= self.view_height:
            return self.height
        h = int(self.height * self.view_height / self.content_height)
        return max(30, h)

    def track_rect_screen(self) -> pygame.Rect:
        """Retourne le rect de la piste en coordonnées écran absolues

        Returns
        -------
        pygame.Rect
        """
        return pygame.Rect(POPUP_X + self.x_local, POPUP_Y + self.y_local,
                           self.width, self.height)

    def handle_rect_screen(self) -> pygame.Rect:
        """Retourne le rect de la poignée en coordonnées écran absolues

        Returns
        -------
        pygame.Rect
        """
        if self.max_offset == 0:
            handle_y = POPUP_Y + self.y_local
        else:
            ratio    = self.offset / self.max_offset
            handle_y = (POPUP_Y + self.y_local
                        + int(ratio * (self.height - self.handle_height)))
        return pygame.Rect(POPUP_X + self.x_local, handle_y,
                           self.width, self.handle_height)

    def track_rect_local(self) -> pygame.Rect:
        """Retourne le rect de la piste en coordonnées locales à la popup

        Returns
        -------
        pygame.Rect
        """
        return pygame.Rect(self.x_local, self.y_local, self.width, self.height)

    def handle_rect_local(self) -> pygame.Rect:
        """Retourne le rect de la poignée en coordonnées locales à la popup

        Returns
        -------
        pygame.Rect
        """
        if self.max_offset == 0:
            return pygame.Rect(self.x_local, self.y_local,
                               self.width, self.handle_height)
        ratio = self.offset / self.max_offset
        y     = self.y_local + int(ratio * (self.height - self.handle_height))
        return pygame.Rect(self.x_local, y, self.width, self.handle_height)

    def _set_offset_from_screen_y(self, screen_y: int, drag_y_offset: int = 0):
        """Calcule et applique l'offset à partir d'une position y écran

        Parameters
        ----------
        screen_y : int
            Position y de la souris en coordonnées écran
        drag_y_offset : int, optional
            Décalage interne au drag pour éviter un saut au premier clic
        """
        track_top = POPUP_Y + self.y_local
        target    = screen_y - drag_y_offset - track_top
        space     = self.height - self.handle_height
        if space <= 0:
            return
        ratio       = target / space
        self.offset = max(0, min(ratio * self.max_offset, self.max_offset))

    def update(self, events):
        """Met à jour l'offset selon les événements souris (clic, drag, molette)

        Parameters
        ----------
        events : list[pygame.event.Event]
            Événements pygame du frame courant
        """
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
                    self.offset = max(0, self.offset - 40)   # scroll vers le haut
                elif event.button == 5 and popup_rect.collidepoint(event.pos):
                    self.offset = min(self.max_offset, self.offset + 40)  # scroll vers le bas
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._dragging = False
            elif event.type == pygame.MOUSEMOTION and self._dragging:
                self._set_offset_from_screen_y(event.pos[1], self._drag_offset_y)

    def get_value(self) -> int:
        """Retourne l'offset courant arrondi à l'entier

        Returns
        -------
        int
            Valeur du défilement en pixels
        """
        return int(self.offset)

    def draw_on_popup(self, surface: pygame.Surface):
        """Dessine la piste et la poignée sur la surface de la popup

        Parameters
        ----------
        surface : pygame.Surface
            Surface de la popup (coordonnées locales)
        """
        pygame.draw.rect(surface, (215, 215, 210),
                         self.track_rect_local(), border_radius=6)
        pygame.draw.rect(surface, (180, 180, 175),
                         self.track_rect_local(), 1, border_radius=6)
        couleur = (90, 90, 90) if self._dragging else (130, 130, 130)
        pygame.draw.rect(surface, couleur,
                         self.handle_rect_local(), border_radius=6)


class QuestCheckbox(pygameui.Checkbox):
    """
    Class QuestCheckbox :
    Checkbox en lecture seule affichant l'état de réalisation d'une quête,
    rafraîchie depuis le fichier CSV à chaque frame
    """

    def __init__(self, x: int, y: int, taille: int, quete_id: str):
        """Initialise une checkbox de quête désactivée (lecture seule)

        Parameters
        ----------
        x, y : int
            Position dans le monde scrollable
        taille : int
            Côté du carré en pixels
        quete_id : str
            Identifiant de la quête dans le CSV
        """
        super().__init__(
            position=(x, y), width=taille, height=taille,
            style="cross", color=croix, background_color=fond
        )
        self.disable()        
        self.quete_id = quete_id

    def refresh(self, joueur_nom: str):
        """Met à jour l'état de la checkbox depuis le fichier CSV

        Parameters
        ----------
        joueur_nom : str
            Nom du joueur dont on lit la progression
        """
        self.set_checked(quete_realisee(joueur_nom, self.quete_id))



# liste des quêtes visibles 
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
_DEPART_Y    = 30    
_ESPACE_Y    = 65    # espacement vertical entre chaque quête

# gfénération des checkboxes et labels 
for i, (libelle, qid) in enumerate(QUETES_AFFICHEES):
    y = _DEPART_Y + i * _ESPACE_Y
    checkboxes.append(QuestCheckbox(80, y, 40, qid))
    instructions.append(pygameui.Text((140, y + 8), libelle, blanc, font_size=22))

#dimensions du contenu scrollable 
WORLD_H = max(POPUP_H - HEADER_H,
              _DEPART_Y + len(QUETES_AFFICHEES) * _ESPACE_Y + 50)
VIEW_H  = POPUP_H - HEADER_H        # hauteur de la zone scrollable visible
world   = pygame.Surface((POPUP_W, WORLD_H))

fond_realisation = pygame.transform.scale(fond_realisation_full, (POPUP_W, WORLD_H))

# scrollbar verticale dans la zone scrollable u
sb_v = ScrollBar(
    x_local=POPUP_W - 22, y_local=HEADER_H + 5,
    width=12, height=VIEW_H - 10,
    content_height=WORLD_H,
    view_height=VIEW_H,
)



def calcul_score():
    """Compte le nombre de quêtes actuellement cochées

    Returns
    -------
    int
        Nombre de checkboxes dont l'état est True
    """
    return sum(1 for cb in checkboxes if cb.is_checked())


def realisation_brouillon(events, joueur_nom: str = "test", *_, **__):
    """Rend la popup des réalisations (500x500) avec un titre "LES QUÊTES" sticky

    Gère le scroll, le rafraîchissement des checkboxes et l'affichage
    du score de progression en dessous du titre fixe.

    Parameters
    ----------
    events : list[pygame.event.Event]
        Événements pygame du frame courant
    joueur_nom : str, optional
        Nom du joueur pour lire sa progression (défaut "test")

    Returns
    -------
    pygame.Surface
        Surface 500x500 prête à être blittée sur la fenêtre principale
    """
    surface = pygame.Surface((POPUP_W, POPUP_H))
    surface.fill(fond)

    # mise à jour du défilement
    sb_v.update(events)
    offset = sb_v.get_value()

    # rafraîchissement des checkboxes depuis le CSV
    for cb in checkboxes:
        cb.refresh(joueur_nom)

    # rendu du contenu scrollable sur le monde
    world.blit(fond_realisation, (0, 0))
    for cb in checkboxes:
        cb.draw(world)
    for text in instructions:
        text.draw(world)

    # découpe de la zone visible et application du décalage de scroll
    visible_zone = surface.subsurface(pygame.Rect(0, HEADER_H, POPUP_W, VIEW_H))
    visible_zone.blit(world, (0, -offset))

    
    pygame.draw.rect(surface, (45, 20, 65),
                     pygame.Rect(0, 0, POPUP_W, HEADER_H))  # fond violet foncé

    draw_title(surface, "LES QUÊTES", POPUP_W // 2, HEADER_H // 2 - 8)

    # Score affiché sous le titre
    score_surf = FONT_SCORE.render(
        f"Complete : {calcul_score()}/{len(checkboxes)}", True, blanc
    )
    score_rect = score_surf.get_rect(center=(POPUP_W // 2, HEADER_H - 14))
    surface.blit(score_surf, score_rect)

    # Scrollbar dessinée par-dessus tout le contenu
    sb_v.draw_on_popup(surface)

    return surface
"""
Power_up_shop.py :
Boutique de power-ups ,
achat via argent du joueur et sauvegarde de la progression
"""

import pygame
import Interface.variable_power_up as data
from Jeu.power_up import apply_powerups
from Fichiers_variables.gestion_fichiers import replace_player_money, sauvegarder_powerup, charger_powerups_joueur
import Interface.pygameui as pygameui

WIDTH, HEIGHT = 500, 500

# ordre d'affichage des power-ups dans la grille
ORDRE_POWERUPS = [
    "Pouvoir",   "sante",     "Protection",      # ligne 1
    "refroidissement", "zone", "vitesse_du_j",   # ligne 2
    "durabilite", "attirance", "chance",         # ligne 3
    "croissance",                                 
]

# noms affichés dans l'interface
NOMS_FR = {
    "Pouvoir":         "Pouvoir",
    "sante":           "Sante",
    "Protection":      "Armure",
    "refroidissement": "Cooldown",
    "zone":            "Zone",
    "vitesse_du_j":    "Vitesse",
    "durabilite":      "Duree",
    "attirance":       "Aimant",
    "chance":          "Chance",
    "croissance":      "Croissance",
}

# dimensions et positionnement de la grille 
CELL_W, CELL_H = 130, 70   # largeur et hauteur d'une cellule
GAP_X          = 25         # espacement horizontal entre cellules
GAP_Y          = 18         # espacement vertical entre cellules
COLS           = 3          # nombre de colonnes
START_Y        = 35         # coordonnée y de départ

GRID_W  = COLS * CELL_W + (COLS - 1) * GAP_X   # largeur totale de la grille
START_X = (WIDTH - GRID_W) // 2                  # x de départ pour centrer la grille


def _calc_positions():
    """Calcule les coordonnées (x, y) de chaque cellule dans la grille

    La dernière ligne incomplète est alignée sur la colonne de gauche.

    Returns
    -------
    list[tuple(int, int, str)]
        Liste de (x, y, nom_du_power_up) dans l'ordre d'affichage
    """
    positions = []
    for i, power in enumerate(ORDRE_POWERUPS):
        col = i % COLS
        row = i // COLS

        nb_dans_ligne = min(COLS, len(ORDRE_POWERUPS) - row * COLS)
        if nb_dans_ligne < COLS:
            x_start = START_X  # ligne incomplète → alignée à gauche
        else:
            x_start = START_X

        x = x_start + col * (CELL_W + GAP_X)
        y = START_Y + row * (CELL_H + GAP_Y)
        positions.append((x, y, power))
    return positions


CELLS_LAYOUT = _calc_positions()

# polices 
try:
    FONT_TITRE_CELL = pygame.font.Font("assets/pixels.ttf", 11)
except Exception:
    FONT_TITRE_CELL = pygame.font.SysFont("Press Start 2P", 13, bold=True)

try:
    FONT_PRIX = pygame.font.Font("assets/pixels.ttf", 16)
except Exception:
    FONT_PRIX = pygame.font.SysFont("Press Start 2P", 20, bold=True)

try:
    FONT_MONEY = pygame.font.Font("assets/pixels.ttf", 18)
except Exception:
    FONT_MONEY = pygame.font.SysFont("Press Start 2P", 22, bold=True)

FONT_MAX_LABEL = pygame.font.SysFont("Arial", 10)

# image argent
try:
    IMG_ARGENT = pygame.image.load("Images/Interface/argent.png").convert_alpha()
except Exception:
    IMG_ARGENT = None


def _scale_argent(taille):
    """Redimensionne l'image argent à une taille carrée donnée

    Parameters
    ----------
    taille : int
        Côté du carré en pixels

    Returns
    -------
    pygame.Surface or None
        Image redimensionnée, ou None si l'image source est absente
    """
    if IMG_ARGENT is None:
        return None
    return pygame.transform.smoothscale(IMG_ARGENT, (taille, taille))


IMG_ARGENT_PETIT = _scale_argent(28)   # affiché à côté du compteur en bas
IMG_ARGENT_MINI  = _scale_argent(22)   # affiché dans le bouton acheter


class PowerUpCell:
    """
    Class PowerUpCell :
    Cellule interactive représentant un power-up dans la boutique,
    avec checkboxes indiquant les niveaux débloqués
    """

    def __init__(self, x, y, w, h, power):
        """Initialise une cellule de power-up avec sa position et ses checkboxes

        Parameters
        ----------
        x, y : int
            Coordonnées du coin supérieur gauche de la cellule
        w, h : int
            Largeur et hauteur de la cellule
        power : str
            Identifiant interne du power-up (clé dans data.liste_power_up)
        """
        self.rect  = pygame.Rect(x, y, w, h)
        self.power = power
        self.label = NOMS_FR.get(power, power)
        self.checkboxes = []
        self._build_checkboxes()

    def _build_checkboxes(self):
        """Construit les checkboxes représentant les niveaux max du power-up

        Les checkboxes sont centrées horizontalement en bas de la cellule.
        """
        self.checkboxes = []
        max_niv = data.MAX_NIVEAUX.get(self.power, 0)

        box_size = 11
        gap      = 3
        total    = max_niv * (box_size + gap) - gap if max_niv > 0 else 0
        start_x  = self.rect.x + (self.rect.w - total) // 2
        y        = self.rect.bottom - box_size - 5

        for i in range(max_niv):
            cb = pygameui.Checkbox(
                (start_x + i * (box_size + gap), y),
                width=box_size,
                height=box_size,
                style="square",
                color=(80, 200, 100),
                background_color=(60, 40, 80),
                border_color=(150, 100, 150),
                border_width=1,
            )
            self.checkboxes.append(cb)

    def sync_checkboxes(self):
        """Synchronise l'état des checkboxes avec le niveau actuel du power-up"""
        niveau = data.playerInventory.get(self.power, 0)
        for i, cb in enumerate(self.checkboxes):
            cb.set_checked(i < niveau)

    @property
    def niveau(self):
        """Niveau actuel du power-up dans l'inventaire du joueur

        Returns
        -------
        int
            Niveau actuel (0 si jamais acheté)
        """
        return data.playerInventory.get(self.power, 0)

    @property
    def max_niveau(self):
        """Niveau maximum atteignable pour ce power-up

        Returns
        -------
        int
            Niveau maximum défini dans data.MAX_NIVEAUX
        """
        return data.MAX_NIVEAUX.get(self.power, 0)

    @property
    def prix_prochain(self):
        """Prix du prochain niveau à acheter

        Returns
        -------
        int or None
            Prix en argent du prochain niveau, ou None si le niveau max est atteint
        """
        if self.niveau >= self.max_niveau:
            return None
        prices, _ = data.liste_power_up[self.power]
        return prices[self.niveau]

    def draw(self, surface, selected=False, offset=(0, 0)):
        """Dessine la cellule avec surbrillance si sélectionnée

        Parameters
        ----------
        surface : pygame.Surface
            Surface sur laquelle dessiner
        selected : bool, optional
            True pour afficher la surbrillance dorée (défaut False)
        offset : tuple(int, int), optional
            Décalage (ox, oy) appliqué au rendu pour le centrage de la fenêtre
        """
        ox, oy = offset
        r = self.rect.move(ox, oy)

        if selected:
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((255, 220, 50, 130))  # fond doré semi-transparent
            surface.blit(s, (r.x, r.y))
            pygame.draw.rect(surface, (255, 200, 0), r, 2, border_radius=6)

        # nom du power-up en violet
        txt = FONT_TITRE_CELL.render(self.label, True, (90, 30, 110))
        surface.blit(txt, (r.x + 6, r.y + 5))

        # indicateur MAX si le niveau maximum est atteint
        if self.niveau >= self.max_niveau:
            p = FONT_MAX_LABEL.render("MAX", True, (80, 220, 80))
            surface.blit(p, (r.right - 30, r.y + 5))

        # checkboxes avec décalage de l'offset appliqué temporairement
        self.sync_checkboxes()
        for cb in self.checkboxes:
            orig = cb._rect
            cb._rect = orig.move(ox, oy)
            cb.draw(surface)
            cb._rect = orig


class ShopPowerUp:
    """
    Class ShopPowerUp :
    Boutique complète de power-ups avec grille de cellules,
    bouton d'achat et affichage du solde du joueur
    """

    def __init__(self):
        """Initialise la boutique : crée les cellules, le fond et le bouton d'achat"""
        pygame.font.init()
        self.cells    = [PowerUpCell(x, y, CELL_W, CELL_H, p)
                         for (x, y, p) in CELLS_LAYOUT]
        self.selected = None                              # cellule actuellement sélectionnée
        self.buy_rect = pygame.Rect(220, 370, 160, 50)   # zone du bouton acheter

        try:
            self.bg = pygame.image.load("Images/Interface/fond_power_up.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((40, 25, 60))  # fond violet de secours si image absente

    def draw(self, win, player_money, offset=(0, 0)):
        """Dessine l'intégralité de la boutique sur la fenêtre

        Parameters
        ----------
        win : pygame.Surface
            Fenêtre de jeu
        player_money : int
            Solde actuel du joueur
        offset : tuple(int, int), optional
            Décalage pour le centrage dans la fenêtre principale
        """
        ox, oy = offset
        win.blit(self.bg, (ox, oy))

        for cell in self.cells:
            cell.draw(win, selected=(cell is self.selected), offset=offset)

        self._draw_money(win, player_money, ox, oy)
        self._draw_buy_button(win, player_money, ox, oy)

    def _draw_money(self, win, player_money, ox, oy):
        """Affiche le solde du joueur en bas à droite avec l'icône argent

        Parameters
        ----------
        win : pygame.Surface
            Fenêtre de jeu
        player_money : int
            Solde à afficher
        ox, oy : int
            Décalage d'affichage
        """
        money_txt = FONT_MONEY.render(str(player_money), True, (255, 230, 80))
        rect      = money_txt.get_rect()
        rect.midright = (ox + WIDTH - 25, oy + HEIGHT - 22)
        win.blit(money_txt, rect)

        if IMG_ARGENT_PETIT is not None:
            ix = rect.left - IMG_ARGENT_PETIT.get_width() - 6
            iy = rect.centery - IMG_ARGENT_PETIT.get_height() // 2
            win.blit(IMG_ARGENT_PETIT, (ix, iy))

    def _draw_buy_button(self, win, player_money, ox, oy):
        """Affiche le bouton d'achat pour la cellule sélectionnée

        Le bouton est vert si le joueur a assez d'argent, rouge sinon,
        et gris si le niveau maximum est déjà atteint.

        Parameters
        ----------
        win : pygame.Surface
            Fenêtre de jeu
        player_money : int
            Solde du joueur pour déterminer la couleur du bouton
        ox, oy : int
            Décalage d'affichage
        """
        if not self.selected:
            return

        prix = self.selected.prix_prochain
        bx = ox + self.buy_rect.x
        by = oy + self.buy_rect.y
        rect = pygame.Rect(bx, by, self.buy_rect.w, self.buy_rect.h)

        if prix is None:
            # Niveau max atteint : bouton gris
            color = (100, 100, 100)
            label = FONT_PRIX.render("MAX", True, (255, 255, 255))
            pygame.draw.rect(win, color, rect, border_radius=8)
            win.blit(label, label.get_rect(center=rect.center))
            return

        color = (80, 180, 100) if player_money >= prix else (180, 80, 80)  # vert ou rouge

        pygame.draw.rect(win, color, rect, border_radius=8)
        pygame.draw.rect(win, (255, 230, 80), rect, 2, border_radius=8)

        # Texte "Acheter <prix> [icône argent]" centré horizontalement
        prix_txt = FONT_PRIX.render(str(prix), True, (255, 255, 255))
        ach_txt  = FONT_PRIX.render("Acheter", True, (255, 255, 255))

        total_w = ach_txt.get_width() + 14 + prix_txt.get_width()
        if IMG_ARGENT_MINI is not None:
            total_w += 6 + IMG_ARGENT_MINI.get_width()

        cur_x = rect.centerx - total_w // 2

        ach_rect = ach_txt.get_rect()
        ach_rect.midleft = (cur_x, rect.centery)
        win.blit(ach_txt, ach_rect)
        cur_x = ach_rect.right + 14

        prix_rect = prix_txt.get_rect()
        prix_rect.midleft = (cur_x, rect.centery)
        win.blit(prix_txt, prix_rect)
        cur_x = prix_rect.right + 6

        if IMG_ARGENT_MINI is not None:
            iy = rect.centery - IMG_ARGENT_MINI.get_height() // 2
            win.blit(IMG_ARGENT_MINI, (cur_x, iy))

    def update(self, events, win, mouse_pos, mouse_pressed,
               player_money, player, offset=(0, 0)):
        """Met à jour et dessine la boutique pour un frame

        Gère les clics sur les cellules et sur le bouton d'achat.

        Parameters
        ----------
        events : list[pygame.event.Event]
            Événements pygame du frame courant
        win : pygame.Surface
            Fenêtre de jeu
        mouse_pos : tuple(int, int)
            Position de la souris
        mouse_pressed : tuple
            État des boutons de la souris
        player_money : int
            Solde actuel du joueur
        player : str or object
            Identifiant ou objet joueur (pour la sauvegarde)
        offset : tuple(int, int), optional
            Décalage pour le centrage de la boutique

        Returns
        -------
        tuple(bool, int)
            (False, solde_mis_à_jour) — le bool est réservé pour une fermeture future
        """
        self.draw(win, player_money, offset)
        ox, oy = offset

        buy_clicked = False
        data.playerInventory.update(charger_powerups_joueur(player))

        if self.selected:
            bx = ox + self.buy_rect.x
            by = oy + self.buy_rect.y
            rect = pygame.Rect(bx, by, self.buy_rect.w, self.buy_rect.h)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if rect.collidepoint(event.pos):
                        buy_clicked = True

        if buy_clicked:
            player_money = self._buy(player_money, player)
        else:
            # Sélection d'une cellule au clic
            for cell in self.cells:
                shifted = cell.rect.move(ox, oy)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if shifted.collidepoint(event.pos):
                            self.selected = cell

        return False, player_money

    def _buy(self, player_money, player):
        """Effectue l'achat du prochain niveau du power-up sélectionné

        Déduit le prix, incrémente le niveau, sauvegarde et applique les effets.

        Parameters
        ----------
        player_money : int
            Solde actuel du joueur
        player : str or object
            Identifiant ou objet joueur

        Returns
        -------
        int
            Nouveau solde après achat (inchangé si achat impossible)
        """
        if self.selected is None:
            return player_money
        prix = self.selected.prix_prochain
        if prix is None or player_money < prix:
            return player_money

        player_money -= prix
        data.playerInventory[self.selected.power] += 1
        sauvegarder_powerup(player, self.selected.power, data.playerInventory[self.selected.power])

        if not isinstance(player, str):
            apply_powerups(player)  # applique les bonus si on a l'objet joueur

        replace_player_money(player, player_money)
        return player_money



_shop_instance = None


def _get_shop():
    """Retourne l'instance unique de ShopPowerUp (pattern singleton)

    Returns
    -------
    ShopPowerUp
        Instance partagée de la boutique
    """
    global _shop_instance
    if _shop_instance is None:
        _shop_instance = ShopPowerUp()
    return _shop_instance


def open_shop(events, WIN, mouse_pos, mouse_pressed,
              close_button, FONT_BUTTON, player_money, player):
    """Ouvre et affiche la boutique de power-ups pour un frame

    Calcule le décalage pour centrer la boutique dans la fenêtre principale.

    Parameters
    ----------
    events : list[pygame.event.Event]
        Événements pygame du frame courant
    WIN : pygame.Surface
        Fenêtre principale du jeu
    mouse_pos : tuple(int, int)
        Position de la souris
    mouse_pressed : tuple
        État des boutons de la souris
    close_button : Button
        Bouton de fermeture de la boutique
    FONT_BUTTON : pygame.font.Font
        Police utilisée pour les boutons
    player_money : int
        Solde actuel du joueur
    player : str or object
        Identifiant ou objet joueur

    Returns
    -------
    tuple(bool, int)
        (True si la boutique doit être fermée, nouveau solde du joueur)
    """
    shop = _get_shop()

    win_w, win_h = WIN.get_size()
    ox = (win_w - WIDTH) // 2
    oy = (win_h - HEIGHT) // 2

    _, player_money = shop.update(events, WIN, mouse_pos, mouse_pressed,
                                  player_money, player, offset=(ox, oy))

    if close_button.is_clicked(mouse_pos, mouse_pressed):
        return True, player_money
    return False, player_money


def sync_checkboxes():
    """Synchronise toutes les checkboxes de la boutique avec l'inventaire actuel"""
    shop = _get_shop()
    for cell in shop.cells:
        cell.sync_checkboxes()


def buy_selected(player_money, player):
    """Achète le prochain niveau du power-up sélectionné dans la boutique

    Parameters
    ----------
    player_money : int
        Solde actuel du joueur
    player : str or object
        Identifiant ou objet joueur

    Returns
    -------
    int
        Nouveau solde après achat
    """
    return _get_shop()._buy(player_money, player)


try:
    checkboxes = [pygameui.Checkbox((0, 0), 1, 1) for _ in data.playerInventory]
except Exception:
    checkboxes = []
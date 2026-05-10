"""
Power_up_shop.py — layout 3 par ligne + police pixel + image argent
"""

import pygame
import Interface.variable_power_up as data
from Jeu.power_up import apply_powerups
from Fichiers_variables.gestion_fichiers import replace_player_money
import Interface.pygameui as pygameui

WIDTH, HEIGHT = 500, 500


# ─────────────────────────────────────────────
#  ORDRE DES POWER-UPS
#  3 par ligne, dernière ligne avec 1 seul (centré)
# ─────────────────────────────────────────────

ORDRE_POWERUPS = [
    "Pouvoir",   "sante",     "Protection",     # ligne 1
    "refroidissement", "zone", "vitesse_du_j",  # ligne 2
    "durabilite", "attirance", "chance",        # ligne 3
    "croissance",                                # ligne 4 (seule, centrée)
]

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


# ─────────────────────────────────────────────
#  POSITIONS DES CELLULES (générées proprement)
# ─────────────────────────────────────────────

CELL_W, CELL_H = 130, 70
GAP_X          = 25
GAP_Y          = 18
COLS           = 3
START_Y        = 35

# Largeur totale de la grille → centrée horizontalement
GRID_W   = COLS * CELL_W + (COLS - 1) * GAP_X
START_X  = (WIDTH - GRID_W) // 2


def _calc_positions():
    """Retourne la liste des (x, y, power) dans l'ordre voulu."""
    positions = []
    for i, power in enumerate(ORDRE_POWERUPS):
        col = i % COLS
        row = i // COLS

        # Si dernière ligne incomplète (1 seul élément), aligné à gauche
        # (au niveau du dessin XP du fond)
        nb_dans_ligne = min(COLS, len(ORDRE_POWERUPS) - row * COLS)
        if nb_dans_ligne < COLS:
            x_start = START_X        # ← aligné colonne de gauche
        else:
            x_start = START_X

        x = x_start + col * (CELL_W + GAP_X)
        y = START_Y + row * (CELL_H + GAP_Y)
        positions.append((x, y, power))
    return positions


CELLS_LAYOUT = _calc_positions()


# ─────────────────────────────────────────────
#  POLICES
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
#  IMAGE ARGENT (remplace le mot "Or")
# ─────────────────────────────────────────────

try:
    IMG_ARGENT = pygame.image.load("Images/Interface/argent.png").convert_alpha()
except Exception:
    IMG_ARGENT = None

# Versions petites pour boutons et compteur
def _scale_argent(taille):
    if IMG_ARGENT is None:
        return None
    return pygame.transform.smoothscale(IMG_ARGENT, (taille, taille))

IMG_ARGENT_PETIT = _scale_argent(28)   # à côté du compteur en bas
IMG_ARGENT_MINI  = _scale_argent(22)   # dans le bouton acheter


# ─────────────────────────────────────────────
#  CELLULE
# ─────────────────────────────────────────────

class PowerUpCell:
    def __init__(self, x, y, w, h, power):
        self.rect  = pygame.Rect(x, y, w, h)
        self.power = power
        self.label = NOMS_FR.get(power, power)
        self.checkboxes = []
        self._build_checkboxes()

    def _build_checkboxes(self):
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
        niveau = data.playerInventory.get(self.power, 0)
        for i, cb in enumerate(self.checkboxes):
            cb.set_checked(i < niveau)

    @property
    def niveau(self):
        return data.playerInventory.get(self.power, 0)

    @property
    def max_niveau(self):
        return data.MAX_NIVEAUX.get(self.power, 0)

    @property
    def prix_prochain(self):
        if self.niveau >= self.max_niveau:
            return None
        prices, _ = data.liste_power_up[self.power]
        return prices[self.niveau]

    def draw(self, surface, selected=False, offset=(0, 0)):
        ox, oy = offset
        r = self.rect.move(ox, oy)

        # Surbrillance si sélectionné
        if selected:
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((255, 220, 50, 130))
            surface.blit(s, (r.x, r.y))
            pygame.draw.rect(surface, (255, 200, 0), r, 2, border_radius=6)

        # Nom du power-up (violet)
        txt = FONT_TITRE_CELL.render(self.label, True, (90, 30, 110))
        surface.blit(txt, (r.x + 6, r.y + 5))

        # Indicateur MAX si plein
        if self.niveau >= self.max_niveau:
            p = FONT_MAX_LABEL.render("MAX", True, (80, 220, 80))
            surface.blit(p, (r.right - 30, r.y + 5))

        # Checkboxes (niveaux acquis)
        self.sync_checkboxes()
        for cb in self.checkboxes:
            orig = cb._rect
            cb._rect = orig.move(ox, oy)
            cb.draw(surface)
            cb._rect = orig


# ─────────────────────────────────────────────
#  SHOP
# ─────────────────────────────────────────────

class ShopPowerUp:
    def __init__(self):
        pygame.font.init()
        self.cells    = [PowerUpCell(x, y, CELL_W, CELL_H, p)
                         for (x, y, p) in CELLS_LAYOUT]
        self.selected = None
        self.buy_rect = pygame.Rect(220, 370, 160, 50)

        try:
            self.bg = pygame.image.load("Images/Interface/fond_power_up.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((40, 25, 60))

    # ── Dessin ───────────────────────────────────────────────────────────

    def draw(self, win, player_money, offset=(0, 0)):
        ox, oy = offset
        win.blit(self.bg, (ox, oy))

        for cell in self.cells:
            cell.draw(win, selected=(cell is self.selected), offset=offset)

        self._draw_money(win, player_money, ox, oy)
        self._draw_buy_button(win, player_money, ox, oy)

    def _draw_money(self, win, player_money, ox, oy):
        # Compteur d'argent en bas à droite avec image
        money_txt = FONT_MONEY.render(str(player_money), True, (255, 230, 80))
        rect      = money_txt.get_rect()
        rect.midright = (ox + WIDTH - 25, oy + HEIGHT - 22)
        win.blit(money_txt, rect)

        if IMG_ARGENT_PETIT is not None:
            ix = rect.left - IMG_ARGENT_PETIT.get_width() - 6
            iy = rect.centery - IMG_ARGENT_PETIT.get_height() // 2
            win.blit(IMG_ARGENT_PETIT, (ix, iy))

    def _draw_buy_button(self, win, player_money, ox, oy):
        if not self.selected:
            return

        prix = self.selected.prix_prochain
        bx = ox + self.buy_rect.x
        by = oy + self.buy_rect.y
        rect = pygame.Rect(bx, by, self.buy_rect.w, self.buy_rect.h)

        if prix is None:
            color = (100, 100, 100)
            label = FONT_PRIX.render("MAX", True, (255, 255, 255))
            pygame.draw.rect(win, color, rect, border_radius=8)
            win.blit(label, label.get_rect(center=rect.center))
            return

        if player_money >= prix:
            color = (80, 180, 100)     # vert : achetable
        else:
            color = (180, 80, 80)       # rouge : trop cher

        pygame.draw.rect(win, color, rect, border_radius=8)
        pygame.draw.rect(win, (255, 230, 80), rect, 2, border_radius=8)

        # Texte "Acheter" + prix + image argent
        prix_txt = FONT_PRIX.render(str(prix), True, (255, 255, 255))
        ach_txt  = FONT_PRIX.render("Acheter", True, (255, 255, 255))

        # Layout horizontal : "Acheter   <prix>  [argent]"
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

    # ── Logique ──────────────────────────────────────────────────────────

    def update(self, events, win, mouse_pos, mouse_pressed,
               player_money, player, offset=(0, 0)):

        self.draw(win, player_money, offset)
        ox, oy = offset

        # Détection clic bouton acheter
        buy_clicked = False
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
            # Sélection d'une cellule
            for cell in self.cells:
                shifted = cell.rect.move(ox, oy)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if shifted.collidepoint(event.pos):
                            self.selected = cell

        return False, player_money

    def _buy(self, player_money, player):
        if self.selected is None:
            return player_money
        prix = self.selected.prix_prochain
        if prix is None or player_money < prix:
            return player_money

        player_money -= prix
        data.playerInventory[self.selected.power] += 1

        if not isinstance(player, str):
            apply_powerups(player)

        replace_player_money(player, player_money)
        return player_money


# ─────────────────────────────────────────────
#  API EXTERNE
# ─────────────────────────────────────────────

_shop_instance = None

def _get_shop():
    global _shop_instance
    if _shop_instance is None:
        _shop_instance = ShopPowerUp()
    return _shop_instance


def open_shop(events, WIN, mouse_pos, mouse_pressed,
              close_button, FONT_BUTTON, player_money, player):
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
    shop = _get_shop()
    for cell in shop.cells:
        cell.sync_checkboxes()


def buy_selected(player_money, player):
    return _get_shop()._buy(player_money, player)


try:
    checkboxes = [pygameui.Checkbox((0, 0), 1, 1) for _ in data.playerInventory]
except Exception:
    checkboxes = []
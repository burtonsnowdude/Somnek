"""
Power_up_shop.py
Boutique power-up calquée sur fond_power_up.png (320x350px).

Layout (ordre d'affichage sur l'image) :
  Ligne 1 : [Pouvoir]  [sante]   [Protection]
  Ligne 2 : [refroid.] ← sac →  [zone]
  Ligne 3 : [vitesse]  ← sac →  [durabilite]
  Ligne 4 : [attirance]          [chance]
  Ligne 5 : [croissance]
"""

import pygame
import Interface.variable_power_up as data
from Jeu.power_up import apply_powerups
from Fichiers_variables.gestion_fichiers import replace_player_money
import Interface.pygameui as pygameui

WIDTH, HEIGHT = 500, 500

NOMS_FR = {
    "Pouvoir":         "Pouvoir",
    "sante":           "Santé",
    "Protection":      "Armure",
    "refroidissement": "Cooldown",
    "zone":            "Zone",
    "vitesse_du_j":    "Vitesse",
    "durabilite":      "Durée",
    "attirance":       "Aimant",
    "chance":          "Chance",
    "croissance":      "Croissance",
}

CELLS_LAYOUT = [
    # ── Ligne 1 : 3 cases en haut ─────────────────────────────────────────
    ( 10,  18,  85, 55, "Pouvoir",         "Pouvoir"),
    (115,  18,  85, 55, "sante",           "Max Heart"),
    (220,  18,  85, 55, "Protection",      "Armor"),
    # ── Ligne 2 : gauche + droite (sac au centre) ─────────────────────────
    ( 10,  83, 100, 45, "refroidissement", "Cooldown"),
    (205,  83, 100, 45, "zone",            "Zone"),
    # ── Ligne 3 : gauche + droite ─────────────────────────────────────────
    ( 10, 138, 100, 45, "vitesse_du_j",    "Speed"),
    (205, 138, 100, 45, "durabilite",      "Duration"),
    # ── Ligne 4 : gauche + droite ─────────────────────────────────────────
    ( 10, 193, 100, 45, "attirance",       "Magnet"),
    (205, 193, 100, 45, "chance",          "Luck"),
    # ── Ligne 5 : une case en bas à gauche ────────────────────────────────
    ( 10, 248,  95, 42, "croissance",      "Growth"),
]


class PowerUpCell:
    def __init__(self, x, y, w, h, power, label, font_title, font_small):
        self.rect       = pygame.Rect(x, y, w, h)
        self.power      = power
        self.label      = label
        self.font_title = font_title
        self.font_small = font_small

    # ── Données ──────────────────────────────────────────────────────────────
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

    # ── Interaction ──────────────────────────────────────────────────────────
    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    # ── Dessin ───────────────────────────────────────────────────────────────
    def draw(self, surface, selected):
        # Fond semi-transparent
        cell_surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        cell_surf.fill(COLOR_CELL)
        surface.blit(cell_surf, (self.rect.x, self.rect.y))

        # Bordure
        border_color = COLOR_SELECTED if selected else COLOR_BORDER
        border_w     = 3 if selected else 2
        pygame.draw.rect(surface, border_color, self.rect, border_w)

        # Label
        txt = self.font_title.render(self.label, True, COLOR_TEXT)
        surface.blit(txt, (self.rect.x + 4, self.rect.y + 3))

        # Petits carrés de niveau
        box_size = 8
        box_gap  = 3
        total_w  = self.max_niveau * (box_size + box_gap) - box_gap
        bx_start = self.rect.x + (self.rect.w - total_w) // 2
        by       = self.rect.bottom - box_size - 4

        for i in range(self.max_niveau):
            bx = bx_start + i * (box_size + box_gap)
            br = pygame.Rect(bx, by, box_size, box_size)
            color = COLOR_BOUGHT if i < self.niveau else COLOR_LOCKED
            pygame.draw.rect(surface, color, br)
            pygame.draw.rect(surface, (80, 40, 80), br, 1)

        # Prix ou MAX
        prix = self.prix_prochain
        if self.max_niveau > 0:
            if prix is not None:
                p_surf = self.font_small.render(f"{prix}g", True, COLOR_PRICE)
            else:
                p_surf = self.font_small.render("MAX", True, COLOR_MAX)
            surface.blit(p_surf, (self.rect.x + 4, self.rect.bottom - box_size - 16))


class ShopPowerUp:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Arial", 11, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 9)

        self.cells = [
            PowerUpCell(x, y, w, h, power, label, self.font_title, self.font_small)
            for (x, y, w, h, power, label) in CELLS_LAYOUT
        ]
        self.selected = None

        # Fond image
        try:
            self.bg = pygame.image.load("Images/Interface/fond_power_up.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((200, 160, 200))

    def draw(self, win, mouse_pos, player_money, offset=(0, 0)):
        ox, oy = offset
        win.blit(self.bg, (ox, oy))

        for cell in self.cells:
            # Décale le rect pour l'affichage si la boutique n'est pas en (0,0)
            shifted = cell.rect.move(ox, oy)
            original_rect = cell.rect
            cell.rect = shifted
            cell.draw(win, selected=(cell is self.selected))
            cell.rect = original_rect

        # Argent
        font = self.font_title
        money_surf = font.render(f"Or: {player_money}", True, (60, 20, 80))
        win.blit(money_surf, (ox + WIDTH - 70, oy + HEIGHT - 20))

    def update(self, events, win, mouse_pos, mouse_pressed,
               player_money, player, offset=(0, 0)) -> tuple[bool, int]:
        ox, oy = offset

        buy_clicked = False
        if self.selected:
            shifted = self.selected.rect.move(ox, oy)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if shifted.collidepoint(event.pos):
                        player_money = self._buy(player_money, player)

        return False, player_money

    def _buy(self, player_money, player):
        if self.selected is None:
            return player_money

        cell = self.selected
        prix = cell.prix_prochain

        if prix is None or player_money < prix:
            return player_money

        player_money -= prix
        data.playerInventory[self.selected.power] += 1

        if not isinstance(player, str):
            apply_powerups(player)

        replace_player_money(player, player_money)
        return player_money


# ── Instance unique ───────────────────────────────────────────────────────────
_shop_instance: ShopPowerUp | None = None

def _get_shop() -> ShopPowerUp:
    global _shop_instance
    if _shop_instance is None:
        _shop_instance = ShopPowerUp()
    return _shop_instance


# ── Compatibilité menu.py ─────────────────────────────────────────────────────
def open_shop(events, WIN, mouse_pos, mouse_pressed,
              close_button, FONT_BUTTON, player_money, player) -> bool:
    """
    Appelé chaque frame par menu.py quand show_shop == True.
    Affiche la boutique centrée dans la fenêtre principale.
    Retourne True pour fermer.
    """
    shop = _get_shop()

    # Centre la boutique dans la fenêtre principale
    win_w, win_h = WIN.get_size()
    ox = (win_w - WIDTH)  // 2
    oy = (win_h - HEIGHT) // 2

    _fermer, player_money = shop.update(
        events, WIN, mouse_pos, mouse_pressed, player_money, player, offset=(ox, oy)
    )

    if close_button.is_clicked(mouse_pos, mouse_pressed):
        return True

    return False


def buy_selected(player_money: int, player) -> int:
    shop = _get_shop()
    return shop._buy(player_money, player)


# ── Compatibilité option.py ───────────────────────────────────────────────────
try:
    import Interface.pygameui as pygameui
    checkboxes = [pygameui.Checkbox((0, 0), 1, 1) for _ in data.playerInventory]
except Exception:
    checkboxes = []

def sync_checkboxes():
    for i, power in enumerate(data.playerInventory):
        niveau  = data.playerInventory[power]
        max_niv = data.MAX_NIVEAUX.get(power, 0)
        if i < len(checkboxes):
            checkboxes[i].set_checked(niveau >= max_niv and max_niv > 0)
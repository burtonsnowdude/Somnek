"""
Power_up_shop.py - Version avec bouton acheter
"""

import pygame
import Interface.variable_power_up as data
from Jeu.power_up import apply_powerups
from Fichiers_variables.gestion_fichiers import replace_player_money, sauvegarder_powerup, charger_powerups_joueur
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
    (43,  37, 117, 65, "Pouvoir"),
    (185, 40, 117, 65, "sante"),
    (340, 40, 117, 65, "Protection"),
    (43, 130, 117, 65, "refroidissement"),
    (340,130, 117, 65, "zone"),
    (43, 200, 117, 65, "vitesse_du_j"),
    (340,200, 117, 65, "durabilite"),
    (43, 280, 117, 65, "attirance"),
    (340,280, 117, 65, "chance"),
    (43, 360, 117, 65, "croissance"),
]


class PowerUpCell:
    def __init__(self, x, y, w, h, power):
        self.rect  = pygame.Rect(x, y, w, h)
        self.power = power
        self.label = NOMS_FR.get(power, power)

        self.font = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 11)

        self.checkboxes = []
        self._build_checkboxes()

    def _build_checkboxes(self):
        self.checkboxes = []
        max_niv = data.MAX_NIVEAUX.get(self.power, 0)

        box_size = 12
        gap = 4
        total = max_niv * (box_size + gap) - gap
        start_x = self.rect.x + (self.rect.w - total) // 2
        y = self.rect.bottom - box_size - 6

        for i in range(max_niv):
            cb = pygameui.Checkbox(
                (start_x + i * (box_size + gap), y),
                width=box_size,
                height=box_size,
                style="square",
                color=(80, 200, 100),
                background_color=(60, 40, 80),
                border_color=(150, 100, 150),
                border_width=1
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

        if selected:
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((255, 220, 50, 120))
            surface.blit(s, (r.x, r.y))
            pygame.draw.rect(surface, (255, 200, 0), r, 2, border_radius=6)
        else:
            pygame.draw.rect(surface, (80, 50, 100), r, 1, border_radius=6)

        txt = self.font.render(self.label, True, (240, 230, 255))
        surface.blit(txt, (r.x + 6, r.y + 6))

        if self.niveau >= self.max_niveau:
            p = self.font_small.render("MAX", True, (80, 200, 80))
            surface.blit(p, (r.x + 6, r.y + 24))

        self.sync_checkboxes()
        for cb in self.checkboxes:
            shifted_rect = cb._rect.move(ox, oy)
            orig = cb._rect
            cb._rect = shifted_rect
            cb.draw(surface)
            cb._rect = orig


class ShopPowerUp:
    def __init__(self):
        pygame.font.init()

        self.cells = [PowerUpCell(x, y, w, h, p) for (x, y, w, h, p) in CELLS_LAYOUT]
        self.selected = None

        self.font_money = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_button = pygame.font.SysFont("Arial", 16, bold=True)

        self.buy_rect = pygame.Rect(170, 430, 160, 43)

        try:
            self.bg = pygame.image.load("Images/Interface/fond_power_up.png").convert_alpha()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((40, 25, 60))

    def draw(self, win, player_money, offset=(0, 0)):
        ox, oy = offset
        win.blit(self.bg, (ox, oy))

        for cell in self.cells:
            cell.draw(win, selected=(cell is self.selected), offset=offset)

        money = self.font_money.render(f"Or : {player_money}", True, (255, 230, 80))
        win.blit(money, (ox + WIDTH - 110, oy + HEIGHT - 30))

        if self.selected:
            prix = self.selected.prix_prochain

            bx = ox + self.buy_rect.x
            by = oy + self.buy_rect.y
            rect = pygame.Rect(bx, by, self.buy_rect.w, self.buy_rect.h)

            if prix is None:
                color = (100, 100, 100)
                texte = "MAX"
            elif player_money >= prix:
                color = (80, 180, 100)
                texte = f"Acheter ({prix} or)"
            else:
                color = (180, 80, 80)
                texte = f"{prix} or"

            pygame.draw.rect(win, color, rect, border_radius=8)
            txt = self.font_button.render(texte, True, (255, 255, 255))
            win.blit(txt, (bx + 10, by + 10))

    def update(self, events, win, mouse_pos, mouse_pressed,
               player_money, player, offset=(0, 0)):

        self.draw(win, player_money, offset)

        ox, oy = offset

        buy_clicked = False
        data.playerInventory.update(charger_powerups_joueur(player))
        if self.selected:
            bx = ox + self.buy_rect.x
            by = oy + self.buy_rect.y
            rect = pygame.Rect(bx, by, self.buy_rect.w, self.buy_rect.h)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect.collidepoint(event.pos):
                        buy_clicked = True

        if buy_clicked:
            player_money = self._buy(player_money, player)
        else:
            for cell in self.cells:
                shifted = cell.rect.move(ox, oy)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
        sauvegarder_powerup(player,self.selected.power,data.playerInventory[self.selected.power])
        if not isinstance(player, str):
            apply_powerups(player)

        replace_player_money(player, player_money)

        return player_money


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
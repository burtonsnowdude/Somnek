import pygame
import pygameui
import variable_power_up as data
from class_Button import Button

WIDTH, HEIGHT = 550, 500

FONT_BUTTON = pygame.font.SysFont(None, 36)

shop_bg_img = pygame.image.load("Images/power_shop.png")
shop_bg_img = pygame.transform.scale(shop_bg_img, (WIDTH, HEIGHT))

current_price = 0
selected_item = None


checkboxes = [
    pygameui.Checkbox((60, 210), 40, 40, style="cross"),
    pygameui.Checkbox((100, 210), 40, 40, style="cross"),
    pygameui.Checkbox((140, 210), 40, 40, style="cross"),
]

def sync_checkboxes():
    for cb in checkboxes:
        power = "Pouvoir"  # adapte si plusieurs powers
        level = checkboxes.index(cb)

        if data.playerInventory[power] > level:
            cb.set_checked(True)
        else:
            cb.set_checked(False)

class ShopItem:
    def __init__(self, x, y, w, h, power, level):
        self.rect = pygame.Rect(x, y, w, h)
        self.power = power
        self.level = level

    def update(self, events):
        global selected_item, current_price

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    selected_item = self
                    prices, _ = data.liste_power_up[self.power]
                    current_price = prices[self.level]

    def draw(self, surface):
        pygame.draw.rect(surface, (120, 120, 120), self.rect, 3)

        if selected_item == self:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)

shop_items = [
    ShopItem(60, 130, 120, 80, "Pouvoir", 0),
    ShopItem(200, 130, 120, 80, "Pouvoir", 1),
    ShopItem(340, 130, 120, 80, "Pouvoir", 2),
]
Boutons = Button("Acheter", "acheter", 390, 450, 120, 40, FONT_BUTTON)


def open_shop(events, WIN, mouse_pos, mouse_pressed, close_button, FONT_BUTTON):
    global current_price
    sync_checkboxes()
    WIN.blit(shop_bg_img, (0, 0))

    # IMPORTANT : update + draw pygameui
    for item in shop_items:
        item.update(events)
        item.draw(WIN)

    for cb in checkboxes:
        cb.update(events)
        cb.draw(WIN)

    price_text = FONT_BUTTON.render(f"Prix: {current_price}", True, (255, 255, 255))
    WIN.blit(price_text, (350, 400))
    Boutons.draw(WIN, mouse_pos)

    if Boutons.is_clicked(mouse_pos, mouse_pressed):
        pygame.time.delay(150)
        buy_selected()
    close_button.draw(WIN, mouse_pos)

    return close_button.is_clicked(mouse_pos, mouse_pressed)


def buy_selected():
    global selected_item

    if not selected_item:
        return

    power = selected_item.power
    level = selected_item.level

    prices, _ = data.liste_power_up[power]

    if data.playerInventory[power] != level:
        return

    price = prices[level]

    if data.player_money >= price:
        data.player_money -= price
        data.playerInventory[power] += 1
        sync_checkboxes()
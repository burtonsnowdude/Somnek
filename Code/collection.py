import pygame
import variable_power_up as data
from Class_Button import Button

pygame.init()

WIDTH, HEIGHT = 550, 400
WOR= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collection")

FONT_BUTTON = pygame.font.SysFont(None, 24)


shop_bg_img = pygame.image.load("Images/Interface/Collection.png")
shop_bg_img = pygame.transform.scale(shop_bg_img, (WIDTH, HEIGHT))


ITEM_SIZE = 55
AFFICH_SIZE = (250, 70)


def load_small(path):
    return pygame.transform.scale(pygame.image.load(path), (ITEM_SIZE, ITEM_SIZE))

def load_big(path):
    return pygame.transform.scale(pygame.image.load(path), AFFICH_SIZE)

# petites images
img_palette = load_small("Images/Armes_items/palette.png")
img_berserk = load_small("Images/Armes_items/berserk.png")
img_nain = load_small("Images/Armes_items/nain.png")
inconnu = load_small("Images/Armes_items/inconnu.png")

# grandes images
palette_affich = load_big("Images/Interface/palette_affich.png")
berserk_affich = load_big("Images/Interface/berserk_affich.png")
pas_trouve = load_big("Images/Interface/pas_trouvé.png")


liste_all_item = {
    "Palette": (img_palette, palette_affich),
    "Berserk": (img_berserk, berserk_affich),
    "Nain riche": (img_nain, pas_trouve)
}

player_Inventory = ["Palette", "Berserk"]


START_X, START_Y = 70, 60
COLS, ROWS = 6, 4
SPACING_X, SPACING_Y = 75, 70

selected_item = None


class ShopItem:
    def __init__(self, name, image, affich, x, y):
        self.name = name
        self.image = image
        self.affich = affich
        self.rect = pygame.Rect(x, y, ITEM_SIZE, ITEM_SIZE)

    def update(self, events):
        global selected_item
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    selected_item = self

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        pygame.draw.rect(surface, (80, 80, 80), self.rect, 2)

        if selected_item == self:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)

def create_items():
    items = []
    i = 0
    keys = list(liste_all_item.keys())

    for row in range(ROWS):
        for col in range(COLS):

            x = START_X + col * SPACING_X
            y = START_Y + row * SPACING_Y

            if i < len(keys):
                name = keys[i]

                if name in player_Inventory:
                    image, affich = liste_all_item[name]
                else:
                    image = inconnu
                    affich = pas_trouve

                items.append(ShopItem(name, image, affich, x, y))
                i += 1
            else:
                items.append(ShopItem("?", inconnu, pas_trouve, x, y))

    return items



def open_collection(events, WIN, mouse_pos, mouse_pressed, close_button):
    global items, selected_item

    # fond
    WIN.blit(shop_bg_img, (0, 0))

    # update + draw items
    for item in items:
        item.update(events)
        item.draw(WIN)
    if selected_item:
        WIN.blit(selected_item.affich, (150, 300))  # ajuste si besoin
    # bouton fermer
    close_button.draw(WIN, mouse_pos)

    return close_button.is_clicked(mouse_pos, mouse_pressed)

btn_close = Button("X", "close", 500, 20, 40, 40, FONT_BUTTON)
clock = pygame.time.Clock()

items = create_items()
if __name__ == "__main__":
  running = True

  while running:
    clock.tick(60)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    
    for item in items:
        item.update(events)

    
    WOR.blit(shop_bg_img, (0, 0))

    for item in items:
        item.draw(WOR)

    
    if selected_item:
        WOR.blit(selected_item.affich, (170, 330))

    btn_close.draw(WOR, mouse_pos)

    if btn_close.is_clicked(mouse_pos, mouse_pressed):
        pygame.time.delay(150)
        running = False

    


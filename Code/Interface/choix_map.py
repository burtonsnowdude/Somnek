import pygame

import Interface.variable_power_up as data
from Interface.Class_Button import Button

pygame.init()

WOR = pygame.display.set_mode((500, 500))
pygame.display.set_caption("selection de map")

FONT_BUTTON = pygame.font.SysFont(None, 24)


selection_bg_img = pygame.image.load("Images/Interface/choix_map.png")
selection_bg_img_img = pygame.transform.scale(selection_bg_img, (500, 500))

img_map_metro = pygame.image.load("Images/Interface/map_metro.png")
img_map_cour = pygame.image.load("Images/Interface/map_cour.png")
img_map_rue = pygame.image.load("Images/Interface/rue_metro.png")

player_Inventory = ["Metro", "Cour"]
inconnu = pygame.image.load("Images/Interface/pas_map.png")
liste_all_map= { "Metro": (img_map_metro), "Rue" : (img_map_rue), "Cour" : (img_map_cour)}

selected_item = None
AFFICH_SIZE = (250, 70)

ITEM_SIZE = 30
START_X = 67
START_Y = 49     
COLS = 8
ROWS = 6        
SPACING_X = 50    
SPACING_Y = 38  
START = Button("START", "entrer", 200, 395, 210, 60, FONT_BUTTON)

class ShopItem:
    def __init__(self, name, image,  x, y):
        self.name = name
        self.image = image
        
        self.rect = pygame.Rect(x, y, 41, 30)

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
    keys = list(liste_all_map.keys())

    for row in range(ROWS):
        for col in range(COLS):

            x = START_X + row
            y = START_Y + row * SPACING_Y

            if i < len(keys):
                name = keys[i]

                if name in player_Inventory:
                    image = liste_all_map[name]
                else:
                    image = inconnu
                    

                items.append(ShopItem(name, image, x, y))
                i += 1
            else:
                items.append(ShopItem("?", inconnu, x, y))

    return items

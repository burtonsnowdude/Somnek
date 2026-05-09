import pygame
from Interface.Class_Button import Button

pygame.init()

WIDTH, HEIGHT = 550, 400
FONT_BUTTON = pygame.font.SysFont(None, 24)

shop_bg_img = pygame.image.load("Images/Interface/choix_du_personnage.png")
shop_bg_img = pygame.transform.scale(shop_bg_img, (WIDTH, HEIGHT))

def load_small(path):
    return pygame.transform.scale(pygame.image.load(path), (60, 60))

def load_big(path):
    return pygame.transform.scale(pygame.image.load(path), (250, 70))

img_fille = load_small("Images/Persos/fille_populaire_l.png")
img_nonne = load_small("Images/Persos/nonne_r.png")
img_nerd = load_small("Images/Persos/nerd_r.png") 

nerd_affich = load_big("Images/Interface/affiche_perso_soeur.png")  
fille_affich = load_big("Images/Interface/affiche_perso_fille.png")
nonne_affich = load_big("Images/Interface/affiche_perso_soeur.png")

img_arme_base_fille = load_small("Images/Armes_items/gloss_rose.png")
img_arme_base_nonne = load_small("Images/Armes_items/croix_de_base.png")
img_arme_base_nerd = load_small("Images/Armes_items/epee_bleue_img.png")
armes = {
    "Fille_populaire": img_arme_base_fille,
    "Nonne": img_arme_base_nonne,
    "Nerd": img_arme_base_nerd
}

liste_all_charac = {
    "Fille_populaire": (img_fille, fille_affich),
    "Nonne": (img_nonne, nonne_affich),
    "Nerd": (img_nerd, nonne_affich) 
}

player_Inventory_charact = ["Fille_populaire"]  

selected_item = None

def pas_trouve(img):
    s = img.copy()
    s.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
    return s

class ShopItem:
    def __init__(self, name, image, affich, x, y):
        self.name = name
        self.base_image = image
        self.image = image
        self.affich = affich
        self.rect = pygame.Rect(x, y, 90, 90)
        self.unlocked = name in player_Inventory_charact
        self.weapon = armes.get(name, None)
        if not self.unlocked:
            self.image = pas_trouve(self.base_image)

    def update(self, events):
        global selected_item
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    selected_item = self

    def draw(self, surface):
        pygame.draw.rect(surface, (60, 60, 60), self.rect)
        pygame.draw.rect(surface, (120, 120, 120), self.rect, 2)
        img_rect = self.image.get_rect(center=self.rect.center)
        surface.blit(self.image, img_rect)
        if self.weapon and self.unlocked:
            surface.blit(self.weapon, (self.rect.right - 25, self.rect.bottom - 25))
        if selected_item == self:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)

def create_items():
    items = []
    spacing = 140
    start_x = 120
    y = 100
    for i, name in enumerate(liste_all_charac.keys()):
        image, affich = liste_all_charac[name]
        x = start_x + i * spacing
        items.append(ShopItem(name, image, affich, x, y))
    return items

items = create_items()

btn_confirm = Button("Confirmer", "confirm", 330, 360, 140, 45, FONT_BUTTON)
btn_unlock = Button("Débloquer", "unlock", 330, 360, 140, 45, FONT_BUTTON)

def draw_selected_panel(surface, selected_item, font):
    if not selected_item:
        return
    pygame.draw.rect(surface, (120, 120, 120), (120, 300, 300, 120))
    pygame.draw.rect(surface, (255, 200, 0), (120, 300, 300, 120), 2)
    surface.blit(selected_item.affich, (130, 305))
    small_img = pygame.transform.scale(selected_item.base_image, (40, 40))
    if not selected_item.unlocked:
        shadow = small_img.copy()
        shadow.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
        surface.blit(shadow, (135, 325))
    else:
        surface.blit(small_img, (135, 325))
    if selected_item.weapon and selected_item.unlocked:
        weapon_img = pygame.transform.scale(selected_item.weapon, (30, 30))
        surface.blit(weapon_img, (180, 330))
    txt = font.render(selected_item.name, True, (255, 255, 255))
    surface.blit(txt, (230, 315))
    if selected_item.unlocked:
        btn_confirm.draw(surface, (0, 0))
    else:
        btn_unlock.draw(surface, (0, 0))

def handle_panel_buttons(mouse_pos, mouse_pressed, selected_item):
    if not selected_item:
        return None
    if selected_item.unlocked and btn_confirm.is_clicked(mouse_pos, mouse_pressed):
        print("Perso confirmé :", selected_item.name)
        return ("start_game", selected_item.name)
    if not selected_item.unlocked and btn_unlock.is_clicked(mouse_pos, mouse_pressed):
        print("Déblocage :", selected_item.name)
        selected_item.unlocked = True
        selected_item.image = selected_item.base_image
    return None

def open_start(WIN, events, mouse_pos, mouse_pressed, btn_close, font):
    global selected_item

    overlay = pygame.Surface((WIN.get_width(), WIN.get_height()))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    WIN.blit(overlay, (0, 0))
    WIN.blit(shop_bg_img, (0, 0))

    for item in items:
        item.update(events)
        item.draw(WIN)

    draw_selected_panel(WIN, selected_item, font)

    result = handle_panel_buttons(mouse_pos, mouse_pressed, selected_item)
    if result is not None and result[0] == "start_game":
        perso = result[1]  # ← corrigé (était "perso" non défini)
        from Interface.choix_map import open_choix_map
        WIN.fill((0, 0, 0))
        pygame.display.flip()
        map_choisie = open_choix_map()
        return ("start_game", perso, map_choisie)

    btn_close.draw(WIN, mouse_pos)
    if btn_close.is_clicked(mouse_pos, mouse_pressed):
        return "close"

    return None
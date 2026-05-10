import pygame
from Interface.Class_Button import Button
from Fichiers_variables.progression import persos_debloques, init_progression
from Fichiers_variables.gestion_fichiers import det_noms

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
img_nerd  = load_small("Images/Persos/nerd_r.png")

nerd_affich  = load_big("Images/Interface/affiche_perso_soeur.png")
fille_affich = load_big("Images/Interface/affiche_perso_fille.png")
nonne_affich = load_big("Images/Interface/affiche_perso_soeur.png")

img_arme_base_fille = load_small("Images/Armes_items/gloss_rose.png")
img_arme_base_nonne = load_small("Images/Armes_items/croix_de_base.png")
img_arme_base_nerd  = load_small("Images/Armes_items/epee_bleue_img.png")

armes = {
    "Fille_populaire": img_arme_base_fille,
    "Nonne":           img_arme_base_nonne,
    "Nerd":            img_arme_base_nerd,
}

liste_all_charac = {
    "Fille_populaire": (img_fille, fille_affich),
    "Nonne":           (img_nonne, nonne_affich),
    "Nerd":            (img_nerd,  nerd_affich),
}

selected_item = None


def img_grisee(img):
    """Retourne une copie noircie de l'image (pour les persos verrouillés)."""
    s = img.copy()
    s.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT)
    return s


# ─────────────────────────────────────────────
#  ITEM PERSO
# ─────────────────────────────────────────────

class ShopItem:
    def __init__(self, name, image, affich, x, y):
        self.name        = name
        self.base_image  = image
        self.affich      = affich
        self.rect        = pygame.Rect(x, y, 90, 90)
        self.weapon      = armes.get(name, None)
        self.unlocked    = False
        self.image       = img_grisee(image)         # grisée par défaut
        self._image_grise = img_grisee(image)        # cache

    def refresh_unlock(self, persos_unlock: list):
        """Met à jour le statut ET l'image à chaque frame (sans cache foireux)."""
        self.unlocked = self.name in persos_unlock
        self.image    = self.base_image if self.unlocked else self._image_grise

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

        if self.unlocked and self.weapon:
            surface.blit(self.weapon, (self.rect.right - 25, self.rect.bottom - 25))

        if selected_item == self:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)


def create_items():
    items = []
    spacing = 140
    start_x = 120
    y       = 100
    for i, name in enumerate(liste_all_charac.keys()):
        image, affich = liste_all_charac[name]
        x = start_x + i * spacing
        items.append(ShopItem(name, image, affich, x, y))
    return items


items = create_items()

btn_confirm = Button("Confirmer", "confirm", 330, 360, 140, 45, FONT_BUTTON)


# ─────────────────────────────────────────────
#  PANNEAU DE SÉLECTION
# ─────────────────────────────────────────────

def draw_selected_panel(surface, selected_item, font):
    if not selected_item:
        return

    pygame.draw.rect(surface, (120, 120, 120), (120, 300, 300, 120))
    pygame.draw.rect(surface, (255, 200, 0),   (120, 300, 300, 120), 2)
    surface.blit(selected_item.affich, (130, 305))

    small_img = pygame.transform.scale(selected_item.base_image, (40, 40))
    if not selected_item.unlocked:
        shadow = small_img.copy()
        shadow.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT)
        surface.blit(shadow, (135, 325))
    else:
        surface.blit(small_img, (135, 325))

    if selected_item.weapon and selected_item.unlocked:
        weapon_img = pygame.transform.scale(selected_item.weapon, (30, 30))
        surface.blit(weapon_img, (180, 330))

    txt = font.render(selected_item.name.replace("_", " "), True, (255, 255, 255))
    surface.blit(txt, (230, 315))

    if selected_item.unlocked:
        btn_confirm.draw(surface, (0, 0))


def handle_panel_buttons(mouse_pos, mouse_pressed, selected_item):
    if not selected_item:
        return None
    if selected_item.unlocked and btn_confirm.is_clicked(mouse_pos, mouse_pressed):
        print("Perso confirmé :", selected_item.name)
        return ("start_game", selected_item.name)
    return None


# ─────────────────────────────────────────────
#  ENTRÉE PRINCIPALE
# ─────────────────────────────────────────────

# Cache pour éviter d'initialiser la progression à chaque frame
_progression_init_pour = set()


def open_start(WIN, events, mouse_pos, mouse_pressed, btn_close, font, joueur):
    """
    Affiche la sélection de personnage. `joueur` : nom du joueur courant.
    """
    global selected_item

    # Initialise la progression du joueur (une seule fois)
    if joueur not in _progression_init_pour:
        try:
            noms, _ = det_noms()
            init_progression(joueur, noms)
        except Exception as e:
            print(f"[Progression] Init impossible : {e}")
        _progression_init_pour.add(joueur)

    # Maj du statut de chaque perso depuis le CSV
    persos_unlock = persos_debloques(joueur)
    for item in items:
        item.refresh_unlock(persos_unlock)

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
        perso = result[1]
        from Interface.choix_map import open_choix_map
        WIN.fill((0, 0, 0))
        pygame.display.flip()
        map_choisie = open_choix_map(joueur)
        if map_choisie is None:
            return None
        return ("start_game", perso, map_choisie)

    btn_close.draw(WIN, mouse_pos)
    if btn_close.is_clicked(mouse_pos, mouse_pressed):
        return "close"

    return None
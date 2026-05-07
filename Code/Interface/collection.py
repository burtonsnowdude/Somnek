import pygame
import Interface.variable_power_up as data
from Interface.Class_Button import Button
from Fichiers_variables.gestion_fichiers import liste_armes_acquises
pygame.init()

WOR = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Collection")

FONT_BUTTON = pygame.font.SysFont(None, 24)


shop_bg_img = pygame.image.load("Images/Interface/Collection.png")
shop_bg_img = pygame.transform.scale(shop_bg_img, (500, 500))



AFFICH_SIZE = (250, 70)

ITEM_SIZE = 30
START_X = 67
START_Y = 49     # ← plus bas
COLS = 8
ROWS = 6          # ← supprime la dernière ligne
SPACING_X = 50    # ← réduit
SPACING_Y = 38  

def load_small(path):
    return pygame.transform.scale(pygame.image.load(path), (ITEM_SIZE, ITEM_SIZE))

def load_big(path):
    return pygame.transform.scale(pygame.image.load(path), AFFICH_SIZE)

# petites images
img_palette = load_small("Images/Armes_items/palette.png")
img_berserk = load_small("Images/Armes_items/berserk.png")
img_nain = load_small("Images/Armes_items/nain.png")
inconnu = load_small("Images/Armes_items/inconnu.png")
img_lunettes_cassees = load_small("Images/Armes_items/lunettes_cassees.png")
img_berserk = load_small("Images/Armes_items/berserk.png")
img_cahier_de_nsi = load_small("Images/Armes_items/cahier_de_nsi.png")
img_nain = load_small("Images/Armes_items/nain.png")
img_chaussettes = load_small("Images/Armes_items/chaussettes.png")
img_souris = load_small("Images/Armes_items/souris.png")
img_cle_usb = load_small("Images/Armes_items/cle_usb.png")
img_pistolets = load_small("Images/Armes_items/pistolets.png")
img_chariot_violet = load_small("Images/Armes_items/chariot_violet.png")
img_pomme_scientifique = load_small("Images/Armes_items/pomme_scientifique.png")
img_vody = load_small("Images/Armes_items/vody.png")
img_ambroisie = load_small("Images/Armes_items/ambroisie.png")
img_nokia = load_small("Images/Armes_items/nokia.png")
img_trefle = load_small("Images/Armes_items/trefle.png")
img_armure = load_small("Images/Armes_items/armure de bronze.png")
img_console = load_small("Images/Armes_items/console.png")
img_serviette = load_small("Images/Armes_items/serviette_nettoyante.png")
# FILLE POPULAIRE
img_gloss_rose = load_small("Images/Armes_items/gloss_rose.png")
img_ticket = load_small("Images/Armes_items/ticket.png")
img_highlighter = load_small("Images/Armes_items/highlighter.png")
img_faux_cils = load_small("Images/Armes_items/faux_cils.png")
img_bracelet_soeur = load_small("Images/Armes_items/bracelet_soeur.png")
img_carte_bleu = load_small("Images/Armes_items/carte_bleu.png")
img_pilule_verte = load_small("Images/Armes_items/pilule_verte.png")
img_mousse_vanille = load_small("Images/Armes_items/mousse_vanille.png")
img_demaquillant = load_small("Images/Armes_items/demaquillant.png")
img_parfum_dioru = load_small("Images/Armes_items/parfum_dioru.png")
img_minuteur = load_small("Images/Armes_items/minuteur.png")
img_chew_gum = load_small("Images/Armes_items/chew_gum.png")
img_crop_top_rose = load_small("Images/Armes_items/crop_top_rose.png")
img_talon_noir = load_small("Images/Armes_items/talon_noir.png")
img_talon_louboutin = load_small("Images/Armes_items/talon_louboutin.png")
img_iphone_2000 = load_small("Images/Armes_items/iphone 2000.png")
img_pass_navigo = load_small("Images/Armes_items/pass navigo.png")
img_fer_a_lisser = load_small("Images/Armes_items/fer_à_lisser.png")
img_jean_stanley = load_small("Images/Armes_items/jean_stanley_cup.png")
img_chargeur = load_small("Images/Armes_items/chargeur.png")
# NONNE
img_croix_de_base = load_small("Images/Armes_items/croix_de_base.png")
img_couronne = load_small("Images/Armes_items/couronne.png")
img_feu_saint = load_small("Images/Armes_items/projectile/feu esprit sain.png")
img_bougie = load_small("Images/Armes_items/bougie.png")
img_bourse = load_small("Images/Armes_items/bourse.png")
img_ostie = load_small("Images/Armes_items/ostie.png")
img_boule_denergie = load_small("Images/Armes_items/boule_denergie.png")
img_eau_benite = load_small("Images/Armes_items/eau_bénite.png")
img_mocassin = load_small("Images/Armes_items/mocassin.png")
img_halo_lumineux = load_small("Images/Armes_items/halo_lumineux.png")

# grandes images
palette_affich = load_big("Images/Interface/palette_affich.png")
berserk_affich = load_big("Images/Interface/berserk_affich.png")
pas_trouve = load_big("Images/Interface/pas_trouvé.png")

"""
liste_all_item = {
    "Palette": (img_palette, palette_affich),
    "Berserk": (img_berserk, berserk_affich),
    "Nain riche": (img_nain, pas_trouve),
    "Lunettes cassées": (img_lunettes_cassees, palette_affich),
    "Cahier de NSI": (img_cahier_de_nsi, palette_affich),
    "Chaussettes": (img_chaussettes, palette_affich),
    "Souris": (img_souris, palette_affich),
    "Clé USB": (img_cle_usb, palette_affich),
    "Pistolets": (img_pistolets, palette_affich),
    "Chariot violet": (img_chariot_violet, palette_affich),
    "Pomme scientifique": (img_pomme_scientifique, palette_affich),
    "Vody": (img_vody, palette_affich),
    "Ambroisie": (img_ambroisie, palette_affich),
    "Nokia": (img_nokia, palette_affich),
    "Trèfle": (img_trefle, palette_affich),
    "Armure": (img_armure, palette_affich),
    "Console": (img_console, palette_affich),
    "Serviette nettoyante": (img_serviette, palette_affich),
    # FILLE POPULAIRE
    "Gloss rose": (img_gloss_rose, palette_affich),
    "Ticket": (img_ticket, palette_affich),
    "Highlighter": (img_highlighter, palette_affich),
    "Faux cils": (img_faux_cils, palette_affich),
    "Bracelet soeur": (img_bracelet_soeur, palette_affich),
    "Carte bleu": (img_carte_bleu, palette_affich),
    "Pilule verte": (img_pilule_verte, palette_affich),
    "Mousse vanille": (img_mousse_vanille, palette_affich),
    "Démaquillant": (img_demaquillant, palette_affich),
    "Parfum Dioru": (img_parfum_dioru, palette_affich),
    "Minuteur": (img_minuteur, palette_affich),
    "Chew gum": (img_chew_gum, palette_affich),
    "Crop top rose": (img_crop_top_rose, palette_affich),
    "Talon noir": (img_talon_noir, palette_affich),
    "Talon Louboutin": (img_talon_louboutin, palette_affich),
    "iPhone 2000": (img_iphone_2000, palette_affich),
    "Pass Navigo": (img_pass_navigo, palette_affich),
    "Fer à lisser": (img_fer_a_lisser, palette_affich),
    "Jean Stanley": (img_jean_stanley, palette_affich),
    "Chargeur": (img_chargeur, palette_affich),
    # NONNE
    "Croix de base": (img_croix_de_base, palette_affich),
    "Couronne": (img_couronne, palette_affich),
    "Feu saint": (img_feu_saint, palette_affich),
    "Bougie": (img_bougie, palette_affich),
    "Bourse": (img_bourse, palette_affich),
    "Ostie": (img_ostie, palette_affich),
    "Boule d'énergie": (img_boule_denergie, palette_affich),
    "Eau bénite": (img_eau_benite, palette_affich),
    "Mocassin": (img_mocassin, palette_affich),
    "Halo lumineux": (img_halo_lumineux, palette_affich),
}
"""
liste_all_item = {
    "Palette": (img_palette, palette_affich),
    "Berserk": (img_berserk, berserk_affich),

    "Petit_nain_roux": (img_nain, pas_trouve),

    "Lunettes_cassees": (img_lunettes_cassees, palette_affich),
    "Souris_pc": (img_souris, palette_affich),
    "Chaussettes_propres": (img_chaussettes, palette_affich),
    "Cahier_NSI": (img_cahier_de_nsi, palette_affich),

    "Vody_Lemonade": (img_vody, palette_affich),
    "Deodorant": (img_serviette, palette_affich),
    "Pomme_scientifique": (img_pomme_scientifique, palette_affich),
    "Armure_de_bronze": (img_armure, palette_affich),

    "Cle_USB": (img_cle_usb, palette_affich),
    "Pistolets": (img_pistolets, palette_affich),
    "Console_allumee": (img_console, palette_affich),

    "Chariot_violet": (img_chariot_violet, palette_affich),
    "Nokia": (img_nokia, palette_affich),
    "Trefle": (img_trefle, palette_affich),
    "Serviette_nettoyante": (img_serviette, palette_affich),

    # FILLE POPULAIRE
    "Gloss_rose": (img_gloss_rose, palette_affich),
    "Chew_gum": (img_chew_gum, palette_affich),
    "Talons_noirs": (img_talon_noir, palette_affich),
    "Bracelet_soeur": (img_bracelet_soeur, palette_affich),
    "Carte_bleue": (img_carte_bleu, palette_affich),
    "Parfum_Dioru": (img_parfum_dioru, palette_affich),
    "Pilule_verte": (img_pilule_verte, palette_affich),
    "Crop_top_rose": (img_crop_top_rose, palette_affich),
    "Coque_trefle": (img_crop_top_rose, palette_affich),
    "Mousse_a_la_vanille": (img_mousse_vanille, palette_affich),
    "Sac_a_main_violet": (img_mousse_vanille, palette_affich),

    # NONNE
    "Croix_marron": (img_croix_de_base, palette_affich),
    "Chapelet": (img_croix_de_base, palette_affich),
    "Mocassin": (img_mocassin, palette_affich),
    "Tableau_sacre": (img_mocassin, palette_affich),
    "Bourse": (img_bourse, palette_affich),
    "Bougie": (img_bougie, palette_affich),
    "Voile": (img_bougie, palette_affich),
    "Huile_benie": (img_bougie, palette_affich),
    "Ostie": (img_ostie, palette_affich),
    "Sac_a_dos_bleu": (img_ostie, palette_affich),
    "Eau_benite": (img_ostie, palette_affich),
}

player_Inventory = [
    "Palette",
    "Berserk",
    "Nain riche",
    "Lunettes cassées",
    "Cahier de NSI",
    "Chaussettes",
    "Souris",
    "Clé USB",
    "Pistolets",
    "Chariot violet",
    "Pomme scientifique",
    "Vody",
    "Ambroisie",
    "Nokia",
    "Trèfle",
    "Armure",
    "Console",
    "Serviette nettoyante",
    "Gloss rose",
    "Ticket",
    "Highlighter",
    "Faux cils",
    "Bracelet soeur",
    "Carte bleu",
    "Pilule verte",
    "Mousse vanille",
    "Démaquillant",
    "Parfum Dioru",
    "Minuteur",
    "Chew gum",
    "Crop top rose",
    "Talon noir",
    "Talon Louboutin",
    "iPhone 2000",
    "Pass Navigo",
    "Fer à lisser",
    "Jean Stanley",
    "Chargeur",
    "Croix de base",
    "Couronne",
    "Feu saint",
    "Bougie",
    "Bourse",
    "Ostie",
    "Boule d'énergie",
    "Eau bénite",
    "Mocassin",
    "Halo lumineux",
]



selected_item = None


class ShopItem:
    def __init__(self, name, image, affich, x, y):
        self.name = name
        self.image = image
        self.affich = affich
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
    joueur = "Daphne"
    player_inventory = liste_armes_acquises(joueur)
    items = []
    i = 0
    keys = list(liste_all_item.keys())

    for row in range(ROWS):
        for col in range(COLS):

            x = START_X + col * SPACING_X
            y = START_Y + row * SPACING_Y

            if i < len(keys):
                name = keys[i]

                if name in player_inventory:
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

    


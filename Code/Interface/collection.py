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

AFFICH_SIZE = (375, 105)
ITEM_SIZE = 30
START_X = 67
START_Y = 49
COLS = 8
ROWS = 6
SPACING_X = 50
SPACING_Y = 38

def load_small(path):
    return pygame.transform.scale(pygame.image.load(path), (ITEM_SIZE, ITEM_SIZE))

def load_big(path):
    return pygame.transform.scale(pygame.image.load(path), AFFICH_SIZE)

# ── Petites images ────────────────────────────────────────────────────────────
img_palette            = load_small("Images/Armes_items/palette.png")
img_berserk            = load_small("Images/Armes_items/berserk.png")
img_nain               = load_small("Images/Armes_items/nain.png")
inconnu                = load_small("Images/Armes_items/inconnu.png")
img_lunettes_cassees   = load_small("Images/Armes_items/lunettes_cassees.png")
img_cahier_de_nsi      = load_small("Images/Armes_items/cahier_de_nsi.png")
img_chaussettes        = load_small("Images/Armes_items/chaussettes.png")
img_souris             = load_small("Images/Armes_items/souris.png")
img_cle_usb            = load_small("Images/Armes_items/cle_usb.png")
img_pistolets          = load_small("Images/Armes_items/pistolets.png")
img_chariot_violet     = load_small("Images/Armes_items/chariot_violet.png")
img_pomme_scientifique = load_small("Images/Armes_items/pomme_scientifique.png")
img_vody               = load_small("Images/Armes_items/vody.png")
img_ambroisie          = load_small("Images/Armes_items/ambroisie.png")
img_nokia              = load_small("Images/Armes_items/nokia.png")
img_trefle             = load_small("Images/Armes_items/trefle.png")
img_armure             = load_small("Images/Armes_items/armure de bronze.png")
img_console            = load_small("Images/Armes_items/console.png")
img_serviette          = load_small("Images/Armes_items/serviette_nettoyante.png")
img_epee_bleue         = load_small("Images/Armes_items/epee_bleue_img.png")
img_epee_enflammee     = load_small("Images/Armes_items/Epee enflamee.png")
img_epee_guts          = load_small("Images/Armes_items/epee_guts.png")
img_ticket             = load_small("Images/Armes_items/ticket.png")
img_apple_watch        = load_small("Images/Armes_items/smart.png")
img_deodorant          = load_small("Images/Armes_items/Deodorant.png")
img_manteau_leopard    = load_small("Images/Armes_items/manteau_leopard.png")
img_jucy               = load_small("Images/Armes_items/jucy.png")

# FILLE POPULAIRE
img_gloss_rose      = load_small("Images/Armes_items/gloss_rose.png")
img_highlighter     = load_small("Images/Armes_items/highlighter.png")
img_faux_cils       = load_small("Images/Armes_items/faux_cils.png")
img_bracelet_soeur  = load_small("Images/Armes_items/bracelet_soeur.png")
img_carte_bleu      = load_small("Images/Armes_items/carte_bleu.png")
img_pilule_verte    = load_small("Images/Armes_items/pilule_verte.png")
img_mousse_vanille  = load_small("Images/Armes_items/mousse_vanille.png")
img_demaquillant    = load_small("Images/Armes_items/demaquillant.png")
img_parfum_dioru    = load_small("Images/Armes_items/parfum_dioru.png")
img_minuteur        = load_small("Images/Armes_items/minuteur.png")
img_chew_gum        = load_small("Images/Armes_items/chew_gum.png")
img_crop_top_rose   = load_small("Images/Armes_items/crop_top_rose.png")
img_talon_noir      = load_small("Images/Armes_items/talon_noir.png")
img_talon_louboutin = load_small("Images/Armes_items/talon_louboutin.png")
img_iphone_2000     = load_small("Images/Armes_items/iphone 2000.png")
img_pass_navigo     = load_small("Images/Armes_items/pass navigo.png")
img_fer_a_lisser    = load_small("Images/Armes_items/fer_à_lisser.png")
img_jean_stanley    = load_small("Images/Armes_items/jean_stanley_cup.png")
img_chargeur        = load_small("Images/Armes_items/chargeur.png")
img_faux_ongles     = load_small("Images/Armes_items/faux_ongles_roses.png")
img_ring_light      = load_small("Images/Armes_items/ring light.png")
img_sac_violet      = load_small("Images/Armes_items/sac_violet.png")

# NONNE
img_croix_de_base  = load_small("Images/Armes_items/croix_de_base.png")
img_couronne       = load_small("Images/Armes_items/couronne.png")
img_feu_saint      = load_small("Images/Armes_items/projectile/feu esprit sain.png")
img_bougie         = load_small("Images/Armes_items/bougie.png")
img_bourse         = load_small("Images/Armes_items/bourse.png")
img_ostie          = load_small("Images/Armes_items/ostie.png")
img_boule_denergie = load_small("Images/Armes_items/boule_denergie.png")
img_eau_benite     = load_small("Images/Armes_items/eau_bénite.png")
img_mocassin       = load_small("Images/Armes_items/mocassin.png")
img_halo_lumineux  = load_small("Images/Armes_items/halo_lumineux.png")
img_medaillon      = load_small("Images/Armes_items/medaillon.png")
img_jalambaya      = load_small("Images/Armes_items/jambalaya.png")
img_aura_divine    = load_small("Images/Armes_items/aura divine.png")
img_lance_sacree   = load_small("Images/Armes_items/lance sacre.png")
img_voile          = load_small("Images/Armes_items/voile.png")
img_huile          = load_small("Images/Armes_items/huile.png")
img_chapelet       = load_small("Images/Armes_items/chapelet.png")
img_tableau_sacre  = load_small("Images/Armes_items/tableau.png")
img_sac_bleu       = load_small("Images/Armes_items/sac_bleu.png")
img_collant        = load_small("Images/Armes_items/collant.png")
img_cape           = load_small("Images/Armes_items/cape.png")
img_coeur          = load_small("Images/Armes_items/coeur.png")

# ── Grandes images ────────────────────────────────────────────────────────────
palette_affich             = load_big("Images/Interface/affiche/palette_affich.png")
berserk_affich             = load_big("Images/Interface/affiche/berserk_affich.png")
nain_affich                = load_big("Images/Interface/affiche/nain_affiche.png")
lunettes_cassees_affich    = load_big("Images/Interface/affiche/lunettes_cassees_affiche.png")
cahier_de_nsi_affich       = load_big("Images/Interface/affiche/cahier_NSI_affiche.png")
chaussettes_affich         = load_big("Images/Interface/affiche/chaussettes_affiche.png")
souris_affich              = load_big("Images/Interface/affiche/souris_affiche.png")
cle_usb_affich             = load_big("Images/Interface/affiche/cle_usb_affiche.png")
pistolets_affich           = load_big("Images/Interface/affiche/pistolets_affiche.png")
chariot_violet_affich      = load_big("Images/Interface/affiche/chariot_affiche.png")
pomme_scientifique_affich  = load_big("Images/Interface/affiche/pomme_affiche.png")
vody_affich                = load_big("Images/Interface/affiche/vody_affiche.png")
deodorant_affich           = load_big("Images/Interface/affiche/deodorant_affiche.png")
ambroisie_affich           = load_big("Images/Interface/affiche/ambroisie_affiche.png")
nokia_affich               = load_big("Images/Interface/affiche/nokia_affiche.png")
trefle_affich              = load_big("Images/Interface/affiche/trefle_affiche.png")
armure_affich              = load_big("Images/Interface/affiche/armure_affiche.png")
console_affich             = load_big("Images/Interface/affiche/console_affiche.png")
serviette_affich           = load_big("Images/Interface/affiche/serviette_affiche.png")
pas_trouve                 = load_big("Images/Interface/affiche/pas_trouvé.png")

# FILLE POPULAIRE
gloss_rose_affich      = load_big("Images/Interface/affiche/gloss_affiche.png")
ticket_affich          = load_big("Images/Interface/affiche/ticket_affiche.png")
highlighter_affich     = load_big("Images/Interface/affiche/highlighter_affiche.png")
faux_cils_affich       = load_big("Images/Interface/affiche/cils_affiche.png")
bracelet_soeur_affich  = load_big("Images/Interface/affiche/bracelet_affiche.png")
carte_bleu_affich      = load_big("Images/Interface/affiche/carte_affiche.png")
pilule_verte_affich    = load_big("Images/Interface/affiche/pilule_affiche.png")
mousse_vanille_affich  = load_big("Images/Interface/affiche/mousse_affiche.png")
demaquillant_affich    = load_big("Images/Interface/affiche/demaquillant_affiche.png")
parfum_dioru_affich    = load_big("Images/Interface/affiche/parfum_affiche.png")
minuteur_affich        = load_big("Images/Interface/affiche/minuteur_affiche.png")
chew_gum_affich        = load_big("Images/Interface/affiche/chew_gum_affiche.png")
crop_top_rose_affich   = load_big("Images/Interface/affiche/crop_top_affiche.png")
talon_noir_affich      = load_big("Images/Interface/affiche/talon_n_affiche.png")
talon_louboutin_affich = load_big("Images/Interface/affiche/talon_l_affiche.png")
iphone_2000_affich     = load_big("Images/Interface/affiche/iphone_affiche.png")
pass_navigo_affich     = load_big("Images/Interface/affiche/pass_affiche.png")
fer_a_lisser_affich    = load_big("Images/Interface/affiche/fer_affiche.png")
jean_stanley_affich    = load_big("Images/Interface/affiche/jean_stanley_affiche.png")
chargeur_affich        = load_big("Images/Interface/affiche/chargeur_affiche.png")

# NONNE
croix_de_base_affich  = load_big("Images/Interface/affiche/croix_affiche.png")
couronne_affich       = load_big("Images/Interface/affiche/couronne_affiche.png")
feu_saint_affich      = load_big("Images/Interface/affiche/feu_affiche.png")
bougie_affich         = load_big("Images/Interface/affiche/bougie_affiche.png")
bourse_affich         = load_big("Images/Interface/affiche/bourse_affiche.png")
voile_affiche         = load_big("Images/Interface/affiche/voile_affiche.png")
huile_affich          = load_big("Images/Interface/affiche/huile_affiche.png")
ostie_affich          = load_big("Images/Interface/affiche/hostie_affiche.png")
boule_denergie_affich = load_big("Images/Interface/affiche/boule_energie_affiche.png")
eau_benite_affich     = load_big("Images/Interface/affiche/eau_affiche.png")
mocassin_affich       = load_big("Images/Interface/affiche/mocassin_affiche.png")
halo_lumineux_affich  = load_big("Images/Interface/affiche/halo_affiche.png")


liste_all_item = {
    
    "Lunettes_cassees":   (img_lunettes_cassees,   lunettes_cassees_affich),
    "Souris_pc":          (img_souris,             souris_affich),
    "Chaussettes_propres":(img_chaussettes,        chaussettes_affich),
    "Cahier_NSI":         (img_cahier_de_nsi,      cahier_de_nsi_affich),
    "Vody_Lemonade":      (img_vody,               vody_affich),
    "Deodorant":          (img_deodorant,           deodorant_affich),
    "Pomme_scientifique": (img_pomme_scientifique, pomme_scientifique_affich),
    "Petit_nain_roux":    (img_nain,               pas_trouve),
    "Armure_chevalier":   (img_armure,             armure_affich),
    "Pantalon_beige":     (img_chaussettes,        pas_trouve),
    "Apple_Watch":        (img_apple_watch,        pas_trouve),
    "Serviette_nettoyante":(img_serviette,         serviette_affich),
    "Nokia":              (img_nokia,              nokia_affich),
    "Trefle":             (img_trefle,             trefle_affich),

    # ── NERD armes 
    "Epee_bleue":         (img_epee_bleue,         pas_trouve),
    "Cle_USB":            (img_cle_usb,            cle_usb_affich),
    "Epee_enflammee":     (img_epee_enflammee,     pas_trouve),
    "Pistolets":          (img_pistolets,          pistolets_affich),
    "Ticket_de_metro":    (img_ticket,             ticket_affich),
    "Epee_de_Guts":       (img_epee_guts,          pas_trouve),
    "Console_allumee":    (img_console,            console_affich),

    # ── FILLE POPULAIRE
    "Chew_gum":           (img_chew_gum,           chew_gum_affich),
    "Talons_noirs":       (img_talon_noir,         talon_noir_affich),
    "Carte_bleue":        (img_carte_bleu,         carte_bleu_affich),
    "Parfum_Dioru":       (img_parfum_dioru,       parfum_dioru_affich),
    "Pilule_verte":       (img_pilule_verte,       pilule_verte_affich),
    "Crop_top_rose":      (img_crop_top_rose,      crop_top_rose_affich),
    "Coque_trefle":       (img_trefle,             trefle_affich),
    "Mousse_vanille":     (img_mousse_vanille,     mousse_vanille_affich),
    "Sac_main_violet":    (img_sac_violet,         pas_trouve),
    "Chargeur":           (img_chargeur,           chargeur_affich),
    "Iphone_2000":        (img_iphone_2000,        iphone_2000_affich),
    "Minuteur":           (img_minuteur,           minuteur_affich),
    "Ambroisie":          (img_ambroisie,          ambroisie_affich),
    "Ensemble_juicy":     (img_jucy,               pas_trouve),
    "Manteau_leopard":    (img_manteau_leopard,    pas_trouve),
    "Talon_louboutin":    (img_talon_louboutin,    talon_louboutin_affich),
    "Jean_stanley":       (img_jean_stanley,       jean_stanley_affich),
    "Gloss_rose":         (img_gloss_rose,         gloss_rose_affich),
    "Faux_cils":          (img_faux_cils,          faux_cils_affich),
    "Faux_ongles_roses":  (img_faux_ongles,        pas_trouve),
    "Bracelet_de_sa_soeur":(img_bracelet_soeur,    bracelet_soeur_affich),
    "Fer_a_lisser":       (img_fer_a_lisser,       fer_a_lisser_affich),
    "Pass_Navigo":        (img_pass_navigo,        pass_navigo_affich),
    "Ring_light":         (img_ring_light,         pas_trouve),
    "Highlighter":        (img_highlighter,        highlighter_affich),


    "Eau_benite":         (img_eau_benite,         eau_benite_affich),
    "Chapelet":           (img_chapelet,           croix_de_base_affich),
    "Mocassin":           (img_mocassin,           mocassin_affich),
    "Tableau_sacre":      (img_tableau_sacre,      croix_de_base_affich),
    "Bourse":             (img_bourse,             bourse_affich),
    "Bougie":             (img_bougie,             bougie_affich),
    "Voile":              (img_voile,              voile_affiche),
    "Huile_benediction":  (img_huile,              huile_affich),
    "Ostie":              (img_ostie,              ostie_affich),
    "Sac_a_dos_bleu":     (img_sac_bleu,           eau_benite_affich),
    "Nokia":              (img_nokia,              nokia_affich),
    "Boule_energie":      (img_boule_denergie,     boule_denergie_affich),
    "Coeur":              (img_coeur,              pas_trouve),
    "Cape":               (img_cape,               pas_trouve),
    "Collant":            (img_collant,            pas_trouve),
    "Halo":               (img_halo_lumineux,      halo_lumineux_affich),

    
    "Croix_marron":             (img_croix_de_base,  croix_de_base_affich),
    "Feu_de_l'Esprit_Saint":    (img_feu_saint,      feu_saint_affich),
    "Medaille_de_bapteme":      (img_medaillon,      pas_trouve),
    "Coiffe_de_rameau":         (img_couronne,       couronne_affich),
    "Lance_sacree":             (img_lance_sacree,   pas_trouve),
    "Aura_divine":              (img_aura_divine,    pas_trouve),
    "JALAMBAYA":                (img_jalambaya,      pas_trouve),
}

selected_item = None


class ShopItem:
    def __init__(self, name, image, affich, x, y):
        self.name  = name
        self.image = image
        self.affich = affich
        self.rect  = pygame.Rect(x, y, 41, 30)

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


def create_items(joueur):
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
                    image  = inconnu
                    affich = pas_trouve
                items.append(ShopItem(name, image, affich, x, y))
                i += 1
            else:
                items.append(ShopItem("?", inconnu, pas_trouve, x, y))

    return items


def open_collection(events, WIN, mouse_pos, mouse_pressed, close_button, joueur):
    global selected_item

    items = create_items(joueur)

    WIN.blit(shop_bg_img, (0, 0))

    for item in items:
        item.update(events)
        item.draw(WIN)

    if selected_item:
        WIN.blit(selected_item.affich, (90, 265))

    close_button.draw(WIN, mouse_pos)

    return close_button.is_clicked(mouse_pos, mouse_pressed)


btn_close = Button("X", "close", 500, 20, 40, 40, FONT_BUTTON)
clock = pygame.time.Clock()
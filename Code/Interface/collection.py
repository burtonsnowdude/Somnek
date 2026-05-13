"""
collection.py :
Interface de collection — affiche les items acquis et inconnus du joueur
sous forme de grille cliquable avec aperçu agrandi de l'item sélectionné
"""

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

# paramètres de la grille 
AFFICH_SIZE = (375, 105)  # dimensions de l'image d'aperçu agrandi
ITEM_SIZE   = 30          # taille des icônes dans la grille
START_X     = 67          # coordonnée x du premier item
START_Y     = 49          # coordonnée y du premier item
COLS        = 8           # nombre de colonnes
ROWS        = 6           # nombre de lignes
SPACING_X   = 50          # écart horizontal entre items
SPACING_Y   = 38          # écart vertical entre items


def load_small(path):
    """Charge une image et la redimensionne à la taille ITEM_SIZE x ITEM_SIZE

    Parameters
    ----------
    path : str
        Chemin vers le fichier image

    Returns
    -------
    pygame.Surface
        Image redimensionnée à (ITEM_SIZE, ITEM_SIZE)
    """
    return pygame.transform.scale(pygame.image.load(path), (ITEM_SIZE, ITEM_SIZE))


def load_big(path):
    """Charge une image et la redimensionne à la taille AFFICH_SIZE

    Parameters
    ----------
    path : str
        Chemin vers le fichier image

    Returns
    -------
    pygame.Surface
        Image redimensionnée à AFFICH_SIZE
    """
    return pygame.transform.scale(pygame.image.load(path), AFFICH_SIZE)


# petites images 
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
img_ensemble_jucy   = load_small("Images/Armes_items/jucy.png")
img_manteau_leopard = load_small("Images/Armes_items/manteau_leopard.png")

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

# ── Grandes images (aperçus) ──────────────────────────────────────────────────
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

# Doublons intentionnels (réassignation après chargement initial)
palette_affich            = load_big("Images/Interface/affiche/palette_affich.png")
berserk_affich            = load_big("Images/Interface/affiche/berserk_affich.png")
nain_affich               = load_big("Images/Interface/affiche/nain_affiche.png")
lunettes_cassees_affich   = load_big("Images/Interface/affiche/lunettes_cassees_affiche.png")
cahier_de_nsi_affich      = load_big("Images/Interface/affiche/cahier_NSI_affiche.png")
chaussettes_affich        = load_big("Images/Interface/affiche/chaussettes_affiche.png")
souris_affich             = load_big("Images/Interface/affiche/souris_affiche.png")
cle_usb_affich            = load_big("Images/Interface/affiche/cle_usb_affiche.png")
pistolets_affich          = load_big("Images/Interface/affiche/pistolets_affiche.png")
chariot_violet_affich     = load_big("Images/Interface/affiche/chariot_affiche.png")
pomme_scientifique_affich = load_big("Images/Interface/affiche/pomme_affiche.png")
vody_affich               = load_big("Images/Interface/affiche/vody_affiche.png")
deodorant_affich          = load_big("Images/Interface/affiche/deodorant_affiche.png")
ambroisie_affich          = load_big("Images/Interface/affiche/ambroisie_affiche.png")
nokia_affich              = load_big("Images/Interface/affiche/nokia_affiche.png")
trefle_affich             = load_big("Images/Interface/affiche/trefle_affiche.png")
armure_affich             = load_big("Images/Interface/affiche/armure_affiche.png")
console_affich            = load_big("Images/Interface/affiche/console_affiche.png")
serviette_affich          = load_big("Images/Interface/affiche/serviette_affiche.png")
apple_watch_affich        = load_big("Images/Interface/affiche/apple_watch_affiche.png")
pantalon_beige_affich     = load_big("Images/Interface/affiche/pantalon_beige_affiche.png")

# FILLE POPULAIRE
gloss_rose_affich        = load_big("Images/Interface/affiche/gloss_affiche.png")
ticket_affich            = load_big("Images/Interface/affiche/ticket_affiche.png")
highlighter_affich       = load_big("Images/Interface/affiche/highlighter_affiche.png")
faux_cils_affich         = load_big("Images/Interface/affiche/cils_affiche.png")
bracelet_soeur_affich    = load_big("Images/Interface/affiche/bracelet_affiche.png")
carte_bleu_affich        = load_big("Images/Interface/affiche/carte_affiche.png")
pilule_verte_affich      = load_big("Images/Interface/affiche/pilule_affiche.png")
mousse_vanille_affich    = load_big("Images/Interface/affiche/mousse_affiche.png")
demaquillant_affich      = load_big("Images/Interface/affiche/demaquillant_affiche.png")
parfum_dioru_affich      = load_big("Images/Interface/affiche/parfum_affiche.png")
minuteur_affich          = load_big("Images/Interface/affiche/minuteur_affiche.png")
chew_gum_affich          = load_big("Images/Interface/affiche/chew_gum_affiche.png")
crop_top_rose_affich     = load_big("Images/Interface/affiche/crop_top_affiche.png")
talon_noir_affich        = load_big("Images/Interface/affiche/talon_n_affiche.png")
talon_louboutin_affich   = load_big("Images/Interface/affiche/talon_l_affiche.png")
iphone_2000_affich       = load_big("Images/Interface/affiche/iphone_affiche.png")
pass_navigo_affich       = load_big("Images/Interface/affiche/pass_affiche.png")
fer_a_lisser_affich      = load_big("Images/Interface/affiche/fer_affiche.png")
jean_stanley_affich      = load_big("Images/Interface/affiche/jean_stanley_affiche.png")
chargeur_affich          = load_big("Images/Interface/affiche/chargeur_affiche.png")
ensemble_jucy_affich     = load_big("Images/Interface/affiche/ensemble_jucy_affiche.png")
manteau_leopard_affich   = load_big("Images/Interface/affiche/manteau_leopard_affiche.png")
sac_a_main_violet_affich = load_big("Images/Interface/affiche/sac_a_main_violet_affiche.png")

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
coeur_affiche         = load_big("Images/Interface/affiche/coeur_affiche.png")
cape_affiche          = load_big("Images/Interface/affiche/cape_affiche.png")
collant_affiche       = load_big("Images/Interface/affiche/collant_affiche.png")
sac_a_dos_bleu_affich = load_big("Images/Interface/affiche/sac_a_dos_bleu_affiche.png")
chapelet_affich       = load_big("Images/Interface/affiche/chapelet_affiche.png")
tableau_sacre_affich  = load_big("Images/Interface/affiche/tableau_sacre_affiche.png")
pas_trouve            = load_big("Images/Interface/affiche/pas_trouvé.png")

# Dictionnaire item adapptés à collection
# Associe chaque item à son icône de grille et son image d'aperçu agrandi.
# Les items non débloqués affichent l'icône "inconnu" et l'image "pas_trouve".
"""
liste_all_item = {
    "Palette": (img_palette, palette_affich),
    "Berserk": (img_berserk, berserk_affich),
    "Nain riche": (img_nain, nain_affich),
    "Lunettes cassées": (img_lunettes_cassees, lunettes_cassees_affich),
    "Cahier de NSI": (img_cahier_de_nsi, cahier_de_nsi_affich),
    "Chaussettes": (img_chaussettes, chaussettes_affich),
    "Souris": (img_souris, souris_affich),
    "Clé USB": (img_cle_usb, cle_usb_affich),
    "Pistolets": (img_pistolets, pistolets_affich),
    "Chariot violet": (img_chariot_violet, chariot_violet_affich),
    "Pomme scientifique": (img_pomme_scientifique, pomme_scientifique_affich),
    "Vody": (img_vody, vody_affich),
    "Deodorant": (img_serviette, deodorant_affich),
    "Ambroisie": (img_ambroisie, ambroisie_affich),
    "Nokia": (img_nokia, nokia_affich),
    "Trèfle": (img_trefle, trefle_affich),
    "Armure": (img_armure, armure_affich),
    "Console": (img_console, console_affich),
    "Serviette nettoyante": (img_serviette, serviette_affich),
    "Apple Watch": (img_apple_watch, apple_watch_affich),
    "Pantalon beige": (img_armure, pantalon_beige_affich),

    # FILLE POPULAIRE
    "Gloss rose": (img_gloss_rose, gloss_rose_affich),
    "Ticket": (img_ticket, ticket_affich),
    "Highlighter": (img_highlighter, highlighter_affich),
    "Faux cils": (img_faux_cils, faux_cils_affich),
    "Bracelet soeur": (img_bracelet_soeur, bracelet_soeur_affich),
    "Carte bleu": (img_carte_bleu, carte_bleu_affich),
    "Pilule verte": (img_pilule_verte, pilule_verte_affich),
    "Mousse vanille": (img_mousse_vanille, mousse_vanille_affich),
    "Démaquillant": (img_demaquillant, demaquillant_affich),
    "Parfum Dioru": (img_parfum_dioru, parfum_dioru_affich),
    "Minuteur": (img_minuteur, minuteur_affich),
    "Chew gum": (img_chew_gum, chew_gum_affich),
    "Crop top rose": (img_crop_top_rose, crop_top_rose_affich),
    "Talon noir": (img_talon_noir, talon_noir_affich),
    "Talon Louboutin": (img_talon_louboutin, talon_louboutin_affich),
    "iPhone 2000": (img_iphone_2000, iphone_2000_affich),
    "Pass Navigo": (img_pass_navigo, pass_navigo_affich),
    "Fer à lisser": (img_fer_a_lisser, fer_a_lisser_affich),
    "Jean Stanley": (img_jean_stanley, jean_stanley_affich),
    "Chargeur": (img_chargeur, chargeur_affich),
    "Ensemble Juicy": (img_ensemble_jucy, ensemble_jucy_affich),
    "Manteau léopard": (img_manteau_leopard, manteau_leopard_affich),
    "Sac à main violet": (img_sac_violet, sac_a_main_violet_affich),

    # NONNE
    "Croix de base": (img_croix_de_base, croix_de_base_affich),
    "Couronne": (img_couronne, couronne_affich),
    "Feu saint": (img_feu_saint, feu_saint_affich),
    "Bougie": (img_bougie, bougie_affich),
    "Bourse": (img_bourse, bourse_affich),
    "Voile": (img_bougie, voile_affiche),
    "Huile bénite": (img_bougie, huile_affich),
    "Ostie": (img_ostie, ostie_affich),
    "Boule d'énergie": (img_boule_denergie, boule_denergie_affich),
    "Eau bénite": (img_eau_benite, eau_benite_affich),
    "Mocassin": (img_mocassin, mocassin_affich),
    "Halo lumineux": (img_halo_lumineux, halo_lumineux_affich),
    "Coeur sacré": (img_coeur, coeur_affiche),
    "Cape sacrée": (img_cape, cape_affiche),
    "Collant sacré": (img_collant, collant_affiche),
    "sac à dos bleu": (img_sac_bleu, sac_a_dos_bleu_affich)
}
"""
liste_all_item = {
    "Palette": (img_palette, palette_affich),
    "Berserk": (img_berserk, berserk_affich),
    "Cle_USB": (img_cle_usb, cle_usb_affich),
    "Petit_nain_roux": (img_nain, pas_trouve),
    "Pistolets": (img_pistolets, pistolets_affich),
    "Chariot Violet": (img_chariot_violet, chariot_violet_affich),
    "Lunettes_cassees": (img_lunettes_cassees, lunettes_cassees_affich),
    "Souris_pc": (img_souris, souris_affich),
    "Chaussettes_propres": (img_chaussettes, chaussettes_affich),
    "Cahier_NSI": (img_cahier_de_nsi, cahier_de_nsi_affich),
    "Vody_Lemonade": (img_vody, vody_affich),
    "Deodorant": (img_serviette, deodorant_affich),
    "Pomme_scientifique": (img_pomme_scientifique, pomme_scientifique_affich),
    "Petit_nain_roux":    (img_nain,               pas_trouve),
    "Armure_chevalier":   (img_armure,             armure_affich),
    "Pantalon_beige":     (img_chaussettes,        pas_trouve),
    "Apple_Watch":        (img_apple_watch,        pas_trouve),
    "Serviette_nettoyante":(img_serviette,         serviette_affich),
    "Nokia":              (img_nokia,              nokia_affich),
    "Trefle":             (img_trefle,             trefle_affich),
    "Sac_a_dos_bleu": (img_sac_bleu, sac_a_dos_bleu_affich),
    "Ambroisie": (img_ambroisie, ambroisie_affich),
    "Console_allumee": (img_console, console_affich),

    # FILLE POPULAIRE
    "Gloss_rose": (img_gloss_rose, gloss_rose_affich),
    "Ticket" : (img_ticket, ticket_affich),
    "Faux_cils" : (img_faux_cils, faux_cils_affich),
    "Minuteur" : (img_minuteur, minuteur_affich),
    "Highlighter" : (img_highlighter, highlighter_affich),
    "Chew_gum": (img_chew_gum, chew_gum_affich),
    "Talons_noirs": (img_talon_noir, talon_noir_affich),
    "Talon_louboutin" : (img_talon_louboutin, talon_louboutin_affich),
    "Iphone_2000" : (img_iphone_2000, iphone_2000_affich),
    "Pass_navigo" : (img_pass_navigo, pass_navigo_affich),
    "Bracelet_soeur": (img_bracelet_soeur, bracelet_soeur_affich),
    "Carte_bleue": (img_carte_bleu, carte_bleu_affich),
    "Parfum_Dioru": (img_parfum_dioru, parfum_dioru_affich),
    "Pilule_verte": (img_pilule_verte, pilule_verte_affich),
    "Crop_top_rose": (img_crop_top_rose, crop_top_rose_affich),
    "Coque_trefle": (img_trefle, trefle_affich),
    "Mousse_a_la_vanille": (img_mousse_vanille, mousse_vanille_affich),
    "Sac_a_main_violet": (img_mousse_vanille, sac_a_main_violet_affich),
    "Jean_stanley" : (img_jean_stanley, jean_stanley_affich),
    "Chargeur" : (img_chargeur, chargeur_affich),
    "Fer_a_lisser": (img_fer_a_lisser, fer_a_lisser_affich),
    "Ensemble_juicy": (img_ensemble_jucy, ensemble_jucy_affich),
    "Manteau_leopard": (img_manteau_leopard, manteau_leopard_affich),

    # NONNE
    "Croix_marron": (img_croix_de_base, croix_de_base_affich),
    "Coiffe_de_rameau" : (img_couronne, couronne_affich),
    "Feu_saint" : (img_feu_saint, feu_saint_affich),
    "Chapelet": (img_croix_de_base, chapelet_affich),
    "Mocassin": (img_mocassin, mocassin_affich),
    "Tableau_sacre": (img_mocassin, tableau_sacre_affich),
    "Bourse": (img_bourse, bourse_affich),
    "Bougie": (img_bougie, bougie_affich),
    "Voile": (img_bougie, voile_affiche),
    "Huile_benie": (img_bougie, huile_affich),
    "Ostie": (img_ostie, ostie_affich),
    "Sac_a_dos_bleu": (img_ostie, sac_a_dos_bleu_affich),
    "Eau_benite": (img_eau_benite, eau_benite_affich),
    "Halo_lumineux": (img_halo_lumineux, halo_lumineux_affich),
    "Boule_energie" : (img_boule_denergie, boule_denergie_affich),
    "Coeur": (img_coeur, coeur_affiche),
    "Cape": (img_cape, cape_affiche),
    "Collant": (img_collant, collant_affiche),
}


selected_item = None  # item actuellement sélectionné dans la grille


class ShopItem:
    """
    Class ShopItem :
    Représente un item cliquable dans la grille de collection
    """

    def __init__(self, name, image, affich, x, y):
        """Initialise un item de la grille avec son nom, ses images et sa position

        Parameters
        ----------
        name : str
            Nom de l'item
        image : pygame.Surface
            Icône affichée dans la grille
        affich : pygame.Surface
            Grande image affichée en aperçu lors de la sélection
        x, y : int
            Coordonnées de l'item dans la grille
        """
        self.name   = name
        self.image  = image
        self.affich = affich
        self.rect   = pygame.Rect(x, y, 41, 30)

    def update(self, events):
        """Met à jour l'item en vérifiant si l'utilisateur a cliqué dessus

        Parameters
        ----------
        events : list[pygame.event.Event]
            Liste des événements pygame du frame courant
        """
        global selected_item
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    selected_item = self

    def draw(self, surface):
        """Dessine l'item sur la surface avec un contour jaune s'il est sélectionné

        Parameters
        ----------
        surface : pygame.Surface
            La surface sur laquelle dessiner l'item
        """
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (80, 80, 80), self.rect, 2)  # contour gris par défaut
        if selected_item == self:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)  # contour jaune si sélectionné


def create_items(joueur):
    """Génère la liste des ShopItem à afficher selon l'inventaire du joueur

    Les items possédés affichent leur vraie image ; les autres affichent
    l'icône "inconnu" et l'aperçu "pas_trouve".

    Parameters
    ----------
    joueur : str
        Nom du joueur dont on charge l'inventaire

    Returns
    -------
    list[ShopItem]
        Liste des items positionnés dans la grille (ROWS × COLS cases)
    """
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
                    image  = inconnu   # item non débloqué → silhouette
                    affich = pas_trouve
                items.append(ShopItem(name, image, affich, x, y))
                i += 1
            else:
                # Case vide au-delà du nombre d'items disponibles
                items.append(ShopItem("?", inconnu, pas_trouve, x, y))

    return items


def open_collection(events, WIN, mouse_pos, mouse_pressed, close_button, joueur):
    """Affiche et gère l'interface de collection pour un frame

    Dessine le fond, les items de la grille et l'aperçu de l'item sélectionné.
    Retourne True si le bouton de fermeture est cliqué.

    Parameters
    ----------
    events : list[pygame.event.Event]
        Liste des événements pygame du frame courant
    WIN : pygame.Surface
        Fenêtre principale du jeu
    mouse_pos : tuple(int, int)
        Position de la souris
    mouse_pressed : tuple
        État des boutons de la souris
    close_button : Button
        Bouton de fermeture de la collection
    joueur : str
        Nom du joueur

    Returns
    -------
    bool
        True si la collection doit être fermée, False sinon
    """
    global selected_item

    items = create_items(joueur)

    WIN.blit(shop_bg_img, (0, 0))

    for item in items:
        item.update(events)
        item.draw(WIN)

    # ffiche l'aperçu agrandi de l'item sélectionné
    if selected_item:
        WIN.blit(selected_item.affich, (90, 265))

    close_button.draw(WIN, mouse_pos)

    return close_button.is_clicked(mouse_pos, mouse_pressed)


btn_close = Button("X", "close", 500, 20, 40, 40, FONT_BUTTON)
clock = pygame.time.Clock()
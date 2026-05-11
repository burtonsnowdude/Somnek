"""
Options du jeu :
Gestion des paramètres (son, musique, effets visuels), réinitialisation des power up
"""
import pygame
import Interface.pygameui as pygameui
from Interface.Class_Button import Button
import Interface.variable_power_up as data
from Interface.Power_up_shop import checkboxes as shop_checkboxes
from Interface.Power_up_shop import sync_checkboxes
from Fichiers_variables.gestion_fichiers import replace_player_money, sauvegarder_powerup
sync_checkboxes()
pygame.init()

fond = (245, 245, 235)
croix = (220, 40, 50)

# options tous désactivés 
settings = {
    "sound": False,
    "music": False,
    "vfx": False,
    "damage": False,
    "bw": False
}
WORLD_W, WORLD_H = 400, 600
world = pygame.Surface((WORLD_W, WORLD_H))

FONT_BUTTON = pygame.font.SysFont(None, 36)

fond_options = pygame.image.load("Images/Interface/fond_options.png")
fond_options = pygame.transform.scale(fond_options, (WORLD_W, WORLD_H))

reset_clicked = False


# checkbox par option 
checkboxes = [
    pygameui.Checkbox((100, 100), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 170), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 240), 40, 40, style="cross", color=croix, background_color=fond),
   
    pygameui.Checkbox((100, 380), 40, 40, style="cross", color=croix, background_color=fond),
]

# bouton de réinitialisation 
buttons = [
    Button("Rénitialiser les power_up", "rénitialiser", 180, 470, 300, 30, FONT_BUTTON),
]

# texte affiché à côté de chaque checkbox
instructions = [
    pygameui.Text((160, 110), "Sons", (0, 0, 0)),
    pygameui.Text((160, 180), "Musique", (0, 0, 0)),
    pygameui.Text((160, 250), "Flashing VFX", (0, 0, 0)),
    
    pygameui.Text((160, 390), "Filtre noir et blanc", (0, 0, 0)),
]

def refund_power_up(joueur, player_money):
    """Rembourse tous les power up du joueur et les remet à 0
    
    Parameters
    ----------
    joueur : str
        Le nom du joueur
    player_money : int
        L'argent actuel du joueur
    """
    # on rembourse la somme des prix des niveaux acquis
    for power in data.playerInventory:
        niveau = data.playerInventory[power]
        if niveau > 0:
            prix_list, _ = data.liste_power_up[power]
            player_money += sum(prix_list[:niveau])  # somme des niveaux achetés
            replace_player_money(joueur, player_money)
            data.playerInventory[power] = 0
            sauvegarder_powerup(joueur, power, data.playerInventory[power])
    
    # reset checkboxes du shop
    for cb in shop_checkboxes:
        cb.set_checked(False)

    # Si une partie est en cours, remet les stats à zéro
    from Jeu.player_actif import get_player_actif
    p = get_player_actif()
    if p is not None:
        from Jeu.power_up import apply_powerups
        apply_powerups(p)

    pygame.event.clear()

def sync_settings():
    """Met à jour le dico settings selon l'état des checkboxes"""
    settings["sound"]  = checkboxes[0].is_checked()
    settings["music"]  = checkboxes[1].is_checked()
    settings["vfx"]    = checkboxes[2].is_checked()
    settings["damage"] = checkboxes[3].is_checked()
    settings["bw"]     = checkboxes[4].is_checked()


def options(events, mouse_pos, mouse_pressed, surface, joueur, player_money):
    """Affiche et gère le menu des options
    
    Parameters
    ----------
    events : list
        Liste des évènements pygame
    mouse_pos : tuple(int, int)
        Position de la souris
    mouse_pressed : tuple
        État des boutons de la souris
    surface : pygame.Surface
        La surface sur laquelle dessiner
    joueur : str
        Le nom du joueur
    player_money : int
        L'argent actuel du joueur
    """
    global reset_clicked

    # fond d'écran des options
    surface.fill(fond)
    surface.blit(fond_options, (0, 0))

    # afficher et maj des checkboxes
    for cb in checkboxes:
        cb.update(events)
        cb.draw(surface)

    sync_settings()

    # afficher des textes
    for text in instructions:
        text.draw(surface)

    # affichage et gestion des boutons
    for btn in buttons:
        btn.draw(surface, mouse_pos)

        if btn.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(150)  # petit délai 
            if btn.action == "rénitialiser":
                refund_power_up(joueur, player_money)
                reset_clicked = True
    
def black_and_white(surface):
    """Applique un filtre noir et blanc sur la surface (pixel par pixel)
    
    Parameters
    ----------
    surface : pygame.Surface
        La surface à filtrer
    """
    
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            gray = (r + g + b) // 3  
            surface.set_at((x, y), (gray, gray, gray))


def flashing_effect(surface):
    """Applique un effet de flash blanc semi-transparent
    
    Parameters
    ----------
    surface : pygame.Surface
        La surface à modifier
    """
    flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    flash.fill((255, 255, 255, 80))  # blanc semi-transparent
    surface.blit(flash, (0, 0))
import pygame
import pygameui
from Class_Button import Button
import variable_power_up as data
from Power_up_shop import checkboxes as shop_checkboxes
from Power_up_shop import sync_checkboxes
sync_checkboxes()
pygame.init()

fond = (245, 245, 235)
croix = (220, 40, 50)
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



checkboxes = [
    pygameui.Checkbox((100, 100), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 170), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 240), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 310), 40, 40, style="cross", color=croix, background_color=fond),
    pygameui.Checkbox((100, 380), 40, 40, style="cross", color=croix, background_color=fond),
]

buttons = [
    Button("Rénitialiser les power_up", "rénitialiser", 180, 470, 300, 30, FONT_BUTTON),
]

instructions = [
    pygameui.Text((160, 110), "Sons", (0, 0, 0)),
    pygameui.Text((160, 180), "Musique", (0, 0, 0)),
    pygameui.Text((160, 250), "Flashing VFX", (0, 0, 0)),
    pygameui.Text((160, 320), "Nombre de dégâts", (0, 0, 0)),
    pygameui.Text((160, 390), "Filtre noir et blanc", (0, 0, 0)),
]

def refund_power_up():
    for power in data.playerInventory:
        niveau = data.playerInventory[power]

        if niveau > 0:
            prix_list, _ = data.liste_power_up[power]
            data.player_money += sum(prix_list[:niveau])
            data.playerInventory[power] = 0

    # reset shop checkboxes pygameui (IMPORTANT)
    for cb in shop_checkboxes:
        cb.set_checked(False)

    pygame.event.clear()
def sync_settings():
    settings["sound"] = checkboxes[0].is_checked()
    settings["music"] = checkboxes[1].is_checked()
    settings["vfx"] = checkboxes[2].is_checked()
    settings["damage"] = checkboxes[3].is_checked()
    settings["bw"] = checkboxes[4].is_checked()


def options(events, mouse_pos, mouse_pressed, surface):
    global reset_clicked

    surface.fill(fond)
    surface.blit(fond_options, (0, 0))

    for cb in checkboxes:
        cb.update(events)
        cb.draw(surface)

    sync_settings()

    for text in instructions:
        text.draw(surface)

    for btn in buttons:
        btn.draw(surface, mouse_pos)

        if btn.is_clicked(mouse_pos, mouse_pressed):
            pygame.time.delay(150)

            if btn.action == "rénitialiser":
                refund_power_up()
                reset_clicked = True
    
def black_and_white(surface):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            gray = (r + g + b) // 3
            surface.set_at((x, y), (gray, gray, gray))


def flashing_effect(surface):
    flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    flash.fill((255, 255, 255, 80))
    surface.blit(flash, (0, 0))
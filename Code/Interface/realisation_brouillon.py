import pygame
import Interface.pygameui as pygameui
import pygame_menu
from pygame_menu.widgets import ScrollBar
pygame.init()

fond = (245, 245, 235)
croix = (220, 40, 50)

POPUP_W, POPUP_H = 350, 400
WORLD_H = 1000  

world = pygame.Surface((POPUP_W, WORLD_H))

fond_realisation = pygame.image.load("Images/Interface/fond_realisation.png")
fond_realisation = pygame.transform.scale(fond_realisation, (POPUP_W, WORLD_H))


checkbox_1 = pygameui.Checkbox(
    position=(100, 100),
    width=40,
    height=40,
    style="cross",
    color=croix,
    background_color=fond
)
checkbox_2 = pygameui.Checkbox(
    position=(100, 170),
    width=40,
    height=40,
    style="cross",
    color=croix,
    background_color=fond
)
checkbox_3 = pygameui.Checkbox(
    position=(100, 240),
    width=40,
    height=40,
    style="cross",
    color=croix,
    background_color=fond
)
checkbox_4 = pygameui.Checkbox(
    position=(100, 310),
    width=40,
    height=40,
    style="cross",
    color=croix,
    background_color=fond
)
checkbox_5 = pygameui.Checkbox(
    position=(100, 380),
    width=40,
    height=40,
    style="cross",
    color=croix,
    background_color=fond
)

checkboxes = [checkbox_1, checkbox_2, checkbox_3, checkbox_4, checkbox_5]


instructions = [
    pygameui.Text((180, 100), "Avoir retrouvé quelqu'un", (0, 0, 0)),
    pygameui.Text((180, 170), "Inspecter le livre mystérieux", (0, 0, 0)),
    pygameui.Text((180, 240), "Trouver ton objet mystérieux", (0, 0, 0)),
    pygameui.Text((180, 310), "Éliminer le boss final", (0, 0, 0)),
    pygameui.Text((180, 380), "Entrer dans le métro", (0, 0, 0)),
]


sb_v = ScrollBar(
    length=POPUP_H,
    values_range=(0, WORLD_H - POPUP_H),
    orientation=pygame_menu.locals.ORIENTATION_VERTICAL,
    slider_pad=4,
    slider_height=80  
)

sb_v.set_position(POPUP_W - 20, 40)  #


def calcul_score():
    score = 0
    if checkbox_1.is_checked(): score += 1
    if checkbox_2.is_checked(): score += 1
    if checkbox_3.is_checked(): score += 1
    if checkbox_4.is_checked(): score += 1
    if checkbox_5.is_checked(): score += 1
    return score


def realisation_brouillon(events):

    surface = pygame.Surface((POPUP_W, POPUP_H))
    surface.fill(fond)

    
    sb_v.update(events)
    offset = sb_v.get_value()

    
    world.fill(fond)

    # fond image
    world.blit(fond_realisation, (0, 0))

    
    for cb in checkboxes:
        cb.update(events)
        cb.draw(world)

   
    for text in instructions:
        text.draw(world)

   
    font = pygame.font.SysFont(None, 24)
    score = calcul_score()
    score_surf = font.render(f"Complété : {score}/5", True, (0, 0, 0))

    world.blit(score_surf, (10, 10))

   
    surface.blit(world, (0, -offset))

    
    sb_v.draw(surface)

    return surface
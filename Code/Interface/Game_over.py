import pygame as pyg

from Fichiers_variables.traitement_images import decouper_image
from Class_Button import Button
from Code.Interface.menu import interface

pyg.init()

WIN = pyg.display.set_mode((500, 400))
pyg.display.set_caption("SOMNEK-Game-Over")

spritesheet_game_over = pyg.image.load("Images/Interface/game_over.png").convert_alpha()
ANIM_GAME_OVER = decouper_image(spritesheet_game_over, 4, 3, 0)


FONT_BUTTON = pyg.font.SysFont(None, 36)
bouton_reveni_menu = Button("X", "retour menu", 550, 130, 40, 40, FONT_BUTTON)


frame = 0
clock = pyg.time.Clock()

run = True
while run:
    clock.tick(10)  # vitesse de l'animation

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

        if event.type == pyg.MOUSEBUTTONDOWN:
            mouse_pos = pyg.mouse.get_pos()
            if bouton_reveni_menu.is_clicked(mouse_pos):
                print("Retour au menu principal")
                interface()
                run = False

    # Dessin écran
    WIN.fill((0, 0, 0))

    # Animation Game Over
    frame = (frame + 1) % len(ANIM_GAME_OVER)
    image = ANIM_GAME_OVER[frame]

    WIN.blit(
        image,
        (
            500 / 2 - image.get_width() / 2,
            400 / 2 - image.get_height() / 2,
        ),
    )

    #
    bouton_reveni_menu.draw(WIN)

    pyg.display.flip()

pyg.quit()
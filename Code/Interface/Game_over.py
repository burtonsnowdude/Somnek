import pygame as pyg
from Fichiers_variables.variables import WIN
from Fichiers_variables.traitement_images import decouper_image
from Interface.Class_Button import Button

spritesheet_game_over = pyg.image.load("Images/Interface/game_over.png").convert_alpha()


ANIM_GAME_OVER = decouper_image(spritesheet_game_over, 23, 1, 0)

FONT_BUTTON = pyg.font.SysFont(None, 36)
bouton_revenir_menu = Button("Revenir au menu", "retour menu", 400 - 75, 500, 150, 40, FONT_BUTTON)

clock = pyg.time.Clock()
frame = 0

def game_over():
    global frame
    
    # Capture l'écran du jeu UNE SEULE FOIS
    fond_jeu = WIN.copy()
    
    filtre = pyg.Surface((800, 600), pyg.SRCALPHA)
    filtre.fill((180, 0, 0, 80))
    
    while True:
        clock.tick(5)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "quit"
            if event.type == pyg.MOUSEBUTTONDOWN:
                if bouton_revenir_menu.is_clicked(pyg.mouse.get_pos(), pyg.mouse.get_pressed()):
                    return "menu"

        # Repose le fond figé + filtre à chaque frame
        WIN.blit(fond_jeu, (0, 0))
        WIN.blit(filtre, (0, 0))
        
        frame = (frame + 1) % len(ANIM_GAME_OVER)
        image = ANIM_GAME_OVER[frame]
        image = pyg.transform.scale(image, (500, 650))
        WIN.blit(image, (400 - image.get_width()//2, 50))
        bouton_revenir_menu.draw(WIN, pyg.mouse.get_pos())
        pyg.display.flip()
"""
Game Over :
Anime l'écran de fin de partie avec un filtre rouge et un bouton retour au menu
"""
import pygame as pyg
from Fichiers_variables.variables import WIN
from Fichiers_variables.traitement_images import decouper_image
from Interface.Class_Button import Button

#  spritesheet du game over
spritesheet_game_over = pyg.image.load("Images/Interface/game_over.png").convert_alpha()

# Découpe l'anim du game over
ANIM_GAME_OVER = decouper_image(spritesheet_game_over, 23, 1, 0)

FONT_BUTTON = pyg.font.SysFont(None, 36)
bouton_revenir_menu = Button("Revenir au menu", "retour menu", 400 - 75, 500, 150, 40, FONT_BUTTON)

clock = pyg.time.Clock()
frame = 0

def game_over():
    """Affiche l'écran de game over avec l'animation et le bouton retour au menu
    
    Returns
    -------
    str
        "menu" si l'utilisateur revient au menu, "quit" s'il quitte
    """
    global frame
    
    # On garde le dernier frame du jeu 
    fond_jeu = WIN.copy()
    
    # Filtre rouge semi-transparent par-dessus
    filtre = pyg.Surface((800, 600), pyg.SRCALPHA)
    filtre.fill((180, 0, 0, 80))
    
    while True:
        clock.tick(5)  # animation lente

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "quit"
            if event.type == pyg.MOUSEBUTTONDOWN:
                if bouton_revenir_menu.is_clicked(pyg.mouse.get_pos(), pyg.mouse.get_pressed()):
                    return "menu"

        # affichage du fond et du filtre
        WIN.blit(fond_jeu, (0, 0))
        WIN.blit(filtre, (0, 0))
        
        # animation du game over
        frame = (frame + 1) % len(ANIM_GAME_OVER)  # boucle l'anim
        image = ANIM_GAME_OVER[frame]
        image = pyg.transform.scale(image, (500, 650))
        WIN.blit(image, (400 - image.get_width()//2, 50))
        bouton_revenir_menu.draw(WIN, pyg.mouse.get_pos())
        pyg.display.flip()
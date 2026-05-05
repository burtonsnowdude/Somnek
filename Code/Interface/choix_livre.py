
import pygame
from Interface.Class_Button import Button

pygame.init()

WORLD_W, WORLD_H = 400, 600
WIN = pygame.display.set_mode((WORLD_W, WORLD_H))

FONT_BUTTON = pygame.font.SysFont(None, 36)

fond_choix = pygame.image.load("../Images/Interface/fond_choix.png")
fond_choix = pygame.transform.scale(fond_choix, (WORLD_W, WORLD_H))

btn_Yes = Button("Prendre le cahier", "yes", 200, 395, 210, 60, FONT_BUTTON)
btn_No = Button("Le laisser", "no", 200, 460, 210, 60, FONT_BUTTON)

clock = pygame.time.Clock()
running = True
livre = False
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    events = pygame.event.get()
        

    WIN.blit(fond_choix, (0, 0))
    btn_Yes.draw(WIN, mouse_pos)
    btn_No.draw(WIN, mouse_pos)

    if btn_Yes.is_clicked(mouse_pos, mouse_pressed):
        livre = True
        running = False
        print("True")
    if btn_No.is_clicked(mouse_pos, mouse_pressed):
        livre = False
        running = False
        print("False")

    pygame.display.flip()

pygame.quit()
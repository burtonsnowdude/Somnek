import pygame as pyg
import pygame_gui
import sys
from Fichiers_variables.variables import WIN, WIDTH, HEIGHT

def get_user_name(fond_intro):
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    text_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pyg.Rect((WIDTH//2 - 150, HEIGHT//2 + 30), (300, 50)),
        manager=manager,
        object_id='#main_text_entry'
    )
    font = pyg.font.SysFont("bahnschrift", 30)
    clock = pyg.time.Clock()

    while True:
        dt = clock.tick(60) / 1000
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                return event.text

            manager.process_events(event)

        manager.update(dt)

        # fond_intro en dessous
        WIN.blit(fond_intro, (0, 0))

        # texte par dessus
        texte = font.render("Entre ton nom :", True, (255, 255, 255))
        WIN.blit(texte, texte.get_rect(center=(WIDTH//2, HEIGHT//2 - 10)))

        manager.draw_ui(WIN)
        pyg.display.flip()
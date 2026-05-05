import pygame
import pygame_gui
import sys

pygame.init()

WIDTH, HEIGHT = 500, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input in PyGame | BaralTech")

manager = pygame_gui.UIManager((500, 600))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((30, 205), (400, 50)), manager=manager,
                                               object_id='#main_text_entry')

clock = pygame.time.Clock()

def get_fitting_font(text, max_width, start_size=30):
    size = start_size
    font = pygame.font.SysFont("bahnschrift", size)

    while font.size(text)[0] > max_width and size > 10:
        size -= 1
        font = pygame.font.SysFont("bahnschrift", size)

    return font

def show_user_name(user_name):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill("white")

        text = f"Bienvenue, {user_name} dans Somnek"

        font = get_fitting_font(text, WIDTH - 40)

        new_text = font.render(text, True, "black")
        new_text_rect = new_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        SCREEN.blit(new_text, new_text_rect)

        clock.tick(60)

        pygame.display.update()



def get_user_name():
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                show_user_name(event.text)
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        SCREEN.fill("white")

        new_exp = pygame.font.SysFont("bahnschrift", 30).render(f" Entre ton nom d'utilisateur : ", True, "black")
        new_text_exp = new_exp.get_rect(center=(WIDTH/2, 180))
        SCREEN.blit(new_exp, new_text_exp)


        manager.draw_ui(SCREEN)

        

        pygame.display.update()
    

get_user_name()
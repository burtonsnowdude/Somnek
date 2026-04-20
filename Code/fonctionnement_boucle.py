import time
from variables import *

def remplir_fond(p):
    # Fond d'écran 
    WIN.fill((225, 225, 225)) 
    offset_x = p.x_monde % WIDTH
    offset_y = p.y_monde % HEIGHT
    for i in range(-WIDTH, 2*WIDTH, WIDTH):
        for j in range(-HEIGHT, 2*HEIGHT, HEIGHT):
                WIN.blit(BG, (i-offset_x, j-offset_y))

def chrono(clock, start_time, pause_time):
    clock.tick(60) # fixe le nombre de frames par seconde
    temps_ecoule = time.time() - start_time - pause_time
    return temps_ecoule

def camera(x, y, p):
    x_screen = CENTREx - (p.x_monde - x)
    y_screen = CENTREy - (p.y_monde - y)
    return x_screen, y_screen

def screen_to_world(x_screen, y_screen, p):
    x_monde = p.x_monde + (x_screen - CENTREx)
    y_monde = p.y_monde + (y_screen - CENTREy)
    return x_monde, y_monde
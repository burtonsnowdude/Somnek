import time
from variables import *

def remplir_fond(p):
    # Fond d'écran 
    WIN.fill((225, 225, 225)) 
    offset_x = p.x_suppose % WIDTH
    offset_y = p.y_suppose % HEIGHT
    for i in range(-WIDTH, 2*WIDTH, WIDTH):
        for j in range(-HEIGHT, 2*HEIGHT, HEIGHT):
                WIN.blit(BG, (i-offset_x, j-offset_y))

def chrono(clock, start_time, pause_time):
    clock.tick(60) # fixe le nombre de frames par seconde
    temps_ecoule = time.time() - start_time - pause_time
    return temps_ecoule

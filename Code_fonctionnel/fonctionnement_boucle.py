import time
from variables import *

def fonc_boucle(clock, start_time, pause_time, bg):
    clock.tick(60) # fixe le nombre de frames par seconde
    temps_ecoule = time.time() - start_time - pause_time
    # Fond d'écran 
    WIN.fill((225, 225, 225)) 
    WIN.blit(BG, bg) 
    return temps_ecoule
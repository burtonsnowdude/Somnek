import pygame as pyg 
import time
from variables import *
from monstre_player import *
from random import *

def main():
    clock = pyg.time.Clock() # crée une horloge pour gérer le temps

    run = True

    monstres_presents = [] # liste qui contiendra les monstres existant
    bg = BG.get_rect() 
    barre_PV = pyg.Rect(500, 10, PLAYER_PV*5, 20)
    p = Player()
    start_time = time.time()  
    frame = 0
    frequence = 50 # fréquence à laquelle un monstre apparait
    last_spawn_update = 0

    while run:
        clock.tick(60) # fixe le nombre de frames par seconde
        temps_ecoulé = time.time() - start_time  

        for event in pyg.event.get():  
            if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                run = False 
                break

        # Fond d'écran et barre de vie
        WIN.fill((225, 225, 225)) 
        WIN.blit(BG, bg) 
        barre_PV = pyg.Rect(500, 10, p.hp*5, 20)
        pyg.draw.rect(WIN, (0, 255, 10), barre_PV)
        
        frame += 1
    
        if frame%frequence == 0 :
            monstres_presents.append(Monstre(choice(TYPES))) # crée un nouveau monstre de type aléatoire
            if temps_ecoulé - last_spawn_update > 30:
                if frequence > 30:
                    frequence -= 1
                last_spawn_update = temps_ecoulé

        for m in monstres_presents[:]:
            existe = m.show() # affiche tous les monstres existant
            if existe :
                m.follow(p) # monstres suivant le joueur
                if p.pos.colliderect(m.pos) and frame%10 == 0:
                    p.degats(m.puissance) # dégâts en cas de collision
            else :
                monstres_presents.remove(m)

        p.draw_player()
        p.move_bg(bg, monstres_presents)

        # Timer
        if temps_ecoulé < 60: 
             time_text = FONT.render(f"{int(temps_ecoulé)}s", 1, (255, 255, 255)) 
        else:
            min = temps_ecoulé // 60 
            sec = temps_ecoulé % 60 
            time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) 
        WIN.blit(time_text, (10, 10)) 

        pyg.display.update()

    pyg.quit() 


if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()
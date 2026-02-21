import pygame as pyg # importer le module pygame (game engine)
import time
from variables import * # importer les variables
from monstres import *
from random import *

def main():
    clock = pyg.time.Clock() # creer une horloge pour gerer le temps

    run = True

    monstres_presents = []
    bg = BG.get_rect() # creer un rectangle pour le fond d'ecran
    barre_PV = pyg.Rect(500, 10, PLAYER_PV*5, 20)
    p = player()
    start_time = time.time()  # temps de debut
    frame = 0
    frequence = 50
    last_spawn_update = 0
    while run:
        clock.tick(60) # fixe le nombre de frames par seconde
        temps_ecoulé = time.time() - start_time  # calcule le temps ecoule

        for event in pyg.event.get():  # cherche appui du bouton sortie
            if event.type == pyg.QUIT: # si le joueur ferme la fenetre
                run = False 
                break

        WIN.fill((225, 225, 225)) # fond d'ecran
        WIN.blit(BG, bg) # dessiner le fond d'ecran
        barre_PV = pyg.Rect(500, 10, p.hp*5, 20)
        pyg.draw.rect(WIN, (0, 255, 10), barre_PV)
        
        frame += 1
    
        if frame%frequence == 0 :
            monstres_presents.append(Monstre(choice(TYPES)))
            
            if temps_ecoulé - last_spawn_update > 30:
                if frequence > 30:
                    frequence -= 1
                last_spawn_update = temps_ecoulé

        for m in monstres_presents[:]:
            existe = m.spawn()
            if existe :
                m.follow(p)
                if p.pos.colliderect(m.pos) and frame%10 == 0:
                    p.degats(m.puissance)
            else :
                monstres_presents.remove(m)

        p.draw_player()
        p.move_bg(bg, monstres_presents)

        if temps_ecoulé < 60: # calculer les minutes et secondes seulement si besoin
             time_text = FONT.render(f"{int(temps_ecoulé)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
        else:
            min = temps_ecoulé // 60 
            sec = temps_ecoulé % 60 

            time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
        WIN.blit(time_text, (10, 10)) # afficher le texte du temps ecoulé

        pyg.display.update()

    pyg.quit() # quitter pygame


if __name__ == "__main__": #s'assure que le main ne s'execute que si on lance ce fichier directement
    main()
import pygame as pyg 
import time
from variables import *
from monstre_player import *
from random import *

def main():
    clock = pyg.time.Clock() # crée une horloge pour gérer le temps

    run = True
    
    # Toutes les variables initiales sont en bazar je pense qu'il faudra les organiser
    monstres_presents = [] # liste qui contiendra les monstres existant
    bg = BG.get_rect() 
    barre_PV = pyg.Rect(500, 10, PLAYER_PV*5, 20)
    p = Player()
    start_time = time.time()  
    frame = 0
    frequence = 50 # fréquence à laquelle un monstre apparait
    last_spawn_update = 0
    xp_attendu = 40
    xp = 0.5
    seuil = 0
    options = []
    armes_possedees = []
    choix = []
    pause_time = 0
    while run:
        clock.tick(60) # fixe le nombre de frames par seconde
        temps_ecoulé = time.time() - start_time - pause_time

        for event in pyg.event.get():  
            if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                run = False 
                break

        # Fond d'écran 
        WIN.fill((225, 225, 225)) 
        WIN.blit(BG, bg) 
        
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

        # là j'ai mis un xp arbitraire mais il faudra le changer quand t'ajouteras les armes
        # exactement comme la boucle pour les monstres mais ici ce serait une double boucle
        # avec d'abord pour chaque arme possédée, puis pour chaque monstre présent s'il y a collision
        # en mettant m.hp à la place de xp je pense 
        # genre on récupère en xp l'équivalent des points de vie du monstre

        p.draw_player() 

        if p.update_xp(xp, xp_attendu) :
            xp_attendu *= 1.5
            if seuil+4 <= len(ARMES) :
                seuil += 4
            if xp_attendu%2 != 0 :
                xp_attendu += 1 # pour toujours avoir un nombre pair (évite un trop grand nombre de décimales)
            # passage de niveau (j'attends la class armes encore une fois c'est des listes arbitraires)
            if p.niveau < seuil :
                armes_dispo = [arme for arme in ARMES if ARMES[arme] < seuil]
                choix = []
                compteur = 0
                while compteur < 3:
                    arme = choice(armes_dispo)
                    if arme not in choix :
                        choix.append(arme) 
                        compteur += 1
                options = [pyg.Rect(370, 200+40*i, 100, 30) for i in range(3)]
                for option in options :
                    pyg.draw.rect(WIN, (255, 255, 255), option)
                for i in range(len(choix)) :
                    texte = FONT.render(choix[i], 1, (0, 0, 0)) 
                    WIN.blit(texte, (390, 205+i*40))
                pyg.display.update()
                clic = False
                debut = time.time()
                while not clic :
                    pause_time = time.time() - debut
                    for event in pyg.event.get() :
                        clic = event.type == pyg.MOUSEBUTTONDOWN
                        pos = pyg.mouse.get_pos()
                        for option in options :
                            if option.collidepoint(pos) and pyg.mouse.get_pressed()[0]:
                                print(choix[options.index(option)])
                                armes_possedees.append(choix[options.index(option)])
                                options = []

        p.move_bg(bg, monstres_presents)

        # Timer et barre de vie
        if temps_ecoulé < 60: 
             time_text = FONT.render(f"{int(temps_ecoulé)}s", 1, (255, 255, 255)) 
        else:
            min = temps_ecoulé // 60 
            sec = temps_ecoulé % 60 
            time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) 
        WIN.blit(time_text, (370, 10)) 
        barre_PV_blanc = pyg.Rect(500, 10, 250, 20)
        barre_PV = pyg.Rect(500, 10, p.hp*5, 20)
        pyg.draw.rect(WIN, (255, 255, 255), barre_PV_blanc)
        pyg.draw.rect(WIN, (0, 255, 10), barre_PV)

        # Barre d'xp
        unit = 250/xp_attendu
        barre_xp_blanc = pyg.Rect(10, 10, 250, 20)
        barre_xp = pyg.Rect(10, 10, p.xp*unit, 20)
        pyg.draw.rect(WIN, (255, 255, 255), barre_xp_blanc)
        pyg.draw.rect(WIN, (0, 0, 255), barre_xp)
        pyg.display.update()

    pyg.quit() 


if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()
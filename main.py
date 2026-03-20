import pygame as pyg 
import time
from variables import *
from monstre_player import *
from random import *
from coffres import *

def main():
    clock = pyg.time.Clock() # crée une horloge pour gérer le temps

    run = True
    
    # Toutes les variables initiales sont en bazar je pense qu'il faudra les organiser
    monstres_presents = [] # liste qui contiendra les monstres existant
    bg = BG.get_rect() 
    p = Player()
    start_time = time.time()  
    frame = 0
    frequence = 50 # fréquence à laquelle un monstre apparait
    xp_attendu = 40 # xp attendu pour passer un niveau (croît exponentiellement)
    xp = 0.5
    seuil = 0
    options = []
    armes_possedees = []
    pause_time = 0 # temps d'inactivité 
    dernier_coffre_apparu = 0 # nombre de frames depuis le dernier coffre apparu
    coffre_existant = False
    nouveau_coffre = None
    argent = 0

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

       
        # Gestion des coffres
        if randint(1,100) == 1 and dernier_coffre_apparu > 100 and not coffre_existant:
            nouveau_coffre = Coffre(p)
            dernier_coffre_apparu = 0 
            coffre_existant = True

        if coffre_existant:
            nouveau_coffre.pointer_coffre(p)
            if nouveau_coffre.coffre_sur_lecran:
                if p.pos.colliderect(nouveau_coffre.rect):
                    gain = nouveau_coffre.determiner_recompense(armes_possedees, seuil)
                    if type(gain) == int :
                        argent += gain
                        print(argent)
                    else :
                        armes_possedees.append(gain)
                        print(armes_possedees)
                    coffre_existant = False
        dernier_coffre_apparu += 1
        
        # Gestion des ennemis
        if frame%frequence == 0 :
            monstres_presents.append(Monstre(choice(TYPES))) # crée un nouveau monstre de type aléatoire
        for m in monstres_presents[:]:
            existe = m.show() # affiche tous les monstres existant
            if existe :
                m.follow(p) # monstres suivant le joueur
                if p.pos.colliderect(m.pos) and frame%10 == 0:
                    p.degats(m.puissance) # dégâts en cas de collision
            else :
                monstres_presents.remove(m)

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
                for arme in armes_dispo[:]:
                    if arme in armes_possedees :
                        armes_dispo.remove(arme)
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
                selec = 0       
                for i in range(len(choix)) :
                    texte = FONT.render(choix[i], 1, (0, 0, 0)) 
                    WIN.blit(texte, (390, 205+i*40))
                pyg.display.update()
                debut = time.time()
                entree = False
                while not entree:
                    pause_time = time.time() - debut
                    for event in pyg.event.get():
                        if event.type == pyg.QUIT:
                            pyg.quit()
                            exit()

                        if event.type == pyg.KEYDOWN:
                            if event.key == pyg.K_UP and selec != 0:
                                pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                                texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                                WIN.blit(texte, (390, 205+selec*40))
                                selec -= 1

                            if event.key == pyg.K_DOWN and selec != 2:
                                pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                                texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                                WIN.blit(texte, (390, 205+selec*40))
                                selec += 1

                            if event.key == pyg.K_RETURN:
                                entree = True

                    pyg.draw.rect(WIN, (120, 120, 250), options[selec])
    
                    texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                    WIN.blit(texte, (390, 205+selec*40))
                    pyg.display.update()

                armes_possedees.append(choix[selec])
                print(armes_possedees)
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
import pygame as pyg 
import time
from variables import *
from player import *
from random import *
from coffres import *
from passage_niveau import *
from barre_xp_vie import *
from class_monstre import *


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
    armes_possedees = []
    pause_time = 0 # temps d'inactivité 
    dernier_coffre_apparu = 0 # nombre de frames depuis le dernier coffre apparu
    coffre_existant = False
    nouveau_coffre = None
    argent = 0

    while run:
        clock.tick(60) # fixe le nombre de frames par seconde
        temps_ecoule = time.time() - start_time - pause_time

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
        if frame%frequence == 0:
            monstres_presents = ajouter_monstre(monstres_presents)
        monstres_presents = gestion_monstres_presents(monstres_presents, frame, p)
    
        p.draw_player() 

        # Passage de niveau
        if p.update_xp(xp, xp_attendu):
            seuil, xp_attendu = passage(xp_attendu, seuil)
            armes_possedees, pause_time = choix_arme(p, seuil, armes_possedees)
        
        p.move_bg(bg, monstres_presents)

        # Barre de vie et d'xp
        afficher_timer(temps_ecoule, p)
        afficher_xp(xp_attendu, p)
    pyg.quit() 


if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()

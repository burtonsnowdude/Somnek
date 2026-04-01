import pygame as pyg 
import time
from variables import *
from player import *
from random import *
from coffres import *
from passage_niveau import *
from barre_xp_vie import *
from class_monstre import *
from fonctionnement_boucle import *
from gestion_fichiers import *

def main():
    noms, new_tab = det_noms()
    nom = "Daphne"
    res = ajouter_utilisateur(nom, noms)
    if  res == False :
        argent = int(new_tab[1][nom])
        new_tab[0][nom] = int(new_tab[0][nom])
    else :
        noms = res
        argent = 0
        new_tab[0][nom] = 1 #niveau
    armes_joueur = contenu_fichier_armes()
    clock = pyg.time.Clock() # crée une horloge pour gérer le temps
    run = True
    p = Player()

    # Initialisation des variables
    monstres_presents, armes_possedees = [], [] 
    bg = BG.get_rect() 

    start_time = time.time()  
    frame = 0
    pause_time = 0 # temps d'inactivité 

    frequence = 50 # fréquence à laquelle un monstre apparait
    xp_attendu = 40 # xp attendu pour passer un niveau (croît exponentiellement)
    xp = 0.5
    seuil = 0
    dernier_coffre_apparu = 0 # nombre de frames depuis le dernier coffre apparu
    coffre_existant = False
    kill_count = 0 
    
    while run:
        for event in pyg.event.get():  
            if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                run = False 
                break

        temps_ecoule = fonc_boucle(clock, start_time, pause_time, p)
        frame += 1

        # Gestion des coffres
        ajout = ajout_coffre(dernier_coffre_apparu, coffre_existant, p)
        if ajout != False :
            nouveau_coffre, dernier_coffre_apparu, coffre_existant = ajout

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
                        ajouter_arme(nom, gain, armes_joueur)
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
            arme, pause_time = choix_arme(p, seuil, armes_possedees)
            armes_possedees.append(arme)
            print(armes_possedees)
            armes_joueur = ajouter_arme(nom, arme, armes_joueur)
            new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
        p.move_bg(bg, monstres_presents)

        # Barre de vie et d'xp, timer
        afficher_timer_vie(temps_ecoule, p)
        afficher_xp(xp_attendu, p)
    
    # Reecriture des fichiers csv avec les données actualisées de la partie
    reecrire_fichier_niveau_argent(new_tab, noms) 
    reecrire_fichier_armes(armes_joueur, noms) 
    pyg.quit() 


if __name__ == "__main__": # s'assure que le main ne s'exécute que si on lance ce fichier directement
    main()

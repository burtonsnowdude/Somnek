import pygame as pyg 
import time
from Fichiers_variables.variables import *
from Jeu.player import *
from Jeu.coffres import ajout_coffre
from Jeu.passage_niveau import *
from Affichage.affichage_divers import *
from Monstres.class_monstre import *
from Affichage.fonctionnement_divers import *
from Fichiers_variables.gestion_fichiers import *
from Jeu.player import Player
from Monstres.vagues import *
from Jeu.Quêtes import verif_k, verif_q  # Import quest verification functions
from Monstres.boss import spawn_boss, gestion_boss
from Minijeux.all_mj import mj

def jeu(perso):
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
    
    p = Player(perso)
    # Initialisation des variables
    monstres_presents, armes_possedees, xp_dispo, boss_acheves, items_possedes = [], [], [], [], []

    start_time = time.time()  

    frame, pause_time, xp, dernier_coffre_apparu, derniere_vague, time_map = [0]*6
    xp_attendu = 20 # xp attendu pour passer un niveau (croît exponentiellement)
    seuil = 2
    monstres_vague, boss, coord_monde = [None] * 3
    vague, pause, boss_present, test_popup_triggered, coffre_existant, minijeu_fini = [False]*6
    popup_message = None
    popup_start_time = 0
    popup_group = pyg.sprite.Group()  # Groupe pour les popups
    completed_kill_quests = set()  # Suivre les quêtes de kills terminées
    completed_acquire_quests = set()  # Suivre les quêtes d'acquisition terminées

    while run:
        xp = 0
        for event in pyg.event.get():  
            if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                run = False 
                break
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_SPACE:
                    pause = not pause
        if pause :
            pause, run, pause_time = menu_pause(new_tab, noms, armes_joueur)

        if not pause : 
            remplir_fond(p)
            temps_ecoule = chrono(clock, start_time, pause_time)
            frame += 1
            coord_monde, minijeu_fini, armes_possedees = mj(perso, coord_monde, minijeu_fini, p, armes_possedees)
            p.lancer_projectile()
            p.update_cooldown()
            # déplace les projectiles
            for projectile in p.all_projectiles : 
                projectile.move() 
                if monstres_vague is not None :
                    monstres = monstres_presents + monstres_vague 
                if boss_present :
                    monstres.append(boss)
                else : 
                    monstres = monstres_presents
                for m in monstres:
                    if projectile.rect.colliderect(m.rect):
                        m.degats(5)
            #appliquer les images de mon groupe projectile
            p.all_projectiles.draw(WIN) 
            # Gestion des ennemis
            if frame%FREQUENCE == 0:
                monstres_presents = ajouter_monstre(monstres_presents, p, perso)
            monstres_presents, p.kill_count = gestion_monstres_presents(monstres_presents, frame, p, xp_dispo)
            xp_dispo, xp = gestion_xp_fenetre(xp_dispo, p, xp_attendu)
            res = gestion_vague(derniere_vague, p, perso)
            if res is not False :
                derniere_vague, monstres_vague, coin = res
                x_monde, y_monde = coord_coin(coin,p)
            else : 
                derniere_vague += 1
            if monstres_vague is not None :
                monstres_vague, p.kill_count = traverser_ecran(monstres_vague, p, frame, xp_dispo, x_monde, y_monde)
            monstres_presents, vague = vague_130(temps_ecoule, monstres_presents, vague, p, perso)

            boss_present, boss = spawn_boss(temps_ecoule, boss_present, boss_acheves, p, boss, perso)
            boss_present = gestion_boss(boss, boss_present, p, frame)
            # Gestion des coffres
            ajout = ajout_coffre(dernier_coffre_apparu, coffre_existant, p)
            if ajout != False :
                nouveau_coffre, dernier_coffre_apparu, coffre_existant = ajout
            if coffre_existant:
                nouveau_coffre.pointer_coffre(p)
                
                if p.pos.colliderect(nouveau_coffre.rect):
                    gain = nouveau_coffre.determiner_recompense(armes_possedees, seuil, p)
                    if type(gain) == int :
                        argent += gain
                        print(argent)
                    else :
                        armes_possedees.append(gain)
                        ajouter_arme(nom, gain, armes_joueur)
                        print(armes_possedees)
                    coffre_existant = False
            dernier_coffre_apparu += 1 

            p.draw_player(frame) 
            # Barre de vie et d'xp, timer
            afficher_xp(xp_attendu, p)
            afficher_timer_vie(temps_ecoule, p)

            # Vérifier et déclencher les quêtes de kills
            kill_quest = verif_k(p)
            if kill_quest and kill_quest not in completed_kill_quests:
                popup = PopupAchievement(kill_quest)
                popup_group.add(popup)
                completed_kill_quests.add(kill_quest)

            # Vérifier et déclencher les quêtes d'acquisition
            acquire_quest = verif_q(len(armes_possedees))  # Passe le nombre actuel d'armes
            if acquire_quest and acquire_quest not in completed_acquire_quests:
                popup = PopupAchievement(acquire_quest)
                popup_group.add(popup)
                completed_acquire_quests.add(acquire_quest)

            # Optionnel : Garder le popup de test pour le débogage
            if temps_ecoule >= 5 and not test_popup_triggered:
                popup = PopupAchievement("Test Achievement: 5 Seconds Passed!")
                popup_group.add(popup)
                test_popup_triggered = True

            # Passage de niveau
            if p.update_xp(xp, xp_attendu):
                seuil, xp_attendu = passage(xp_attendu, seuil)
                arme, pause_time = choix_arme(p, seuil, armes_possedees)
                armes_possedees.append(arme)
                print(armes_possedees)
                armes_joueur = ajouter_arme(nom, arme, armes_joueur)
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
            p.move_bg(monstres_presents, xp_dispo, monstres_vague, boss, boss_present)
            
            popup_group.update()  # Met à jour les popups
            popup_group.draw(WIN)  # Dessine les popups
            
            pyg.display.flip()
    
    
    pyg.quit() 
    # Reecriture des fichiers csv avec les données actualisées de la partie
    reecrire_fichier_niveau_argent(new_tab, noms) 
    reecrire_fichier_armes(armes_joueur, noms) 




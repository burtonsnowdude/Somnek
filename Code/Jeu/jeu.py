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
from Jeu.Quêtes import verif_k, verif_q
from Monstres.boss import spawn_boss, gestion_boss
from Minijeux.all_mj import mj

def jeu(perso):
    perso = "Nerd"
    noms, new_tab = det_noms()
    print("1 :", new_tab)
    nom = "Daphne"
    res = ajouter_utilisateur(nom, noms)
    if  res == False :
        argent = int(new_tab[1][nom])
        new_tab[0][nom] = int(new_tab[0][nom])
    else :
        noms = res
        argent = 0
        new_tab[0][nom] = 1
    print("2 :", new_tab)

    armes_joueur = contenu_fichier_armes()
    clock = pyg.time.Clock()
    run = True
    
    p = Player(perso, nom)

    monstres_presents, armes_et_items_possedees, xp_dispo, boss_acheves, armes_possedees, items_possedes = [], [], [], [], [], []

    start_time = time.time()  

    frame, pause_time, xp, dernier_coffre_apparu, derniere_vague, time_map = [0]*6
    xp_attendu = 20
    
    monstres_vague, boss, coord_monde = [None] * 3
    vague, pause, boss_present, test_popup_triggered, coffre_existant, minijeu_fini = [False]*6

    popup_group = pyg.sprite.Group()
    completed_kill_quests = set()
    completed_acquire_quests = set()

    while run:
        xp = 0

        for event in pyg.event.get():  
            if event.type == pyg.QUIT:
                run = False 
                break

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_SPACE:
                    pause = not pause

                if event.key == pyg.K_z:
                    p.arme_active = (p.arme_active + 1) % len(p.armes)

                if event.key == pyg.K_f:
                    p.attack()

        if pause:
            pause, run, pause_time = menu_pause(new_tab, noms, armes_joueur)

        if not pause: 
            remplir_fond(p)
            temps_ecoule = chrono(clock, start_time, pause_time)
            frame += 1

            coord_monde, minijeu_fini, armes_et_items_possedees, armes_joueur = mj(
                perso, coord_monde, minijeu_fini, p, armes_et_items_possedees, armes_joueur
            )

            # =====================
            # UPDATE ARMES / GROUPES
            # =====================
            p.update_armes()
            p.all_projectiles.update()
            p.all_zones.update()
            # =====================
            # COLLISIONS ZONES
            # =====================
            for zone in p.all_zones:
                for m in monstres_presents:
                    if zone.rect.colliderect(m.rect):
                        m.degats(10)
                        

                if boss_present and zone.rect.colliderect(boss.rect):
                    boss.degats(10)
                    

            # =====================
            # COLLISIONS PROJECTILES
            # =====================
            for projectile in p.all_projectiles:
                for m in monstres_presents:
                    if projectile.rect.colliderect(m.rect):
                        m.degats(10)
                        projectile.kill()

                if boss_present and projectile.rect.colliderect(boss.rect):
                    boss.degats(10)
                    projectile.kill()

            # =====================
            # SPAWN / LOGIQUE MONSTRES
            # =====================
            if frame % FREQUENCE == 0:
                monstres_presents = ajouter_monstre(monstres_presents, p, perso)

            monstres_presents, p.kill_count = gestion_monstres_presents(
                monstres_presents, frame, p, xp_dispo
            )

            xp_dispo, xp = gestion_xp_fenetre(xp_dispo, p, xp_attendu)

            res = gestion_vague(derniere_vague, p, perso)
            if res is not False:
                derniere_vague, monstres_vague, coin = res
                x_monde, y_monde = coord_coin(coin, p)
            else:
                derniere_vague += 1

            if monstres_vague is not None:
                monstres_vague, p.kill_count = traverser_ecran(
                    monstres_vague, p, frame, xp_dispo, x_monde, y_monde
                )

            monstres_presents, vague = vague_130(
                temps_ecoule, monstres_presents, vague, p, perso
            )

            boss_present, boss = spawn_boss(
                temps_ecoule, boss_present, boss_acheves, p, boss, perso
            )

            boss_present, boss_acheves = gestion_boss(
                boss, boss_present, p, frame, boss_acheves
            )

            # =====================
            # COFFRES
            # =====================
            ajout = ajout_coffre(dernier_coffre_apparu, coffre_existant, p)
            if ajout != False:
                nouveau_coffre, dernier_coffre_apparu, coffre_existant = ajout

            if coffre_existant:
                nouveau_coffre.pointer_coffre(p)

                if p.pos.colliderect(nouveau_coffre.rect):
                    gain = nouveau_coffre.determiner_recompense(
                        armes_et_items_possedees, p
                    )

                    if type(gain) == int:
                        argent += gain
                    else:
                        armes_et_items_possedees.append(gain[1])
                        armes_joueur = ajouter_arme(nom, gain, armes_joueur)

                        if gain[0] == "arme":
                            armes_possedees.append(gain[1])
                        else:
                            items_possedes.append(gain[1])

                    coffre_existant = False

            dernier_coffre_apparu += 1 

            # =====================
            # AFFICHAGE
            # =====================
            p.draw_player(frame)

            # arme active visible
            for arme in p.armes:
                if arme.visible:
                    arme.draw(WIN)

            p.all_projectiles.draw(WIN)
            p.all_zones.draw(WIN)

            afficher_xp(xp_attendu, p)
            afficher_timer_vie(temps_ecoule, p)

            # =====================
            # QUÊTES
            # =====================
            kill_quest = verif_k(p)
            if kill_quest and kill_quest not in completed_kill_quests:
                popup_group.add(PopupAchievement(kill_quest))
                completed_kill_quests.add(kill_quest)

            acquire_quest = verif_q(len(armes_et_items_possedees))
            if acquire_quest and acquire_quest not in completed_acquire_quests:
                popup_group.add(PopupAchievement(acquire_quest))
                completed_acquire_quests.add(acquire_quest)

            # =====================
            # LEVEL UP
            # =====================
            if p.update_xp(xp, xp_attendu):
                xp_attendu = passage(xp_attendu)

                objet, pause_time = choix_arme(p, armes_possedees)
                armes_et_items_possedees.append(objet[1])

                if objet[0] == "arme":
                    armes_possedees.append(objet[1])
                else:
                    items_possedes.append(objet[1])

                armes_joueur = ajouter_arme(nom, objet, armes_joueur)
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)

            p.move_bg(monstres_presents, xp_dispo, monstres_vague, boss, boss_present)

            popup_group.update()
            popup_group.draw(WIN)

            pyg.display.flip()

    reecrire_fichier("niveau_argent", new_tab, noms)
    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
    pyg.quit()
"""
Boucle principale de jeu
"""

import pygame as pyg
import time
from Fichiers_variables.variables import *
from Jeu.player import *
from Jeu.coffres import ajout_coffre
from Interface.option import settings, flashing_effect, black_and_white
from Jeu.passage_niveau import *
from Affichage.affichage_divers import *
from Fichiers_variables.dictionnaire_armes import ARMES
from Monstres.class_monstre import *
from Affichage.fonctionnement_divers import *
from Fichiers_variables.gestion_fichiers import *
from Monstres.vagues import *
from Jeu.Quêtes import verif_kill_id, verif_acquerir_id, LIBELLES_QUETES
from Monstres.boss import spawn_boss, gestion_boss
from Minijeux.all_mj import mj
from Armes_Items.Classe_par_type_darme import ArmeOrbitale, ArmeOrbitaleExplosion
from Interface.Game_over import game_over
from Interface.victoire import victoire
from Fichiers_variables.dictionnaire_items import TYPES_ITEMS
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
from Fichiers_variables.progression import (
    init_progression, map_terminee, temps_limite
)

# Dico des objets spéciaux des joueurs (s'ils ne l'obtiennent pas pendant leur quête ils meurent)
OBJ_SPECIAL = {
    "Nerd":            "Console_allumee",
    "Nonne":           "Aura_divine",
    "Fille_populaire": "Highlighter",
}





def jeu(perso, nom, map_choisie="Cour"):
    """Boucle principale de jeu.

    Parameters
    ----------
    perso : str
        Le nom du perso choisi
    nom : str
        Le nom du joueur
    map_choisie : str
        Le nom de la map

    Returns
    -------
    str
        "menu" ou "quit" pour déterminer la suite
    """
    from Armes_Items.Explosions import Explosion
    from Armes_Items.Item_system import appliquer_stats_items
    from Armes_Items.Animation_items import lancer_animation_item
    Explosion.init_frames()
    # on récupère les noms des joueurs enregistrés pour la gestion de fichiers
    noms, new_tab = det_noms()
    res = ajouter_utilisateur(nom, noms)
    if res == False:
        argent = int(new_tab[1][nom])
        new_tab[0][nom] = int(new_tab[0][nom])
    else:
        noms, new_tab_armes, new_tab_quetes, new_tab_powerups = res
        argent = 0
        new_tab[0][nom] = 1
        new_tab[1][nom] = 0
        reecrire_fichier("niveau_argent", new_tab, noms)
        reecrire_fichier("armes_obtenues_par_joueur", new_tab_armes, noms)
        reecrire_fichier("quetes_reussis", new_tab_quetes, noms)
    definir_fichier_nouv_armes(noms) 
    # Initialise la progression du joueur
    init_progression(nom, noms)

    armes_joueur = contenu_fichier_armes() #armes acquises par le joueur, toutes parties confondues
    clock = pyg.time.Clock()
    run   = True

    from Jeu.power_up import apply_powerups
    p = Player(perso, nom)

    
    p.explosions = []

    # Armes de départ
    DEPART = {
        "Nerd":            {"armes": ["Epee_bleue"],   "items": []},
        "Fille_populaire": {"armes": ["Gloss_rose"],   "items": []},
        "Nonne":           {"armes": ["Croix_marron"], "items": []},
    }

    for nom_arme in DEPART[perso]["armes"]:
        p.ajouter_arme(nom_arme)

    for nom_item in DEPART[perso]["items"]:
        p.ajouter_item(nom_item)

    apply_powerups(p)
    p.vitesse_base = p.vitesse
    p.hp_max_base  = p.hp_max

    from Jeu.player_actif import set_player_actif
    set_player_actif(p)

    from Affichage.fonctionnement_divers import changer_map
    changer_map(map_choisie)

    monstres_presents, armes_et_items_possedees, xp_dispo = [], [], []
    boss_acheves, armes_possedees, items_possedes = [], [], []

    start_time = time.time()
    frame, pause_time, xp, dernier_coffre_apparu = 0, 0, 0, 0
    derniere_vague = 0
    xp_attendu = 20

    monstres_vague, boss, coord_monde = None, None, None
    vague = pause = boss_present = False
    coffre_existant = minijeu_fini = False

    anim_item     = None
    victoire_decl = False
    force_victoire = False
    TEMPS_OBJECTIF = temps_limite(map_choisie)

    popup_group = pyg.sprite.Group()
    completed_kill_quests    = set()
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
                if event.key == pyg.K_m:
                    force_victoire = True
                if event.key == pyg.K_z:
                    p.arme_active = (p.arme_active + 1) % len(p.armes)

        if not p.alive:
            if p.resurrection:
                p.hp           = p.hp_max // 2
                p.alive        = True
                p.resurrection = False
            else:
                action  = game_over()
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
                reecrire_fichier("niveau_argent", new_tab, noms)
                reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                if action == "menu":
                    return "menu"
                if action == "quit":
                    return "quit"

        if pause:
            pause, run, pause_time = menu_pause(new_tab, noms, armes_joueur)

        if not pause:
            remplir_fond(p)
            temps_ecoule = chrono(clock, start_time, pause_time)
            frame += 1

            # Gestion des mini-jeux
            coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees, armes_joueur = mj(
                perso, coord_monde, minijeu_fini, p,
                armes_et_items_possedees, armes_possedees, armes_joueur, map_choisie
            )

            
            if minijeu_fini and OBJ_SPECIAL[p.perso] not in armes_possedees:
                action  = game_over()
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
                reecrire_fichier("niveau_argent", new_tab, noms)
                reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                if action == "menu":
                    return "menu"
                if action == "quit":
                    return "quit"

            # Victoire
            if not victoire_decl and (temps_ecoule >= TEMPS_OBJECTIF or force_victoire):
                victoire_decl = True
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
                reecrire_fichier("niveau_argent", new_tab, noms)
                reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)

                nouvelle_map, nouveau_perso, nouvel_item = map_terminee(
                    nom, map_choisie, noms, perso, p
                )
                if nouvel_item:
                    armes_joueur = ajouter_arme(nom, nouvel_item, armes_joueur)
                    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                 # nouvel appel avec les stats
                action = victoire(
                    map_choisie,
                    nouvelle_map,
                    nouveau_perso,
                    temps_survie     = temps_ecoule,
                    argent_recolte   = argent,
                    monstres_tues    = p.kill_count,
                    armes_debloquees = len(armes_et_items_possedees),
                )
                if action == "menu":
                    return "menu"
                if action == "quit":
                    return "quit"

            
            coord_monde, minijeu_fini, armes_et_items_possedees, armes_possedees, armes_joueur = mj(
                perso, coord_monde, minijeu_fini, p,
                armes_et_items_possedees, armes_possedees, armes_joueur, map_choisie
            )

            # Armes
            p.update_armes()
            p.all_projectiles.update()
            p.all_zones.update()

            
            if frame % 10 == 0:
                print(f"--- Frame {frame} | zones: {len(p.all_zones)} | monstres: {len(monstres_presents)}")
                for zone in p.all_zones:
                    print(f"  Zone rect={zone.rect} damage={zone.damage}")
                    for m in monstres_presents:
                        collide = zone.rect.colliderect(m.rect)
                        if collide:
                            print(f"    HIT monstre rect={m.rect} -> degats({zone.damage})")
                            m.degats(zone.damage)
                    if boss_present and zone.rect.colliderect(boss.rect):
                        boss.degats(zone.damage)     

            # Armes orbitales
            for arme in p.armes:
                if isinstance(arme, ArmeOrbitale):
                    rect_orb = arme.get_rect_ecran()
                    for m in monstres_presents:
                        if rect_orb.colliderect(m.rect):
                            if isinstance(arme, ArmeOrbitaleExplosion):
                                arme.declencher_explosion()
                            m.degats(arme.damage)
                    if boss_present and rect_orb.colliderect(boss.rect):
                        if isinstance(arme, ArmeOrbitaleExplosion):
                            arme.declencher_explosion()
                        boss.degats(arme.damage)

            
            for explosion in p.explosions[:]:
                explosion.update(clock.get_time())
                if not explosion.a_fait_degats:
                    for m in monstres_presents:
                        if explosion.rect.colliderect(m.rect):
                            m.degats(explosion.degats)
                    if boss_present and explosion.rect.colliderect(boss.rect):
                        boss.degats(explosion.degats)
                    explosion.a_fait_degats = True
                if explosion.finished():
                    p.explosions.remove(explosion)

            
            for projectile in p.all_projectiles:
                for m in monstres_presents:
                    if projectile.rect.colliderect(m.rect):
                        m.degats(10)
                        if projectile.explode:
                            p.explosions.append(Explosion(m.x_monde, m.y_monde, p))
                        if hasattr(projectile, "poison") and projectile.poison:
                            m.empoisonner(
                                projectile.duree_poison,
                                projectile.degats_poison,
                                projectile.tick
                            )
                        projectile.kill()
                        break
                if boss_present and projectile.rect.colliderect(boss.rect):
                    boss.degats(10)
                    projectile.kill()

             # Gestion des monstres
            if frame % FREQUENCE == 0: # ajout d'un monstre toutes les 50 frames
                monstres_presents = ajouter_monstre(monstres_presents, p, perso)

            monstres_presents, p.kill_count = gestion_monstres_presents(
                monstres_presents, frame, p, xp_dispo
            )

            xp_dispo, xp = gestion_xp_fenetre(xp_dispo, p, xp_attendu)#xp récupéré par le joueur

            res = gestion_vague(derniere_vague, p, perso)
            if res is not False:
                derniere_vague, monstres_vague, coin = res
                x_monde, y_monde = coord_coin(coin, p)
            else:
                derniere_vague += 1  # actualise le nb de frames depuis la dernière vague

            if monstres_vague is not None:
                monstres_vague, p.kill_count = traverser_ecran(
                    monstres_vague, p, frame, xp_dispo, x_monde, y_monde
                )
                monstres_presents, vague = vague_130(
                    temps_ecoule, monstres_presents, vague, p, perso
                )

             # Gestion des boss
            boss_present, boss = spawn_boss(
                map_choisie, boss_present, boss_acheves, p, boss, perso
            )
            boss_present, boss_acheves = gestion_boss(
                boss, boss_present, p, frame, boss_acheves
            )

            # Gestion des coffres
            ajout = ajout_coffre(dernier_coffre_apparu, coffre_existant, p)
            if ajout is not False:
                nouveau_coffre, dernier_coffre_apparu, coffre_existant = ajout

            if coffre_existant:
                nouveau_coffre.pointer_coffre(p)
                if p.pos.colliderect(nouveau_coffre.rect):
                    gain = nouveau_coffre.determiner_recompense(
                        armes_et_items_possedees, p
                    )
                    if type(gain) == int:
                        argent += int(gain * (1 + p.argent_bonus))
                    else:
                        armes_et_items_possedees.append(gain[1])
                        if gain[0] == "arme":
                            armes_possedees.append(gain[1])
                            p.equiper_arme(gain[1])
                            armes_joueur = ajouter_arme(nom, gain[1], armes_joueur)
                            reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                        else:
                            items_possedes.append(gain[1])
                            p.inventaire_items.equiper_item(gain[1], p.niveau)
                            appliquer_stats_items(p, p.inventaire_items.calculer_stats())
                            armes_joueur = ajouter_arme(nom, gain[1], armes_joueur)
                            reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                            if gain[1] in TYPES_ITEMS.get(p.perso, {}):
                                anim_item = lancer_animation_item(
                                    gain[1], p, nom,
                                    TYPES_ITEMS[p.perso][gain[1]]["image"]
                                )
                    coffre_existant = False

            dernier_coffre_apparu += 1 # actualisation du nb de frames depuis l'apparition du dernier coffre
            dt = clock.get_time() / 1000.0 #ms en sec
            p.regen_hp(dt)
            
            # Dessin joueur et armes
            
            p.draw_player(frame)

            
            for arme in p.armes:
                if arme.visible:
                    arme.draw(WIN)

            p.all_projectiles.draw(WIN)
            p.all_zones.draw(WIN)

            for explosion in p.explosions:
                explosion.draw(WIN)
            # Anim items
            if anim_item is not None:
                if anim_item.en_cours():
                    anim_item.update()
                    anim_item.draw(WIN)
                else:
                    anim_item = None

            # Affichage des différentes barres de vie/xp/timer/kill_count
            afficher_xp(xp_attendu, p)
            afficher_timer_vie(temps_ecoule, p)

             # Quêtes
            kill_qid = verif_kill_id(p)
            if kill_qid and kill_qid not in completed_kill_quests:
                popup_group.add(PopupAchievement(LIBELLES_QUETES[kill_qid]))
                actualiser_quete(nom, kill_qid)
                completed_kill_quests.add(kill_qid)

            acq_qid = verif_acquerir_id(len(armes_et_items_possedees))
            if acq_qid and acq_qid not in completed_acquire_quests:
                popup_group.add(PopupAchievement(LIBELLES_QUETES[acq_qid]))
                actualiser_quete(nom, acq_qid)
                completed_acquire_quests.add(acq_qid)

            # Passage de niveau
            if p.update_xp(xp, xp_attendu):
                xp_attendu = passage(xp_attendu)# actualisation de l'xp attendu
                nb_choix   = p.get_nb_choix()# nbre de choix possibles (change en fonction de la chance)
                objet, pause_time = choix_arme(
                    p, armes_et_items_possedees,
                    monstres_presents, xp_dispo,
                    map_choisie, nb_choix
                )
                armes_et_items_possedees.append(objet[1])
                # même principe que les coffres
                if objet[0] == "arme":
                    armes_possedees.append(objet[1])
                    p.equiper_arme(objet[1])
                    armes_joueur = ajouter_arme(nom, objet[1], armes_joueur)
                    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                else:
                    items_possedes.append(objet[1])
                    p.inventaire_items.equiper_item(objet[1], p.niveau)
                    appliquer_stats_items(p, p.inventaire_items.calculer_stats())
                    armes_joueur = ajouter_arme(nom, objet[1], armes_joueur)
                    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
                    if objet[1] in TYPES_ITEMS.get(p.perso, {}):
                        anim_item = lancer_animation_item(
                            objet[1], p, nom,
                            TYPES_ITEMS[p.perso][objet[1]]["image"]
                        )

                from Jeu.player_actif import set_player_actif
                set_player_actif(None)
                new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
                

             # Déplace le fond et les objets sur la map en fonction des déplacements du joueur
            p.move_bg(monstres_presents, xp_dispo, monstres_vague, boss, boss_present)

            popup_group.update()
            popup_group.draw(WIN)

            if settings["music"]:
                if not pyg.mixer.music.get_busy():
                    pyg.mixer.music.load("Sons/son_quete2.mp3")
                    pyg.mixer.music.play(-1)
            else:
                if pyg.mixer.music.get_busy():
                    pyg.mixer.music.stop()
            if settings["bw"]:
                black_and_white(WIN)
            if settings["vfx"]:
                flashing_effect(WIN)

            pyg.display.flip()
        

    # Actualisation des données 
    new_tab = actualiser_donnees(nom, p.niveau, argent, new_tab)
    reecrire_fichier("niveau_argent", new_tab, noms)
    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
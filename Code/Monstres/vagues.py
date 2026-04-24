import pygame as pyg
from variables import *
from random import choice
from Monstres.class_monstre import *

################## FONCTION QUI REGROUPE TOUS LES EVENEMENTS ################

################################ VAGUE NORMALE #############################################
def gestion_vague(derniere_vague, niveau, p):
    if derniere_vague > 1800 and randint(1, 2)== 1:
        nb_monstres = randint(5, 10)
        monstres_dispos = [monstre for monstre in TYPES_MONSTRES if TYPES_MONSTRES[monstre]["niveau"] <= niveau]
        type = choice(monstres_dispos)
        coin = randint(1,4)
        if coin == 1 :
            x, y = 0, 0
        if coin == 2 :
            x, y = WIDTH, 0
        if coin == 3 :
            x, y = 0, HEIGHT
        if coin == 4 : 
            x, y = WIDTH, HEIGHT
        x, y = screen_to_world(x, y, p)
        monstres_vague = []
        for i in range(nb_monstres) :
            m = Monstre(type, p)
            m.vitesse += 7
            m.choix_coord((x, y))
            if choice((True, False)) :
                x += randint(-60,60)
            else : 
                y += randint(-60, 60)
            monstres_vague.append(m)
        return 0, monstres_vague, coin
    return False
    
def coord_coin(coin, p):
    coin_a_atteindre = 5 - coin # le coin en diagonale
    if coin_a_atteindre == 1:
        x_screen, y_screen = (-25,-25)
    if coin_a_atteindre == 2 :
        x_screen, y_screen = (WIDTH+25, -25)
    if coin_a_atteindre == 3 :
        x_screen, y_screen = (-25, HEIGHT+25)
    if coin_a_atteindre == 4 :
        x_screen, y_screen = (WIDTH+25, HEIGHT+25)
    x_monde, y_monde = screen_to_world(x_screen, y_screen, p)
    return x_monde, y_monde

def traverser_ecran(monstres_vague, p, frame, xp_dispo, x_monde, y_monde):
    kill_count = p.kill_count
    for m in monstres_vague[:]:
        dx = x_monde - m.x_monde
        dy = y_monde - m.y_monde
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 5:
            m.show(frame) # affiche tous les monstres existant
            if m.hp > 0 :
                m.follow(x_monde, y_monde) # monstres suivant le joueur
                if p.pos.colliderect(m.rect) and frame%10 == 0:
                    p.degats(m.puissance) # dégâts en cas de collision
            else :
                kill_count += 1
                monstres_vague.remove(m)
                xp_dispo.append(m)
    return monstres_vague, kill_count
################### VAGUE AU BOUT D'1 MIN 30 #####################

def vague_130(temps_ecoule, monstres_presents, vague, p):
    if int(temps_ecoule%90) == 0 and int(temps_ecoule) != 0 and not vague:
        type = choice(TYPES)
        w = TYPES_MONSTRES[type]["image"].get_width()
        h = TYPES_MONSTRES[type]["image"].get_height()
        nb_mx = WIDTH//(w)
        nb_my = HEIGHT//(h)
        for x in range(1,nb_mx) :
            m1, m4 = Monstre(type, p), Monstre(type, p)
            coord1 = screen_to_world(x*w, 0, p)
            m1.choix_coord(coord1)
            coord4 = screen_to_world(x*w, HEIGHT, p)
            m4.choix_coord(coord4)
            monstres_presents.append(m1)
            monstres_presents.append(m4)
        for y in range(nb_my):
            m2, m3 = Monstre(type, p), Monstre(type, p)
            coord2 = screen_to_world(0, y*h, p)
            coord3 = screen_to_world(WIDTH, y*h, p)
            m2.choix_coord(coord2)
            m3.choix_coord(coord3)
            monstres_presents.append(m2)
            monstres_presents.append(m3)
        return monstres_presents, True
    elif int(temps_ecoule)%90 == 0:
        return monstres_presents, True
    else : 
        return monstres_presents, False
    
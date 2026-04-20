import pygame as pyg
from variables import *
from random import choice
from class_monstre import *

################## FONCTION QUI REGROUPE TOUS LES EVENEMENTS ################

################### VAGUE AU BOUT D'1 MIN 30 #####################

def vague_130(temps_ecoule, monstres_presents, vague, p):
    if int(temps_ecoule%30) == 0 and int(temps_ecoule) != 0 and not vague:
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
    elif int(temps_ecoule)%30 == 0:
        return monstres_presents, True
    else : 
        return monstres_presents, False
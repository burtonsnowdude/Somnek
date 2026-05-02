"""
Minijeu de la nonne : N'oubliez pas les paroles
"""
from Minijeux.minijeu2 import regler_volume, spawn_objet, play_sound, draw_objet, collision, retour_ligne, replique
import pygame as pyg
from Fichiers_variables.variables import *
from random import shuffle
from Affichage.fonctionnement_divers import screen_to_world, camera
from Fichiers_variables.gestion_fichiers import ajouter_arme

import time
pyg.init()
pyg.mixer.init()

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = [0]*4
OBJET = pyg.image.load("Images/Armes_items/berserk.png")
spritesheet_noubliez_pas_les_paroles = pyg.image.load("Images/Autre/anim_noubliez_pas_les_paroles.png")
ANIM_NOUBLIEZ_PAS_LES_PAROLES = decouper_image(spritesheet_noubliez_pas_les_paroles, 5, 5, 3)
SON = "Sons/son_quete2.mp3"
GRIS_1 = (164, 155, 182, 200)
GRIS_2 = (164, 186, 176, 200)
JE_VOUS_SALUE_MARIE = "Sons/je_vous_salue_marie.mp3"
TROIS_PTITS_CHATS = "Sons/chats.mp3"
NOTRE_PERE = "Sons/notre_pere.mp3"
CHANTS = ["Je vous salue Marie", "Notre père", "3 ptits chats"]

PAROLES = {
    "Je vous salue Marie" : {"Musique" : JE_VOUS_SALUE_MARIE,
        "Paroles_trou" : ["Je vous salue, Marie, pleine de grâces",
        "Le Seigneur est avec vous.",
        "Vous êtes bénie entre toutes les _______",
        "Et Jésus, le fruit de vos entrailles, est béni.",
        "Sainte Marie, Mère de Dieu,",
        "Priez pour nous, pauvres ________", 
        "Maintenant et à l'heure de notre ____",
        "Amen."],
        "Mots_non_accentues" : ["femmes", "beni", "pecheurs", "mort"]},
    "Notre père" : {"Musique" : NOTRE_PERE,
        "Paroles_trou" : ["Notre Père, qui est aux _____,",
                     "Que ton nom soit _________,",
                     "Que ton règne vienne",
                     "Que ta volonté soit faite", 
                     "Sur la terre comme au ____",
                     "Donne-nous aujourd'hui",
                     "Notre pain de ce jour",
                     "Pardonne-nous nos ________",
                     "Comme nous pardonnons aussi",
                     "A ceux qui nous ont offensés",
                     "Et ne nous laisse pas entrer en tentation",
                     "Mais délivre nous du ___", 
                     "Amen"],
        "Mots_non_accentues" : ["cieux", "sanctifie", "ciel", "offenses", "mal"]},
    "3 ptits chats" : {"Musique" : TROIS_PTITS_CHATS,
        "Paroles_trou" : ["Trois p'tits chats",
            "Trois p'tits chats",
            "Trois p'tits chats chats chats",
            "Chapeau de _____",
            "Chapeau de paille",
            "Chapeau de paille paille paille paille",
            "Paillasson",
            "Paillasson",
            "Paillasson son son son",
            "__________",
            "Somnambule",
            "Somnambule bull bull bull",
            "________",
            "Bulletin",
            "Bulletin tin tin tin",
            "__________",
            "Tintamarre",
            "Tintamarre marre marre",
            "________",
            "Marabout",
            "Marabout bout bout bout",
            "Bout d'ficelle",
            "Bout d'ficelle",
            "Bout d'ficelle celle celle celle",
            "Selle de ______",
            "Selle de cheval",
            "Selle de cheval val val val"],
        "Mots_non_accentues" : ["paille", "somnambule", "bulletin", "tintamarre", "marabout", "cheval"]}
}

def minijeu3(p, coord_monde, minijeu3_fini, armes_possedees, armes_joueur):
    if coord_monde == None:
        coord_screen = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN, p)
        coord_screen = (300, 200)
        coord_monde = screen_to_world(coord_screen[0], coord_screen[1], p)
    coord_screen = camera(coord_monde[0], coord_monde[1], p)
    regler_volume(coord_monde, p, SON)
    play_sound(SON)
    draw_objet(coord_screen, OBJET)
    if collision(coord_screen, OBJET, p):
        anim_debut(SON)
        victoire = noubliez_pas_les_paroles()
        if victoire :
            armes_possedees.append("Aura_divine")
            armes_joueur = ajouter_arme(p.nom, "Aura_divine", armes_joueur)
        anim_fin(victoire, SON)
        minijeu3_fini = True
    return coord_monde, minijeu3_fini, armes_possedees, armes_joueur

def anim_debut(son):
    replique("Bien le bonjour ! Vous êtes venue pour prier j'imagine ?", GRIS_1, (0,0,0))
    play_sound(son)
    replique("Moi ? (* regarde derrière elle *) Je... Ah oui, oui tout à fait.", GRIS_2, (0,0,0))
    play_sound(son)
    replique("Parfait, dans ce cas prenez place ! On a essayé d'être un petit peu 'fun' comme disent les jeunes donc ce sera un peu différent aujourd'hui.", GRIS_1, (0,0,0))
    play_sound(son)
    replique("C'est un prank ? Où sont les caméras ? Et d'ailleurs, je ne vois personne, est-ce Dieu qui me parle ?", GRIS_2, (0,0,0))
    play_sound(son)
    replique("Et bien, on dirait qu'on ne peut rien vous cacher à vous... C'est un N'oubliez pas les paroles ! (Oui oui comme l'émission)", GRIS_1, (0,0,0))
    play_sound(son)
    replique("... Un peu bizarre les développeurs quand même... Et comment on joue ?", GRIS_2, (0,0,0))
    play_sound(son)
    replique("Rien de plus simple ! Vous allez entendre 3 musiques, il faudra tout simplement écrire les mots manquants ! Ah, aussi, pas besoin de vous préoccuper des accents, des majuscules... le Saint Esprit s'en occupe pour vous. ", GRIS_1, (0,0,0))
    play_sound(son)
    replique("Et pour valider, vous faites Entrée, voilà c'est tout bonne chance !", GRIS_1, (0,0,0))
    frame = 0
    i = 0
    while i < 21 :
        play_sound(son)
        frame += 1
        WIN.blit(ANIM_NOUBLIEZ_PAS_LES_PAROLES[i], (0,0))
        if frame%6 == 0:
            i += 1
        pyg.display.update()
    pyg.mixer.music.stop()

def anim_fin(victoire, son):
    if victoire :
        replique("Bravo ! Vous maitrisez vos classiques à ce que je vois.", GRIS_1, (0,0,0))
        play_sound(son)
        replique("Bien sûr !", GRIS_2, (0,0,0))
        play_sound(son)
        replique("Oh, mais qu'est-ce que c'est que ça ??? Le halo du Saint Esprit qui vient sur vous ???", GRIS_1, (0,0,0))
        play_sound(son)
        replique("Comment ? Dieu soit loué, je l'ai attendu toute ma vie !", GRIS_2, (0,0,0))
        play_sound(son)
        replique("Chanceuse... j'aurais dû participer aussi finalement...", GRIS_1, (0,0,0))
        play_sound(son)
        replique("Mais Vous êtes déjà divin nan ?", GRIS_2, (0,0,0))
        play_sound(son)
        replique("Ah oui c'est vrai, j'avais oublié (my bad).", GRIS_1, (0,0,0))
    else :
        replique("Que dire... vous avez échoué.", GRIS_1, (0,0,0))
        play_sound(son)
        replique("Je vais me confesser tout de suite alors.", GRIS_2, (0,0,0))
        play_sound(son)
        replique("Non non hors de question, vous m'avez cruellement déçue. Hors de mon église svp.", GRIS_1, (0,0,0))
        play_sound(son)
        replique("Ah... Bon, bonne journée alors (Amen).", GRIS_2, (0,0,0))
    frame = 0
    i = 0
    while i < 21 :
        play_sound(son)
        frame += 1
        WIN.blit(ANIM_NOUBLIEZ_PAS_LES_PAROLES[i], (0,0))
        if frame%6 == 0:
            i += 1
        pyg.display.update()

def pause_differenciee(chant, j):
    if chant == "3 ptits chats":
        if j%3 == 2 :
            pyg.time.delay(2180)
        else :
            pyg.time.delay(730)
    elif chant == "Je vous salue Marie":
        pyg.time.delay(5300)
    else :
        pyg.time.delay(5000)

def noubliez_pas_les_paroles():
    i = 0
    clock = pyg.time.Clock()
    win_count = 0
    for i in range(3) :
        run = True
        complete = 0
        chant = CHANTS[i]
        texte = PAROLES[chant]["Paroles_trou"]
        play_sound(PAROLES[chant]["Musique"])
        while run :
            clock.tick(60)
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
            for j in range(len(texte)) :
                if j%3 == 0:
                    WIN.fill((225, 225, 225))
                    for t in range(-BGX, WIDTH + BGX, BGX):
                        for x in range(-BGY, HEIGHT + BGY, BGY):
                                WIN.blit(BG, (t, x))

                    gris = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
                    gris.fill(GRIS_1)  
                    WIN.blit(gris, (0, 0))
                ligne = texte[j]
                l = FONT.render(ligne, True, (20, 20, 20))
                WIN.blit(l, (80, 100+20*(j%3)))
                pyg.display.update()
                if "_" in ligne :
                    pyg.mixer.music.pause()
                    mot = ecrire(l, j)
                    if mot == PAROLES[chant]["Mots_non_accentues"][complete]:
                        win_count += 1
                    complete += 1
                    pyg.mixer.music.unpause()
                pause_differenciee(chant, j)
                if j == len(texte)-1:
                    pyg.mixer.music.stop()
                    run = False
                    frame = 0
                    i = 0
                    while i < 21 :
                        frame += 1
                        WIN.blit(ANIM_NOUBLIEZ_PAS_LES_PAROLES[i], (0,0))
                        if frame%6 == 0:
                            i += 1
                        pyg.display.update()
    return win_count >= 5

        
def ecrire(l, k):
    waiting = True
    mot = ""
    while waiting:
        lettre = None
        WIN.fill((225, 225, 225))
        for t in range(-BGX, WIDTH + BGX, BGX):
            for j in range(-BGY, HEIGHT + BGY, BGY):
                    WIN.blit(BG, (t, j))
        gris = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        gris.fill(GRIS_1)  
        WIN.blit(gris, (0, 0))
        WIN.blit(l, (80, 100+20*(k%3)))
        l_rect = l.get_rect()
        l_rect.topleft = (80, 100+20*(k%3))
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN :
                keys = pyg.key.get_pressed()
                if keys[pyg.K_a]:
                    lettre = "a"
                if keys[pyg.K_b]:
                    lettre = "b"
                if keys[pyg.K_c]:
                    lettre = "c"
                if keys[pyg.K_d]:
                    lettre = "d"
                if keys[pyg.K_e]:
                    lettre = "e"
                if keys[pyg.K_f]:
                    lettre = "f"
                if keys[pyg.K_g]:
                    lettre = "g"
                if keys[pyg.K_h]:
                    lettre = "h"
                if keys[pyg.K_i]:
                    lettre = "i"
                if keys[pyg.K_j]:
                    lettre = "j"
                if keys[pyg.K_k]:
                    lettre = "j"
                if keys[pyg.K_l]:
                    lettre = "l"
                if keys[pyg.K_m]:
                    lettre = "m"
                if keys[pyg.K_n]:
                    lettre = "n"
                if keys[pyg.K_o]:
                    lettre = "o"
                if keys[pyg.K_p]:
                    lettre = "p"
                if keys[pyg.K_q]:
                    lettre = "q"
                if keys[pyg.K_r]:
                    lettre = "r"
                if keys[pyg.K_s]:
                    lettre = "s"
                if keys[pyg.K_t]:
                    lettre = "t"
                if keys[pyg.K_u]:
                    lettre = "u"
                if keys[pyg.K_v]:
                    lettre = "v"
                if keys[pyg.K_w]:
                    lettre = "w"
                if keys[pyg.K_x]:
                    lettre = "x"
                if keys[pyg.K_y]:
                    lettre = "y"
                if keys[pyg.K_z]:
                    lettre = "z"
                if keys[pyg.K_SPACE]:
                    lettre = " "
                if keys[pyg.K_BACKSPACE]:
                    mot = mot[0:-1]
                if keys[pyg.K_RETURN]:
                    return mot
        if lettre is not None:
            mot += lettre
        affichage = FONT.render(mot, True, (0, 0, 0))
        rect = affichage.get_rect()
        rect.bottomright= l_rect.bottomright
        WIN.blit(affichage, rect)
        pyg.display.update()
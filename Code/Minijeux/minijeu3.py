"""
Minijeu de la nonne : N'oubliez pas les paroles
"""
from Minijeux.minijeu2 import regler_volume, spawn_objet, play_sound, draw_objet, collision, retour_ligne
import pygame as pyg
from Fichiers_variables.variables import *
from random import shuffle
from Affichage.fonctionnement_divers import screen_to_world, camera

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = [0]*4
OBJET = pyg.image.load("Images/Armes_items/berserk.png")

PAROLES = {
    0 : {"Musique" : None,
        "Paroles" : None},
    1 : {"Musique" : None,
        "Paroles" : None},
    2 : {"Musique" : None,
        "Paroles" : None}
}

def minijeu3(p, coord_monde, minijeu3_fini):
    if coord_monde == None:
        coord_screen = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN, p)
        coord_screen = (300, 200)
        coord_monde = screen_to_world(coord_screen[0], coord_screen[1], p)
    coord_screen = camera(coord_monde[0], coord_monde[1], p)
    #regler_volume(coord_monde, p, SON)
    #play_sound(SON)
    draw_objet(coord_screen, OBJET)
    if collision(coord_screen, OBJET, p):
        noubliez_pas_les_paroles()
        minijeu3_fini = True
        
    return coord_monde, minijeu3_fini

def noubliez_pas_les_paroles():
    run = True
    i = 0
    clock = pyg.time.Clock()
    win_count = 0
    #ordre = [[PAROLES[i]["Paroles"], j] for j in range(len(PAROLES[i][1]))]
    while run and i < max(PAROLES)+1:
        clock.tick(60)
        WIN.fill((225, 225, 225))
        for t in range(-BGX, WIDTH + BGX, BGX):
            for j in range(-BGY, HEIGHT + BGY, BGY):
                    WIN.blit(BG, (t, j))
        mouse_pos = pyg.mouse.get_pos()

        gris = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        gris.fill((255, 182, 229, 200))  
        WIN.blit(gris, (0, 0))
        #texte = PAROLES[i][0]
        #texte = retour_ligne(texte)
        #for t in texte :
        #    question = FONT.render(t, True, (163, 38, 47))
        #    WIN.blit(question, (80, 100+20*texte.index(t)))
        waiting = True
        mot = ""
        while waiting:
            WIN.fill((225, 225, 225))
            for t in range(-BGX, WIDTH + BGX, BGX):
                for j in range(-BGY, HEIGHT + BGY, BGY):
                        WIN.blit(BG, (t, j))
            gris = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
            gris.fill((255, 182, 229, 200))  
            WIN.blit(gris, (0, 0))
            lettre = None
            #play_sound(PAROLES[i]["Musique"])
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()

                if event.type == pyg.MOUSEBUTTONDOWN:
                    mouse_pos = pyg.mouse.get_pos()
        
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
            if lettre is not None:
                mot += lettre
            affichage = FONT.render(mot, True, (0, 0, 0))
            rect = affichage.get_rect()
            rect.center = (CENTREx, CENTREy)
            WIN.blit(affichage, rect)
            pyg.display.update()
        i += 1
    return win_count >= 2
# (oui c'est de la fausse générosité) comme ça vous pouvez ajouter des questions sans tout casser
        

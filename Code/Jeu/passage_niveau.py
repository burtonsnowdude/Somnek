from Fichiers_variables.variables import *
from random import *
import time
import pygame as pyg
from math import ceil
from Interface.Class_Button import Button
from Fichiers_variables.dictionnaire_items import *

FONT_NIVEAU = pyg.font.SysFont("Press Start 2P", 50) 
def passage(xp_attendu, seuil):
    """Incrémente le seuil et augmente l'xp attendu pour le prochain niveau

    Parameters
    ----------
    xp_attendu : float
        L'xp attendu pour passer au prochain niveau
    seuil : int
            Le seuil de valeur maximale pour une arme (en fonction du niveau atteint)
    
    Returns
    -------
    tuple(int, float)
        contient le seuil et l'xp attendu actualisés
    """
    xp_attendu = ceil(1.5*xp_attendu)
    if seuil+4 <= len(ARMES) :
        seuil += 4
    
    return seuil, xp_attendu
    

def choix_arme(p, seuil, armes_possedees):
    """Permet au joueur de choisir une arme à la fin d'un niveau

    Parameters
    ----------
    p : Self@Player
        Le joueur
    seuil : int
            Le seuil de valeur maximale pour une arme (en fonction du niveau atteint)
    armes_possedees : list
        La liste des armes possédées par le joueur

    Returns
    -------
    tuple(list, float)
        contient la liste des armes possedees par le joueur et le temps de pause
    """
    if p.niveau < seuil :
        debut = time.time()
        clock = pyg.time.Clock()
        armes_dispo = []
        niveau = 1
        while niveau < p.niveau :
            for arme in GESTION_NIVEAU_ITEMS[p.perso]["Niveau "+str(niveau)]:
                armes_dispo.append(arme)
            niveau += 1
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
        vert = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        vert.fill((204, 237, 204, 200))
        texte = FONT_NIVEAU.render("Niveau "+str(p.niveau)+" atteint !", True, (17, 97, 17))
        buttons = [Button(choix[i], choix[i], 400, 200+100*i, 650, 80, FONT) for i in range(3)]
        for b in buttons :
            b.color1 = (17, 97, 17)
            b.color2 = (43, 119, 52)
        waiting = True
        selec = 0

        while waiting:
            clock.tick(60)
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_UP and selec != 0:
                        selec -= 1
                    if event.key == pyg.K_DOWN and selec != 2:
                        selec += 1
                    if event.key == pyg.K_RETURN:
                        choix = buttons[selec].action
                        waiting = False
                if event.type == pyg.MOUSEBUTTONDOWN:
                    mouse_pos = pyg.mouse.get_pos()
                
                    for btn in buttons:
                        if btn.rect.collidepoint(mouse_pos):
                            choix = btn.action
                            waiting = False
            mouse_pos = pyg.mouse.get_pos()
            
            WIN.fill((225, 225, 225))
            for t in range(-BGX, WIDTH + BGX, BGX):
                for j in range(-BGY, HEIGHT + BGY, BGY):
                        WIN.blit(BG, (t, j))
            mouse_pos = pyg.mouse.get_pos()
  
            WIN.blit(vert, (0, 0))
            for btn in buttons:
                btn.draw(WIN, mouse_pos)
            WIN.blit(texte, texte.get_rect(center=(CENTREx, 100)))
            pyg.display.update()
        return choix, time.time()-debut
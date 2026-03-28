from variables import *
from random import *
import time
import pygame as pyg

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
    xp_attendu *= 1.5
    if seuil+4 <= len(ARMES) :
        seuil += 4
    if xp_attendu%2 != 0 :
        xp_attendu += 1 
    return seuil, xp_attendu
    # pour toujours avoir un nombre pair (évite un trop grand nombre de décimales)
    # passage de niveau (j'attends la class armes encore une fois c'est des listes arbitraires)

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
        armes_dispo = [arme for arme in ARMES if ARMES[arme] < seuil]
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
        options = [pyg.Rect(370, 200+40*i, 100, 30) for i in range(3)]
        for option in options :
            pyg.draw.rect(WIN, (255, 255, 255), option)
        selec = 0       
        for i in range(len(choix)) :
            texte = FONT.render(choix[i], 1, (0, 0, 0)) 
            WIN.blit(texte, (390, 205+i*40))
        pyg.display.update()
        debut = time.time()
        entree = False
        while not entree:
            pause_time = time.time() - debut
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()

                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_UP and selec != 0:
                        pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                        texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                        WIN.blit(texte, (390, 205+selec*40))
                        selec -= 1

                    if event.key == pyg.K_DOWN and selec != 2:
                        pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                        texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                        WIN.blit(texte, (390, 205+selec*40))
                        selec += 1

                    if event.key == pyg.K_RETURN:
                        entree = True

            pyg.draw.rect(WIN, (120, 120, 250), options[selec])

            texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
            WIN.blit(texte, (390, 205+selec*40))
            pyg.display.update()

        armes_possedees.append(choix[selec])
        print(armes_possedees)
        return armes_possedees, pause_time

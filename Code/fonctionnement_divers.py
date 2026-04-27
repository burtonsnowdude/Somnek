import time
from variables import *
from gestion_fichiers import reecrire_fichier_niveau_argent, reecrire_fichier_armes
from affichage_divers import PopupAchievement

def remplir_fond(p):
    # Fond d'écran 
    WIN.fill((225, 225, 225)) 
    offset_x = p.x_monde % BGX
    offset_y = p.y_monde % BGY
    for i in range(-BGX, WIDTH + BGX, BGX):
        for j in range(-BGY, HEIGHT + BGY, BGY):
                WIN.blit(BG, (i-offset_x, j-offset_y))

def chrono(clock, start_time, pause_time):
    clock.tick(60) # fixe le nombre de frames par seconde
    temps_ecoule = time.time() - start_time - pause_time
    return temps_ecoule

def camera(x, y, p):
    x_screen = CENTREx - (p.x_monde - x)
    y_screen = CENTREy - (p.y_monde - y)
    return x_screen, y_screen

def screen_to_world(x_screen, y_screen, p):
    x_monde = p.x_monde + (x_screen - CENTREx)
    y_monde = p.y_monde + (y_screen - CENTREy)
    return x_monde, y_monde

def menu_pause(new_tab, noms, armes_joueur):
    taille_btn = 300
    pause_options = ["SAUVEGARDER", "QUITTER", "STATISTIQUES", "INVENTAIRE"]
    boutons = [pyg.Rect(CENTREx-taille_btn//2, 200+40*i, taille_btn, 30) for i in range(len(pause_options))]
    for bouton in boutons :
        pyg.draw.rect(WIN, (255, 255, 255), bouton)
    selec = 0       
    for i in range(len(pause_options)) :
        texte = FONT.render(pause_options[i], 1, (0, 0, 0)) 
        WIN.blit(texte, (CENTREx-taille_btn//2, 205+i*40))
    pyg.display.update()
    entree = False
    pause = True
    run = True
    choix = None
    debut = time.time()
    while not entree and pause:
        pause_time = time.time() - debut
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_SPACE:
                    pause = False
                if event.key == pyg.K_UP and selec != 0:
                    pyg.draw.rect(WIN, (255, 255, 255), boutons[selec])
                    texte = FONT.render(pause_options[selec], 1, (0, 0, 0)) 
                    WIN.blit(texte, (CENTREx-taille_btn//2, 205+selec*40))
                    selec -= 1

                if event.key == pyg.K_DOWN and selec != len(boutons)-1:
                    pyg.draw.rect(WIN, (255, 255, 255), boutons[selec])
                    texte = FONT.render(pause_options[selec], 1, (0, 0, 0)) 
                    WIN.blit(texte, (CENTREx-taille_btn//2, 205+selec*40))
                    selec += 1

                if event.key == pyg.K_RETURN:
                    entree = True
                    choix = pause_options[selec]

        pyg.draw.rect(WIN, (120, 120, 250), boutons[selec])

        texte = FONT.render(pause_options[selec], 1, (0, 0, 0)) 
        WIN.blit(texte, (CENTREx-taille_btn//2, 205+selec*40))
        pyg.display.update()
    if choix == "SAUVEGARDE":
        sauvegarde(new_tab, noms, armes_joueur)
        popup = PopupAchievement("Sauvegarde effectuée !")
        popup.update()

    if choix == "QUITTER":
        run = False
    if choix == "STATISTIQUES":
        pass
    if choix == "INVENTAIRE":
        pass
    return pause, run, pause_time

def sauvegarde(new_tab, noms, armes_joueur):
    reecrire_fichier_niveau_argent(new_tab, noms) 
    reecrire_fichier_armes(armes_joueur, noms) 



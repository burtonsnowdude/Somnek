import time
from Fichiers_variables.variables import *
from Fichiers_variables.gestion_fichiers import reecrire_fichier
from Affichage.affichage_divers import PopupAchievement
from Interface.Class_Button import Button

FONT_PAUSE = pyg.font.SysFont("Press Start 2P", 50)

MAPS_CHEMINS = {
    "Metro": "Images/Maps/metro.png",
    "Cour":  "Images/Maps/map_cour_vraie.png",
    "Rue":   "Images/Maps/map_rue.png",
    "Ruelle":   "Images/Maps/Alley.png",
    "Foire":   "Images/Maps/map_foire.png" }

def changer_map(nom_map):
    global BG, BGX, BGY
    BG = pyg.image.load(MAPS_CHEMINS.get(nom_map, "Images/Maps/map_cour_vraie.png"))
    BGX, BGY = BG.get_size()

def remplir_fond(p):
    WIN.fill((225, 225, 225))
    offset_x = p.x_monde % BGX
    offset_y = p.y_monde % BGY
    for i in range(-BGX, WIDTH + BGX, BGX):
        for j in range(-BGY, HEIGHT + BGY, BGY):
            WIN.blit(BG, (i-offset_x, j-offset_y))

def chrono(clock, start_time, pause_time):
    clock.tick(60)
    return time.time() - start_time - pause_time

def camera(x, y, p):
    x_screen = CENTREx - (p.x_monde - x)
    y_screen = CENTREy - (p.y_monde - y)
    return x_screen, y_screen

def screen_to_world(x_screen, y_screen, p):
    x_monde = p.x_monde + (x_screen - CENTREx)
    y_monde = p.y_monde + (y_screen - CENTREy)
    return x_monde, y_monde

def menu_pause(new_tab, noms, armes_joueur):
    run = True
    debut = time.time()
    clock = pyg.time.Clock()
    choix = ["SAUVEGARDER", "QUITTER", "STATISTIQUES", "INVENTAIRE"]
    vert = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    vert.fill((204, 237, 204, 200))
    texte = FONT_PAUSE.render("Menu de pause", True, (17, 97, 17))
    buttons = [Button(choix[i], choix[i], 400, 200+100*i, 650, 80, FONT) for i in range(4)]
    for b in buttons:
        b.color1 = (17, 97, 17)
        b.color2 = (43, 119, 52)
    waiting = True
    selec = 0
    pause = True

    while waiting and pause:
        clock.tick(60)
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_SPACE:
                    pause = False
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
        WIN.blit(vert, (0, 0))
        for btn in buttons:
            btn.draw(WIN, mouse_pos)
        WIN.blit(texte, texte.get_rect(center=(CENTREx, 100)))
        pyg.display.update()

    if choix == "SAUVEGARDER":  # ← corrigé (était "SAUVEGARDE")
        sauvegarde(new_tab, noms, armes_joueur)
    if choix == "QUITTER":
        run = False
    if choix == "STATISTIQUES":
        pass
    if choix == "INVENTAIRE":
        pass

    return pause, run, time.time() - debut

def sauvegarde(new_tab, noms, armes_joueur):
    reecrire_fichier("niveau_argent", new_tab, noms)
    reecrire_fichier("armes_obtenues_par_joueur", armes_joueur, noms)
from Fichiers_variables.variables import *
from random import *
import time
import pygame as pyg
from math import ceil
from Interface.Class_Button import Button
from Fichiers_variables.dictionnaire_items import GESTION_NIVEAU_ITEMS, TYPES_ITEMS
from Fichiers_variables.dictionnaire_armes import GESTION_DES_NIVEAUX_ARMES, TYPES_ARMES
from Minijeux.minijeu2 import retour_ligne
from Interface.choix_map import IMAGES_MAPS

FONT_NIVEAU     = pyg.font.SysFont("Press Start 2P", 50)
FONT_TEXTE_ARME = pyg.font.SysFont("Press Start 2P", 17)
GEMMES          = pyg.image.load("Images/Autre/gemmes.png")


def passage(xp_attendu):
    xp_attendu = ceil(1.5 * xp_attendu)
    return xp_attendu


def show_image(button, p):
    y = button.rect.center[1]
    if button.action in TYPES_ARMES[p.perso]:
        image = TYPES_ARMES[p.perso][button.action]["image"]
    else:
        image = TYPES_ITEMS[p.perso][button.action]["image"]
    rect = image.get_rect()
    rect.center = (550, y)
    WIN.blit(image, rect)


def show_texte(button, p):
    if button.action in TYPES_ARMES[p.perso]:
        texte = TYPES_ARMES[p.perso][button.action]["texte"]
    else:
        texte = TYPES_ITEMS[p.perso][button.action]["texte"]
    texte = retour_ligne(texte, 50)
    for t in range(len(texte)):
        txt = FONT_TEXTE_ARME.render(texte[t], True, (255, 255, 255))
        rect = txt.get_rect()
        x, y = button.rect.center
        rect.center = (x, y + t * 15)
        WIN.blit(txt, rect)


def scroll_gemme(frame):
    y = frame % HEIGHT
    if y != 0:
        y2 = y - HEIGHT
        WIN.blit(GEMMES, (0, y2))
    WIN.blit(GEMMES, (0, y))


def choix_arme(p, armes_et_items_possedees, monstres_presents, xp_present, map_name, nb_choix):
    map_img = IMAGES_MAPS[map_name]
    mapX, mapY = map_img.get_size()
    debut  = time.time()
    clock  = pyg.time.Clock()

    armes_dispo = []
    items_dispo = []
    niveau = 1
    while niveau < p.niveau:
        for item in GESTION_NIVEAU_ITEMS[p.perso]["Niveau " + str(niveau)]:
            items_dispo.append(item)
        niveau += 1
    niveau = 1
    while niveau < p.niveau:
        if "Niveau " + str(niveau) in GESTION_DES_NIVEAUX_ARMES[p.perso]:
            for arme in GESTION_DES_NIVEAUX_ARMES[p.perso]["Niveau " + str(niveau)]:
                armes_dispo.append(arme)
        niveau += 1

    dispo = items_dispo + armes_dispo
    armes_enlevees = []
    for arme in dispo[:]:
        if arme in armes_et_items_possedees and not arme in armes_enlevees:
            dispo.remove(arme)
            armes_enlevees.append(arme)

    # Fallback si tout est déjà possédé
    if len(dispo) == 0:
        dispo = items_dispo + armes_dispo

    choix = []
    compteur = 0
    while compteur < nb_choix:
        arme = choice(dispo)
        if arme not in choix:
            choix.append(arme)
            compteur += 1

    affich = []
    for mot in choix:
        m = mot.replace("_", " ").upper()
        affich.append(m)

    violet = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    violet.fill((102, 62, 86, 150))
    texte  = FONT_NIVEAU.render("Niveau " + str(p.niveau) + " atteint !", True, (255, 255, 255))
    buttons = [Button(affich[i], choix[i], 400, 200 + 100 * i, 400, 80, FONT) for i in range(nb_choix)]
    for b in buttons:
        b.color1      = (122, 48, 113)
        b.color2      = (161, 99, 158)
        b.rect_center = (400, b.rect.topleft[1] + 20)

    waiting = True
    selec   = 0
    frame   = 0

    while waiting:
        clock.tick(60)
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                exit()
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_UP and selec != 0:
                    selec -= 1
                if event.key == pyg.K_DOWN and selec != 2:
                    selec += 1
                if event.key == pyg.K_RETURN:
                    choix_final = buttons[selec].action
                    type_objet  = "arme" if choix_final in armes_dispo else "item"
                    waiting     = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                mouse_pos = pyg.mouse.get_pos()
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        choix_final = btn.action
                        type_objet  = "arme" if btn.action in armes_dispo else "item"
                        waiting     = False

        mouse_pos = pyg.mouse.get_pos()
        WIN.fill((225, 225, 225))
        for t in range(-mapX, WIDTH + mapX, mapX):
            for j in range(-mapY, HEIGHT + mapY, mapY):
                WIN.blit(map_img, (t, j))
        for m in monstres_presents:
            m.show(1)
        for xp in xp_present:
            xp.show_xp()
        WIN.blit(violet, (0, 0))
        scroll_gemme(frame)
        frame += 1
        for btn in buttons:
            btn.draw(WIN, mouse_pos)
            show_image(btn, p)
            show_texte(btn, p)
        WIN.blit(texte, texte.get_rect(center=(CENTREx, 100)))
        pyg.display.update()

    return (type_objet, choix_final), time.time() - debut
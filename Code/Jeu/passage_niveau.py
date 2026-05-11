"""
passage de niveau — somnek

ce fichier gère :
- l'évolution de l'xp nécessaire
- l'écran de choix d'arme / item lors d'un level up

logique :
- priorité aux objets débloqués au niveau actuel
- fallback sur les anciens niveaux si besoin
- gestion dynamique du nombre de choix
"""

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
    """
    calcule l'xp nécessaire pour le prochain niveau.
    """
    return ceil(1.5 * xp_attendu)


def show_image(button, p):
    """
    affiche l'image correspondant au bouton (arme ou item).
    """
    y = button.rect.center[1]

    # récupère l'image selon si c'est une arme ou un item
    if button.action in TYPES_ARMES[p.perso]:
        image = TYPES_ARMES[p.perso][button.action]["image"]
    else:
        image = TYPES_ITEMS[p.perso][button.action]["image"]

    rect = image.get_rect()
    rect.center = (550, y)
    WIN.blit(image, rect)


def show_texte(button, p):
    """
    affiche le texte descriptif de l'objet.
    """
    if button.action in TYPES_ARMES[p.perso]:
        texte = TYPES_ARMES[p.perso][button.action]["texte"]
    else:
        texte = TYPES_ITEMS[p.perso][button.action]["texte"]

    # coupe le texte en plusieurs lignes
    texte = retour_ligne(texte, 50)

    for t in range(len(texte)):
        txt = FONT_TEXTE_ARME.render(texte[t], True, (255, 255, 255))
        rect = txt.get_rect()
        x, y = button.rect.center
        rect.center = (x, y + t * 15)
        WIN.blit(txt, rect)


def scroll_gemme(frame):
    """
    effet de fond avec les gemmes qui défilent verticalement.
    """
    y = frame % HEIGHT

    # double affichage pour effet infini
    if y != 0:
        y2 = y - HEIGHT
        WIN.blit(GEMMES, (0, y2))

    WIN.blit(GEMMES, (0, y))



def _collect_niveau_courant(p, items_dispo, armes_dispo):
    """
    récupère les objets débloqués au niveau actuel.
    """
    nv_key = "Niveau " + str(p.niveau)

    if nv_key in GESTION_NIVEAU_ITEMS.get(p.perso, {}):
        for it in GESTION_NIVEAU_ITEMS[p.perso][nv_key]:
            items_dispo.append(it)

    if nv_key in GESTION_DES_NIVEAUX_ARMES.get(p.perso, {}):
        for a in GESTION_DES_NIVEAUX_ARMES[p.perso][nv_key]:
            armes_dispo.append(a)


def _collect_tout_unlocked(p, items_dispo, armes_dispo):
    """
    récupère tous les objets débloqués jusqu'au niveau actuel.

    utilisé si aucun objet n'est dispo au niveau courant.
    """
    for n in range(1, p.niveau + 1):
        k = "Niveau " + str(n)

        if k in GESTION_NIVEAU_ITEMS.get(p.perso, {}):
            for it in GESTION_NIVEAU_ITEMS[p.perso][k]:
                if it not in items_dispo:
                    items_dispo.append(it)

        if k in GESTION_DES_NIVEAUX_ARMES.get(p.perso, {}):
            for a in GESTION_DES_NIVEAUX_ARMES[p.perso][k]:
                if a not in armes_dispo:
                    armes_dispo.append(a)




def choix_arme(p, armes_et_items_possedees, monstres_presents,
               xp_present, map_name, nb_choix):
    """
    affiche le menu de level up et renvoie le choix du joueur.

    étapes :
    - récupère les objets dispo
    - priorise ceux du niveau actuel
    - complète avec anciens objets si besoin
    - gère le choix clavier/souris
    """
    map_img = IMAGES_MAPS[map_name]
    mapX, mapY = map_img.get_size()

    debut = time.time()
    clock = pyg.time.Clock()

   

    # objets du niveau actuel
    prioritaire_items = []
    prioritaire_armes = []
    _collect_niveau_courant(p, prioritaire_items, prioritaire_armes)

    prioritaire = list(dict.fromkeys(
        x for x in prioritaire_items + prioritaire_armes
        if x not in armes_et_items_possedees
    ))

    # objets cumulés 
    complement_items = []
    complement_armes = []
    _collect_tout_unlocked(p, complement_items, complement_armes)

    complement = list(dict.fromkeys(
        x for x in complement_items + complement_armes
        if x not in armes_et_items_possedees and x not in prioritaire
    ))

    # listes globales 
    items_dispo = list(dict.fromkeys(prioritaire_items + complement_items))
    armes_dispo = list(dict.fromkeys(prioritaire_armes + complement_armes))

    

    # priorité aux objets du niveau
    if len(prioritaire) <= nb_choix:
        choix = list(prioritaire)
    else:
        choix = sample(prioritaire, nb_choix)

    # complète si pas assez
    pool_comp = list(complement)
    while len(choix) < nb_choix and pool_comp:
        pick = choice(pool_comp)
        pool_comp.remove(pick)
        if pick not in choix:
            choix.append(pick)

    # fallback ultime si tout est déjà possédé
    if len(choix) == 0:
        tous = list(dict.fromkeys(items_dispo + armes_dispo))
        while len(choix) < nb_choix and tous:
            pick = choice(tous)
            tous.remove(pick)
            if pick not in choix:
                choix.append(pick)

    nb_choix = len(choix)

    if nb_choix == 0:
        return (None, None), time.time() - debut

    affich = [mot.replace("_", " ").upper() for mot in choix]

    violet = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    violet.fill((102, 62, 86, 150))

    texte = FONT_NIVEAU.render(
        "Niveau " + str(p.niveau) + " atteint !",
        True, (255, 255, 255)
    )

    buttons = [
        Button(affich[i], choix[i], 400, 200 + 100 * i, 400, 80, FONT)
        for i in range(nb_choix)
    ]

    for b in buttons:
        b.color1 = (122, 48, 113)
        b.color2 = (161, 99, 158)
        b.rect_center = (400, b.rect.topleft[1] + 20)

    waiting = True
    selec = 0
    frame = 0
    choix_final = None
    type_objet = "item"

    # boucle du menu 
    while waiting:
        clock.tick(60)

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                exit()

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_UP and selec > 0:
                    selec -= 1
                if event.key == pyg.K_DOWN and selec < nb_choix - 1:
                    selec += 1
                if event.key == pyg.K_RETURN:
                    choix_final = buttons[selec].action
                    type_objet = "arme" if choix_final in armes_dispo else "item"
                    waiting = False

            if event.type == pyg.MOUSEBUTTONDOWN:
                mouse_pos = pyg.mouse.get_pos()
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        choix_final = btn.action
                        type_objet = "arme" if btn.action in armes_dispo else "item"
                        waiting = False

        mouse_pos = pyg.mouse.get_pos()

        WIN.fill((225, 225, 225))

        # affichage map
        for t in range(-mapX, WIDTH + mapX, mapX):
            for j in range(-mapY, HEIGHT + mapY, mapY):
                WIN.blit(map_img, (t, j))

        # affichage fond dynamique
        for m in monstres_presents:
            m.show(1)

        for xp in xp_present:
            xp.show_xp()

        WIN.blit(violet, (0, 0))

        scroll_gemme(frame)
        frame += 1

        # boutons 
        for btn in buttons:
            btn.draw(WIN, mouse_pos)
            show_image(btn, p)
            show_texte(btn, p)

        WIN.blit(texte, texte.get_rect(center=(CENTREx, 100)))

        pyg.display.update()

    return (type_objet, choix_final), time.time() - debut
"""
Passage de niveau
Ce fichier gère :
    la variation d'xp attendu
    le choix d'une arme ou d'un item (en fonction de la chance du joueur)
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

FONT_NIVEAU = pyg.font.SysFont("Press Start 2P", 50)
FONT_TEXTE_ARME = pyg.font.SysFont("Press Start 2P", 17)
GEMMES = pyg.image.load("Images/Autre/gemmes.png")


def passage(xp_attendu):
    """ Actualise l'xp attendu 
    
    Parameters
    ----------
    xp_attendu : int
        L'xp attendu au niveau précédent 
    
    Returns
    -------
    int
        L'xp attendu au niveau d'après
    """
    xp_attendu = ceil(1.5 * xp_attendu) # pour toujours avoir un entier
    return xp_attendu


def show_image(button, p):
    """ Montre l'image de l'arme ou de l'item correspondant
    
    Parameters
    ----------
    button : Self@Button
        Le bouton correspondant à une certaine arme/un certain item
    p : Self@Player
        Le joueur
    """

    y = button.rect.center[1] # ordonnée du centre du bouton pour aligner l'image
    if button.action in TYPES_ARMES[p.perso]:
        image = TYPES_ARMES[p.perso][button.action]["image"]
    else:
        image = TYPES_ITEMS[p.perso][button.action]["image"]
    rect = image.get_rect()
    rect.center = (550, y)
    WIN.blit(image, rect)


def show_texte(button, p):
    """ Affiche le texte explicatif de l'arme ou de l'item
    
    Parameters
    -----------
    button : Self@Button
        Bouton affiché
    p : Self@Player
        Le joueur
    """
    if button.action in TYPES_ARMES[p.perso]:
        texte = TYPES_ARMES[p.perso][button.action]["texte"]
    else:
        texte = TYPES_ITEMS[p.perso][button.action]["texte"]
    texte = retour_ligne(texte, 50) # fonction pour retourner à la ligne (cf minijeu2)
    for t in range(len(texte)):
        txt = FONT_TEXTE_ARME.render(texte[t], True, (255, 255, 255))
        rect = txt.get_rect()
        x, y = button.rect.center
        rect.center = (x, y + t * 15)
        WIN.blit(txt, rect)


def scroll_gemme(frame):
    """ Fait défiler un écran de gemmes très très beau
    
    Parameters
    ----------
    frame : int
        Le numéro de la frame actuelle
    """
    y = frame % HEIGHT # pour rester dans les limites de l'écran
    if y != 0:
        y2 = y - HEIGHT 
        WIN.blit(GEMMES, (0, y2)) # 2e image pour combler le vide
    WIN.blit(GEMMES, (0, y))

def _collect_niveau_courant(p, items_dispo, armes_dispo):
    """Remplit items_dispo/armes_dispo avec les unlocks du niveau ATTEINT."""
    nv_key = "Niveau " + str(p.niveau)
    if nv_key in GESTION_NIVEAU_ITEMS.get(p.perso, {}):
        for it in GESTION_NIVEAU_ITEMS[p.perso][nv_key]:
            items_dispo.append(it)
    if nv_key in GESTION_DES_NIVEAUX_ARMES.get(p.perso, {}):
        for a in GESTION_DES_NIVEAUX_ARMES[p.perso][nv_key]:
            armes_dispo.append(a)
 
 
def _collect_tout_unlocked(p, items_dispo, armes_dispo):
    """Fallback : tous les niveaux <= p.niveau (sans doublons)."""
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
 
def choix_arme(p, armes_et_items_possedees, monstres_presents, xp_present, map_name, nb_choix):
    """Choix d'une arme ou d'un item en fonction du niveau et de la chance du joueur
    
    Parameters
    -----------
    p : Self@Player
        Le joueur
    armes_et_items_possedees : list
        Liste des armes et items possédés
    monstres_presents : list
        Liste des monstres présents
    xp_present : list
        Liste de tous les xp disponibles sur la map
    map_name : str
        Map choisie
    Nb_choix : int
        Nombre de choix possibles (varie en fonction de la chance)
    
    Returns
    -------
    tuple(
        tuple(
            str, 
                Type d'objet
            str), 
                Choix
        float
            Temps écoulé
    )

    """
    map_img = IMAGES_MAPS[map_name]
    mapX, mapY = map_img.get_size()
    debut  = time.time()
    clock  = pyg.time.Clock()
    # Détermination des armes et items disponibles
    armes_dispo = []
    items_dispo = []
    
    _collect_niveau_courant(p, items_dispo, armes_dispo)
    dispo = [x for x in items_dispo + armes_dispo
             if x not in armes_et_items_possedees]
 
    # ÉTAPE 2 (fallback) : si tout ce qui était au niveau courant est possédé,
    # on retombe sur l'ensemble des unlocks cumulés.
    if len(dispo) == 0:
        items_dispo.clear()
        armes_dispo.clear()
        _collect_tout_unlocked(p, items_dispo, armes_dispo)
        dispo = [x for x in items_dispo + armes_dispo
                 if x not in armes_et_items_possedees]
 
    # ÉTAPE 3 (ultime fallback) : tout est déjà possédé → on autorise re-pick.
    if len(dispo) == 0:
        dispo = list(dict.fromkeys(items_dispo + armes_dispo))  # dédoublonné, ordre conservé
 
    # Cas extrême : aucun unlock du tout pour ce perso → on sort proprement.
    if len(dispo) == 0:
        return (None, None), time.time() - debut

    choix = []
    compteur = 0
    while compteur < nb_choix:
        if nb_choix > len(dispo) : # pour éviter une boucle infinie en cas de choix insuffisants
            choix    = list(dispo)
            nb_choix = len(dispo)
            break
        arme = choice(dispo)
        if arme not in choix:
            choix.append(arme)
            compteur += 1
    # Normalisation de l'affichage (avec espaces et en majuscules)
    affich = []
    for mot in choix:
        m = mot.replace("_", " ").upper()
        affich.append(m)

    violet = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
    violet.fill((102, 62, 86, 150))
    texte  = FONT_NIVEAU.render("Niveau " + str(p.niveau) + " atteint !", True, (255, 255, 255))
    buttons = [Button(affich[i], choix[i], 400, 200 + 100 * i, 400, 80, FONT) for i in range(nb_choix)]
    for b in buttons:
        b.color1 = (122, 48, 113)
        b.color2 = (161, 99, 158)
        b.rect_center = (400, b.rect.topleft[1] + 20)

    waiting = True
    selec   = 0 # sélection actuelle (pour le clavier)
    frame   = 0
    choix_final = None
    type_objet  = "item"
    while waiting:
        clock.tick(60)
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                exit()
            if event.type == pyg.KEYDOWN:
                # Permet de sélectionner avec le clavier pour aller plus vite lors des tests
                if event.key == pyg.K_UP and selec > 0:
                    selec -= 1
                if event.key == pyg.K_DOWN and selec < nb_choix - 1:
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
            m.show(1) # pour que les monstres ne changent pas d'anim
        for xp in xp_present:
            xp.show_xp()
        WIN.blit(violet, (0, 0))
        scroll_gemme(frame) # écran magnifique de gemmes en fond
        frame += 1
        for btn in buttons:
            btn.draw(WIN, mouse_pos)
            show_image(btn, p)
            show_texte(btn, p)
        WIN.blit(texte, texte.get_rect(center=(CENTREx, 100)))
        pyg.display.update()

    return (type_objet, choix_final), time.time() - debut
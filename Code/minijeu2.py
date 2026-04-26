"""
QUIZZ SUR LE MAQUILLAGE
ETAPE 1 : FAIRE SPAWN L'OBJET SUR LA MAP fait
ETAPE 2 : GUIDER LE JOUEUR JUSQU'A L'OBJET (idées : par le son, mini map  
        (bcp plus chiant à faire), la flèche la fameuse (mais c'est trop simple))
ETAPE 3 : DIALOGUE AVEC LA DAME DU MAGASIN (scène, demander à Feerose ou Liam)
ETAPE 4 : QUIZZ
"""
import pygame as pyg
from random import randint, shuffle
from math import sqrt
from fonctionnement_boucle import screen_to_world
from Interface import Button
from variables import *

pyg.init()
pyg.mixer.init()

QUIZZ = { 
    0 :
    ("Vrai ou Faux : M.Rossier est le propriétaire officiel de la marque Rare Beauty.",
    ["Faux", "Vrai"]),
    1 :
    ("Il est possible d'aquérir du maquillage à :",
    ["Sephora", "Pétrelle", "Sepharo"]),
    2 :
    ("Quelle est la formule chimique du myricyl palmitate, couramment présent dans les rouges à lèvres ?",
    ["C₃₁H₆₂O₂", "Hein ?", "C₃₂H₆₁O₂"]),
    3 :
    ("Quelle est la peine maximale encourue pour un vol à l'étalage de mascara (sans circonstances aggravantes) ?", 
    ["3 ans de prison et 45 000 euros d'amende", "1 heure de colle", "Repasser le bac blanc de Physique (impossible, les juges ne seraient pas si cruels)"]),
    4 :
    ("Sur une échelle de 0 à 20, quelle note donneriez-vous à ce jeu ?", 
    ["20", "10100", "VINGT"]),
    5 :
    ("Vrai ou Faux : Ce jeu est vraiment incroyable.",
    ["Vrai", "Vrai"])
    }


def spawn_objet(x_debut, x_fin, y_debut, y_fin, p):
    nb_aleat = randint(-5, 5)
    for i in [x_debut, x_fin, y_debut, y_fin] :
        i *= nb_aleat
    coord = (randint(x_debut, x_fin), randint(y_debut, y_fin))
    coord = screen_to_world(coord[0], coord[1], p)
    son = pyg.mixer.Sound("Sons/son_quete2.mp3")
    return coord, son

def regler_volume(coord, p, son):
    dist = sqrt((coord[0] - p.x_monde)**2 + (coord[1] - p.y_monde)**2)
    son.set_volume((100-dist)/100)
    return son

def play_sound(son):
    if not son.get_busy():
        son.play()

def quizz():
    run = True
    i = 0
    clock = pyg.time.Clock()
    win_count = 0
    #text, action, x,y, width, height
    while run and i < 6:
        clock.tick(60)
        WIN.blit(BG, (0, 0))
        mouse_pos = pyg.mouse.get_pos()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
        texte = QUIZZ[i][0]
        texte = FONT.render(texte, True, (0, 0, 0))
        WIN.blit(texte, (200, 100))
        buttons = [Button(QUIZZ[i][1][j], j, 200, 100*j, 400, 80) for j in range(len(QUIZZ[i][1]))]
        shuffle(buttons)
        waiting = True
        while waiting:
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()
                                
            if event.type == pyg.MOUSEBUTTONDOWN:
                mouse_pos = pyg.mouse.get_pos()
                for btn in buttons:
                    mouse_pressed = pyg.mouse.get_pressed()
                    if btn.is_clicked(mouse_pos, mouse_pressed):  
                        if btn.action == 0:
                            win_count += 1
                        elif i == 4 or i == 5:
                            win_count += 1
                        waiting = False  
            WIN.fill((225, 225, 225))
            for i in range(-BGX, WIDTH + BGX, BGX):
                for j in range(-BGY, HEIGHT + BGY, BGY):
                        WIN.blit(BG, (i, j))
            mouse_pos = pyg.mouse.get_pos()
            for btn in buttons:
                btn.draw(WIN, mouse_pos)
            pyg.display.update()

        i += 1
        
quizz()
"""
Minijeu Fille_populaire : QUIZZ SUR LE MAQUILLAGE

"""
import pygame as pyg
from random import randint, shuffle
from math import sqrt
from Affichage.fonctionnement_divers import screen_to_world, camera
from Interface.Class_Button import Button
from Fichiers_variables.variables import *
from Fichiers_variables.traitement_images import decouper_image
from Fichiers_variables.gestion_fichiers import ajouter_arme

import time
pyg.init()
pyg.mixer.init()

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = 600, 650, 300, 350 # c'est faux c'est juste pour test
OBJET = pyg.image.load("Images/Autre/sephora_exterieur.png")
SON = "Sons/son_quete2.mp3"
spritesheet_quizz = pyg.image.load("Images/Autre/anim_quizz.png")
ANIM_QUIZZ = decouper_image(spritesheet_quizz, 5, 5, 3)
ROSE = (255, 182, 229, 200)
BLEU = (154, 158, 200, 200)
ECRITURE = (167, 67, 86)

QUIZZ = { 
    0 :
    ("Vrai ou Faux : M.Rossier est le propriétaire officiel de la marque Rare Beauty.",
    ["Faux", "Vrai"]),
    1 :
    ("Il est possible d'aquérir du maquillage à :",
    ["Sephora", "Pétrelle", "Sepharo"]),
    2 :
    ("Quelle est la formule chimique du myricyl palmitate, couramment présent dans les rouges à lèvres ?",
    ["C31H62O2", "Hein ?", "C32H61O2"]),
    3 :
    ("Quelle est la peine maximale encourue pour un vol à l'étalage de mascara (sans circonstances aggravantes) ?", 
    ["3 ans de prison et 45 000 euros d'amende", "1 heure de colle", 
     "Repasser le bac blanc de Physique (impossible, les juges ne seraient pas si cruels)"]),
    4 :
    ("Sur une échelle de 0 à 20, quelle note donneriez-vous à ce jeu ?", 
    ["20", "0b10100", "VINGT", "0x14"]),
    5 :
    ("Vrai ou Faux : Ce jeu est vraiment incroyable.",
    ["Vrai", "Vrai"])
    }


def spawn_objet(x_debut, x_fin, y_debut, y_fin, p, map):
    """Faire spawn l'objet dans un des magasins
    x_debut, x_fin, y_debut, y_fin : int
        Les coordonnées du magasin
    p : Self@Player
        Le joueur
    """
    nb_aleat1 = randint(-1, 1)
    nb_aleat2 = randint(-1, 1)
    mapX, mapY = map.get_size()
    x_debut += nb_aleat1 * mapX
    y_debut += nb_aleat2 * mapY
    x_fin += nb_aleat1 * mapX
    y_fin += nb_aleat2 * mapY
    coord = (randint(x_debut, x_fin), randint(y_debut, y_fin))
    coord = screen_to_world(coord[0], coord[1], p)
    coord = (300, 200)
    return coord

def draw_objet(coord, image):
    WIN.blit(image, coord)

def collision(coord, image, p):
    rect = image.get_rect()
    rect.topleft = coord
    if p.pos.colliderect(rect):
        return True
    return False

def regler_volume(coord, p, map):
    dist = sqrt((coord[0] - p.x_monde)**2 + (coord[1] - p.y_monde)**2)
    mapX, mapY = map.get_size()
    # distance max d'entente 
    max_dist = 2*mapX

    volume = 1 - (dist / max_dist)
    volume = max(0, min(1, volume))
    pyg.mixer.music.set_volume(volume)
    #son.set_volume(volume)
    
from Interface.option import settings

def play_sound(son):
    if settings["sound"] and not pyg.mixer.music.get_busy():
        pyg.mixer.music.load(son)
        pyg.mixer.music.play()

def replique(texte, color, text_color):
    textes = retour_ligne(texte, 80)
    temps_debut = time.time()
    fond = pyg.Surface((WIDTH-40, 80), pyg.SRCALPHA)
    fond.fill(color)
    while time.time() - temps_debut < 3:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN :
                keys = pyg.key.get_pressed()
                if keys[pyg.K_RETURN]:
                    return
        WIN.blit(fond, (20, HEIGHT-100))
        for t in textes :
            texte = FONT.render(t, True, text_color)
            WIN.blit(texte, (30, HEIGHT-90+20*textes.index(t)))
        pyg.display.update()

def anim_quizz(son):
    replique("Bonjour ! Bienvenue au magasin !", ROSE, ECRITURE)
    play_sound(son)
    replique("Heuu... qui êtes vous ? Je ne vois personne.", BLEU, ECRITURE)
    play_sound(son)
    replique("T'inquièteeeee, je sais pourquoi tu viens.", ROSE, ECRITURE)
    play_sound(son)
    replique("Ah bonn moi-même je ne savais pas pour être honnête.", BLEU, ECRITURE)
    play_sound(son)
    replique("Bon, assez parlé. Venez à bout de ce quizz et vous remporterez un lot incroyable !", ROSE, ECRITURE)
    play_sound(son)
    replique("Ça fait rêver...", BLEU, ECRITURE)
    frame = 0
    i = 0
    while i < 21 :
        play_sound(son)
        frame += 1
        WIN.blit(ANIM_QUIZZ[i], (0,0))
        if frame%6 == 0:
            i += 1
        pyg.display.update()

def anim_fin(victoire, son):
    play_sound(son)
    if victoire :
        play_sound(son)
        replique("Bravo ! Vous avez réussi à avoir la moyenne ! Vous repartez avec ce magnifique highlighter, et ce sans le payer !", ROSE, ECRITURE)
        play_sound(son)
        replique("Je suis émue là... Tout d'abord j'aimerais remercier mes parents qui m'ont toujours soutenue et mes a-", BLEU, ECRITURE)
        play_sound(son)
        replique("Bon chut maintenant on en a marre.", ROSE, ECRITURE)
        play_sound(son)
        replique("Ah... Ok... Merci quand même...", BLEU, ECRITURE)
    else : 
        play_sound(son)
        replique("Malheureusement pour vous, vous avez lamentablement échoué. Vous repartez bredouille de ce magasin.", ROSE, ECRITURE)
        play_sound(son)
        replique("...", BLEU, ECRITURE)
        play_sound(son)
        replique("Le lot était un highlighter de trèèèèèès haute qualité !", ROSE, ECRITURE)
        play_sound(son)
        replique("De toute façon c'est nul les highlighters.", BLEU, ECRITURE)
        play_sound(son)
        replique("Arrêtez d'avoir le seum et fichez le camp de mon magasin s'il vous plait.", ROSE, ECRITURE)        
    frame = 0
    i = 0
    while i < 21 :
        play_sound(son)
        frame += 1
        WIN.blit(ANIM_QUIZZ[i], (0,0))
        if frame%6 == 0:
            i += 1
        pyg.display.update()
              
def quizz(son, map):
    mapX, mapY = map.get_size()
    run = True
    i = 0
    clock = pyg.time.Clock()
    win_count = 0
    while run and i < max(QUIZZ)+1:
        clock.tick(60)
        WIN.fill((225, 225, 225))
        for t in range(-mapX, WIDTH + mapX, mapX):
            for j in range(-mapY, HEIGHT + mapY, mapY):
                    WIN.blit(map, (t, j))
        mouse_pos = pyg.mouse.get_pos()

        rose = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        rose.fill((255, 182, 229, 200))  
        WIN.blit(rose, (0, 0))
        texte = QUIZZ[i][0]
        texte = retour_ligne(texte, 80)
        for t in texte :
            question = FONT.render(t, True, (163, 38, 47))
            WIN.blit(question, (80, 100+20*texte.index(t)))
        ordre = [[QUIZZ[i][1][j], j] for j in range(len(QUIZZ[i][1]))]
        shuffle(ordre)
        buttons = [Button(ordre[j][0], ordre[j][1], 400, 200+100*j, 650, 80, FONT) for j in range(len(QUIZZ[i][1]))]
        for b in buttons :
            b.color1 = (200, 46, 74)
            b.color2 = (232, 73, 105)
        waiting = True
        while waiting:
            play_sound(son)
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    pyg.quit()
                    exit()

                if event.type == pyg.MOUSEBUTTONDOWN:
                    mouse_pos = pyg.mouse.get_pos()

                    for btn in buttons:
                        if btn.rect.collidepoint(mouse_pos):
                            if btn.action == 0:
                                win_count += 1
                            elif i == 4 or i == 5:
                                win_count += 1
                            waiting = False
            mouse_pos = pyg.mouse.get_pos()
            for btn in buttons:
                btn.draw(WIN, mouse_pos)
            pyg.display.update()
        i += 1
    return win_count >= (len(QUIZZ)+2)/2 # moyenne des questions sans les 2 cadeaux
# (oui c'est de la fausse générosité) comme ça vous pouvez ajouter des questions sans tout casser
        
def retour_ligne(texte, longueur):
    nb_carac = len(texte)
    if nb_carac >= longueur:
        i = longueur - 1
        while texte[i] != " " :
            i -= 1
        liste = [texte[0:i], texte[i+1:nb_carac] ]
        nb_carac = len(liste[1])
        if nb_carac >= longueur:
            i = longueur - 1
            while liste[1][i] != " " :
                i -= 1
            liste2 = [liste[1][0:i], liste[1][i+1:nb_carac] ]
            liste.remove(liste[1])
            liste += liste2
    else : 
        liste = [texte]

    return liste


def minijeu2(p, coord_monde, minijeu2_fini, armes_possedees, armes_joueur, map):
    if coord_monde == None:
        coord_screen = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN, p, map)
        coord_monde = screen_to_world(coord_screen[0], coord_screen[1], p)
    coord_screen = camera(coord_monde[0], coord_monde[1], p)
    regler_volume(coord_monde, p, map)
    play_sound(SON)
    draw_objet(coord_screen, OBJET)
    if collision(coord_screen, OBJET, p):
        anim_quizz(SON)
        victoire = quizz(SON, map)
        if victoire :
            armes_possedees.append("Aura_divine")
            armes_joueur = ajouter_arme(p.nom, "Aura_divine", armes_joueur)
        anim_fin(victoire, SON)
        minijeu2_fini = True
        pyg.mixer.music.stop()
    return coord_monde, minijeu2_fini, armes_possedees, armes_joueur

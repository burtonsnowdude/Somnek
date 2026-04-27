"""
Minijeu Fille_populaire : QUIZZ SUR LE MAQUILLAGE

"""
import pygame as pyg
from random import randint, shuffle
from math import sqrt
from fonctionnement_divers import screen_to_world, camera
from Class_Button import Button
from variables import *

pyg.init()
pyg.mixer.init()

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = 300, 350, 100, 200 # c'est faux c'est juste pour test
OBJET = pyg.image.load("Images/Armes_items/berserk.png")
SON = pyg.mixer.Sound("Sons/son_quete2.mp3")

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


def spawn_objet(x_debut, x_fin, y_debut, y_fin, p):
    """Faire spawn l'objet dans un des magasins
    x_debut, x_fin, y_debut, y_fin : int
        Les coordonnées du magasin
    p : Self@Player
        Le joueur
    """
    nb_aleat1 = randint(-2, 2)
    nb_aleat2 = randint(-2, 2)
    x_debut += nb_aleat1 * WIDTH
    y_debut += nb_aleat2 * HEIGHT
    x_fin += nb_aleat1 * WIDTH
    y_fin += nb_aleat2 * HEIGHT
    coord = (randint(x_debut, x_fin), randint(y_debut, y_fin))
    coord = screen_to_world(coord[0], coord[1], p)
    print(coord)
    return coord

def draw_objet(coord, image):
    WIN.blit(image, coord)

def collision(coord, image, p):
    rect = image.get_rect()
    rect.topleft = coord
    if p.pos.colliderect(rect):
        return True
    return False

def regler_volume(coord, p, son):
    dist = sqrt((coord[0] - p.x_monde)**2 + (coord[1] - p.y_monde)**2)

    # distance max d'entente 
    max_dist = 2*WIDTH

    volume = 1 - (dist / max_dist)
    volume = max(0, min(1, volume))

    son.set_volume(volume)
    

def play_sound(son):
    if not pyg.mixer.get_busy():
        son.play()

def quizz():
    run = True
    i = 0
    clock = pyg.time.Clock()
    win_count = 0
    while run and i < max(QUIZZ)+1:
        clock.tick(60)
        WIN.fill((225, 225, 225))
        for t in range(-BGX, WIDTH + BGX, BGX):
            for j in range(-BGY, HEIGHT + BGY, BGY):
                    WIN.blit(BG, (t, j))
        mouse_pos = pyg.mouse.get_pos()

        rose = pyg.Surface((WIDTH, HEIGHT), pyg.SRCALPHA)
        rose.fill((255, 182, 229, 200))  
        WIN.blit(rose, (0, 0))
        texte = QUIZZ[i][0]
        texte = retour_ligne(texte)
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
        
def retour_ligne(texte):
    nb_carac = len(texte)
    if nb_carac >= 80:
        i = 79
        while texte[i] != " " :
            i -= 1
        liste = [texte[0:i], texte[i+1:nb_carac] ]
    else : 
        liste = [texte]

    return liste


def minijeu2(p, coord_monde, minijeu2_fini):
    if coord_monde == None:
        coord_screen = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN, p)
        coord_monde = screen_to_world(coord_screen[0], coord_screen[1], p)
    coord_screen = camera(coord_monde[0], coord_monde[1], p)
    regler_volume(coord_monde, p, SON)
    play_sound(SON)
    draw_objet(coord_screen, OBJET)
    if collision(coord_screen, OBJET, p):
        quizz()
        minijeu2_fini = True
        SON.stop()
    return coord_monde, minijeu2_fini
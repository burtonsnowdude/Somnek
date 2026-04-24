# N'hésitez pas à ajouter des répliques si vous avez de l'inspi
from random import choice, randint
import pygame as pyg
from variables import *
from math import sqrt, cos, sin
from fonctionnement_boucle import camera, screen_to_world
import time

REPLIQUES_BOSS = [
    "Brrrrrr",
    "Tu vas regretter d'être sorti de ton misérable lycée...",
    "Arghhhhhhh",
    "1101 0001 1110... (c'est une menace de fou faut juste comprendre le binaire et l'hexadécimal)",
    "Le magasin est ouvert  !",
    "1010 1010 1010 1010 1010 1010 1010 !!!(ça c'est pas une menace de fou j'avoue)"
]

REPLIQUES_ELEVES = [
    "J'ai survécu à l'algèbre booléen, je peux survivre à ça...",
    "J'ai survécu au bac blanc de physique, je peux survivre à ça...",
    "Svp j'ai même pas encore mon bac...",
    "Je savais que j'aurais dû sécher aujourd'hui...",
    "En vrai ça reste mieux que les cours..."
]

BOSS = {
    1 : {
        "hp" : 100,
        "image" : SPIDER,
        "particularites" : ["dialogue_boss", "move", "dash_boss", "rotation_boss", "hallucination"],
        "vitesse" : 2
    },
    2 : {
        "hp" : 200,
        "image" : SPIDER,
        "particularites" : [],
        "vitesse" : 0
    },
    3 : {
        "hp" : 300,
        "image" : None,
        "particularites" : [],
        "vitesse" : 0
    },
    4 : {
        "hp" : 0,
        "image" : None,
        "particularites" : [],
        "vitesse" : 0
    } # etc là c'est juste des modèles vides
}

# Class Boss 
class Boss :
    def __init__(self, temps, p):
        self.hp = BOSS[temps]["hp"]
        self.image = BOSS[temps]["image"]
        self.vitesse = BOSS[temps]["vitesse"]
        self.particularites = BOSS[temps]["particularites"]
        self.color_boss = (54, 78, 125)
        self.color_joueur = (107, 120, 146)
        self.action_is_over = True
        self.iteration1 = True
        bord = randint(1,4)
        if bord == 1 :
            self.x_screen, self.y_screen = 0, randint(0, HEIGHT)
        elif bord == 2 :
            self.x_screen, self.y_screen = randint(0, WIDTH), 0
        elif bord == 3 :
            self.x_screen, self.y_screen = WIDTH, randint(0, HEIGHT)
        else :
            self.x_screen, self.y_screen = randint(0, WIDTH), HEIGHT
        self.x_monde, self.y_monde = screen_to_world(self.x_screen, self.y_screen, p)
        self.rect = self.image.get_rect()

    def update_coord_monde(self, p):
        self.x_monde, self.y_monde = screen_to_world(self.x_screen, self.y_screen, p)
    
    def update_coord_screen(self, p):
        self.x_screen, self.y_screen = camera(self.x_monde, self.y_monde, p)

    def draw_boss(self):
        """Dessine le boss"""
        WIN.blit(self.image, (self.x_screen, self.y_screen))

    def cinematique_spawn_boss(self):
        """Cinématique d'apparition du boss"""
        pass

    def cinematique_mort_boss(self):
        pass

    def dialogue_perso(self):
        """Faire répondre le personnage parce que c'est encore plus sympathique"""
        if self.iteration1 :
            self.iteration1 = False
            self.temps_debut = time.time()
            self.texte = choice(REPLIQUES_ELEVES)
            self.texte = FONT.render(self.texte, 1, (255, 255, 255))
        if time.time() - self.temps_debut < 5:
            fond = pyg.Rect(20, HEIGHT-20, WIDTH-40, 10)
            pyg.draw.rect(WIN, self.color_joueur, fond)
            WIN.blit(self.texte, (25, HEIGHT-15))
            pyg.display.flip()
        else :
            self.action_is_over = True

    def dialogue_boss(self):
        """Faire parler le boss parce que c'est sympathique"""
        if self.iteration1 :
            self.iteration1 = False
            self.temps_debut = time.time()
            self.texte = choice(REPLIQUES_BOSS)
            self.texte = FONT.render(self.texte, 1, (255, 255, 255))
        if time.time() - self.temps_debut < 5:
            fond = pyg.Rect(20, HEIGHT-20, WIDTH-40, 10)
            pyg.draw.rect(WIN, self.color_boss, fond)
            WIN.blit(self.texte, (25, HEIGHT-15))
            pyg.display.flip()
        else :
            self.action_is_over = True

    def rotation_boss(self, p):
        """Faire tourner le boss autour du joueur"""
        if self.iteration1 :
            self.iteration1 = False
            self.coord_a_atteindre = (self.x_screen, self.y_screen)
            self.dist = sqrt((self.x_screen-CENTREx)**2 + (self.y_screen-CENTREy)**2)
            self.angle = 0
        elif (self.x_screen, self.y_screen) == self.coord_a_atteindre :
            self.action_is_over = True
        else :
            angle += 0.02
            self.x_screen = CENTREx + self.dist * cos(self.angle)
            self.y_screen = CENTREy + self.dist * sin(self.angle)
        self.update_coord_monde(p)
        
    def follow(self, x, y):
        dx = x - self.x_monde
        dy = y - self.y_monde
        distance = sqrt(dx**2 + dy**2)
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move 
            self.x_monde += (dx / distance) * self.vitesse
            self.y_monde += (dy / distance) * self.vitesse

    def move(self, p):
        """Déplace le boss vers un point aléatoire et revient à sa coord screen initiale"""

        if self.iteration1:
            self.x_base_screen, self.y_base_screen = self.x_screen, self.y_screen
            self.x_base_monde, self.y_base_monde = self.x_monde, self.y_monde
            self.x_aleat_screen, self.y_aleat_screen = (randint(0, WIDTH), randint(0, HEIGHT))
            self.x_aleat_monde, self.y_aleat_monde = screen_to_world(self.x_aleat_screen, self.y_aleat_screen, p)
            self.but = "aleat"

        if self.but == "aleat":
            self.follow(self.x_aleat_monde, self.y_aleat_monde)

        if (self.x_monde, self.y_monde) == (self.x_aleat_monde, self.y_aleat_monde):
            self.but = "base"

        if self.but == "base":
            self.follow(self.x_base_monde, self.y_base_monde)

        if (self.x_screen, self.y_screen) == (self.x_base_screen, self.y_base_screen):
            self.action_is_over = True
            
        self.update_coord_screen(p)

    def dash_boss(self, p):
        self.vitesse += 10
        self.move(p)
        self.vitesse -= 10

    def attaque_dist(self):
        pass


def spawn_boss(temps, boss_present, boss_acheves, p):
    temps /= 60
    temps = int(temps)
    boss = False
    if not boss_present and temps in BOSS and not temps in boss_acheves : 
        boss_present = True
        boss = Boss(temps, p)
    return boss_present, boss


def gestion_boss(boss, boss_present, temps_ecoule):
    """Choisit une action du boss et l'exécute jusqu'à sa fin"""
    if boss_present:
        particularites = boss.particularites # liste d'actions que le boss peut faire

        if boss.action_is_over :
            boss.action = choice(particularites)
            boss.iteration1 = True
            boss.action_is_over = False
        action = boss.action
        if action == "attaque_a_distance":
            boss.attaque_a_distance()

        if action == "hallucination":
            effet = effet_hallucination(WIN, temps_ecoule)
            WIN.blit(effet, (0,0))
            overlay = pyg.Surface((WIDTH, HEIGHT))
            overlay.fill((255, 0, 150))  
            overlay.set_alpha(40)
            WIN.blit(overlay, (0, 0))

        if action == "dialogue_boss":
            boss.dialogue_boss()
            boss.dialogue_perso()

        if action == "move":
            boss.move()

        if action == "dash_boss":
            boss.dash_boss()

        if action == "rotation_boss":
            boss.rotation_boss()

        boss.draw_boss()

        if boss.hp <= 0:
            boss_present = False

    return boss_present

def effet_hallucination(surface, t):
    new_surface = pyg.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):
        offset = int(10 * sin(y * 0.05 + t))
        new_surface.blit(surface, (offset, y), (0, y, WIDTH, 1))

    return new_surface
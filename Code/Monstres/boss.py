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
BOSS = {}
temps = [15, 25, 30, 38, 50, 62, 82]
for t in temps :
    BOSS[t] = {"hp" : t*10,
               "vitesse" : temps.index(t),
               "puissance" : 10* temps.index(t)}
BOSS[15]["particularites"] = ["dialogue_boss", "dash_boss", "hallucination"]
BOSS[25]["particularites"] = ["dialogue_perso", "move", "rotation_boss"]
BOSS[30]["particularites"] = ["dash_boss", "move", "hallucination"]
BOSS[38]["particularites"] = ["dialogue_boss", "attaque_a_distance", "rotation_boss"]
BOSS[50]["particularites"] = ["dialogue_perso", "attaque_a_distance", "dash_boss"]
BOSS[62]["particularites"] = ["move", "dash_boss", "attaque_a_distance"]
BOSS[82]["particularites"] = ["move", "dash_boss", "attaque_a_distance", "hallucination"]

BOSS_PAR_PERSO = {
    "Nerd" : {15 : { ** BOSS[15],
              "image" : None},
            25 : {** BOSS[25],
              "image" : None},
            30 : {** BOSS[30],
              "image" : None},
            38 : {** BOSS[38],
              "image" : None},
            50 : {** BOSS[50],
              "image" : None},
            62 : {** BOSS[62],
              "image" : None},
            82 : {** BOSS[82],
              "image" : None}
    },
    "Fille_populaire": {15 : { ** BOSS[15],
              "image" : None},
            25 : {** BOSS[25],
              "image" : None},
            30 : {** BOSS[30],
              "image" : None},
            38 : {** BOSS[38],
              "image" : None},
            50 : {** BOSS[50],
              "image" : None},
            62 : {** BOSS[62],
              "image" : None},
            82 : {** BOSS[82],
              "image" : None}
    },
    "Nonne" : {15 : { ** BOSS[15],
              "image" : None},
            25 : {** BOSS[25],
              "image" : None},
            30 : {** BOSS[30],
              "image" : None},
            38 : {** BOSS[38],
              "image" : None},
            50 : {** BOSS[50],
              "image" : None},
            62 : {** BOSS[62],
              "image" : None},
            82 : {** BOSS[82],
              "image" : None}
    }
}
# Class Boss 
class Boss :
    def __init__(self, temps, p, perso):
        self.hp = BOSS_PAR_PERSO[perso][temps]["hp"]
        self.temps = temps
        if "image" in BOSS_PAR_PERSO[perso][temps]:
            self.image = BOSS_PAR_PERSO[perso][temps]["image"]
            self.rect = self.image.get_rect()
        elif "anim" in BOSS_PAR_PERSO[perso][temps]:
            self.anim = BOSS_PAR_PERSO[temps]["anim"]
            self.index = 0
            self.rect = self.anim[0].get_rect()
        self.vitesse = BOSS_PAR_PERSO[perso][temps]["vitesse"]
        self.particularites = BOSS_PAR_PERSO[perso][temps]["particularites"]
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

    def draw_boss(self, frame):
        """Dessine le boss"""
        if "image" in BOSS_PAR_PERSO[self.temps]:
            WIN.blit(self.image, (self.x_screen, self.y_screen))
        elif frame%4 == 0 :
            WIN.blit(self.anim[self.index], (self.x_screen, self.y_screen))
            self.index += 1
            self.index = self.index%len(self.anim)

    def cinematique_spawn_boss(self):
        """Cinématique d'apparition du boss"""
        pass

    def cinematique_mort_boss(self):
        pass
    
    def degats(self, degats):
        """Inflige des dégâts au monstre

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats

    def dialogue_perso(self):
        """Faire répondre le personnage parce que c'est encore plus sympathique"""
        if self.iteration1 :
            self.iteration1 = False
            self.temps_debut = time.time()
            self.texte = choice(REPLIQUES_ELEVES)
            self.texte = FONT.render(self.texte, 1, (255, 255, 255))
        if time.time() - self.temps_debut < 5:
            fond = pyg.Surface(HEIGHT-40, WIDTH-40, 30)
            fond.set_alpha(150)
            fond.fill(self.color_boss)
            WIN.blit(fond, (20, HEIGHT-40))
            WIN.blit(self.texte, (25, HEIGHT-30))
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
            fond = pyg.Surface(HEIGHT-40, WIDTH-40, 30)
            fond.set_alpha(150)
            fond.fill(self.color_boss)
            WIN.blit(fond, (20, HEIGHT-40))
            WIN.blit(self.texte, (25, HEIGHT-30))
        else :
            self.action_is_over = True

    def rotation_boss(self, p):
        """Faire tourner le boss autour du joueur"""
        if self.iteration1 :
            self.iteration1 = False
            self.coord_a_atteindre = (self.x_screen, self.y_screen)
            self.dist = sqrt((self.x_screen-CENTREx)**2 + (self.y_screen-CENTREy)**2)
            self.angle = 0
            self.debut = time.time()
        if time.time() - self.debut > 10:
            self.action_is_over = True
        else :
            self.angle += 0.02
            self.x_screen = CENTREx + self.dist * cos(self.angle)
            self.y_screen = CENTREy + self.dist * sin(self.angle)
        self.x_monde, self.y_monde = screen_to_world(self.x_screen, self.y_screen, p)
        
    def follow(self, x, y):
        dx = x - self.x_monde
        dy = y - self.y_monde
        distance = sqrt(dx**2 + dy**2)
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move 
            self.x_monde += (dx / distance) * self.vitesse
            self.y_monde += (dy / distance) * self.vitesse
    
    def hallucination(self, surface):
        if self.iteration1 :
            self.debut = time.time()
            self.iteration1 = False
        temps_ecoule = time.time() - self.debut
        new_surface = pyg.Surface((WIDTH, HEIGHT))

        for y in range(HEIGHT):
            offset = int(10 * sin(y * 0.05 + temps_ecoule))
            new_surface.blit(surface, (offset, y), (0, y, WIDTH, 1))
        if temps_ecoule > 10 :
            self.action_is_over = True
        return new_surface

    def move(self, p):
        """Déplace le boss vers un point aléatoire"""

        if self.iteration1:
            self.x_aleat_screen, self.y_aleat_screen = (randint(0, WIDTH), randint(0, HEIGHT))
            self.x_aleat_monde, self.y_aleat_monde = screen_to_world(self.x_aleat_screen, self.y_aleat_screen, p)
            self.iteration1 = False
            self.debut = time.time()

        self.follow(self.x_aleat_monde, self.y_aleat_monde)
        t = time.time() -self.debut
        if (self.x_monde, self.y_monde) == (self.x_aleat_monde, self.y_aleat_monde) or t > 5:
            self.action_is_over = True

    def dash_boss(self, p):
        self.vitesse += 10
        self.move(p)
        self.vitesse -= 10

    def follow_player(self, p):
        self.follow(p.x_monde, p.y_monde)
        
    def attaque_dist(self):
        pass


def spawn_boss(temps, boss_present, boss_acheves, p, boss, perso):
    temps /= 60
    temps = int(temps)
    if not boss_present and temps in BOSS and not temps in boss_acheves : 
        boss_present = True
        boss = Boss(temps, p, perso)
    return boss_present, boss


def gestion_boss(boss, boss_present, p, frame):
    """Choisit une action du boss et l'exécute jusqu'à sa fin"""
    if boss_present:
        particularites = boss.particularites # liste d'actions que le boss peut faire

        if boss.action_is_over :
            boss.action = choice(particularites)
            boss.iteration1 = True
            boss.action_is_over = False
            print(boss.action)
        action = boss.action

        if action == "attaque_a_distance":
            boss.attaque_a_distance()

        if action == "hallucination":
            effet = boss.hallucination(WIN)
            WIN.blit(effet, (0,0))
            overlay = pyg.Surface((WIDTH, HEIGHT))
            overlay.fill((255, 0, 150))  
            overlay.set_alpha(40)
            WIN.blit(overlay, (0, 0))
            boss.follow_player(p)

        if action == "dialogue_boss":
            boss.dialogue_boss()
            boss.follow_player(p)

        if action == "dialogue_perso":
            boss.dialogue_perso()
            boss.follow_player(p)
            
        if action == "move":
            boss.move(p)

        if action == "dash_boss":
            boss.dash_boss(p)

        if action == "rotation_boss":
            boss.rotation_boss(p)

        if p.pos.colliderect(boss.rect) and frame%10 == 0:
            p.degats(boss.puissance)
        boss.draw_boss()

        if boss.hp <= 0:
            boss_present = False
            boss = None

    return boss_present

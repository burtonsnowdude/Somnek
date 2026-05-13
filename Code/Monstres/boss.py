# N'hésitez pas à ajouter des répliques si vous avez de l'inspi
from random import choice, randint
import pygame as pyg
from Fichiers_variables.variables import *
from math import sqrt, cos, sin
from Affichage.fonctionnement_divers import screen_to_world
import time
from Minijeux.minijeu2 import replique, retour_ligne

REPLIQUES_BOSS = [
    "Brrrrrr",
    "Tu vas regretter d'être sorti de ton misérable lycée...",
    "Arghhhhhhh",
    "1101 0001 1110... (c'est une menace de fou faut juste comprendre le binaire et l'hexadécimal)",
    "Le magasin est ouvert  !",
    "1010 1010 1010 1010 1010 1010 1010 !!! (ça c'est pas une menace de fou j'avoue)"
]

REPLIQUES_ELEVES = [
    "J'ai survécu à l'algèbre booléen, je peux survivre à ça...",
    "J'ai survécu au bac blanc de physique, je peux survivre à ça...",
    "Svp j'ai même pas encore mon bac...",
    "Je savais que j'aurais dû sécher aujourd'hui...",
    "En vrai ça reste mieux que les cours..."
]
BOSS = {}
maps = ["Ruelle", "Foire"] # maps des boss
for t in maps:
    BOSS[t] = {"hp": (maps.index(t) + 1) * 1000,
               "vitesse": maps.index(t) + 1,
               "puissance": 10 * maps.index(t)}

BOSS["Ruelle"]["particularites"] = ["dialogue_boss", "rotation_boss", "move"]
BOSS["Foire"]["particularites"] = ["dialogue_perso", "dash_boss", "hallucination"]

# Dico des BOSS
BOSS_PAR_PERSO = {
    "Nerd" : {
            "Ruelle" : {** BOSS["Ruelle"],
              "anim" : ANIM_HARCELEUR},
            "Foire" : {** BOSS["Foire"],
              "image" : DARK_VADARO}
    },
    "Fille_populaire": {
            "Ruelle" : {** BOSS["Ruelle"],
              "anim" : ANIM_EX_AMIES},
            "Foire" : {** BOSS["Foire"],
              "image" : PALETTE}
    },
    "Nonne" : {
            "Ruelle" : {** BOSS["Ruelle"],
              "anim" : ANIM_NONNE},
            "Foire" : {** BOSS["Foire"],
              "anim" : ANIM_HOMME_MI_DEMON}
    }
}
# Class Boss 
class Boss :
    def __init__(self, maps, p, perso):
        self.hp = BOSS_PAR_PERSO[perso][maps]["hp"]
        self.maps = maps
        self.perso = perso
        self.puissance = BOSS_PAR_PERSO[perso][maps]["puissance"]
        if "image" in BOSS_PAR_PERSO[perso][maps]:
            self.image = BOSS_PAR_PERSO[perso][maps]["image"]
            self.rect = self.image.get_rect()
        elif "anim" in BOSS_PAR_PERSO[perso][maps]:
            self.anim = BOSS_PAR_PERSO[perso][maps]["anim"]
            self.index = 0
            self.rect = self.anim[0].get_rect()
        self.vitesse = BOSS_PAR_PERSO[perso][maps]["vitesse"]
        self.particularites = BOSS_PAR_PERSO[perso][maps]["particularites"]
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

    def draw_boss(self, frame):
        """Dessine le boss
        
        Parameters
        ----------
        frame : int
            Numéro de la frame actuelle
        """
        self.rect.center = (self.x_screen, self.y_screen)
        if "image" in BOSS_PAR_PERSO[self.perso][self.maps]:
            WIN.blit(self.image, self.rect)
        elif frame%4 == 0 :
            WIN.blit(self.anim[self.index], self.rect)
            self.index += 1
            self.index = self.index%len(self.anim)
        else :
            WIN.blit(self.anim[self.index], self.rect)

    def degats(self, degats):
        """Inflige des dégâts au boss

        Parameters
        ----------
        degats : int
        """
        self.hp -= degats

    def dialogue_perso(self, p):
        """Faire répondre le personnage parce que c'est encore plus sympathique
        
        Parameters
        -----------
        p : Self@Player
            Le joueur
        """
        if self.iteration1:
            self.iteration1 = False
            self.temps_debut = time.time()
            texte_brut = choice(REPLIQUES_ELEVES)
            self.textes = retour_ligne(texte_brut, 80)
        if time.time() - self.temps_debut < 5:
            fond = pyg.Surface((WIDTH-40, 80), pyg.SRCALPHA)
            fond.fill(p.color)
            WIN.blit(fond, (20, HEIGHT-100))
            for idx, t in enumerate(self.textes):
                texte = FONT.render(t, True, (0, 0, 0))
                WIN.blit(texte, (30, HEIGHT - 90 + 20 * idx))
        else:
            self.action_is_over = True

    def dialogue_boss(self):
        """Faire parler le boss parce que c'est sympathique

        Parameters
        -----------
        p : Self@Player
            Le joueur
        """
        if self.iteration1:
            self.iteration1 = False
            self.temps_debut = time.time()
            # on garde la string brute et on la coupe une seule fois
            texte_brut = choice(REPLIQUES_BOSS)
            self.textes = retour_ligne(texte_brut, 80)
        if time.time() - self.temps_debut < 5:
            fond = pyg.Surface((WIDTH-40, 80), pyg.SRCALPHA)
            fond.fill((92, 101, 184, 200))
            WIN.blit(fond, (20, HEIGHT-100))
            for idx, t in enumerate(self.textes):
                texte = FONT.render(t, True, (0, 0, 0))
                WIN.blit(texte, (30, HEIGHT - 90 + 20 * idx))
        else:
            self.action_is_over = True

    def rotation_boss(self, p):
        """Faire tourner le boss autour du joueur

        Parameters
        -----------
        p : Self@Player
            Le joueur
        """
        if self.iteration1 :
            self.iteration1 = False
            self.coord_a_atteindre = (self.x_screen, self.y_screen)
            self.dist = sqrt((self.x_screen-CENTREx)**2 + (self.y_screen-CENTREy)**2)
            self.angle = 0 # initialisation de l'angle pour le déplacement
            self.debut = time.time()
        if time.time() - self.debut > 5:
            self.action_is_over = True
        else :
            self.angle += 0.02
            # Trigo pour calculer les nouvelles coord
            self.x_screen = CENTREx + self.dist * cos(self.angle)
            self.y_screen = CENTREy + self.dist * sin(self.angle)
        # Actualisation des coord monde
        self.x_monde, self.y_monde = screen_to_world(self.x_screen, self.y_screen, p)
        
    def follow(self, x, y):
        """ Suivre un point de coordonnées x et y
        
        Parameters
        ----------
        x, y : int
            Coordonnées monde du point
        """
        dx = x - self.x_monde
        dy = y - self.y_monde
        distance = sqrt(dx**2 + dy**2)
        # Only move if distance > 0 to avoid division by zero
        if distance > 0:
            # Normalize and move 
            self.x_monde += (dx / distance) * self.vitesse
            self.y_monde += (dy / distance) * self.vitesse

    def hallucination(self, surface):
        """ Déforme la vision du joueur
        
        Parameters
        ----------
        surface : Surface
            Fond

        Returns
        -------
        Surface
            surface déformée
        """
        if self.iteration1 :
            self.debut = time.time()
            self.iteration1 = False
        temps_ecoule = time.time() - self.debut
        new_surface = pyg.Surface((WIDTH, HEIGHT))

        for y in range(HEIGHT):
            # modifie les coordonnées de chaque pixel avec un offset qui évolue avec le temps
            offset = int(10 * sin(y * 0.05 + temps_ecoule))
            new_surface.blit(surface, (offset, y), (0, y, WIDTH, 1))
        if temps_ecoule > 10 :
            self.action_is_over = True
        return new_surface

    def move(self, p):
        """Déplace le boss vers un point aléatoire

        Parameters
        -----------
        p : Self@Player
            Le joueur
        """

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
        """Déplace rapidement le boss vers un point aléatoire

        Parameters
        -----------
        p : Self@Player
            Le joueur
        """
        self.vitesse += 10
        self.move(p)
        self.vitesse -= 10

    def follow_player(self, p):
        """Déplace le boss vers le joueur

        Parameters
        -----------
        p : Self@Player
            Le joueur
        """
        self.follow(p.x_monde, p.y_monde)


def spawn_boss(map, boss_present, boss_acheves, p, boss, perso):
    """Fait apparaitre un boss
    
    Parameters
    ----------
    map : str
        Map choisie
    boss_present : bool
    boss_acheves : list
        liste des boss déjà vaincus
    p : Self@Player
        Le joueur
    boss : Self@Boss ou None
    perso : str
        Le perso sélectionné
    
    Returns
    -------
    bool 
        boss présent ou non
    boss 
        l'objet Self@Boss ou None
    """
    if not boss_present and map in BOSS and not map in boss_acheves : 
        boss_present = True
        boss = Boss(map, p, perso)
    return boss_present, boss


def gestion_boss(boss, boss_present, p, frame, boss_acheves):
    """Choisit une action du boss et l'exécute jusqu'à sa fin
    
    Parameters
    ----------
    boss : Self@Boss ou None
    boss_present : bool
    p : Self@Player
        Le joueur
    frame : int
        Numéro de la frame actuelle
    boss_acheves : list 
        Liste des boss tués
    
    Returns
    -------
    bool
        boss présent
    list
        boss achevés
    """
    if boss_present:
        particularites = boss.particularites # liste d'actions que le boss peut faire

        if boss.action_is_over : # si l'action est terminée
            boss.action = choice(particularites) # choix d'une nouvelle action
            boss.iteration1 = True # réinitialisation des attributs
            boss.action_is_over = False
        action = boss.action

        if action == "hallucination":
            effet = boss.hallucination(WIN)
            WIN.blit(effet, (0,0))
            overlay = pyg.Surface((WIDTH, HEIGHT))
            overlay.fill((255, 0, 150))  
            overlay.set_alpha(100)
            WIN.blit(overlay, (0, 0))
            boss.follow_player(p)

        if action == "dialogue_boss":
            boss.dialogue_boss()
            boss.follow_player(p)

        if action == "dialogue_perso":
            boss.dialogue_perso(p)
            boss.follow_player(p)
            
        if action == "move":
            boss.move(p)

        if action == "dash_boss":
            boss.dash_boss(p)

        if action == "rotation_boss":
            boss.rotation_boss(p)

        if p.pos.colliderect(boss.rect) and frame%10 == 0:
            p.degats(boss.puissance)
        boss.draw_boss(frame)

        if boss.hp <= 0: # mort du boss
            boss_present = False
            boss_acheves.append(boss.maps)
            boss = None

    return boss_present, boss_acheves

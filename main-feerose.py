"Daphné j'ai créé mon propre fichier pour ne pas supprimer le tien mais j'ai conservé tes élements"
import pygame as pyg 
import time
from variables import *
from monstre_player import *
from random import *
from coffres import *
import tkinter as tk
import math
import random
import pygame

def main():
    clock = pyg.time.Clock() # crée une horloge pour gérer le temps

    run = True
    
    # Toutes les variables initiales sont en bazar je pense qu'il faudra les organiser
    monstres_presents = [] # liste qui contiendra les monstres existant
    bg = BG.get_rect() 
    p = Player()
    start_time = time.time()  
    frame = 0
    frequence = 50 # fréquence à laquelle un monstre apparait
    xp_attendu = 40 # xp attendu pour passer un niveau (croît exponentiellement)
    xp = 0.5
    seuil = 0
    options = []
    armes_possedees = []

    pause_time = 0 # temps d'inactivité 
    dernier_coffre_apparu = 0 # nombre de frames depuis le dernier coffre apparu
    coffre_existant = False
    nouveau_coffre = None
    argent = 0

    while run:
        clock.tick(60) # fixe le nombre de frames par seconde
        temps_ecoulé = time.time() - start_time - pause_time

        for event in pyg.event.get():  
            if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                run = False 
                break

        # Fond d'écran 
        WIN.fill((225, 225, 225)) 
        WIN.blit(BG, bg) 
        
        frame += 1

       
        # Gestion des coffres
        if randint(1,100) == 1 and dernier_coffre_apparu > 100 and not coffre_existant:
            nouveau_coffre = Coffre(p)
            dernier_coffre_apparu = 0 
            coffre_existant = True

        if coffre_existant:
            nouveau_coffre.pointer_coffre(p)
            if nouveau_coffre.coffre_sur_lecran:
                if p.pos.colliderect(nouveau_coffre.rect):
                    gain = nouveau_coffre.determiner_recompense(armes_possedees, seuil)
                    if type(gain) == int :
                        argent += gain
                        print(argent)
                    else :
                        armes_possedees.append(gain)
                        print(armes_possedees)
                    coffre_existant = False
        dernier_coffre_apparu += 1
        
        # Gestion des ennemis
        if frame%frequence == 0 :
            monstres_presents.append(Monstre(choice(TYPES))) # crée un nouveau monstre de type aléatoire
        for m in monstres_presents[:]:
            existe = m.show() # affiche tous les monstres existant
            if existe :
                m.follow(p) # monstres suivant le joueur
                if p.pos.colliderect(m.pos) and frame%10 == 0:
                    p.degats(m.puissance) # dégâts en cas de collision
            else :
                monstres_presents.remove(m)

        p.draw_player() 

        if p.update_xp(xp, xp_attendu) :
            xp_attendu *= 1.5
            if seuil+4 <= len(ARMES) :
                seuil += 4
            if xp_attendu%2 != 0 :
                xp_attendu += 1 # pour toujours avoir un nombre pair (évite un trop grand nombre de décimales)
            # passage de niveau (j'attends la class armes encore une fois c'est des listes arbitraires)
            if p.niveau < seuil :
                armes_dispo = [arme for arme in ARMES if ARMES[arme] < seuil]
                for arme in armes_dispo[:]:
                    if arme in armes_possedees :
                        armes_dispo.remove(arme)
                choix = []
                compteur = 0
                while compteur < 3:
                    arme = choice(armes_dispo)
                    if arme not in choix :
                        choix.append(arme) 
                        compteur += 1
                options = [pyg.Rect(370, 200+40*i, 100, 30) for i in range(3)]
                for option in options :
                    pyg.draw.rect(WIN, (255, 255, 255), option)
                selec = 0       
                for i in range(len(choix)) :
                    texte = FONT.render(choix[i], 1, (0, 0, 0)) 
                    WIN.blit(texte, (390, 205+i*40))
                pyg.display.update()
                debut = time.time()
                entree = False
                while not entree:
                    pause_time = time.time() - debut
                    for event in pyg.event.get():
                        if event.type == pyg.QUIT:
                            pyg.quit()
                            exit()

                        if event.type == pyg.KEYDOWN:
                            if event.key == pyg.K_UP and selec != 0:
                                pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                                texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                                WIN.blit(texte, (390, 205+selec*40))
                                selec -= 1

                            if event.key == pyg.K_DOWN and selec != 2:
                                pyg.draw.rect(WIN, (255, 255, 255), options[selec])
                                texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                                WIN.blit(texte, (390, 205+selec*40))
                                selec += 1

                            if event.key == pyg.K_RETURN:
                                entree = True

                    pyg.draw.rect(WIN, (120, 120, 250), options[selec])
    
                    texte = FONT.render(choix[selec], 1, (0, 0, 0)) 
                    WIN.blit(texte, (390, 205+selec*40))
                    pyg.display.update()

                armes_possedees.append(choix[selec])
                print(armes_possedees)
                options = []

        p.move_bg(bg, monstres_presents)

        # Timer et barre de vie
        if temps_ecoulé < 60: 
             time_text = FONT.render(f"{int(temps_ecoulé)}s", 1, (255, 255, 255)) 
        else:
            min = temps_ecoulé // 60 
            sec = temps_ecoulé % 60 
            time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) 
        WIN.blit(time_text, (370, 10)) 
        barre_PV_blanc = pyg.Rect(500, 10, 250, 20)
        barre_PV = pyg.Rect(500, 10, p.hp*5, 20)
        pyg.draw.rect(WIN, (255, 255, 255), barre_PV_blanc)
        pyg.draw.rect(WIN, (0, 255, 10), barre_PV)

        # Barre d'xp
        unit = 250/xp_attendu
        barre_xp_blanc = pyg.Rect(10, 10, 250, 20)
        barre_xp = pyg.Rect(10, 10, p.xp*unit, 20)
        pyg.draw.rect(WIN, (255, 255, 255), barre_xp_blanc)
        pyg.draw.rect(WIN, (0, 0, 255), barre_xp)
        pyg.display.update()


class Arme:
    """Class arme"""
    Carac_base = {
        "type_arme": None,
        "dgbase": 0,
        "prix": 0,
        "portee": 0,
        "reduction": 0,
        "niveau_req": 0,
        "niveau": 0
    }
    ARMES= {
        "Epee_bleu": {
            Carac_base,
            "dgbase": 4,
            "prix": 0,
            "niveau_req": 0,
            "niveau": 1
        },
        "Clé_usb": {
            Carac_base,
            "dgbase": 23,
            "prix": 9,
            "niveau_req": 4,
            "niveau": 1
        },
        "Epee_enflammee": {
            Carac_base,
            "dgbase": 10,
            "prix": 2,
            "niveau_req": 4,
            "niveau": 1
        }
    }
    def __init__(self, nom_arme):
        """Initialiser"""
        if nom_arme not in self.ARMES:
            raise ValueError(f"Arme '{nom_arme}' non trouvée")
        
        self.nom = nom_arme
        self.caracteristiques = self.ARMES[nom_arme].copy()
    
    def ameliorer_arme(self, nv_degat):
        """Améliorer les statistiques de l'arme"""
        niveau_req = self.caracteristiques["niveau_req"]
        niveau_actuel = self.caracteristiques["niveau"]
        
        if niveau_actuel >= niveau_req:
            self.caracteristiques["dgbase"] += nv_degat
            self.caracteristiques["niveau"] += 1
            return True
        return False
    
    def est_a_portee(self, distance_monstre):
        """Vérifie que le monstre est à la portée"""
        return distance_monstre <= self.caracteristiques["portee"]
    
    def calculer_degat(self):
        """Calcule les degats"""
        degat = self.caracteristiques["dgbase"]
        reduction = self.caracteristiques["reduction"]
        
        if reduction > 0:
            return degat - reduction
        return degat
    
    def get_prix(self):
        """Avoir le prix de l'arme"""
        return self.caracteristiques["prix"]


class Items:
    """Class items"""
    
    Carac_base__item= {
        "type_item": None,
        "hp": 0,
        "hp_max": 0,
        "prix": 0,
        "niveau_requis": 0,
        "degat": 0,
        "durabilite": None,
        "refroidissement": None,
        "recuperation": None,
        "vitesse_du_j": None,
        "chance": None,
        "cupidite": None,
        "attirance": None,
        "malchance": None,
        "zone": None,
        "resurrection": None,
        "dernier_tir": 0,
        "portee_xp": None,
        "refroidir": None,
        "quantite": 5,
        "sante": None,
        "protection": 0
    }
    
    Items = {
        "Parfum_Dioru": {
            Carac_base__item,
            "refroidir": 30,
            "prix": 5
        },
        "Gloss_rose": {
            Carac_base__item,
            "attirance": 15,
            "prix": 3
        },
        "Chew_gum": {
            Carac_base__item,
            "sante": 0.2,
            "prix": 2
        },
        "Talons_noirs": {
            Carac_base__item,
            "vitesse_du_j": 0.2,
            "prix": 7
        },
        "Crop_top_rose": {
            Carac_base__item,
            "protection": 0.2,
            "prix": 6
        }
    }
    
    def __init__(self, nom_item):
        """Initialisez les items"""
        if nom_item not in self.Items:
            raise ValueError(f"Item '{nom_item}' non trouvé")
        
        self.nom = nom_item
        self.caracteristiques = self.Items[nom_item].copy()
    
    
    def acheter_item(solde_j, prix):
        """Acheter un item"""
        if solde_j >= prix:
            solde_j -= prix
            return solde_j
        return solde_j
    
    def refroidissement(self):
        """Reduit le temps entre les attaques"""
        refroidissement_base = 100
        refroidir = self.caracteristiques.get("refroidir")
        
        if refroidir is None:
            return refroidissement_base
        
        nv_reduction = refroidissement_base - refroidir
        return max(nv_reduction, 0)  
    
    def vitesse(self):
        """Augmenter la vitesse du joeuuur"""
        vitesse_base = 20
        vitesse_j = self.caracteristiques.get("vitesse_du_j")
        
        if vitesse_j is None:
            return vitesse_base
        
        nv_vitesse = vitesse_base * (1 + vitesse_j)
        return nv_vitesse
    
    def chance(self):
        """Increase player chance"""
        chance_base = 10
        chance_val = self.caracteristiques.get("chance")
        
        if chance_val is None:
            return chance_base
        
        nv_chance = chance_base * (1 + chance_val)
        return nv_chance
    
    def cupidite(self, somme):
        """Augmenter l'argent récolté"""
        cupidite_val = self.caracteristiques.get("cupidite")
        
        if cupidite_val is None:
            return somme
        
        argent_final = somme * (1 + cupidite_val)
        return argent_final
    
    def attirance_xp(self, xp_base, distance, portee_xp):
        """Collect XP at distance based on attraction"""
        attirance_val = self.caracteristiques.get("attirance")
        
        if attirance_val is None or portee_xp is None:
            return 0
        
        if distance <= portee_xp:
            xp_collecte = xp_base * (1 + attirance_val * 0.01)
            return xp_collecte
        
        return 0
    
    def malchance(self, dg_ennemis, frequence):
        """Effets malchance"""
        malchance_val = self.caracteristiques.get("malchance")
        
        if malchance_val is None:
            return dg_ennemis, frequence
        
        dg_supp = dg_ennemis + malchance_val
        nv_frequence = frequence + malchance_val
        return dg_supp, nv_frequence
    
    def protection(self, dg_ennemis):
        """Reduire les degats"""
        protection_val = self.caracteristiques.get("protection")
        
        if protection_val == 0:
            return dg_ennemis
        
        dg_reduit = dg_ennemis * (1 - protection_val)
        return max(dg_reduit, 0) 
    
    def augmentation_sante(self, sante_base):
        """Améliore la santé de base"""
        sante_val = self.caracteristiques.get("sante")
        
        if sante_val is None or sante_val <= 0:
            return sante_base
        
        nv_sante = sante_base * (1 + sante_val)
        return nv_sante



class Player(pygame.sprite.Sprite):
    """Class player pour la projection"""
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_count = 10
        self.standing = True
        
        # Player stats
        self.hp = 100
        self.hp_max = 100
        self.xp = 0
        self.argent = 0
        self.equipe_armes = []
        self.equipe_items = []
    
    def draw(self, win):
        """Dessine le joeur"""
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        
        # Placeholder rectangle (replace with actual sprites)
        color = (0, 100, 255) if self.right else (255, 100, 0)
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))
    
    def update_position(self, keys):
        """Update player position based on key input"""
        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.left = True
            self.right = False
            self.standing = False
        elif keys[pygame.K_RIGHT] and self.x < 500 - self.width - self.vel:
            self.x += self.vel
            self.right = True
            self.left = False
            self.standing = False
        else:
            self.standing = True
            self.walk_count = 0
        
        # Handle jump
        if not self.is_jump:
            if keys[pygame.K_UP]:
                self.is_jump = True
                self.right = False
                self.left = False
                self.walk_count = 0
        else:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10
    
    def equiper_arme(self, arme):
        """Equip a weapon"""
        if isinstance(arme, Arme):
            self.equipe_armes.append(arme)
    
    def equiper_item(self, item):
        """Equip an item"""
        if isinstance(item, Items):
            self.equipe_items.append(item)
    
    def prendre_degat(self, degat):
        """Take damage"""
        self.hp -= degat
        if self.hp < 0:
            self.hp = 0
    
    def gagner_xp(self, xp):
        """Gain experience"""
        self.xp += xp
    
    def gagner_argent(self, montant):
        """Gain money"""
        self.argent += montant



class Projectile(pygame.sprite.Sprite):
    """Class projectile pour la statistique"""
    
    def __init__(self, x, y, radius, color, facing):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    
    def update(self):
        """Update projectile position"""
        self.x += self.vel
    
    def draw(self, win):
        """Draw projectile on screen"""
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)
    
    def is_off_screen(self):
        """Regarde si le projectile est sur la map"""
        return self.x < 0 or self.x > 500



class Game:
    """Main game controller class"""
    
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 500
    FPS = 27
    
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game - Armes et Items")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Player(200, 410, 64, 64)
        self.bullets = pygame.sprite.Group()
        
        # Background
        self.bg = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.bg.fill((255, 255, 255))
        
        # Game settings
        self.max_bullets = 5
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        """Update game state"""
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update_position(keys)
        
        # Handle shooting
        if keys[pygame.K_SPACE]:
            if len(self.bullets) < self.max_bullets:
                facing = -1 if self.player.left else 1
                new_bullet = Projectile(
                    round(self.player.x + self.player.width // 2),
                    round(self.player.y + self.player.height // 2),
                    6,
                    (0, 0, 0),
                    facing
                )
                self.bullets.add(new_bullet)
        
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
    
    def draw(self):
        """Draw all game elements"""
        self.screen.blit(self.bg, (0, 0))
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        pygame.display.update()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()


def calculer_application_refroidissement(dernier_tir, refroidissement):
    """Check if enough time has passed for next shot"""
    maintenant = time.time()
    if dernier_tir == 0:
        dernier_tir = maintenant
        return True, maintenant
    
    if maintenant - dernier_tir >= refroidissement:
        dernier_tir = maintenant
        return True, dernier_tir
    
    return False, dernier_tir


def regen_hp(player, recuperation, interval=1):
    """Regenerate HP every interval seconds"""
    if recuperation is None or recuperation <= 0:
        return
    
    while player.hp < player.hp_max:
        time.sleep(interval)
        player.hp += recuperation
        if player.hp > player.hp_max:
            player.hp = player.hp_max


def durabilite_effect(player, durabilite_val, damage_per_tick=5, interval=2):
    """Decrease HP based on item durability"""
    if durabilite_val is None:
        return
    
    for _ in range(durabilite_val):
        time.sleep(interval)
        player.hp -= damage_per_tick

    pyg.quit() 

pygame.init()

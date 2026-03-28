import tkinter as tk
import time
import math
import pygame
import random
from Code_fonctionnel import variables as vb

global projectileYPosition

class Arme:

    def __init__(self, type):
        for carac in vb.ARMES[type]:
            self.str(carac) = vb.ARMES[type][carac]

    def améliorer_arme(self, nv_degat):
        """Améliorer une arme"""
        if self.niveau >= self.niveau_req:
            self.dgbase += nv_degat
            self.niveau += 1


    def est_a_portee(self, distance_monstre):
        """Vérifier qu'une arme peut atteindre sa cible"""
        return distance_monstre <= self.portee


    def arme_degat(self, degat):
        """Appliquer des dégats"""
        if self.reduction:
            return degat - self.reduction
        return degat
    
    def acheter_armes(self, prix):
        """Acheter une arme"""
        self.solde_j -= prix
    def afficher_armes(ARMES,update_xp):
        """Affiche les armes"""
        if update_xp() == True :
            label.config(text=epee.nom)
            epee = Arme("Épée")
            fenetre = tk.Tk() 
            bouton = tk.Button(fenetre, text="Voir arme", command="show_arme")
            bouton.pack()
            label = tk.Label(fenetre, text="")
            label.pack()
            fenetre.mainloop()
    
class Items:
    hp = 100 # Vie du joueur
    xp = 0  # XP du joueur
    argent = 0  # Argent du joueur
    

"""
# initialize pygame objects
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
"""

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)



def redrawGameWindow():
    vb.WIN.blit(vb.BG, (0,0))
    man.draw(vb.WIN)
    for bullet in bullets:
        bullet.draw(vb.WIN)
    
    pygame.display.update()


#mainloop
man = player(200, 410, 64,64)
bullets = []
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 0:

            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

    
    def acheter_items(items, solde_j, prix):
        """Achat d'items"""
        if solde_j >= prix:
            solde_j -= prix
        return solde_j

    def regen_hp(items):
        """Récupération  de PV toutes les secondes"""
        if recuperation is None:
            return
        while hp < hp_max:
            time.sleep(1)
            hp += recuperation
            if hp > hp_max:
                hp = hp_max

def améliorer_items(items, degat, niveau,niveau_rq):
    """Améliorer un item"""
    """Ce n'est pas une fonction complete """
    """Pour la compléter il faudrais faire une fonction par items"""
    """Ici je l'ai mise juste pour avoir l'idée"""   
    if niveau >= niveau_req:
        dgbase += nv_degat
        niveau += 1
def durabilite(items):
    """Augmente les dégats de l'item selon sa durabilité"""
    if durabilite is None:
        return
    for _ in range(durabilite):
        time.sleep(2)
        hp -= 5
def refroidissement(items, refroidir):
    """Réduit le temps entre attaques"""
    refroidissement = 100
    if refroidir  is None:
        return
    else :
        nv_reduction = refroidissement - refroidir
        return nv_reduction
def vitesse(items, vitesse_j):
    """Augmente la  vitesse du joueur"""
    vitesse_base = 20
    if vitesse_j  is None:
        return
    else :
        nv_vitesse_j = vitesse_base*(1+ vitesse_j)
        return nv_vitesse_j
def chance(items, chance):
    """Augmente la  chance du joueur"""
    chance_base = 10
    if chance is None:
        return
    else :
        nv_chance = chance_base*(1 + chance)
        return nv_chance

def application_refroidissement(items, dernier_tire):
    """Appliquer le refroidisemment"""
    maintenant = time.time()
    if dernier_tir is None:
        dernier_tir = 0
    if maintenant - dernier_tir >= refroidissement:
        dernier_tir = maintenant
        return True
    else:
        return False
def resurrection(items, hp, barre_de_vie):  

    """Phénomène de resurrection""" 
    """Prendre la resurection c'est accepter de perdre ses bonus""" 
    if resurrection>=1:
        if hp == 0 :
            (hp + barre_vie)*(1.5)
        else:
            return
    else:
        return 


def cupidite(items, somme):
    """Ajoute un pourcentage à l'argent récolté"""
    if cupidite is None:
        return somme
    argent_final = somme * (1 + cupidite)
    return argent_final

def attirance(items, xp, res_x, res_y, jpos_x, jpos_y, portee_xp):
    """Ramasse de l'XP à distance selon l'attirance"""
    if attirance is None or portee_xp is None:
        return 0
    distance = math.sqrt((jpos_x - res_x)**2 + (jpos_y - res_y)**2)
    while distance <= self.portee_xp:
        xp += xp
        return xp
    else:
        return 0

def malchance(items,dg_ennemis, frequence):
    """Applique les effets de la malchance'"""
    if malchance is None : 
        return
    dg_supp = dg_ennemis + malchance
    nv_frequence = frequence + malchance
    return dg_supp, nv_frequence
def protection(items,dg_ennemis):
    """Réduit les dégats reçus"""
    if dg_ennemis>0:
        efprotection = dg_ennemis*(1+protection)
        return efprotection
def quantite_proj(items,quantite_b):
    """Augmente la quantité de projectile"""
    if quantite_b is None :
        return
    else: 
        quantite_nv =  len(bullets)*quantite_b
    return quantite_nv
def augmentation_sante(items,sante, sante_base):
    """Augmenter la santé de base"""
    if sante>0:
        nv_sante = sante_base *(1+sante)
        return sante



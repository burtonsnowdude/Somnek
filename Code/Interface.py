import pygame as pyg
import sys
import random
import subprocess
from variables import *

pyg.init()

# Fenêtre
WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("SOMNEK")

# Fond d'écran
fond_decran = pyg.image.load("Images/Interface/fond_accueil.png")
fond_decran = pyg.transform.scale(fond_decran, (WIDTH, HEIGHT))

fond_enter = pyg.image.load("Images/Interface/press.png")
fond_enter = pyg.transform.scale(fond_enter, (WIDTH, HEIGHT))



# Musique
"""pyg.mixer.music.load("Musique/Music_interface.mp3")"""
"""pyg.mixer.music.play(-1)"""

# Couleurs
WHITE = (255, 255, 255)
TRANSLUCENT_BLUE = (0, 0, 255, 128)
HOVER_BLUE = (0, 0, 200)
SHADOW = (0, 0, 0, 100)
game_enter = False
# Polices
try:
    FONT_TITLE = pyg.font.Font("assets/pixels.ttf",130)
    FONT_BUTTON = pyg.font.Font("assets/pixels.ttf", 36)
except:
    FONT_TITLE = pyg.font.SysFont(None, 130)
    FONT_BUTTON = pyg.font.SysFont(None, 36)

# Classe Button
class Button:
    def __init__(self, text, action, x,y, width, height):
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.rect = pyg.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

    def draw(self, win, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = HOVER_BLUE if hovered else TRANSLUCENT_BLUE
        button_surface = pyg.Surface((self.width, self.height), pyg.SRCALPHA)
        pyg.draw.rect(button_surface, color, (0, 0, self.width, self.height), border_radius=10)
        win.blit(button_surface, self.rect)

        # Texte
        shadow = FONT_BUTTON.render(self.text, True, SHADOW)
        text_surface = FONT_BUTTON.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        win.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

# Création des boutons  
buttons = [ 
    Button("COMMENCER", "load", 400, 305, 300, 65),   

    Button("COLLECTION", "collection", 150, 440, 220, 60), 
    Button("POWER UP", "power_up", 400, 440, 250, 70), 
    Button("REALISATIONS", "realisations", 670, 440, 260, 60), 

    Button("Credits", "credits", 400, 520, 200, 50), 
    Button("Options", "options", 100, 50, 180, 45),   
    Button("QUITTER", "quit", 700, 50, 180, 45),       
    Button("Pressez ESPACE pour commencer", "start", 400, 300, 300, 50)]
# Initialiser la police
font = pyg.font.Font(None, 36)
# Initialiser le score
argent = 0
# Boucle principale
running = True
clock = pyg.time.Clock()

while running:
    clock.tick(60)
    WIN.blit(fond_decran, (0, 0))
    mouse_pos = pyg.mouse.get_pos()
    mouse_pressed = pyg.mouse.get_pressed()

    # Titre
    title_shadow = FONT_TITLE.render("SOMNEK", True, SHADOW)
    title = FONT_TITLE.render("SOMNEK", True, WHITE)
    WIN.blit(title_shadow, (210, 165))  
    WIN.blit(title, (210, 150)) 

    # Boutons
    for btn in buttons:
        btn.draw(WIN, mouse_pos)
        if btn.is_clicked(mouse_pos, mouse_pressed):
            pyg.time.delay(200)

            if btn.action == "load":
                print("Commencer")
            elif btn.action == "collection":
                print("Collection")     
            elif btn.action == "credits":
                print("Credits")                
            elif btn.action == "power_up":
                print("Power Up")
            elif btn.action == "realisations":
                print("Réalisations")   
            elif btn.action == "options":
                print("Options")
            elif btn.action == "quit":  
                running = False
 
    
    # Afficher l'argent
    argent_text = font.render(f"Argent: {argent}", True, (0, 0, 0))
    argent_rect = argent_text.get_rect(center=(400, 50))  # centre haut
    WIN.blit(argent_text, argent_rect)
 

    # Événements
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_SPACE:
                print("Espace pressé - Lancer le jeu")
                game_enter = True

    pyg.display.flip()

pyg.quit()
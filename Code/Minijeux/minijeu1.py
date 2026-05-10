"""
mini jeu du nerd : binaire
"""
import pygame as pyg
from Minijeux.minijeu2 import spawn_objet, draw_objet, collision
from Affichage.fonctionnement_divers import screen_to_world, camera
from Fichiers_variables.variables import *
from random import randint

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = 300, 350, 100, 200
COMPUTER = pyg.image.load("Images/Autre/game_stop_exterieur.png")
FOND_QUIZ = pyg.transform.scale(pyg.image.load("Images/Autre/game_stop_interieur.png"), (WIDTH, HEIGHT))


def binary_quiz():
    """Quiz binaire simple - affiche le binaire, obtiens la réponse entière"""
    binary_number = randint(0, 255)
    binary_str = format(binary_number, '08b')
    
    user_answer = ""
    clock = pyg.time.Clock()
    feedback = None
    feedback_time = 0
    
    # Dimensions du popup
    popup_width = 400
    popup_height = 250
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    
    while True:
        clock.tick(60)
        
        WIN.blit(FOND_QUIZ, (0, 0))
        
        # Popup box
        pyg.draw.rect(WIN, (50, 50, 50), (popup_x, popup_y, popup_width, popup_height))
        pyg.draw.rect(WIN, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height), 3)
        
        # Affiche le nombre binaire
        text = FONT.render(binary_str, True, (0, 255, 0))
        text_rect = text.get_rect(center=(WIDTH//2, popup_y + 50))
        WIN.blit(text, text_rect)
        
        # Affiche l'entrée
        answer_text = FONT.render("Reponse: " + user_answer, True, (255, 255, 255))
        WIN.blit(answer_text, (popup_x + 20, popup_y + 120))
        
        # Affiche le feedback (succès ou erreur)
        if feedback:
            color = (0, 255, 0) if feedback == "Correct!" else (255, 0, 0)
            feedback_text = FONT.render(feedback, True, color)
            feedback_rect = feedback_text.get_rect(center=(WIDTH//2, popup_y + 200))
            WIN.blit(feedback_text, feedback_rect)
            
            # Quitter après 2 secondes
            if clock.get_time() + feedback_time > 2000:
                return feedback == "Correct!"
            feedback_time += clock.get_time()
        
        pyg.display.update()
        
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_RETURN and user_answer and not feedback:
                    if int(user_answer) == binary_number:
                        feedback = "Correct!"
                    else:
                        feedback = "Faux!"
                    feedback_time = 0
                elif event.key == pyg.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                elif event.unicode.isdigit() and not feedback:
                    user_answer += event.unicode


def minijeu1(p, coord_monde, minijeu1_fini, map):
    if coord_monde == None:
        coord_screen = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN, p, map)
        coord_monde = screen_to_world(coord_screen[0], coord_screen[1], p)
    
    coord_screen = camera(coord_monde[0], coord_monde[1], p)
    draw_objet(coord_screen, COMPUTER)
    
    if collision(coord_screen, COMPUTER, p):
        binary_quiz()
        minijeu1_fini = True
    
    return coord_monde, minijeu1_fini
    

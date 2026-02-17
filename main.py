import pygame as pyg # importer le module pygame (game engine)
import time
from variables import * # importer les variables


def draw(player, temp_ecoulé, monster, bg, barre_PV): # dessiner tout
    WIN.fill((225, 225, 225)) # fond d'ecran

    WIN.blit(BG, bg) # dessiner le fond d'ecran
    pyg.draw.rect(WIN, (255, 0, 0), player) # dessiner le joueur (rectangle rouge)
    pyg.draw.rect(WIN, (0, 255, 0), monster) # dessiner le joueur (rectangle rouge)
    pyg.draw.rect(WIN, (0, 255, 10), barre_PV)

    if temp_ecoulé < 60: # calculer les minutes et secondes seulement si besoin

        time_text = FONT.render(f"{int(temp_ecoulé)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    else:
        min = temp_ecoulé // 60 
        sec = temp_ecoulé % 60 

        time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    WIN.blit(time_text, (10, 10)) # afficher le texte du temps ecoulé
    

    pyg.display.update() # mettre a jour l'affichage

def main():
    clock = pyg.time.Clock() # creer une horloge pour gerer le temps

    run = True

    bg = BG.get_rect() # creer un rectangle pour le fond d'ecran
    player = pyg.Rect(CENTREx, CENTREy, PLAYER_WIDTH, PLAYER_HEIGHT)# creer le joueur (rectangle)
    monster = pyg.Rect(20, 20, PLAYER_WIDTH, PLAYER_HEIGHT)# creer le joueur (rectangle)
    barre_PV = pyg.Rect(400, 10, PLAYER_PV*30, 20)

    start_time = time.time()  # temps de debut
    temp_ecoulé = 0  # temps ecoule

    while run:
        clock.tick(60) # fixer le nombre de frames par seconde
        temp_ecoulé = time.time() - start_time  # calculer le temps ecoule

        for event in pyg.event.get():  # cherche pour l'appuye du bouton sortie
            if event.type == pyg.QUIT: # si le joueur ferme la fenetre
                run = False 
                break

        # controle du joueur (avec les fleches ou les touches WASD)
        keys = pyg.key.get_pressed()
        
        if (keys[pyg.K_LEFT] or keys[pyg.K_a]):                       # gauche
            bg.x += PLAYER_VIT
            monster.x += PLAYER_VIT

        if (keys[pyg.K_RIGHT] or keys[pyg.K_d]) and (player.x + PLAYER_VIT + PLAYER_WIDTH) <= WIDTH:   # droite
            bg.x -= PLAYER_VIT
            monster.x -= PLAYER_VIT

        if (keys[pyg.K_UP] or keys[pyg.K_w]) and (player.y - PLAYER_VIT) >= 0:                         # haut
            bg.y += PLAYER_VIT
            monster.y += PLAYER_VIT

        if (keys[pyg.K_DOWN] or keys[pyg.K_s]) and (player.y + PLAYER_VIT + PLAYER_HEIGHT) <= HEIGHT:  # bas
            bg.y -= PLAYER_VIT
            monster.y -= PLAYER_VIT

        follow(player, monster)

        "PLAYER_PV = degats(player, monster, PLAYER_PV)"

        draw(player, temp_ecoulé, monster, bg, barre_PV) # dessiner tout

    pyg.quit() # quitter pygame

"""
def degats(player, monster, PV):
    if player.colliderect(monster) and PV>0:
            PV -= 1
            time.sleep(1)
    elif PV <= 0:
         return 0
    return PV
"""


def follow(player, monster):
    import math
    # Calculate direction vector from monster to player
    dx = player.centerx - monster.centerx
    dy = player.centery - monster.centery
    
    distance = math.sqrt(dx**2 + dy**2)
    
    # Only move if distance > 0 to avoid division by zero
    if distance > 0:
        # Normalize and move at MONSTER_VIT speed
        monster.x += (dx / distance) * MONSTER_VIT
        monster.y += (dy / distance) * MONSTER_VIT


if __name__ == "__main__": #s'assure que le main ne s'execute que si on lance ce fichier directement
    main()
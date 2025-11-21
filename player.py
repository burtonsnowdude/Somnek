import pygame as pyg # importer le module pygame (game engine)
import time
pyg.font.init() # initialiser le module font de pygame


WIDTH, HEIGHT = 800, 600 # dimensions de la fenetre
WIN = pyg.display.set_mode((WIDTH, HEIGHT)) # creer la fenetre
pyg.display.set_caption("Player Movement Example") 

BG = pyg.transform.scale(pyg.image.load("background.jpg"), (WIDTH, HEIGHT)) # charger et redimensionner le fond d'ecran


PLAYER_WIDTH, PLAYER_HEIGHT = 25, 45 # taille du joueur
PLAYER_VIT = 5 # vitesse de deplacement du joueur
PLAYER_PV = 10 # points de vie du joueur
MONSTER_VIT= 1

FONT = pyg.font.SysFont("comicsans", 30) # definir la police d'ecriture


def draw(player, temp_ecoulé, monster): # dessiner tout
    WIN.blit(BG, (0, 0)) # fond d'ecran

    pyg.draw.rect(WIN, (0, 0, 255), player) # dessiner le joueur (rectangle rouge)
    pyg.draw.rect(WIN, (0, 255, 0), monster) # dessiner le joueur (rectangle rouge)

    if temp_ecoulé < 60: # calculer les minutes et secondes seulement si besoin

        time_text = FONT.render(f"{int(temp_ecoulé)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    else:
        min = temp_ecoulé // 60 # calculer les minutes
        sec = temp_ecoulé % 60 # calculer les secondes

        time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) # creer le texte du temps ecoulé
    WIN.blit(time_text, (10, 10)) # afficher le texte du temps ecoulé

    pyg.display.update() # mettre a jour l'affichage

def main():
    clock = pyg.time.Clock() # creer une horloge pour gerer le temps

    run = True

    player = pyg.Rect(WIDTH/2 - PLAYER_WIDTH, HEIGHT/2 - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)# creer le joueur (rectangle)
    monster = pyg.Rect(20, 20, PLAYER_WIDTH, PLAYER_HEIGHT)# creer le joueur (rectangle)

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
        
        if (keys[pyg.K_LEFT] or keys[pyg.K_a]) and (player.x - PLAYER_VIT) >= 0:                       # gauche
            player.x -= PLAYER_VIT
        
        if (keys[pyg.K_RIGHT] or keys[pyg.K_d]) and (player.x + PLAYER_VIT + PLAYER_WIDTH) <= WIDTH:   # droite
            player.x += PLAYER_VIT
        
        if (keys[pyg.K_UP] or keys[pyg.K_w]) and (player.y - PLAYER_VIT) >= 0:                         # haut
            player.y -= PLAYER_VIT
        
        if (keys[pyg.K_DOWN] or keys[pyg.K_s]) and (player.y + PLAYER_VIT + PLAYER_HEIGHT) <= HEIGHT:  # bas
            player.y += PLAYER_VIT

        follow(player, monster)

        draw(player, temp_ecoulé, monster) # dessiner tout

    pyg.quit() # quitter pygame

def follow(player, monster):
    if(player.x < monster.x):
        monster.x -= MONSTER_VIT
    if(player.x > monster.x):
        monster.x += MONSTER_VIT
    if(player.y < monster.y):
        monster.y -= MONSTER_VIT
    if(player.y > monster.y):
        monster.y += MONSTER_VIT

if __name__ == "__main__": #s'assure que le main ne s'execute que si on lance ce fichier directement
    main()

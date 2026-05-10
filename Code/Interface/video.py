import pygame as pyg
from Fichiers_variables.traitement_images import decouper_image
from Fichiers_variables.variables import WIN, CENTREx, CENTREy, FONT

def play_video(image, col, row, nb_a_enlever):
    image = "Images/Autre/" + image +".png"
    spritesheet = pyg.image.load(image)
    anims = decouper_image(spritesheet, col, row, nb_a_enlever)
    rect = anims[0].get_rect()
    rect.center = (CENTREx, CENTREy)
    frame = 0
    i = 0
    texte = FONT.render("Pour passer la cinématique, cliquez Entrée.", True, (255, 255, 255))
    rect_texte = texte.get_rect()
    rect_texte.center = (600, 550)
    fade = 255
    while i < len(anims) - 1 :
        for event in pyg.event.get():  
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.KEYDOWN :
                keys = pyg.key.get_pressed()
                if keys[pyg.K_RETURN]:
                    return 
        WIN.fill((0, 0, 0))
        WIN.blit(anims[i], rect)
        texte.set_alpha(fade)
        WIN.blit(texte, rect_texte)
        if frame %15 == 0 :
            i += 1
            if fade > 4 :
                fade -= 5
        frame += 1
        pyg.display.update()
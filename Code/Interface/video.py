import pygame as pyg
from Fichiers_variables.traitement_images import decouper_image
from Fichiers_variables.variables import WIN, CENTREx, CENTREy

def play_video(image, col, row, nb_a_enlever):
    image = "Images/Autre/" + image +".png"
    spritesheet = pyg.image.load(image)
    anims = decouper_image(spritesheet, col, row, nb_a_enlever)
    rect = anims[0].get_rect()
    rect.center = (CENTREx, CENTREy)
    frame = 0
    i = 0
    while i < len(anims) - 1 :
        for event in pyg.event.get():  
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
        WIN.blit(anims[i], rect)
        if frame %15 == 0 :
            i += 1
        frame += 1
        pyg.display.update()
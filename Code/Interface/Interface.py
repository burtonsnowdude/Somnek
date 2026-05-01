from turtle import position
from Interface.option import settings, flashing_effect, black_and_white
import pygame as pyg
import sys

from Fichiers_variables.variables import *
from Interface.realisation_brouillon import realisation_brouillon, POPUP_W, POPUP_H
from Interface.Power_up_shop import open_shop
from Interface.option import options, checkboxes
from Interface.Class_Button import Button
import Interface.variable_power_up as data
from Interface.collection import open_collection
from Interface.start import open_start
from Interface.collection import selected_item
from Fichiers_variables.gestion_fichiers import get_info

pyg.init()
pyg.font.init()
pyg.mixer.init()

WIN = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("SOMNEK")



def play_music(path):
    pyg.mixer.music.stop()
    pyg.mixer.music.load(path)
    pyg.mixer.music.play(0)

try:
    FONT_TITLE = pyg.font.Font("assets/pixels.ttf", 130)
    FONT_BUTTON = pyg.font.Font("assets/pixels.ttf", 36)
except:
    FONT_TITLE = pyg.font.SysFont(None, 130)
    FONT_BUTTON = pyg.font.SysFont(None, 36)

FONT_BUTTON = pyg.font.SysFont(None, 36)


buttons = [
    Button("COMMENCER", "load", 400, 305, 300, 65, FONT_BUTTON),
    Button("COLLECTION", "collection", 150, 440, 220, 60, FONT_BUTTON),
    Button("POWER UP", "power_up", 400, 440, 250, 70, FONT_BUTTON),
    Button("REALISATIONS", "realisations", 670, 440, 260, 60, FONT_BUTTON),
    Button("Credits", "credits", 400, 520, 200, 50, FONT_BUTTON),
    Button("Options", "options", 100, 50, 180, 45, FONT_BUTTON),
    Button("QUITTER", "quit", 700, 50, 180, 45, FONT_BUTTON),
]

btn_rev_coll = Button("X", "rev_coll", 550, 130, 40, 40, FONT_BUTTON)
btn_rev_real = Button("X", "rev_real", 550, 130, 40, 40, FONT_BUTTON)
btn_rev_cre = Button("X", "rev_cre", 550, 130, 40, 40, FONT_BUTTON)
btn_rev_opt = Button("X", "rev_opt", 550, 130, 40, 40, FONT_BUTTON)  # Bouton pour fermer les options
btn_confirm_nerd = Button("Confirmer", "confirm", 550, 500, 80, 40, FONT_BUTTON)
btn_rev_start = Button("X", "rev_start", 550, 130, 40, 40, FONT_BUTTON)

def interface():
    fond_intro = pyg.image.load("Images/Interface/press.png")
    fond_intro = pyg.transform.scale(fond_intro, (WIDTH, HEIGHT))

    fond_menu = pyg.image.load("Images/Interface/fond_accueil.png")
    fond_menu = pyg.transform.scale(fond_menu, (WIDTH, HEIGHT))



    fond_credits = pyg.image.load("Images/Interface/fond_credits.png")
    fond_credits = pyg.transform.scale(fond_credits, (350, 400))

    buttons = [
    Button("COMMENCER", "load", 400, 305, 300, 65, FONT_BUTTON),
    Button("COLLECTION", "collection", 150, 440, 220, 60, FONT_BUTTON),
    Button("POWER UP", "power_up", 400, 440, 250, 70, FONT_BUTTON),
    Button("REALISATIONS", "realisations", 670, 440, 260, 60, FONT_BUTTON),
    Button("Credits", "credits", 400, 520, 200, 50, FONT_BUTTON),
    Button("Options", "options", 100, 50, 180, 45, FONT_BUTTON),
    Button("QUITTER", "quit", 700, 50, 180, 45, FONT_BUTTON),
    ]

    btn_rev_coll = Button("X", "rev_coll", 550, 130, 40, 40, FONT_BUTTON)
    btn_rev_real = Button("X", "rev_real", 550, 130, 40, 40, FONT_BUTTON)
    btn_rev_cre = Button("X", "rev_cre", 550, 130, 40, 40, FONT_BUTTON)
    btn_rev_opt = Button("X", "rev_opt", 550, 130, 40, 40, FONT_BUTTON)  # Bouton pour fermer les options
    btn_confirm_nerd = Button("Confirmer", "confirm", 550, 500, 80, 40, FONT_BUTTON)
    btn_rev_start = Button("X", "rev_start", 550, 130, 40, 40, FONT_BUTTON)

    game = False
    show_image = False
    show_realisation = False
    show_credits = False
    show_start = False
    show_options = False  # Ajoutez cette variable
    show_shop = False



    musique_bout = False
    musique_load = False
    musique_close = False
    musique_back = False

    musique_bout_played = False
    musique_load_played = False
    musique_close_played = False
    musique_back_played = False
    argent = 0

    joueur = "Daphne"
    player_money = get_info(joueur, "argent", None)

    reset_clicked = False
    clock = pyg.time.Clock()
    running = True

    while running:
        clock.tick(60)

        mouse_pos = pyg.mouse.get_pos()
        mouse_pressed = pyg.mouse.get_pressed()
        events = pyg.event.get()

        # RESET AUDIO FLAGS CHAQUE FRAME
        musique_bout_played = False
        musique_load_played = False
        musique_close_played = False

        if not game:
            WIN.blit(fond_intro, (0, 0))
            texte = FONT_BUTTON.render("Pressez ESPACE", True, (255, 255, 255))
            WIN.blit(texte, (250, 300))

        else:
            WIN.blit(fond_menu, (0, 0))

            title = FONT_TITLE.render("SOMNEK", True, (255, 255, 255))
            WIN.blit(title, (210, 150))

            argent_text = FONT_BUTTON.render(f"Argent: {player_money}", True, (0, 0, 0))
            WIN.blit(argent_text, (330, 50))

            for btn in buttons:
                btn.draw(WIN, mouse_pos)

                if btn.is_clicked(mouse_pos, mouse_pressed):
                    pyg.time.delay(200)

                    if btn.action == "collection":
                        show_image = True
                        musique_bout = True

                    elif btn.action == "options":
                        show_options = True  # Afficher les options
                        musique_bout = True

                    elif btn.action == "quit":
                        musique_close = True
                        running = False
                        pyg.quit()
                        exit()
                        return False

                    elif btn.action == "realisations":
                        show_realisation = True
                        musique_bout = True

                    elif btn.action == "credits":
                        show_credits = True
                        musique_bout = True

                    elif btn.action == "load":
                        musique_load = True
                        show_start = True
                        

                    elif btn.action == "power_up":
                        musique_bout = True
                        if btn.action == "power_up":
                            show_shop = True
            if not settings["music"]:
                pyg.mixer.music.stop()

            if musique_bout and not musique_bout_played:
                if settings["sound"]:
                    play_music("Sons/sound_button.mp3")
                    musique_bout = False

            if musique_load and not musique_load_played:
                if settings["sound"]:
                    play_music("Sons/start.mp3")
                    musique_load = False

            if musique_close and not musique_close_played:
                if settings["sound"]:
                        play_music("Sons/rev.mp3")
                        musique_close = False
            if settings["music"]:
                if pyg.mixer.music.get_busy() == False:
                    pyg.mixer.music.load("Sons/music_interface.mp3")
                    pyg.mixer.music.play(-1)

            if show_realisation:
                popup = realisation_brouillon(events)

                WIN.blit(
                    popup,
                    ((WIDTH - POPUP_W)//2, (HEIGHT - POPUP_H)//2)
                )

                btn_rev_real.draw(WIN, mouse_pos)

                if btn_rev_real.is_clicked(mouse_pos, mouse_pressed):
                    pyg.time.delay(200)
                    show_realisation = False
                    musique_close = True

            if show_credits:
                WIN.blit(fond_credits, (240, 150))
                btn_rev_cre.draw(WIN, mouse_pos)

                if btn_rev_cre.is_clicked(mouse_pos, mouse_pressed):
                    pyg.time.delay(200)
                    show_credits = False
                    musique_close = True
                    

            if show_start:
                result = open_start(WIN, events, mouse_pos, mouse_pressed, btn_rev_start, FONT_BUTTON)
                print(result)
                if result is not None :
                    if result == "close":
                        show_start = False

                    elif result[0] == "start_game":
                        show_start = False
                        return result[1]

            # AFFICHER LES OPTINS
            if show_options:
                # Vérifiez que events contient les bonnes données
                options(events, mouse_pos, mouse_pressed, WIN)
                
                btn_rev_opt.draw(WIN, mouse_pos)

                if btn_rev_opt.is_clicked(mouse_pos, mouse_pressed):
                    pyg.time.delay(200)
                    show_options = False
                    musique_close = True
            if show_shop:
                from Interface.Power_up_shop import open_shop, buy_selected

                close = open_shop(events, WIN, mouse_pos, mouse_pressed, btn_rev_opt, FONT_BUTTON, player_money, joueur)

                if btn_confirm_nerd.is_clicked(mouse_pos, mouse_pressed):
                    buy_selected(player_money, joueur)

                if close:
                    show_shop = False
                player_money = get_info(joueur, "argent", None)    
            if show_image:
                    close = open_collection(events, WIN, mouse_pos, mouse_pressed, btn_rev_coll)

                    if close:
                        show_image = False
                        musique_close = True
            

        for event in events:
                if event.type == pyg.QUIT:
                    running = False
                    return False
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_SPACE:
                        game = True

        if settings["bw"]:
            black_and_white(WIN)

        if settings["vfx"]:
            flashing_effect(WIN)
        pyg.display.flip()


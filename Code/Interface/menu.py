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


def interface(skip_intro=False, joueur=None):  # ← joueur en paramètre
    fond_intro = pyg.image.load("Images/Interface/press.png")
    fond_intro = pyg.transform.scale(fond_intro, (WIDTH, HEIGHT))
    if joueur is None:
        from Interface.utilisateur import get_user_name
        joueur = get_user_name(fond_intro)

    fond_menu = pyg.image.load("Images/Interface/fond_accueil.png")
    fond_menu = pyg.transform.scale(fond_menu, (WIDTH, HEIGHT))

    fond_credits = pyg.image.load("Images/Interface/fond_credits.png")
    fond_credits = pyg.transform.scale(fond_credits, (350, 400))

    img_title = pyg.image.load("Images/Interface/titre.png").convert_alpha()
    img_title = pyg.transform.smoothscale(img_title, (600, 250))
    rect_title = img_title.get_rect(center=(WIDTH // 2, 180))

    img_commencer = pyg.image.load("Images/Interface/commencer_btn.png").convert_alpha()
    img_collection = pyg.image.load("Images/Interface/collection_btn.png").convert_alpha()
    img_option = pyg.image.load("Images/Interface/options_btn.png").convert_alpha()
    img_power_up = pyg.image.load("Images/Interface/power_up_btn.png").convert_alpha()
    img_credit = pyg.image.load("Images/Interface/credit_btn.png").convert_alpha()
    img_avancement = pyg.image.load("Images/Interface/avancement_btn.png").convert_alpha()
    img_quitter = pyg.image.load("Images/Interface/quitter_btn.png").convert_alpha()

    img_argent = pyg.image.load("Images/Interface/argent.png").convert_alpha()
    img_argent = pyg.transform.smoothscale(img_argent, (130, 120))

    buttons = [
        Button("COMMENCER",   "load",         400, 300, 400, 95,  FONT_BUTTON, image=img_commencer),
        Button("COLLECTION",  "collection",   150, 390, 290, 65,  FONT_BUTTON, image=img_collection),
        Button("POWER UP",    "power_up",     423, 387, 310, 65,  FONT_BUTTON, image=img_power_up),
        Button("REALISATIONS","realisations", 650, 390, 485, 270, FONT_BUTTON, image=img_avancement),
        Button("Credits",     "credits",      370, 560, 200, 45,  FONT_BUTTON, image=img_credit),
        Button("Options",     "options",      110, 40,  210, 80,  FONT_BUTTON, image=img_option),
        Button("QUITTER",     "quit",         700, 40,  200, 350, FONT_BUTTON, image=img_quitter),
    ]

    btn_rev_coll  = Button("X", "rev_coll",  550, 130, 40, 40, FONT_BUTTON)
    btn_rev_real  = Button("X", "rev_real",  550, 130, 40, 40, FONT_BUTTON)
    btn_rev_cre   = Button("X", "rev_cre",   550, 130, 40, 40, FONT_BUTTON)
    btn_rev_opt   = Button("X", "rev_opt",   550, 130, 40, 40, FONT_BUTTON)
    btn_confirm_nerd = Button("Confirmer", "confirm", 550, 500, 80, 40, FONT_BUTTON)
    btn_rev_start = Button("X", "rev_start", 550, 130, 40, 40, FONT_BUTTON)

    if joueur is None:
        from Interface.utilisateur import get_user_name
        joueur = get_user_name(fond_intro)


    game = skip_intro
    show_image = False
    show_realisation = False
    show_credits = False
    show_start = False
    show_options = False
    show_shop = False

    musique_bout = False
    musique_load = False
    musique_close = False

    musique_bout_played = False
    musique_load_played = False
    musique_close_played = False

    player_money = get_info(joueur, "argent", None)

    clock = pyg.time.Clock()
    running = True

    while running:
        clock.tick(60)

        mouse_pos = pyg.mouse.get_pos()
        mouse_pressed = pyg.mouse.get_pressed()
        events = pyg.event.get()

        musique_bout_played = False
        musique_load_played = False
        musique_close_played = False

        if not game:
            WIN.blit(fond_intro, (0, 0))
            texte = FONT_BUTTON.render("Pressez ESPACE", True, (255, 255, 255))
            WIN.blit(texte, (250, 300))

        else:
            WIN.blit(fond_menu, (0, 0))
            WIN.blit(img_title, rect_title)
            WIN.blit(img_argent, (270, 3))
            argent_text = FONT_BUTTON.render(f"{player_money}", True, (0, 0, 0))
            WIN.blit(argent_text, (380, 50))

            aucune_fenetre_ouverte = not (show_image or show_realisation or show_credits or show_start or show_options or show_shop)

            for btn in buttons:
                btn.draw(WIN, mouse_pos)

                if aucune_fenetre_ouverte and btn.is_clicked(mouse_pos, mouse_pressed):
                    if btn.action == "collection":
                        show_image = True
                        musique_bout = True
                    elif btn.action == "options":
                        show_options = True
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
                        show_shop = True
                        musique_bout = True

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
                if not pyg.mixer.music.get_busy():
                    pyg.mixer.music.load("Sons/music_interface.mp3")
                    pyg.mixer.music.play(-1)

            if show_realisation:
                popup = realisation_brouillon(events)
                WIN.blit(popup, ((WIDTH - POPUP_W)//2, (HEIGHT - POPUP_H)//2))
                btn_rev_real.draw(WIN, mouse_pos)
                if btn_rev_real.is_clicked(mouse_pos, mouse_pressed):
                    show_realisation = False
                    musique_close = True

            if show_credits:
                WIN.blit(fond_credits, (240, 150))
                btn_rev_cre.draw(WIN, mouse_pos)
                if btn_rev_cre.is_clicked(mouse_pos, mouse_pressed):
                    show_credits = False
                    musique_close = True

            if show_start:
                result = open_start(WIN, events, mouse_pos, mouse_pressed, btn_rev_start, FONT_BUTTON)
                if result is not None:
                    if result == "close":
                        show_start = False
                    elif result[0] == "start_game":
                        show_start = False  
            
                        show_image = False
                        show_realisation = False
                        show_credits = False
                        show_options = False
                        show_shop = False
                        perso = result[1]
                        map_choisie = result[2]
                        return perso, map_choisie, joueur

            if show_options:
                options(events, mouse_pos, mouse_pressed, WIN, joueur, player_money)
                btn_rev_opt.draw(WIN, mouse_pos)
                if btn_rev_opt.is_clicked(mouse_pos, mouse_pressed):
                    show_options = False
                    musique_close = True
                player_money = get_info(joueur, "argent", None)

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
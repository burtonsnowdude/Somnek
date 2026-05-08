import pygame as pyg
from Fichiers_variables.variables import WIN, WIDTH, HEIGHT
from Interface.Class_Button import Button

FONT = pyg.font.SysFont(None, 24)
fond_img = pyg.image.load("Images/Interface/fond_choix_map.png").convert_alpha()
fond_img = pyg.transform.scale(fond_img, (WIDTH, HEIGHT))

MAPS_DISPO = {
    "Metro": "Images/Interface/img_map_metro.png",
    "Cour":  "Images/Interface/img_map_cour.png",
    "Rue":   "Images/Interface/img_map_rue.png",
    "Ruelle":   "Images/Interface/img_map_ruelle.png",
}

MAPS_DEBLOQUEES = ["Metro", "Cour"]

inconnu = pyg.image.load("Images/Maps/pas_map.png")
inconnu = pyg.transform.scale(inconnu, (150, 120))

def open_choix_map(joueur_maps=None):
    if joueur_maps is None:
        joueur_maps = MAPS_DEBLOQUEES

    images = {}
    for nom, path in MAPS_DISPO.items():
        if nom in joueur_maps:
            img = pyg.image.load(path).convert_alpha()
            images[nom] = pyg.transform.scale(img, (150, 120))
        else:
            images[nom] = inconnu

    fond = pyg.Surface((600, 400), pyg.SRCALPHA)
    fond.fill((40, 40, 40, 230))
    fond_rect = fond.get_rect(center=(WIDTH//2, HEIGHT//2))

    keys = list(MAPS_DISPO.keys())
    nb = len(keys)
    spacing = 180
    start_x = WIDTH//2 - (nb-1) * spacing//2
    positions = [(start_x + i * spacing, HEIGHT//2 - 30) for i in range(nb)]

    btn_start = Button("START", "start", WIDTH//2, HEIGHT//2 + 150, 200, 55, FONT)
    selected = keys[0]
    clock = pyg.time.Clock()

    while True:
        clock.tick(60)
        mouse_pos = pyg.mouse.get_pos()
        mouse_pressed = pyg.mouse.get_pressed()
        WIN.blit(fond_img, (0, 0))  # ← fond image
        WIN.blit(fond, fond_rect)   
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                for i, (x, y) in enumerate(positions):
                    rect = pyg.Rect(x - 75, y - 60, 150, 120)
                    if rect.collidepoint(event.pos):
                        if keys[i] in joueur_maps:
                            selected = keys[i]

        WIN.blit(fond, fond_rect)

        for i, (x, y) in enumerate(positions):
            nom = keys[i]
            img = images[nom]
            rect = img.get_rect(center=(x, y))
            WIN.blit(img, rect)
            couleur = (255, 255, 0) if nom == selected else (80, 80, 80)
            pyg.draw.rect(WIN, couleur, rect, 3)
            texte = FONT.render(nom, True, (255, 255, 255))
            WIN.blit(texte, texte.get_rect(center=(x, y + 75)))

        btn_start.draw(WIN, mouse_pos)
        if btn_start.is_clicked(mouse_pos, mouse_pressed):
            return selected

        pyg.display.flip()
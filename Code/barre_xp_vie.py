from variables import *

def afficher_timer_vie(temps_ecoule, p) :
    """Affiche le timer et la barre de PV

    Parameters
    ----------
    temps_ecoule : float
        Le temps écoulé depuis le début de la partie (hors moments de choix)
    p : Self@Player
        Le joueur
    """
    
    min = int(temps_ecoule // 60)
    if len(str(min)) != 2 :
            min = "0"+str(min)
    sec = int(temps_ecoule % 60)
    if len(str(sec)) != 2 :
        sec = "0"+str(sec)
    time_text = FONT.render(f"{min} : {sec}", 1, (255, 255, 255)) 
    WIN.blit(time_text, (370, 20)) 
    height = 5
    const = 4*height
    barre_PV_blanc = pyg.Rect(CENTREx - PLAYER_WIDTH/2, CENTREy - height/2 - PLAYER_HEIGHT/2 - const, PLAYER_WIDTH, height)
    barre_PV = pyg.Rect(CENTREx - PLAYER_WIDTH/2, CENTREy - height/2 - PLAYER_HEIGHT/2 - const, p.hp/2, height)
    pyg.draw.rect(WIN, (255, 255, 255), barre_PV_blanc)
    pyg.draw.rect(WIN, (200, 0, 0), barre_PV)

def afficher_xp(xp_attendu, p):
    """Affiche la barre d'xp

    Parameters
    ----------
    xp_attendu : int
        Le seuil d'xp attendu pour passer au niveau suivant
    p : Self@Player
        Le joueur
    """
    unit = 760/xp_attendu
    barre_xp_blanc = pyg.Rect(20, 3, 760, 10)
    barre_xp = pyg.Rect(20, 3, p.xp*unit, 10)
    pyg.draw.rect(WIN, (255, 255, 255), barre_xp_blanc)
    pyg.draw.rect(WIN, (0, 0, 255), barre_xp)
    pyg.display.update()
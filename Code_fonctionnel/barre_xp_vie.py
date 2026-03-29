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
    if temps_ecoule < 60: 
            time_text = FONT.render(f"{int(temps_ecoule)}s", 1, (255, 255, 255)) 
    else:
        min = temps_ecoule // 60 
        sec = temps_ecoule % 60 
        time_text = FONT.render(f"{int(min)}min {int(sec)}s", 1, (255, 255, 255)) 
    WIN.blit(time_text, (370, 10)) 
    barre_PV_blanc = pyg.Rect(500, 10, 250, 20)
    barre_PV = pyg.Rect(500, 10, p.hp*5, 20)
    pyg.draw.rect(WIN, (255, 255, 255), barre_PV_blanc)
    pyg.draw.rect(WIN, (0, 255, 10), barre_PV)

def afficher_xp(xp_attendu, p):
    """Affiche la barre d'xp

    Parameters
    ----------
    xp_attendu : int
        Le seuil d'xp attendu pour passer au niveau suivant
    p : Self@Player
        Le joueur
    """
    unit = 250/xp_attendu
    barre_xp_blanc = pyg.Rect(10, 10, 250, 20)
    barre_xp = pyg.Rect(10, 10, p.xp*unit, 20)
    pyg.draw.rect(WIN, (255, 255, 255), barre_xp_blanc)
    pyg.draw.rect(WIN, (0, 0, 255), barre_xp)
    pyg.display.update()
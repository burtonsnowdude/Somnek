from variables import *
import pygame as pyg 

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
    txt_niveau = FONT.render(f"LVL {p.niveau}", 1, (255, 255, 255))
    WIN.blit(txt_niveau, (740, 15))
    txt_kill = FONT.render(f"KILLS {p.kill_count}", 1, (255, 255, 255))
    WIN.blit(txt_kill, (720, 30))

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

class PopupAchievement(pyg.sprite.Sprite):
    def __init__(self, message, duration=3000):
        super().__init__()
        self.image = pyg.Surface((300, 50), pyg.SRCALPHA)
        self.image.fill((255, 227, 112, 255))  # Start fully opaque
        pyg.draw.rect(self.image, (0, 0, 0), (5, 5, 290, 40), 2)
        font = pyg.font.SysFont(None, 24)
        text = font.render(message, True, (0, 0, 0))
        self.image.blit(text, (10, 10))
        self.rect = self.image.get_rect(topright=(800, 50))
        self.start_time = pyg.time.get_ticks()
        self.duration = duration

    def update(self):
        elapsed = pyg.time.get_ticks() - self.start_time
        if elapsed > self.duration:
            self.kill()  # Remove from group
        elif elapsed < 2000:  # Opaque for first 2 seconds
            self.image.set_alpha(255)
        else:  # Fade out over the last 1 second
            fade_elapsed = elapsed - 2000
            alpha = max(0, 255 - int((fade_elapsed / 1000) * 255))
            self.image.set_alpha(alpha)
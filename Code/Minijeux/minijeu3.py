"""
Minijeu de la nonne : N'oubliez pas les paroles
"""
from minijeu2 import regler_volume, spawn_objet, play_sound, draw_objet, collision

X_DEBUT, X_FIN, Y_DEBUT, Y_FIN = [0]*4
OBJET = None


def minijeu3(p):
    coord, son = spawn_objet(X_DEBUT, X_FIN, Y_DEBUT, Y_FIN)
    son = regler_volume(coord, p, son)
    play_sound(son)
    draw_objet(coord, OBJET)
    if collision(coord, OBJET):
        pass
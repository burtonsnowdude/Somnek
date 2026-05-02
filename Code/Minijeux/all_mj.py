from Minijeux.minijeu2 import minijeu2 
from Minijeux.minijeu3 import minijeu3

def mj(perso, coord_monde, minijeu_fini, p, armes_possedees, armes_joueur):
    if not minijeu_fini :
        if perso == "Fille_populaire":
            coord_monde, minijeu_fini, armes_possedees, armes_joueur = minijeu2(p, coord_monde, minijeu_fini, armes_possedees, armes_joueur)
        elif perso == "Nerd":
            coord_monde, minijeu_fini, armes_possedees, armes_joueur = minijeu3(p, coord_monde, minijeu_fini, armes_possedees, armes_joueur)
    return coord_monde, minijeu_fini, armes_possedees, armes_joueur

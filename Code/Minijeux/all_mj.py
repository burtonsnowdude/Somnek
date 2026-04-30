from Minijeux.minijeu2 import minijeu2 
from Minijeux.minijeu3 import minijeu3

def mj(perso, coord_monde, minijeu_fini, p, armes_possedees):
    if not minijeu_fini :
        if perso == "Fille_populaire":
            coord_monde, minijeu_fini, armes_possedees = minijeu2(p, coord_monde, minijeu_fini, armes_possedees)
        elif perso == "Nonne":
            coord_monde, minijeu_fini, armes_possedees = minijeu3(p, coord_monde, minijeu_fini, armes_possedees)
    return coord_monde, minijeu_fini, armes_possedees

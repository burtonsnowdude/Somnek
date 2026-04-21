import csv
from variables import *

QUETES ={
    "histoire" : {
        "scene1" : [
            "trouver quelqu’un",
            "survie aux vagues de creatures",
            "inspecte le livre mysterieux",
            "cherche l’exterieur"
            ],

        "scene2" : [
            "trouve ton (objet spécial)",
            "survie aux vagues de créatures"
            ],

        "scene3" : [],

        "scene4" : [],

        "scene5" : [
            "Elimine (nom de boss)",
            "rentre chez toi",
            "sauve le civil",
            "survie aux monstres",
            "entre dans le metro"
            ],

        "scene 6" : [
            "élimine les monstres",
            "prend le metro"
        ],

        "scene7" : ["tue (nom du boss)"]
    },

    "kill" : {

        10 : "tue 10 ennemis ",
        20 : "tue 20 ennemis ",
        50 : "tue 50 ennemis ",
        100 : "tue 100 ennemis ",
        500 : "tue 500 ennemis ",
        1000 : "tue 1000 ennemis ",
        5000 : "tue 5000 ennemis ",
        10000 : "tue 10000 ennemis "
    },

    "aquerir": [
        "aquerir ton premier arme",
        "aquerir 5 armes",
        "aquerir 10 armes",
        "aquerir 20 armes",
        "aquerir 50 armes",
        "aquerir 100 armes",
        "aquerir 200 armes",
        "aquerir 500 armes"
    ]
}

#j'ai besoin que on fini les scenes avant le code des scnes
#j'ai aussi besoin du compteur de morts pour les kill quetes

def verif_q(nb_armes):  # Modified to take nb_armes as parameter for real-time checking
    if nb_armes >= 1:  # Adjusted to >= for cumulative triggers (e.g., first weapon)
        return QUETES["aquerir"][0]
    elif nb_armes >= 5:
        return QUETES["aquerir"][1]
    elif nb_armes >= 10:
        return QUETES["aquerir"][2]
    elif nb_armes >= 20:
        return QUETES["aquerir"][3]
    elif nb_armes >= 50:
        return QUETES["aquerir"][4]
    elif nb_armes >= 100:
        return QUETES["aquerir"][5]
    elif nb_armes >= 200:
        return QUETES["aquerir"][6]
    elif nb_armes >= 500:
        return QUETES["aquerir"][7]
    return False


def verif_k(p):
    nb_kills = p.kill_count
    if nb_kills == 10 and nb_kills < 20:
        return(QUETES["kill"][10])
    elif nb_kills == 20 and nb_kills < 50:
        return(QUETES["kill"][20])
    elif nb_kills == 50 and nb_kills < 100:
        return(QUETES["kill"][50])
    elif nb_kills == 100 and nb_kills < 500:
        return(QUETES["kill"][100])
    elif nb_kills == 500 and nb_kills < 1000:
        return(QUETES["kill"][500])
    elif nb_kills == 1000:
        return(QUETES["kill"][1000])
    elif nb_kills == 5000:
        return(QUETES["kill"][5000])
    elif nb_kills == 10000:
        return(QUETES["kill"][10000])
    return False
    
    
    
    
verif_q(1)

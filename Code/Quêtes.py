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
        1000 : "tue 1000 ennemis "
    },

    "aquerir": [

    ]
}

#j'ai besoin que on fini les scenes avant le code des scnes
#j'ai aussi besoin du compteur de morts pour les kill quetes

def verif_q(utilisateur):
    nb_armes = 0
    with open("Fichiers_csv/armes_obtenues_par_joueur.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row == utilisateur:
                for i in row:
                    nb_armes+=row[i]
    return nb_armes


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
    return False
    
    
    
    
verif_q("Dapne")

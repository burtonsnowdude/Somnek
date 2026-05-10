import csv
from Fichiers_variables.variables import *

QUETES = {
    "histoire": {
        "scene1": [
            "trouver quelqu'un",
            "survie aux vagues de creatures",
            "inspecte le livre mysterieux",
            "cherche l'exterieur",
        ],
        "scene2": ["trouve ton (objet spécial)", "survie aux vagues de créatures"],
        "scene3": [],
        "scene4": [],
        "scene5": [
            "Elimine (nom de boss)",
            "rentre chez toi",
            "sauve le civil",
            "survie aux monstres",
            "entre dans le metro",
        ],
        "scene 6": ["élimine les monstres", "prend le metro"],
        "scene7": ["tue (nom du boss)"],
    },

    "kill": {
        10:    "tue 10 ennemis",
        20:    "tue 20 ennemis",
        50:    "tue 50 ennemis",
        100:   "tue 100 ennemis",
        500:   "tue 500 ennemis",
        1000:  "tue 1000 ennemis",
        5000:  "tue 5000 ennemis",
        10000: "tue 10000 ennemis",
    },

    "aquerir": [
        "aquerir ton premier arme",
        "aquerir 5 armes",
        "aquerir 10 armes",
        "aquerir 20 armes",
        "aquerir 50 armes",
        "aquerir 100 armes",
        "aquerir 200 armes",
        "aquerir 500 armes",
    ],
}




def verif_kill_id(p):
    """Retourne l'ID de la quête kill atteinte au compteur exact, sinon None."""
    n = p.kill_count
    if n == 10:    return "kill_10"
    if n == 50:    return "kill_50"
    if n == 100:   return "kill_100"
    if n == 500:   return "kill_500"
    if n == 1000:  return "kill_1000"
    if n == 5000:  return "kill_5000"
    if n == 10000: return "kill_10000"
    return None


def verif_acquerir_id(nb_armes):
    """Retourne l'ID de la quête acquérir au seuil exact franchi, sinon None."""
    if nb_armes == 1:   return "acquerir_1"
    if nb_armes == 5:   return "acquerir_5"
    if nb_armes == 10:  return "acquerir_10"
    if nb_armes == 50:  return "acquerir_50"
    if nb_armes == 100: return "acquerir_100"
    return None




LIBELLES_QUETES = {
    "kill_10":    "Tuer 10 ennemis",
    "kill_50":    "Tuer 50 ennemis",
    "kill_100":   "Tuer 100 ennemis",
    "kill_500":   "Tuer 500 ennemis",
    "kill_1000":  "Tuer 1000 ennemis",
    "kill_5000":  "Tuer 5000 ennemis",
    "kill_10000": "Tuer 10000 ennemis",

    "acquerir_1":   "Acquérir ta première arme",
    "acquerir_5":   "Acquérir 5 armes",
    "acquerir_10":  "Acquérir 10 armes",
    "acquerir_50":  "Acquérir 50 armes",
    "acquerir_100": "Acquérir 100 armes",

    "trouver_quelquun": "Avoir retrouvé quelqu'un",
    "inspecter_livre":  "Inspecter le livre mystérieux",
    "trouver_objet":    "Trouver ton objet mystérieux",
    "boss_final":       "Éliminer le boss final",
    "Entrer_metro":     "Entrer dans le métro",
}




def verif_k(p):
    qid = verif_kill_id(p)
    return LIBELLES_QUETES.get(qid, False) if qid else False


def verif_q(nb_armes):
    qid = verif_acquerir_id(nb_armes)
    return LIBELLES_QUETES.get(qid, False) if qid else False
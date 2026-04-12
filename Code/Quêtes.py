import csv

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
        "armes projectiles" : {
            10 : "tue 10 ennemis avec une arme projectile",
            20 : "tue 20 ennemis avec une arme projectile",
            50 : "tue 50 ennemis avec une arme projectile",
            100 : "tue 100 ennemis avec une arme projectile",
            500 : "tue 500 ennemis avec une arme projectile",
            1000 : "tue 1000 ennemis avec une arme projectile"
        },
        "armes de mêlée" : {
            10 : "tue 10 ennemis avec une arme de mêlée",
            20 : "tue 20 ennemis avec une arme de mêlée",
            50 : "tue 50 ennemis avec une arme de mêlée",
            100 : "tue 100 ennemis avec une arme de mêlée",
            500 : "tue 500 ennemis avec une arme de mêlée",
            1000 : "tue 1000 ennemis avec une arme de mêlée"
        },
        "armes de zone" : {
            10 : "tue 10 ennemis avec une arme de zone",
            20 : "tue 20 ennemis avec une arme de zone",
            50 : "tue 50 ennemis avec une arme de zone",
            100 : "tue 100 ennemis avec une arme de zone",
            500 : "tue 500 ennemis avec une arme de zone",
            1000 : "tue 1000 ennemis avec une arme de zone"
        }
    
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
    
    
    
verif_q("Dapne")
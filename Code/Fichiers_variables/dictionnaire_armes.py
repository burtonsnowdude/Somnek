from Fichiers_variables.traitement_images import *

TYPES_ARMES = {

    "Epée bleue" : {"type_arme" : None,
                    "image" : None, # j'ai pas
                    "texte" : None}, # pas besoin
    "Lunettes cassées" :
                        {"type_arme": None,
                        "image" : LUNETTES_CASSEES,
                        "texte" : None},
    "Souris de PC" : 
                        {"type_arme": None,
                        "image" : SOURIS,
                        "texte" : None},
    "Chaussettes propres" :
                        {"type_arme": None,
                        "image" : CHAUSSETTES,
                        "texte" : None},
    "Cahier de NSI" :
                        {"type_arme": None,
                        "image" : CAHIER_DE_NSI,
                        "texte" : None},
    "Clé USB" :
                        {"type_arme": None,
                        "image" : CLE_USB,
                        "texte" : None},
    "Epee enflammée" :
                        {"type_arme": None,
                        "image" : None,
                        "texte" : None},
    "Pistolets" :
                        {"type_arme": None,
                        "image" : None,
                        "texte" : None},
    "Tome 1 de Bersek" :
                        {"type_arme": None,
                        "image" : BERSEK,
                        "texte" : None},
    "Petit nain roux à tenue verte" :
                        {"type_arme": None,
                        "image" : NAIN,
                        "texte" : None},
}

ARMES = {
    # Nerd
    "Nerd" : {
        "Epée bleue" : 
                        {**TYPES_ARMES["Epée bleue"
                        "niveau_req" : 1]},
        "Lunettes cassées" :
                        {**TYPES_ARMES["Lunettes cassées"],
                        "niveau_req": 2},
        "Souris de PC" : 
                        {**TYPES_ARMES["Souris de PC"],
                        "niveau_req": 2},
        "Chaussettes propres" :
                        {**TYPES_ARMES["Chaussettes propres"],
                        "niveau_req": 2},
        "Niveau 2 : Lunettes cassées" :
                        {**TYPES_ARMES["Lunettes cassées"],
                        "niveau_req": 3},
        "Niveau 2 : Souris de PC" : 
                        {**TYPES_ARMES["Souris de PC"],
                        "niveau_req": 3},
        "Niveau 2 : Chaussettes propres" :
                        {**TYPES_ARMES["Chaussettes propres"],
                        "niveau_req": 3},
        "Niveau 3 : Lunettes cassées" :
                        {**TYPES_ARMES["Lunettes cassées"],
                        "niveau_req": 4},
        "Niveau 3 : Souris de PC" : 
                        {**TYPES_ARMES["Souris de PC"],
                        "niveau_req": 4},
        "Cahier de NSI" :
                        {**TYPES_ARMES["Cahier de NSI"],
                        "niveau_req": 4},
        "Niveau 4 : Souris de PC" : 
                        {**TYPES_ARMES["Souris de PC"],
                        "niveau_req": 5},
        "Clé USB" :
                        {**TYPES_ARMES["Clé USB"],
                        "niveau_req": 5},
        "Epee enflammée" :
                        {**TYPES_ARMES["Epee enflammée"],
                        "niveau_req": 5},
        "Tome 1 de Bersek" :
                        {**TYPES_ARMES["Tome 1 de Bersek"],
                        "niveau_req": 5},
        "Niveau 4 : Lunettes cassées" :
                        {**TYPES_ARMES["Lunettes cassées"],
                        "niveau_req": 6},
        "Pistolets" :
                        {**TYPES_ARMES["Pistolets"],
                        "niveau_req": 6},
        "Niveau 3 : Chaussettes propres" :
                        {**TYPES_ARMES["Chaussettes propres"],
                        "niveau_req": 6},
        "Petit nain roux à tenue verte" :
                        {**TYPES_ARMES["Petit nain roux à tenue verte"],
                        "niveau_req": 7,
                        "texte" : None},
        "Niveau 4 : Chaussettes propres" :
                        {**TYPES_ARMES["Chaussettes propres"],
                        "niveau_req": 7},
        
        }
}

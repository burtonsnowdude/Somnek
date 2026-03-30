import csv

"""
Niveau atteint
Argent obtenu
Personnages débloqués (pour le moment pas faisable) 
Armes/ items débloqués
Quêtes réussies (pareil pour le moment pas faisable) 


--> Mettre un système d'identifiant ? Parce que sinon dès qu'on fera une partie ça enregistrera pour tout
le monde donc faudra en permanence supprimer les données créées.
--> Donc créer l'interface plus tôt que prévu
--> Pour l'instant juste stocker les infos mais tout sera affiché plus tard sur l'interface d'accueil

Dans chaque fichier : une colonne par personne
1 fichier par catégorie : persos, armes/items, quêtes, et niveau+argent ensemble
    1 ligne par arme-item/perso/quête
    Si obtenu : 1
    Si pas obtenu : 0
Dans 1 autre fichier : niveau + argent
    1 ligne pour le niveau, 1 ligne pour l'argent
    Avec juste les valeurs pour chacun dedans
"""

######################### Niveau et argent #################################
def det_noms():
    contenu_niveau = csv.DictReader(open("niveau_argent.csv"))
    new_tab = []
    for row in contenu_niveau :
        new_tab.append(row)
    noms = [nom for nom in new_tab[0]]
    return noms, new_tab

def ajouter_utilisateur(nom, noms):
    """Ajouter un nouvel utilisateur"""
    if nom not in noms :
        noms.append(nom)
        return noms
    return False
    
def actualiser_donnees(nom, niveau, argent, new_tab):
    """Actualise les donnees de niveau et l'argent possede par le joueur
    
    Parameters
    ----------
    nom : str
        Le nom du joueur actuel"""
    if new_tab[0][nom] < niveau :
        new_tab[0][nom] = niveau
    new_tab[1][nom] = argent
    return new_tab


def reecrire_fichier_niveau_argent(new_tab, noms):
    """Réécrit le fichier csv avec les données actualisées
    
    Parameters
    ----------
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires"""
    
    with open("niveau_argent.csv", "w", newline = "") as fichier_niveau :
        writer = csv.DictWriter(fichier_niveau, noms)
        writer.writeheader()
        for row in new_tab:
            writer.writerow(row)


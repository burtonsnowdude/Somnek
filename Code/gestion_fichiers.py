import csv
from variables import *

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
######################## Fonctions générales #############################

def det_noms():
    """Récupère les noms des joueurs inscrits"""
    contenu_niveau = csv.DictReader(open("Fichiers_csv/niveau_argent.csv"))
    new_tab = []
    for row in contenu_niveau :
        new_tab.append(row)
    noms = [nom for nom in new_tab[0]]
    return noms, new_tab

def ajouter_utilisateur(nom, noms):
    """Ajouter un nouvel utilisateur
    
    Parameters
    ----------
    nom : str
        Le nom du joueur actuel
    noms : str
        La liste de tous les joueurs inscrits
    
    Returns
    -------
    list
        La liste de joueurs inscrits actualisée
    ou 
    False
    """
    if nom not in noms :
        noms.append(nom)
        return noms
    return False 

######################### Niveau et argent #################################

def actualiser_donnees(nom, niveau, argent, new_tab):
    """Actualise les donnees de niveau et l'argent possede par le joueur
    
    Parameters
    ----------
    nom : str
        Le nom du joueur actuel
    niveau : int
        Le niveau actuel atteint par le joueur
    argent : int
        L'argent récolté par le joueur
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires
    
    Returns
    -------
    list(dict)
        La liste de données qui seront réécrites dans le fichier csv
    """
    if new_tab[0][nom] < niveau :
        new_tab[0][nom] = niveau
    new_tab[1][nom] = argent
    return new_tab


def reecrire_fichier_niveau_argent(new_tab, noms):
    """Réécrit le fichier csv avec les données actualisées
    
    Parameters
    ----------
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires
    noms : list
        La liste des joueurs inscrits
    """

    with open("Fichiers_csv/niveau_argent.csv", "w", newline = "") as fichier_niveau :
        writer = csv.DictWriter(fichier_niveau, noms)
        writer.writeheader()
        for row in new_tab:
            writer.writerow(row)

########################## Armes ###########################

def definir_fichier_nouv_armes(noms):
    """Réinitialise le fichier armes_obtenues_par_joueur.csv, sera utile quand on aura 
    le bon dico pour les ARMES
    
    Parameters
    ----------
    noms : list(str)
        La liste des joueurs inscrits
    """
    headers = ["Type"] + noms
    with open("Fichiers_csv/armes_obtenues_par_joueur.csv", "w", newline = "") as fichier_niveau :
            writer = csv.DictWriter(fichier_niveau, headers)
            writer.writeheader()
            for arme in ARMES:
                row = {}
                row["Type"] = arme
                for nom in noms :
                    row[nom] = 0
                writer.writerow(row)
    


def contenu_fichier_armes():
    """Récupère les données du fichier armes_obtenues_par_joueur.csv"""
    contenu_niveau = csv.DictReader(open("Fichiers_csv/armes_obtenues_par_joueur.csv"))
    
    new_tab = []
    for row in contenu_niveau :
        new_tab.append(row)
    return new_tab

def ajouter_arme(nom, arme, new_tab):
    """Actualise les donnees des armes possedees par le joueur
    
    Parameters
    ----------
    nom : str
        Le nom du joueur actuel
    arme : str
        Le nom de l'arme récupérée
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires
    
    Returns
    -------
    list(dict)
        La liste de données qui seront réécrites dans le fichier csv
    """
    for row in new_tab :
        if row["Type"] == arme:
            if int(row[nom]) == 0:
                row[nom] = 1
            return new_tab
    
def reecrire_fichier_armes(new_tab, noms):
    """Réécrit le fichier csv avec les données actualisées

    Parameters
    ----------
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires
    """
    headers = ["Type"] + noms
    with open("Fichiers_csv/armes_obtenues_par_joueur.csv", "w", newline = "") as fichier_niveau :
            writer = csv.DictWriter(fichier_niveau, headers)
            writer.writeheader()
            for row in new_tab:
                writer.writerow(row)


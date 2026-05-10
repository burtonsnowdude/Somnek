"""
Gestion de fichiers en csv, ce fichier gère les sauvegardes
    du niveau 
    de l'argent
    des armes et items acquises
    des quêtes accomplies
    des powerups achetés
Il possède différentes fonctions non utilisées dans le code mais qui sont utiles pour réinitialiser les fichiers
"""

import csv
from Fichiers_variables.variables import *
from Fichiers_variables.dictionnaire_items import TYPES_ITEMS
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
import Interface.variable_power_up as data


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
    list(dict) 
        La liste de joueurs inscrits actualisée
    list(dict)
        Le contenu actualisé du fichier armes
    list(dict)
        Le contenu actualisé du fichier quêtes
    list(dict)
        Le contenu actualisé du fichier powerups   
    ou 
    False
    """
    if nom not in noms:
        noms.append(nom)

        # on met toutes les données du nouveau joueur à 0
        new_tab_armes = contenu_fichier_armes()
        for ligne in new_tab_armes:
            ligne[nom] = 0

        new_tab_quetes = contenu_fichier_quetes()
        for ligne in new_tab_quetes:
            ligne[nom] = 0

        new_tab_powerups = contenu_fichier_powerups()
        for ligne in new_tab_powerups:
            ligne[nom] = 0

        # débloque fille populaire dès l'inscription
        from Fichiers_variables.progression import init_progression
        try:
            init_progression(nom)
            print(f"[Inscription] '{nom}' inscrit avec Fille_populaire débloquée.")
        except Exception as e:
            import traceback
            print(f"[Inscription] Erreur init_progression : {e}")
            traceback.print_exc()
        

        return noms, new_tab_armes, new_tab_quetes, new_tab_powerups
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
    # seulement si le niveau est meilleur que celui précedemment atteint
    if new_tab[0][nom] < niveau :
        new_tab[0][nom] = niveau
    new_tab[1][nom] = argent
    return new_tab


########################## Armes ###########################

def definir_fichier_nouv_armes(noms):
    """Réinitialise le fichier armes_obtenues_par_joueur.csv, est utile lorsuqu'il y a un changement
    du dictionnaire des armes et items
    
    Parameters
    ----------
    noms : list(str)
        La liste des joueurs inscrits
    """
    headers = ["Type"] + noms
    with open("Fichiers_csv/armes_obtenues_par_joueur.csv", "w", newline = "") as fichier_niveau :
            writer = csv.DictWriter(fichier_niveau, headers)
            writer.writeheader()
            # On parcourt le dico de chaque perso dans les 2 dictionnaires
            for perso in TYPES_ITEMS : 
                for arme in TYPES_ITEMS[perso]:
                    row = {}
                    row["Type"] = arme
                    for nom in noms :
                        row[nom] = 0 # mettre à 0 toutes les données 
                    writer.writerow(row)
            for perso in TYPES_ARMES:
                for arme in TYPES_ARMES[perso]:
                    row = {}
                    row["Type"] = arme
                    for nom in noms :
                        row[nom] = 0 # mettre à 0 toutes les données 
                    writer.writerow(row)

def contenu_fichier_armes():
    """Récupère les données du fichier armes_obtenues_par_joueur.csv
    
    Returns
    --------
    list(dict)
        le contenu du fichier armes
    """
    contenu_niveau = csv.DictReader(open("Fichiers_csv/armes_obtenues_par_joueur.csv"))
    new_tab = []
    for row in contenu_niveau :
        new_tab.append(row)
    return new_tab



def liste_armes_acquises(joueur):
    """Donne la liste des armes acquises par un joueur
    
    Parameters
    ----------
    joueur : str
        Le nom du joueur
    
    Returns
    -------
    list
        La liste des armes acquises par le joueur
    """
    contenu = contenu_fichier_armes()
    liste = [ligne["Type"] for ligne in contenu if ligne[joueur] == "1"]
    return liste

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

def reecrire_fichier(fichier, new_tab, noms):
    """ Permet de réécrire un certain fichier avec des données actualisées
    
    Parameters
    ----------
    fichier : str
        le nom du fichier
    new_tab : list
        Le contenu actualisé du fichier
    noms : list(str)
        La liste de noms de tous les joueurs enregistrés
    """
    if fichier in ("armes_obtenues_par_joueur", "quetes_reussis", "powerups"):
        headers = ["Type"] + noms
    else:
        headers = noms
    fichier = "Fichiers_csv/" + fichier + ".csv"
    with open(fichier, "w", newline="") as tab:
        # extrasaction="ignore", ignore les colonnes en trop 
        writer = csv.DictWriter(tab, headers, extrasaction="ignore")
        writer.writeheader()
        for row in new_tab:
            # Nettoyer les clés parasites (virgule en trop dans le csv)
            for k in list(row.keys()):
                if k is None or k == "":
                    del row[k]
            writer.writerow(row)

def get_info(joueur, info, arme):
    """Permet de déterminer soit l'argent possédé par le joueur soit s'il possède une arme ou non
    
    Parameters
    ----------
    joueur : str
        Le nom du joueur
    info : str
        Le type d'infos souhaité
    arme : str
        L'arme en question
    
    Returns
    -------
    int
        L'argent possédé par le joueur
    ou
    bool
        Si l'arme a été acquise ou non
    """
    if info == "argent" :
        tab = det_noms()[1]
        if joueur not in tab[1]:
            return 0
        return int(tab[1][joueur])
    if info == "arme":
        tab = contenu_fichier_armes()
        for row in tab :
            if row["Type"] == arme :
                if joueur not in row:
                    return False
                if row[joueur] == 1 :
                    return True
                else : 
                    return False
                
def replace_player_money(joueur, argent):
    """Actualise l'argent du joueur
    
    Parameters
    ----------
    joueur : str
        Le nom du joueur
    argent : int
        L'argent actualisé du joueur
    """
    noms, new_tab = det_noms()
    new_tab[1][joueur] = argent
    reecrire_fichier("niveau_argent", new_tab, noms)

def joueur_qui_a_tout(noms):
    """Ajouter un utilisateur nommé test qui a absolument toutes les armes/items (pour tester)
    
    Parameters
    ----------
    noms : str
        La liste de tous les joueurs inscrits
    """
    nom = "test"
    noms.append(nom)
    new_tab_armes = contenu_fichier_armes()
    for ligne in new_tab_armes:
        ligne[nom] = 1
    reecrire_fichier("armes_obtenues_par_joueur", new_tab_armes, noms)
    
    
########################### Quêtes ###########################

def contenu_fichier_quetes():
    """Récupère les données du fichier quetes_reussis.csv"""
    contenu = csv.DictReader(open("Fichiers_csv/quetes_reussis.csv"))
    return [row for row in contenu]

def actualiser_quete(nom, quete):
    """Marque une quête comme réussie pour un joueur et sauvegarde

    Parameters
    ----------
    nom : str
        Le nom du joueur
    quete : str
        L'identifiant de la quête (ex: 'Entrer_metro')
    """
    noms, _ = det_noms()
    new_tab = contenu_fichier_quetes()
    for row in new_tab:
        if row["Type"] == quete:
            row[nom] = 1
    reecrire_fichier("quetes_reussis", new_tab, noms)

############################ Power ups ###########################

def contenu_fichier_powerups():
    """Récupère les données du fichier powerups.csv"""
    contenu = csv.DictReader(open("Fichiers_csv/powerups.csv"))
    return [row for row in contenu]


def definir_fichier_powerups(noms):
    """Réinitialise le fichier powerups
    
    Parameters
    ----------
    noms : list
        La liste des noms des joueurs enregistrés
    """
    headers = ["Type"] + noms
    with open("Fichiers_csv/powerups.csv", "w", newline="") as fichier:
        writer = csv.DictWriter(fichier, headers)
        writer.writeheader()
        for powerup in data.playerInventory:
            row = {}
            row["Type"] = powerup
            for nom in noms:
                row[nom] = 0
            writer.writerow(row)

def sauvegarder_powerup(nom, powerup, niveau):
    """Sauvegarde le niveau d'un power up pour un joueur
    
    Parameters
    ----------
    nom : str
        Nom du joueur
    powerup : str
        Nom du powerup acheté
    niveau :
        Niveau du powerup acheté
    """

    noms, _ = det_noms()
    new_tab = contenu_fichier_powerups()

    for row in new_tab:
        if row["Type"] == powerup:
            row[nom] = niveau

    reecrire_fichier("powerups", new_tab, noms)


def charger_powerups_joueur(nom):
    """Charge les powerups d'un joueur

    Parameters
    ----------
    nom : str
        Nom du joueur
    
    Returns
    --------
    dict
        Le dictionnaire des powerups du joueur
    """

    contenu = contenu_fichier_powerups()

    powerups = {}

    for row in contenu:
        if nom in row:
            powerups[row["Type"]] = int(row[nom])

    return powerups

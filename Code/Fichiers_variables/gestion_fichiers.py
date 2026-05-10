import csv
from Fichiers_variables.variables import *
from Fichiers_variables.dictionnaire_items import TYPES_ITEMS
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
import Interface.variable_power_up as data
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
        new_tab_armes = contenu_fichier_armes()
        for ligne in new_tab_armes:
            ligne[nom] = 0
        new_tab_quetes = contenu_fichier_quetes()
        for ligne in new_tab_quetes:
            ligne[nom] = 0
        new_tab_powerups = contenu_fichier_powerups()
        for ligne in new_tab_powerups:
                ligne[nom] = 0
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
    if new_tab[0][nom] < niveau :
        new_tab[0][nom] = niveau
    new_tab[1][nom] = argent
    return new_tab


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
            for perso in TYPES_ITEMS : 
                for arme in TYPES_ITEMS[perso]:
                    row = {}
                    row["Type"] = arme
                    for nom in noms :
                        row[nom] = 0
                    writer.writerow(row)
            for perso in TYPES_ARMES:
                for arme in TYPES_ARMES[perso]:
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



def liste_armes_acquises(joueur):
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
    """Réécrit le fichier csv avec les données actualisées

    Parameters
    ----------
    new_tab : list(dict)
        La liste actualisée contenant les lignes de données sous forme de dictionnaires
    """
    if fichier in ("armes_obtenues_par_joueur", "quetes_reussis", "powerups") :
        headers = ["Type"] + noms
    else :
        headers = noms
    fichier = "Fichiers_csv/"+fichier+".csv"
    with open(fichier, "w", newline = "") as tab :
            writer = csv.DictWriter(tab, headers)
            writer.writeheader()
            for row in new_tab:
                writer.writerow(row)

def get_info(joueur, info, arme):
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
    noms, new_tab = det_noms()
    new_tab[1][joueur] = argent
    reecrire_fichier("niveau_argent", new_tab, noms)

def joueur_qui_a_tout(noms):
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
    """Sauvegarde le niveau d'un power up pour un joueur"""

    noms, _ = det_noms()
    new_tab = contenu_fichier_powerups()

    for row in new_tab:
        if row["Type"] == powerup:
            row[nom] = niveau

    reecrire_fichier("powerups", new_tab, noms)


def charger_powerups_joueur(nom):
    """Charge les power ups d'un joueur"""

    contenu = contenu_fichier_powerups()

    powerups = {}

    for row in contenu:
        if nom in row:
            powerups[row["Type"]] = int(row[nom])

    return powerups

import csv
from Fichiers_variables.variables import *
from Fichiers_variables.dictionnaire_items import TYPES_ITEMS
from Fichiers_variables.dictionnaire_armes import GESTION_DES_NIVEAUX_ARMES, TYPES_ARMES

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
    if nom not in noms :
        noms.append(nom)
        new_tab_armes = contenu_fichier_armes()
        for ligne in new_tab_armes:
            ligne[nom] = 0
        new_tab_quetes = contenu_fichier_quetes()
        for ligne in new_tab_quetes:
            ligne[nom] = 0
        return noms, new_tab_armes, new_tab_quetes
    return False

######################### Niveau et argent #################################

def actualiser_donnees(nom, niveau, argent, new_tab):
    if new_tab[0][nom] < niveau :
        new_tab[0][nom] = niveau
    new_tab[1][nom] = argent
    return new_tab

########################## Armes / Items ###################################

def definir_fichier_nouv_armes(noms):
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
    """Marque une arme/item comme acquis dans le tableau en mémoire."""
    for row in new_tab :
        if row["Type"] == arme:
            if int(row[nom]) == 0:
                row[nom] = 1
    return new_tab

def ajouter_arme_acquise(joueur_nom: str, nom_item: str):
    """
    Marque un item/arme comme acquis pour un joueur et sauvegarde immédiatement.
    """
    noms, _ = det_noms()
    new_tab  = contenu_fichier_armes()
    new_tab  = ajouter_arme(joueur_nom, nom_item, new_tab)
    reecrire_fichier("armes_obtenues_par_joueur", new_tab, noms)

def reecrire_fichier(fichier, new_tab, noms):
    if fichier in ("armes_obtenues_par_joueur", "quetes_reussis") :
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
    nom = "test"
    noms.append(nom)
    new_tab_armes = contenu_fichier_armes()
    for ligne in new_tab_armes:
        ligne[nom] = 1
    reecrire_fichier("armes_obtenues_par_joueur", new_tab_armes, noms)

########################### Quêtes ##########################################

def contenu_fichier_quetes():
    """Récupère les données du fichier quetes_reussis.csv"""
    contenu = csv.DictReader(open("Fichiers_csv/quetes_reussis.csv"))
    return [row for row in contenu]


def actualiser_quete(nom, quete):
    """
    Marque une quête comme réussie pour un joueur et sauvegarde immédiatement.
    Si la quête n'existe pas encore dans le CSV, ajoute la ligne automatiquement.
    """
    noms, _ = det_noms()
    new_tab = contenu_fichier_quetes()

    # Cherche la ligne de la quête
    trouve = False
    for row in new_tab:
        if row.get("Type") == quete:
            row[nom] = 1
            trouve = True
            break

    # Crée la ligne si elle n'existe pas
    if not trouve:
        nouvelle_ligne = {"Type": quete}
        for n in noms:
            nouvelle_ligne[n] = 1 if n == nom else 0
        new_tab.append(nouvelle_ligne)

    reecrire_fichier("quetes_reussis", new_tab, noms)

"""
Système de progression — SOMNEK
Gère le déblocage progressif des maps et des personnages.

Règles :
  - Au tout premier lancement : Cour + Fille_populaire débloqués
  - Survivre à une map jusqu'à TEMPS_LIMITE_MAP débloque la map suivante
    ET le personnage suivant (s'il en reste un à débloquer).
  - Ordre des maps   : Cour → Rue → Ruelle → Foire → Metro
  - Ordre des persos : Fille_populaire → Nerd → Nonne
"""

import csv
import os


ORDRE_MAPS   = ["Cour", "Rue", "Ruelle", "Foire", "Metro"]
ORDRE_PERSOS = ["Fille_populaire", "Nerd", "Nonne"]

MAPS_FINALES = {
    "Fille_populaire": "Villa",
    "Nerd":            "immeuble",
    "Nonne":           "Eglise",
}

# temps en secondes pour valider une map comme terminée
TEMPS_LIMITE_MAP = {
    "Cour":     8  * 60,
    "Rue":      12 * 60,
    "Ruelle":   9 * 60,
    "Foire":    15* 60,
    "Metro":    12 * 60,
    "Villa":    17* 60,
    "immeuble": 17* 60,
    "Eglise":   17 * 60,
}

CHEMIN_MAPS   = "Fichiers_csv/maps_debloquees.csv"
CHEMIN_PERSOS = "Fichiers_csv/persos_debloques.csv"


def _lire_csv(chemin):
    """Lit un fichier CSV de progression et retourne les lignes et les headers.

    Parameters
    ----------
    chemin : str
        Chemin vers le fichier CSV

    Returns
    -------
    tuple : (rows, headers)
        rows : liste de dicts, une ligne par élément
        headers : liste des noms de colonnes (sans les clés vides/parasites)
    """
    if not os.path.exists(chemin):
        return [], []
    with open(chemin, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        # fieldnames peut être None si le fichier est vide
        headers = list(reader.fieldnames) if reader.fieldnames else ["Type"]

    # enleve les clés parasites genre None ou "" qui aparaissent avec des virgules en trop
    clean_headers = [h for h in headers if h and h.strip()]
    for row in rows:
        for k in list(row.keys()):
            if k is None or k == "" or not k.strip():
                del row[k]
    return rows, clean_headers


def _ecrire_csv_avec_headers(chemin, rows, headers):
    """Réécrit entièrement un CSV avec les headers et lignes fournis.

    Parameters
    ----------
    chemin : str
        Chemin du fichier à écrire
    rows : list
        Liste de dicts représentant chaque ligne
    headers : list
        Ordre exact des colonnes à écrire
    """
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", newline="") as f:
        writer = csv.DictWriter(f, headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # rempli les cases manquantes avec 0 pour pas avoir de trous
            for h in headers:
                if h not in row:
                    row[h] = "0"
            writer.writerow(row)


def init_progression(joueur, noms=None):
    """Inscrit un joueur dans les deux CSV de progression.

    Appelé à la création du profil. Débloque Cour et Fille_populaire par défaut.

    Parameters
    ----------
    joueur : str
        Nom du joueur à initialiser
    noms : list, optional
        Pas utilisé, gardé pour compatibilité
    """
    _init_fichier(CHEMIN_PERSOS, ORDRE_PERSOS, ORDRE_PERSOS[0], joueur)
    _init_fichier(CHEMIN_MAPS,   ORDRE_MAPS,   ORDRE_MAPS[0],   joueur)


def _init_fichier(chemin, ordre_canonique, element_de_depart, joueur):
    """Ajoute un joueur dans un CSV de progression, ou le crée si inexistant.

    Si le joueur est déjà là, vérifie juste qu'il a bien son élément de départ.
    Si le fichier n'existe pas, le crée avec toutes les lignes à 0 sauf l'élément de départ.

    Parameters
    ----------
    chemin : str
        Chemin du CSV (maps ou persos)
    ordre_canonique : list
        Liste ordonnée de tous les éléments possibles
    element_de_depart : str
        Celui qui est débloqué par défaut (Cour ou Fille_populaire)
    joueur : str
        Nom du joueur
    """
    if not os.path.exists(chemin):
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "w", newline="") as f:
            writer = csv.DictWriter(f, ["Type", joueur])
            writer.writeheader()
            for elt in ordre_canonique:
                writer.writerow({"Type": elt, joueur: "1" if elt == element_de_depart else "0"})
        print(f"[Progression] {chemin} créé, '{joueur}' initialisé avec {element_de_depart}.")
        return

    rows, headers = _lire_csv(chemin)

    # joueur déjà dans le fichier, on vérifie juste qu'il a son point de départ
    if joueur in headers:
        modifie = False
        for row in rows:
            if row.get("Type") == element_de_depart and row.get(joueur, "0") in ("0", "", None):
                row[joueur] = "1"
                modifie = True
        if modifie:
            _ecrire_csv_avec_headers(chemin, rows, headers)
        return

    # nouveau joueur, on rajoute sa colonne
    headers.append(joueur)
    for row in rows:
        row[joueur] = "1" if row.get("Type") == element_de_depart else "0"

    _ecrire_csv_avec_headers(chemin, rows, headers)
    print(f"[Progression] nouveau joueur '{joueur}' ajouté avec {element_de_depart} débloqué(e).")


def maps_debloquees(joueur):
    """Retourne la liste des maps débloquées pour ce joueur.

    Si le joueur n'a rien (fichier absent, colonne absente, tout à 0),
    on lui remet Cour par défaut pour pas bloquer.

    Parameters
    ----------
    joueur : str
        Nom du joueur

    Returns
    -------
    list
        Maps débloquées dans l'ordre canonique (maps principales + maps finales)
    """
    map_depart = ORDRE_MAPS[0]

    # fichier pas encore créé, on le crée maintenant
    if not os.path.exists(CHEMIN_MAPS):
        os.makedirs(os.path.dirname(CHEMIN_MAPS), exist_ok=True)
        with open(CHEMIN_MAPS, "w", newline="") as f:
            writer = csv.DictWriter(f, ["Type", joueur])
            writer.writeheader()
            for m in ORDRE_MAPS:
                writer.writerow({"Type": m, joueur: "1" if m == map_depart else "0"})
        return [map_depart]

    rows, headers = _lire_csv(CHEMIN_MAPS)

    # joueur pas encore dans le csv, on l'ajoute direct
    if joueur not in headers:
        headers.append(joueur)
        for row in rows:
            row[joueur] = "1" if row.get("Type") == map_depart else "0"
        _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
        return [map_depart]

    debloquees = {row["Type"] for row in rows if str(row.get(joueur, "0")).strip() == "1"}

    # sécurité : si vraiment rien de débloqué on remet cour
    if not debloquees:
        for row in rows:
            if row.get("Type") == map_depart:
                row[joueur] = "1"
        _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
        return [map_depart]

    # maps principales d'abord, maps finales ensuite
    toutes = ORDRE_MAPS + list(MAPS_FINALES.values())
    return [m for m in toutes if m in debloquees]


def persos_debloques(joueur):
    """Retourne la liste des persos débloqués pour ce joueur.

    Même logique que maps_debloquees — fallback sur Fille_populaire si rien.

    Parameters
    ----------
    joueur : str
        Nom du joueur

    Returns
    -------
    list
        Persos débloqués dans l'ordre canonique
    """
    perso_depart = ORDRE_PERSOS[0]

    if not os.path.exists(CHEMIN_PERSOS):
        os.makedirs(os.path.dirname(CHEMIN_PERSOS), exist_ok=True)
        with open(CHEMIN_PERSOS, "w", newline="") as f:
            writer = csv.DictWriter(f, ["Type", joueur])
            writer.writeheader()
            for p in ORDRE_PERSOS:
                writer.writerow({"Type": p, joueur: "1" if p == perso_depart else "0"})
        return [perso_depart]

    rows, headers = _lire_csv(CHEMIN_PERSOS)

    if joueur not in headers:
        headers.append(joueur)
        for row in rows:
            row[joueur] = "1" if row.get("Type") == perso_depart else "0"
        _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
        return [perso_depart]

    debloques = {row["Type"] for row in rows if str(row.get(joueur, "0")).strip() == "1"}

    # pareil, fallback si le csv est vide pour ce joueur
    if not debloques:
        for row in rows:
            if row.get("Type") == perso_depart:
                row[joueur] = "1"
        _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
        return [perso_depart]

    return [p for p in ORDRE_PERSOS if p in debloques]


def map_est_debloquee(joueur, nom_map):
    """Vérifie si une map spécifique est débloquée pour ce joueur.

    Parameters
    ----------
    joueur : str
        Nom du joueur
    nom_map : str
        Nom de la map à vérifier

    Returns
    -------
    bool
    """
    return nom_map in maps_debloquees(joueur)


def perso_est_debloque(joueur, nom_perso):
    """Vérifie si un perso spécifique est débloqué pour ce joueur.

    Parameters
    ----------
    joueur : str
        Nom du joueur
    nom_perso : str
        Nom du perso à vérifier

    Returns
    -------
    bool
    """
    return nom_perso in persos_debloques(joueur)


def map_terminee(joueur, nom_map, noms, perso=None, player=None):
    """Appelée à la victoire d'une map — débloque la map suivante et le perso suivant.

    Logique de déblocage :
      - La map suivante dans l'ordre (maps principales puis map finale du perso) est débloquée.
      - Le perso suivant non débloqué est débloqué, mais seulement sur les maps principales.
      - L'item spécial est donné uniquement à la fin de Metro.

    Parameters
    ----------
    joueur : str
        Nom du joueur
    nom_map : str
        Map que le joueur vient de terminer
    noms : list
        Pas utilisé, gardé pour compatibilité
    perso : str, optional
        Perso actif — sert pour l'item spécial et pour savoir quelle map finale débloquer
    player : Player, optional
        Instance du joueur — nécessaire pour ajouter l'item dans l'inventaire

    Returns
    -------
    tuple : (nouvelle_map, nouveau_perso, nouvel_item)
        Chaque valeur est None si rien de nouveau n'a été débloqué
    """
    nouvelle_map  = None
    nouveau_perso = None
    nouvel_item   = None

    # item spécial donné une seule fois à la fin de metro
    if nom_map == "Metro" and perso is not None and player is not None:
        items_perso = {
            "Nonne":           "Voile",
            "Nerd":            "Armure_chevalier",
            "Fille_populaire": "Ensemble_juicy",
        }
        nouvel_item = items_perso.get(perso)
        if nouvel_item:
            player.ajouter_item(nouvel_item)

    # ordre des maps pour ce perso : les 5 principales + la map finale si elle existe
    ordre_complet = list(ORDRE_MAPS)
    if perso and perso in MAPS_FINALES:
        ordre_complet.append(MAPS_FINALES[perso])

    # on cherche la map suivante et on la débloque
    if nom_map in ordre_complet:
        idx = ordre_complet.index(nom_map)
        if idx + 1 < len(ordre_complet):
            map_suivante = ordre_complet[idx + 1]

            rows, headers = _lire_csv(CHEMIN_MAPS)

            if joueur not in headers:
                headers.append(joueur)
                for row in rows:
                    row[joueur] = "0"

            # la map finale n'est pas dans le csv de base, on l'ajoute si besoin
            if not any(r.get("Type") == map_suivante for r in rows):
                new_row = {"Type": map_suivante}
                for h in headers[1:]:
                    new_row[h] = "0"
                rows.append(new_row)

            for row in rows:
                if row.get("Type") == map_suivante and str(row.get(joueur, "0")).strip() == "0":
                    row[joueur] = "1"
                    nouvelle_map = map_suivante
                    break

            _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
            print(f"[Progression] map débloquée : {nouvelle_map} pour '{joueur}'")
        else:
            # fini toutes les maps dispo pour ce perso
            print(f"[Progression] '{joueur}' a tout terminé avec {perso}, rien de plus à débloquer.")

    # le perso se débloque seulement sur les maps principales, pas sur les maps finales
    if nom_map in ORDRE_MAPS:
        rows, headers = _lire_csv(CHEMIN_PERSOS)

        if joueur not in headers:
            headers.append(joueur)
            for row in rows:
                row[joueur] = "0"

        # on cherche le premier perso pas encore débloqué
        for nom_perso_canonique in ORDRE_PERSOS:
            for row in rows:
                if row.get("Type") == nom_perso_canonique and str(row.get(joueur, "0")).strip() == "0":
                    row[joueur]   = "1"
                    nouveau_perso = nom_perso_canonique
                    break
            if nouveau_perso:
                break

        _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
        if nouveau_perso:
            print(f"[Progression] perso débloqué : {nouveau_perso} pour '{joueur}'")

    return nouvelle_map, nouveau_perso, nouvel_item


def temps_limite(nom_map):
    """Retourne le temps en secondes nécessaire pour valider une map.

    Parameters
    ----------
    nom_map : str
        Nom de la map

    Returns
    -------
    int
        Temps en secondes (défaut 5 min si la map est inconnue)
    """
    return TEMPS_LIMITE_MAP.get(nom_map, 5 * 60)
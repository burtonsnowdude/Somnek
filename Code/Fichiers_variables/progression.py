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
from Jeu.player import Player as p



ORDRE_MAPS   = ["Cour", "Rue", "Ruelle", "Foire", "Metro"]
ORDRE_PERSOS = ["Fille_populaire", "Nerd", "Nonne"]

# Temps en secondes pour considérer la map comme terminée
TEMPS_LIMITE_MAP = {
    "Cour":    5 * 60,    # 5 min
    "Rue":     7 * 60,    # 7 min
    "Ruelle":  9 * 60,    # 9 min
    "Foire":  11 * 60,    # 11 min
    "Metro":  13 * 60,    # 13 min
}

CHEMIN_MAPS   = "Fichiers_csv/maps_debloquees.csv"
CHEMIN_PERSOS = "Fichiers_csv/persos_debloques.csv"


# ─────────────────────────────────────────────
#  HELPERS CSV (privés)
# ─────────────────────────────────────────────

def _lire_csv(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, "r", newline="") as f:
        return list(csv.DictReader(f))


def _ecrire_csv(chemin, rows, noms):
    headers = ["Type"] + noms
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", newline="") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in rows:
            for n in noms:
                if n not in row:
                    row[n] = 0
            writer.writerow(row)


def _creer_fichier_si_manque(chemin, types_initiaux, noms):
    """Si le fichier n'existe pas, le crée avec une ligne par type et 0 partout."""
    if os.path.exists(chemin):
        return
    rows = []
    for t in types_initiaux:
        row = {"Type": t}
        for n in noms:
            row[n] = 0
        rows.append(row)
    _ecrire_csv(chemin, rows, noms)


def _ajouter_colonne_joueur_si_manque(chemin, joueur, noms):
    """Ajoute la colonne du joueur (à 0) si elle n'existe pas."""
    if not os.path.exists(chemin):
        return
    data = _lire_csv(chemin)
    if data and joueur not in data[0]:
        for row in data:
            row[joueur] = 0
        _ecrire_csv(chemin, data, noms)


# ─────────────────────────────────────────────
#  API PUBLIQUE
# ─────────────────────────────────────────────

def init_progression(joueur, noms):
    """
    À appeler au démarrage avant tout. Si le joueur est nouveau,
    Cour et Fille_populaire sont débloqués.
    """
    _creer_fichier_si_manque(CHEMIN_MAPS,   ORDRE_MAPS,   noms)
    _creer_fichier_si_manque(CHEMIN_PERSOS, ORDRE_PERSOS, noms)

    _ajouter_colonne_joueur_si_manque(CHEMIN_MAPS,   joueur, noms)
    _ajouter_colonne_joueur_si_manque(CHEMIN_PERSOS, joueur, noms)

    # Maps : Cour débloquée par défaut
    maps_data = _lire_csv(CHEMIN_MAPS)
    a_au_moins_une_map = any(str(row.get(joueur, "0")) == "1" for row in maps_data)
    if not a_au_moins_une_map:
        for row in maps_data:
            if row["Type"] == "Cour":
                row[joueur] = 1
        _ecrire_csv(CHEMIN_MAPS, maps_data, noms)

    # Persos : Fille_populaire débloquée par défaut
    persos_data = _lire_csv(CHEMIN_PERSOS)
    a_au_moins_un_perso = any(str(row.get(joueur, "0")) == "1" for row in persos_data)
    if not a_au_moins_un_perso:
        for row in persos_data:
            if row["Type"] == "Fille_populaire":
                row[joueur] = 1
        _ecrire_csv(CHEMIN_PERSOS, persos_data, noms)


def maps_debloquees(joueur):
    """Liste des maps débloquées pour ce joueur, dans l'ordre canonique."""
    data = _lire_csv(CHEMIN_MAPS)
    debloquees = {row["Type"] for row in data if str(row.get(joueur, "0")) == "1"}
    return [m for m in ORDRE_MAPS if m in debloquees]


def persos_debloques(joueur):
    """Liste des persos débloqués pour ce joueur, dans l'ordre canonique."""
    data = _lire_csv(CHEMIN_PERSOS)
    debloques = {row["Type"] for row in data if str(row.get(joueur, "0")) == "1"}
    return [p for p in ORDRE_PERSOS if p in debloques]


def map_est_debloquee(joueur, nom_map):
    return nom_map in maps_debloquees(joueur)


def perso_est_debloque(joueur, nom_perso):
    return nom_perso in persos_debloques(joueur)


def map_terminee(joueur, nom_map, noms, perso=None, player=None):
    """
    Appelée à la victoire d'une map.
    Débloque la map suivante + le perso suivant non encore débloqué.

    Retourne (nouvelle_map, nouveau_perso) — chacun peut être None si plus rien
    à débloquer dans sa catégorie.
    """
    nouvelle_map  = None
    nouveau_perso = None
    nouvel_item   = None

    #debloque item
    if nom_map == "Metro" and perso is not None and player is not None:
        if perso == "Nonne":
            nouvel_item = "Voile"
        elif perso == "Nerd":
            nouvel_item = "Armure_chevalier"
        elif perso == "Fille_populaire":
            nouvel_item = "Ensemble_juicy"
        if nouvel_item:
            player.ajouter_item(nouvel_item)

    # ─── Map suivante ────────────────────────────────────────────────────
    if nom_map in ORDRE_MAPS:
        idx = ORDRE_MAPS.index(nom_map)
        if idx + 1 < len(ORDRE_MAPS):
            map_suivante = ORDRE_MAPS[idx + 1]
            maps_data    = _lire_csv(CHEMIN_MAPS)
            for row in maps_data:
                if row["Type"] == map_suivante and str(row.get(joueur, "0")) == "0":
                    row[joueur]  = 1
                    nouvelle_map = map_suivante
                    break
            _ecrire_csv(CHEMIN_MAPS, maps_data, noms)

    # ─── Perso suivant ───────────────────────────────────────────────────
    persos_data = _lire_csv(CHEMIN_PERSOS)
    for nom_perso_canonique in ORDRE_PERSOS:
        for row in persos_data:
            if row["Type"] == nom_perso_canonique and str(row.get(joueur, "0")) == "0":
                row[joueur]   = 1
                nouveau_perso = nom_perso_canonique
                break
        if nouveau_perso:
            break
    _ecrire_csv(CHEMIN_PERSOS, persos_data, noms)

    return nouvelle_map, nouveau_perso, nouvel_item


def temps_limite(nom_map):
    """Temps (secondes) pour considérer la map comme victorieuse."""
    return TEMPS_LIMITE_MAP.get(nom_map, 5 * 60)
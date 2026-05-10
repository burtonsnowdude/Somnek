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

# Temps en secondes pour considérer la map comme terminée
TEMPS_LIMITE_MAP = {
    "Cour":          5 * 60,
    "Rue":           7 * 60,
    "Ruelle":        9 * 60,
    "Foire":        11 * 60,
    "Metro":        13 * 60,
    "Villa":    15 * 60,
    "immeuble": 15 * 60,
    "Eglise":   15 * 60,
}

CHEMIN_MAPS   = "Fichiers_csv/maps_debloquees.csv"
CHEMIN_PERSOS = "Fichiers_csv/persos_debloques.csv"


# ─────────────────────────────────────────────
#  HELPERS CSV (privés)
# ─────────────────────────────────────────────

def _lire_csv(chemin):
    if not os.path.exists(chemin):
        return [], []
    with open(chemin, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = list(reader.fieldnames) if reader.fieldnames else ["Type"]
    # Nettoie les clés parasites (None, "") dues aux virgules en trop
    clean_headers = [h for h in headers if h and h.strip()]
    for row in rows:
        for k in list(row.keys()):
            if k is None or k == "" or not k.strip():
                del row[k]
    return rows, clean_headers


def _ecrire_csv_avec_headers(chemin, rows, headers):
    """Réécrit un CSV avec les headers exacts fournis."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", newline="") as f:
        writer = csv.DictWriter(f, headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # S'assure que toutes les colonnes existent
            for h in headers:
                if h not in row:
                    row[h] = "0"
            writer.writerow(row)


def init_progression(joueur, noms=None):
    """Inscrit le joueur dans persos_debloques.csv ET maps_debloquees.csv,
    avec Fille_populaire et Cour débloquées par défaut."""
    _init_fichier(CHEMIN_PERSOS, ORDRE_PERSOS, ORDRE_PERSOS[0], joueur)
    _init_fichier(CHEMIN_MAPS,   ORDRE_MAPS,   ORDRE_MAPS[0],   joueur)


def _init_fichier(chemin, ordre_canonique, element_de_depart, joueur):
    """Ajoute le joueur dans un fichier CSV de progression avec
    `element_de_depart` débloqué par défaut."""

    # Le fichier n'existe pas → on le crée
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

    # Joueur déjà présent → on s'assure qu'il a au moins l'élément de départ
    if joueur in headers:
        modifie = False
        for row in rows:
            if row.get("Type") == element_de_depart and row.get(joueur, "0") in ("0", "", None):
                row[joueur] = "1"
                modifie = True
        if modifie:
            _ecrire_csv_avec_headers(chemin, rows, headers)
            print(f"[Progression] '{joueur}' avait perdu {element_de_depart}, restauré.")
        return

    # Nouveau joueur → on ajoute la colonne
    headers.append(joueur)
    for row in rows:
        row[joueur] = "1" if row.get("Type") == element_de_depart else "0"

    _ecrire_csv_avec_headers(chemin, rows, headers)
    print(f"[Progression] Nouveau joueur '{joueur}' ajouté avec {element_de_depart} débloqué(e).")


def maps_debloquees(joueur):
    """Liste des maps débloquées pour ce joueur, dans l'ordre canonique."""
    map_depart = ORDRE_MAPS[0]

    if not os.path.exists(CHEMIN_MAPS):
        os.makedirs(os.path.dirname(CHEMIN_MAPS), exist_ok=True)
        with open(CHEMIN_MAPS, "w", newline="") as f:
            writer = csv.DictWriter(f, ["Type", joueur])
            writer.writeheader()
            for m in ORDRE_MAPS:
                writer.writerow({"Type": m, joueur: "1" if m == map_depart else "0"})
        print(f"[Auto-progression] maps_debloquees.csv créé pour '{joueur}'.")
        return [map_depart]

    rows, headers = _lire_csv(CHEMIN_MAPS)

    # Joueur absent → on l'ajoute
    if joueur not in headers:
        headers.append(joueur)
        for row in rows:
            row[joueur] = "1" if row.get("Type") == map_depart else "0"
        _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
        print(f"[Auto-progression] '{joueur}' ajouté dans maps avec {map_depart} débloquée.")
        return [map_depart]

    debloquees = {row["Type"] for row in rows if str(row.get(joueur, "0")).strip() == "1"}
    if not debloquees:
        for row in rows:
            if row.get("Type") == map_depart:
                row[joueur] = "1"
        _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
        print(f"[Auto-progression] '{joueur}' n'avait aucune map, {map_depart} restaurée.")
        return [map_depart]

    toutes = ORDRE_MAPS + list(MAPS_FINALES.values())
    return [m for m in toutes if m in debloquees]


def persos_debloques(joueur):
    """Liste des persos débloqués pour ce joueur, dans l'ordre canonique."""
    perso_depart = ORDRE_PERSOS[0]

    if not os.path.exists(CHEMIN_PERSOS):
        os.makedirs(os.path.dirname(CHEMIN_PERSOS), exist_ok=True)
        with open(CHEMIN_PERSOS, "w", newline="") as f:
            writer = csv.DictWriter(f, ["Type", joueur])
            writer.writeheader()
            for p in ORDRE_PERSOS:
                writer.writerow({"Type": p, joueur: "1" if p == perso_depart else "0"})
        print(f"[Auto-progression] Fichier créé pour '{joueur}'.")
        return [perso_depart]

    rows, headers = _lire_csv(CHEMIN_PERSOS)

    if joueur not in headers:
        headers.append(joueur)
        for row in rows:
            row[joueur] = "1" if row.get("Type") == perso_depart else "0"
        _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
        print(f"[Auto-progression] '{joueur}' ajouté avec {perso_depart} débloquée.")
        return [perso_depart]

    debloques = {row["Type"] for row in rows if str(row.get(joueur, "0")).strip() == "1"}
    if not debloques:
        for row in rows:
            if row.get("Type") == perso_depart:
                row[joueur] = "1"
        _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
        print(f"[Auto-progression] '{joueur}' n'avait rien, {perso_depart} restaurée.")
        return [perso_depart]

    return [p for p in ORDRE_PERSOS if p in debloques]


def map_est_debloquee(joueur, nom_map):
    return nom_map in maps_debloquees(joueur)


def perso_est_debloque(joueur, nom_perso):
    return nom_perso in persos_debloques(joueur)


def map_terminee(joueur, nom_map, noms, perso=None, player=None):
    """
    Appelée à la victoire d'une map.
    Débloque la map suivante + le perso suivant non encore débloqué.

    Retourne (nouvelle_map, nouveau_perso, nouvel_item).
    """
    nouvelle_map  = None
    nouveau_perso = None
    nouvel_item   = None

    # Débloque item spécial (Metro uniquement)
    if nom_map == "Metro" and perso is not None and player is not None:
        if perso == "Nonne":
            nouvel_item = "Voile"
        elif perso == "Nerd":
            nouvel_item = "Armure_chevalier"
        elif perso == "Fille_populaire":
            nouvel_item = "Ensemble_juicy"
        if nouvel_item:
            player.ajouter_item(nouvel_item)

    # ── Débloque la map suivante ──────────────────────────────────────────
    if nom_map in ORDRE_MAPS:
        idx = ORDRE_MAPS.index(nom_map)
        if idx + 1 < len(ORDRE_MAPS):
            map_suivante = ORDRE_MAPS[idx + 1]
            rows, headers = _lire_csv(CHEMIN_MAPS)

            # Ajoute la colonne joueur si elle manque
            if joueur not in headers:
                headers.append(joueur)
                for row in rows:
                    row[joueur] = "0"

            for row in rows:
                if row.get("Type") == map_suivante and str(row.get(joueur, "0")).strip() == "0":
                    row[joueur]  = "1"
                    nouvelle_map = map_suivante
                    break

            # ✅ FIX : on utilise les vrais headers du fichier, pas `noms`
            _ecrire_csv_avec_headers(CHEMIN_MAPS, rows, headers)
            print(f"[Progression] Map débloquée : {nouvelle_map} pour '{joueur}'")

    # ── Débloque le perso suivant ─────────────────────────────────────────
    rows, headers = _lire_csv(CHEMIN_PERSOS)

    if joueur not in headers:
        headers.append(joueur)
        for row in rows:
            row[joueur] = "0"

    for nom_perso_canonique in ORDRE_PERSOS:
        for row in rows:
            if row.get("Type") == nom_perso_canonique and str(row.get(joueur, "0")).strip() == "0":
                row[joueur]   = "1"
                nouveau_perso = nom_perso_canonique
                break
        if nouveau_perso:
            break

    # ✅ FIX : on utilise les vrais headers du fichier, pas `noms`
    _ecrire_csv_avec_headers(CHEMIN_PERSOS, rows, headers)
    print(f"[Progression] Perso débloqué : {nouveau_perso} pour '{joueur}'")

    return nouvelle_map, nouveau_perso, nouvel_item


def temps_limite(nom_map):
    """Temps (secondes) pour considérer la map comme victorieuse."""
    return TEMPS_LIMITE_MAP.get(nom_map, 5 * 60)
"""
Script one-shot : débloque Fille_populaire pour tous les joueurs déjà inscrits.
À lancer une seule fois si le fichier existe déjà.
"""

import csv
import os

# chemin du fichier des persos
CHEMIN = "Fichiers_csv/persos_debloques.csv"
PERSO_DEPART = "Fille_populaire"

if not os.path.exists(CHEMIN):
    # rien à faire si le fichier n'existe même pas encore
    exit()

# lecture du fichier
with open(CHEMIN, "r", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    headers = list(reader.fieldnames)

# nettoyage des clés parasites
for row in rows:
    for k in list(row.keys()):
        if k is None or k == "":
            del row[k]

# on récupère tous les joueurs (tout sauf la colonne Type)
joueurs = [h for h in headers if h != "Type"]

# débloque Fille_populaire pour tout le monde
for row in rows:
    if row.get("Type") == PERSO_DEPART:
        for j in joueurs:
            row[j] = "1"

# réécriture du fichier
with open(CHEMIN, "w", newline="") as f:
    writer = csv.DictWriter(f, headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print("Fille_populaire débloquée pour :", ", ".join(joueurs))
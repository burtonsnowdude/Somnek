"""
Test map, script de debug 
Débloque la map Cour pour tous les joueurs dans le CSV.
"""

import csv, os

# chemin vers le fichier de progression des maps
CHEMIN = "Fichiers_csv/maps_debloquees.csv"

if os.path.exists(CHEMIN):
    # lecture du fichier
    with open(CHEMIN, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = list(reader.fieldnames)

    # nettoyage des clés parasites (virgules en trop dans le csv)
    for row in rows:
        for k in list(row.keys()):
            if k is None or k == "":
                del row[k]
        # on met tout le monde à 1 sur la ligne Cour
        if row.get("Type") == "Cour":
            for j in headers[1:]:
                row[j] = "1"

    # réécriture du fichier avec les modifs
    with open(CHEMIN, "w", newline="") as f:
        writer = csv.DictWriter(f, headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print("Cour débloquée pour tous les joueurs.")
else:
    print("maps_debloquees.csv n'existe pas encore il sera créé au premier lancement.")
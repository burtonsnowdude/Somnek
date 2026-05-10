import csv, os
CHEMIN = "Fichiers_csv/maps_debloquees.csv"

if os.path.exists(CHEMIN):
    with open(CHEMIN, "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = list(reader.fieldnames)
    for row in rows:
        for k in list(row.keys()):
            if k is None or k == "":
                del row[k]
        if row.get("Type") == "Cour":
            for j in headers[1:]:
                row[j] = "1"
    with open(CHEMIN, "w", newline="") as f:
        writer = csv.DictWriter(f, headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print("✅ Cour débloquée pour tous les joueurs.")
else:
    print("⚠ maps_debloquees.csv n'existe pas encore — il sera créé au premier lancement.")
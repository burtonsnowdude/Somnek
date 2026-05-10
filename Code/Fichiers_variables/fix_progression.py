"""Script one-shot : débloque Fille_populaire pour tous les joueurs déjà inscrits."""
import csv
import os

CHEMIN = "Fichiers_csv/persos_debloques.csv"
PERSO_DEPART = "Fille_populaire"

if not os.path.exists(CHEMIN):
    print(f"❌ Fichier introuvable : {CHEMIN}")
    exit()

# Lire
with open(CHEMIN, "r", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    headers = list(reader.fieldnames)

# Nettoyer les clés parasites
for row in rows:
    for k in list(row.keys()):
        if k is None or k == "":
            del row[k]

# Débloquer Fille_populaire pour TOUT LE MONDE
joueurs = [h for h in headers if h != "Type"]
for row in rows:
    if row.get("Type") == PERSO_DEPART:
        for j in joueurs:
            row[j] = "1"

# Réécrire
with open(CHEMIN, "w", newline="") as f:
    writer = csv.DictWriter(f, headers, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)

print("✅ Fille_populaire débloquée pour :", ", ".join(joueurs))
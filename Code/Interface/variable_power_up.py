"""
Variables liées aux power up :
Argent du joueur, inventaire des niveaux, prix et effets de chaque power up
"""




# niveau  de base de chaque power up pour le joueur
playerInventory = {
    "Pouvoir":          0,
    "Protection":       0,
    "quantite":         0,
    "refroidissement":  0,
    "zone":             0,
    "durabilite":       0,
    "vitesse_du_j":     0,
    "chance":           0,
    "attirance":        0,
    "sante":            0,
    "croissance":       0,
}

# liste des prix par niveau, liste des effets par niveau pour chaque power up 
liste_power_up = {
    "Pouvoir":          ([50, 100, 150, 200, 250],  [0.10, 0.10, 0.10, 0.10, 0.10]),
    "Protection":       ([50, 100, 150, 200, 250],  [0.05, 0.05, 0.05, 0.05, 0.05]),
    "quantite":         ([80, 160, 240],             [1, 1, 1]),
    "refroidissement":  ([60, 120, 180, 240],        [0.08, 0.08, 0.08, 0.08]),
    "zone":             ([70, 140, 210, 280],        [0.10, 0.10, 0.10, 0.10]),
    "durabilite":       ([60, 120, 180],             [0.15, 0.15, 0.15]),
    "vitesse_du_j":     ([50, 100, 150, 200],        [0.08, 0.08, 0.08, 0.08]),
    "chance":           ([70, 140, 210],             [0.10, 0.10, 0.10]),
    "attirance":        ([50, 100, 150],             [30, 30, 30]),
    "sante":            ([60, 120, 180, 240],        [20, 20, 20, 20]),
    "croissance":       ([70, 140, 210],             [0.10, 0.10, 0.10]),
}

# calcule le niveau max de chaque power up à partir du nombre de prix dispo
MAX_NIVEAUX = {key: len(val[0]) for key, val in liste_power_up.items()}
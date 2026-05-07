

import Interface.variable_power_up as data

def apply_powerups(player):
    """
    Applique tous les bonus au joueur
    """

    
    player.vitesse = 5
    player.projectile_cadence = 30
    player.hp_max = 100

    
    level = data.playerInventory.get("Pouvoir", 0)

    
    if level >= 1:
        player.vitesse *= 1.2   # +20% vitesse

    if level >= 2:
        player.projectile_cadence -= 5  # tire plus vite

    if level >= 3:
        player.hp_max += 50  # + vie

    # clamp sécurité
    if player.projectile_cadence < 5:
        player.projectile_cadence = 5
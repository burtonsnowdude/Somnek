# Jeu/player_actif.py
# Référence globale au joueur actif (None si on est dans le menu)

_player_actif = None

def set_player_actif(player):
    global _player_actif
    _player_actif = player

def get_player_actif():
    return _player_actif
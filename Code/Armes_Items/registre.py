

"""
registre.py — SOMNEK
Source unique de vérité pour la classification arme / item.
Toujours importer depuis ici plutôt que de dupliquer la logique.
"""
 
from Fichiers_variables.dictionnaire_armes import TYPES_ARMES
from Fichiers_variables.dictionnaire_items import ITEMS_PAR_PERSO
 
 
def est_arme(nom: str, perso: str) -> bool:
    """Retourne True si `nom` est une arme connue pour ce personnage."""
    return nom in TYPES_ARMES.get(perso, {})
 
 
def est_item(nom: str, perso: str) -> bool:
    """Retourne True si `nom` est un item connu pour ce personnage."""
    return nom in ITEMS_PAR_PERSO.get(perso, {})
 
 
def type_objet(nom: str, perso: str) -> str:
    """
    Retourne "arme", "item", ou "inconnu".
    Utilisé partout où l'on doit distinguer les deux.
    """
    if est_arme(nom, perso):
        return "arme"
    if est_item(nom, perso):
        return "item"
    return "inconnu"
 
 
def verifier_objet(nom: str, perso: str) -> None:
    """
    Lève une ValueError claire si l'objet est introuvable.
    Pratique pour le débogage.
    """
    t = type_objet(nom, perso)
    if t == "inconnu":
        armes = list(TYPES_ARMES.get(perso, {}).keys())
        items = list(ITEMS_PAR_PERSO.get(perso, {}).keys())
        raise ValueError(
            f"[Registre] '{nom}' introuvable pour '{perso}'.\n"
            f"  Armes connues : {armes}\n"
            f"  Items connus  : {items}"
        )
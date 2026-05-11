"""
Gestion du nom du joueur :
Saisie du nom à l'écran et inscription dans tous les fichiers CSV
"""
import pygame as pyg
import pygame_gui
import sys
from Fichiers_variables.variables import WIN, WIDTH, HEIGHT


def get_user_name(fond_intro):
    """Crée un champ  pour récupérer le nom du joueur
    
    Parameters
    ----------
    fond_intro : pygame.Surface
        Image de fond affichée pendant la saisie
    
    Returns
    -------
    str
        Le nom saisi par le joueur
    """
    # Création du manager d'interface et du champ de saisie
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    text_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pyg.Rect((WIDTH // 2 - 150, HEIGHT // 2 + 30), (300, 50)),
        manager=manager,
        object_id='#main_text_entry'
    )
    font = pyg.font.SysFont("bahnschrift", 30)
    clock = pyg.time.Clock()

    while True:
        dt = clock.tick(60) / 1000
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            # Quand le joueur valide son nom avec entrée
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                nom = event.text.strip()
                if nom:
                    _enregistrer_joueur(nom)   # inscrit le joueur dans les CSV
                return nom

            manager.process_events(event)

        # affichage du fond et du texte d'invite
        manager.update(dt)
        WIN.blit(fond_intro, (0, 0))
        texte = font.render("Entre ton nom :", True, (255, 255, 255))
        WIN.blit(texte, texte.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))
        manager.draw_ui(WIN)
        pyg.display.flip()


def _enregistrer_joueur(nom):
    """Inscrit le joueur dans TOUS les CSV avec Fille_populaire débloqué
    
    Parameters
    ----------
    nom : str
        Le nom du joueur à inscrire
    """
    from Fichiers_variables.gestion_fichiers import (
        det_noms, contenu_fichier_armes, contenu_fichier_quetes,
        contenu_fichier_powerups, reecrire_fichier
    )
    from Fichiers_variables.progression import init_progression

    
    try:
        noms, niveau_tab = det_noms()
    except Exception as e:
        print(f"[Inscription] Erreur lecture niveau_argent : {e}")
        return

    #vérifie la progression des persos
    if nom in noms:
        print(f"[Inscription] '{nom}' déjà présent, vérification progression…")
        try:
            init_progression(nom)
        except Exception as e:
            print(f"[Inscription] init_progression KO : {e}")
        return

    # ajout du nouveau joueur
    noms.append(nom)
    for ligne in niveau_tab:
        ligne[nom] = 0

    # Ajout dans le fichier des armes
    new_armes = contenu_fichier_armes()
    for ligne in new_armes:
        ligne[nom] = 0

    # ajout dans le fichier des quêtes
    new_quetes = contenu_fichier_quetes()
    for ligne in new_quetes:
        ligne[nom] = 0

    # ajout dans le fichier des power ups
    new_powerups = contenu_fichier_powerups()
    for ligne in new_powerups:
        ligne[nom] = 0

    # écrit sur  tous les fichiers
    reecrire_fichier("niveau_argent",              niveau_tab,    noms)
    reecrire_fichier("armes_obtenues_par_joueur",  new_armes,     noms)
    reecrire_fichier("quetes_reussis",             new_quetes,    noms)
    reecrire_fichier("powerups",                   new_powerups,  noms)

    # Débloque Fille_populaire dans persos_debloques.csv
    try:
        init_progression(nom)
    except Exception as e:
        print(f"[Inscription] init_progression KO : {e}")

"""
Animation d'item — SOMNEK
Quand un item est choisi :
  1. L'image tombe du ciel vers le joueur avec une traînée colorée
  2. Impact visuel (rebond)
  3. Teinte colorée sur le joueur pendant 3s (2s fixes + 1s de fondu)
  4. L'item est enregistré dans la collection au lancement
"""

import pygame
import time
import math



COULEUR_ITEM = {
    # Nerd
    "Lunettes_cassees":      (180, 220, 255),
    "Souris_pc":             (200, 200, 200),
    "Chaussettes_propres":   (255, 255, 255),
    "Cahier_NSI":            (30,  100, 200),
    "Vody_Lemonade":         (255, 220,  50),
    "Apple_Watch":           (80,   80,  80),
    "Deodorant":             (150, 230, 255),
    "Pomme_scientifique":    (80,  160,  80),
    "Serviette_nettoyante":  (240, 240, 240),
    "Cle_USB":               (30,   30, 180),
    "Pistolets":             (80,   80,  80),
    "Epee_enflammee":        (255, 120,   0),
    "Epee_de_guts":          (180,   0,   0),
    "Armure_chevalier":      (160, 160, 160),
    "Pantalon_beige":        (210, 180, 140),
    "Petit_nain_roux":       (200,  60,  20),
    "Mousse_vanille":        (245, 222, 179),
    # Fille populaire
    "Chew_gum":              (255, 180, 200),
    "Talons_noirs":          (20,   20,  20),
    "Carte_bleue":           (0,   120, 215),
    "Parfum_Dioru":          (255, 215,   0),
    "Pilule_verte":          (50,  200,  80),
    "Crop_top_rose":         (255, 100, 150),
    "Coque_trefle":          (34,  139,  34),
    "Sac_main_violet":       (148,   0, 211),
    "Chargeur":              (100, 100, 100),
    "Ambroisie":             (255, 240, 100),
    "Iphone_2000":           (200, 200, 200),
    "Minuteur":              (255, 140,   0),
    "Ensemble_juicy":        (255,  80, 130),
    "Manteau_leopard":       (200, 150,  50),
    # Nonne
    "Eau_benite":            (180, 220, 255),
    "Chapelet":              (139,  90,  43),
    "Mocassin":              (160, 120,  80),
    "Bourse":                (210, 180, 140),
    "Bougie":                (255, 200,  50),
    "Huile_benediction":     (220, 180,  80),
    "Ostie":                 (255, 255, 240),
    "Sac_a_dos_bleu":        (50,  100, 200),
    "Nokia":                 (0,   100, 200),
    "Voile":                 (240, 240, 255),
    "Tableau_sacre":         (180, 130,  80),
    "Boule_energie":         (120,   0, 255),
    "Coeur":                 (255,  50,  80),
    "Cape":                  (60,   60, 100),
    "Collant":               (50,   50,  50),
    "Halo":                  (255, 255, 150),
}

COULEUR_DEFAUT = (200, 200, 255)




class AnimationItemTombe:
    """
    3 phases :
      "chute"  → item tombe du ciel avec traînée
      "impact" → rebond visuel à l'arrivée sur le joueur
      "flash"  → teinte colorée sur le joueur (2s fixe + 1s fondu)
      "fini"   → terminé, peut être supprimé
    """

    VITESSE_CHUTE   = 8       # px/frame
    TAILLE_ITEM     = (40, 40)
    FLASH_DUREE     = 3.0     # secondes totales de teinte
    FLASH_INTENSITE = 130     # opacité max
    FONDU_DEBUT     = 2.0     # à partir de quand le fondu commence

    def __init__(self, nom_item: str, image_surface: pygame.Surface, joueur):
        self.nom_item = nom_item
        self.image    = pygame.transform.scale(image_surface, self.TAILLE_ITEM)
        self.joueur   = joueur
        self.couleur  = COULEUR_ITEM.get(nom_item, COULEUR_DEFAUT)

        self.x = float(joueur.pos.centerx - self.TAILLE_ITEM[0] // 2)
        self.y = float(-self.TAILLE_ITEM[1])
        self.cible_y = float(joueur.pos.top)

        self._phase        = "chute"
        self._flash_debut  = 0.0
        self._impact_scale = 1.0

    def en_cours(self) -> bool:
        return self._phase != "fini"

    def update(self):
        if self._phase == "chute":
            self.y += self.VITESSE_CHUTE
            if self.y >= self.cible_y:
                self.y = self.cible_y
                self._phase       = "impact"
                self._impact_scale = 1.4
                self._flash_debut  = time.time()

        elif self._phase == "impact":
            self._impact_scale = max(1.0, self._impact_scale - 0.06)
            if self._impact_scale <= 1.0:
                self._phase = "flash"

        elif self._phase == "flash":
            if time.time() - self._flash_debut >= self.FLASH_DUREE:
                self._phase = "fini"

    def draw(self, surface: pygame.Surface):
        if self._phase in ("chute", "impact"):
            self._draw_trainee(surface)
            taille = (
                int(self.TAILLE_ITEM[0] * self._impact_scale),
                int(self.TAILLE_ITEM[1] * self._impact_scale),
            )
            img  = pygame.transform.scale(self.image, taille)
            rect = img.get_rect(
                centerx=int(self.x + self.TAILLE_ITEM[0] // 2),
                top=int(self.y)
            )
            surface.blit(img, rect)

        elif self._phase == "flash":
            elapsed = time.time() - self._flash_debut
            if elapsed < self.FONDU_DEBUT:
                intensite = self.FLASH_INTENSITE
            else:
                ratio     = (elapsed - self.FONDU_DEBUT) / (self.FLASH_DUREE - self.FONDU_DEBUT)
                intensite = int(self.FLASH_INTENSITE * (1.0 - ratio))
            intensite = max(0, intensite)
            if intensite > 0:
                # Overlay coloré directement sur le rect du joueur — pas de
                # modification de surface, compatible images et animations
                overlay = pygame.Surface(
                    (self.joueur.pos.width, self.joueur.pos.height),
                    pygame.SRCALPHA
                )
                overlay.fill((*self.couleur, intensite))
                surface.blit(overlay, self.joueur.pos.topleft)

    # ── Privé ─────────────────────────────────────────────────────────────

    def _draw_trainee(self, surface: pygame.Surface):
        cx = int(self.x + self.TAILLE_ITEM[0] // 2)
        for i in range(1, 9):
            alpha = int(150 * (1 - i / 9))
            rayon = max(2, int(9 * (1 - i / 9)))
            vy    = int(self.y - i * self.VITESSE_CHUTE * 1.6)
            tmp   = pygame.Surface((rayon * 2, rayon * 2), pygame.SRCALPHA)
            pygame.draw.circle(tmp, (*self.couleur, alpha), (rayon, rayon), rayon)
            surface.blit(tmp, (cx - rayon, vy - rayon))



"""
def enregistrer_item_collection(joueur_nom: str, nom_item: str):"""
""" Ajoute immédiatement l'item dans le CSV collection du joueur."""
"""   try:
        ajouter_arme(joueur_nom, nom_item)
    except Exception as e:
        print(f"[Collection] Erreur ajout '{nom_item}' : {e}")"""


def lancer_animation_item(nom_item: str, joueur, joueur_nom: str,
                           image_small: pygame.Surface) -> AnimationItemTombe:
    """
    Enregistre l'item dans la collection ET retourne l'objet animation.

    Dans jeu.py :
        anim_item = lancer_animation_item(
            objet[1], p, nom,
            TYPES_ITEMS[p.perso][objet[1]]["image"]
        )
    """
    #enregistrer_item_collection(joueur_nom, nom_item)
    return AnimationItemTombe(nom_item, image_small, joueur)
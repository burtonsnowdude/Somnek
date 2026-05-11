"""
Class Button :
Bouton cliquable avec image optionnelle et effet de survol
"""
import pygame as pyg

class Button:
    """Class Button"""
    def __init__(self, text, action, x, y, width, height, font, image=None):
        """Initialise un bouton avec son texte, sa position, sa taille et éventuellement une image
        
        Parameters
        ----------
        text : str
            Le texte affiché sur le bouton
        action : str
            L'action déclenchée par le bouton
        x, y : int
            Coordonnées du centre du bouton
        width, height : int
            Dimensions du bouton
        font : pygame.font.Font
            La police utilisée pour le texte
        image : pygame.Surface, optional
            Image à afficher à la place du fond coloré
        """
        self.text = text
        self.action = action
        self.rect = pyg.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.font = font  
        self.color1 = (0, 0, 200)       # couleur au survol
        self.color2 = (0, 0, 255, 128)  # couleur de base (semi-transparente)
        self.rect_center = self.rect.center
        
        # Si une image est fournie, on la redimensionne en gardant le ratio
        if image is not None:
            img_w, img_h = image.get_size()
            ratio = min(width / img_w, height / img_h)  # ratio pour rentrer dans la taille demandée
            new_size = (int(img_w * ratio), int(img_h * ratio))
            self.image = pyg.transform.smoothscale(image, new_size)
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.image = None

    def draw(self, win, mouse_pos):
        """Dessine le bouton avec un effet de survol
        
        Parameters
        ----------
        win : pygame.Surface
            La fenêtre sur laquelle dessiner
        mouse_pos : tuple(int, int)
            Position de la souris
        """
        if self.image:
            # Légère transparence au survol
            alpha = 180 if self.rect.collidepoint(mouse_pos) else 255
            img = self.image.copy()
            img.set_alpha(alpha)
            win.blit(img, self.rect)
        else:
            # Couleur différente si survolé
            color = self.color1 if self.rect.collidepoint(mouse_pos) else self.color2
            surface = pyg.Surface(self.rect.size, pyg.SRCALPHA)
            pyg.draw.rect(surface, color, surface.get_rect(), border_radius=10)
            win.blit(surface, self.rect)
            text = self.font.render(self.text, True, (255, 255, 255))
            win.blit(text, text.get_rect(center=self.rect_center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        """Vérifie si le bouton a été cliqué
        
        Parameters
        ----------
        mouse_pos : tuple(int, int)
            Position de la souris
        mouse_pressed : tuple
            État des boutons de la souris (clic gauche, milieu, droit)
        
        Returns
        -------
        bool
            True si le bouton est cliqué, False sinon
        """
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            return True
        return False
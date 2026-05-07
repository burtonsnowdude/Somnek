import pygame as pyg

class Button:
    def __init__(self, text, action, x, y, width, height, font, image=None):
        self.text = text
        self.action = action
        self.rect = pyg.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.font = font  
        self.color1 = (0, 0, 200)
        self.color2 = (0, 0, 255, 128)
        self.rect_center = self.rect.center
        
       
        if image is not None:
            img_w, img_h = image.get_size()
            ratio = min(width / img_w, height / img_h)

            new_size = (int(img_w * ratio), int(img_h * ratio))
            self.image = pyg.transform.smoothscale(image, new_size)
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.image = None

    def draw(self, win, mouse_pos):
        if self.image:
            # Légère transparence au survol
            alpha = 180 if self.rect.collidepoint(mouse_pos) else 255
            img = self.image.copy()
            img.set_alpha(alpha)
            win.blit(img, self.rect)
        else:
            color = self.color1 if self.rect.collidepoint(mouse_pos) else self.color2
            surface = pyg.Surface(self.rect.size, pyg.SRCALPHA)
            pyg.draw.rect(surface, color, surface.get_rect(), border_radius=10)
            win.blit(surface, self.rect)
            text = self.font.render(self.text, True, (255, 255, 255))
            win.blit(text, text.get_rect(center=self.rect_center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            return True
        return False
import pygame as pyg

class Button:
    def __init__(self, text, action, x, y, width, height, font):
        self.text = text
        self.action = action
        self.rect = pyg.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.font = font  
        self.color1 = (0, 0, 200)
        self.color2 = (0, 0, 255, 128)
    def draw(self, win, mouse_pos):
        color = self.color1 if self.rect.collidepoint(mouse_pos) else self.color2

        surface = pyg.Surface(self.rect.size, pyg.SRCALPHA)
        pyg.draw.rect(surface, color, surface.get_rect(), border_radius=10)
        win.blit(surface, self.rect)

        text = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]
import pygame
from DrawableObject import DrawableObject

class DrawableFontObject(DrawableObject, pygame.sprite.Sprite):

    def __init__(self,text,font, x = 0, y = 0):

        self.font = font
        self.textImage = font.render(text, 1, (255,255,255))
        self.text = text
        DrawableObject.__init__(self, [self.textImage], '')

    def changeText(self, newText, color=(0,0,0)):
        self.text = newText
        self._images[0] = self.font.render(str(newText), True, color)
        self.image = self._images[0]
    
    def getText(self):
        return str(self.text)

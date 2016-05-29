import pygame

class Character:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):
        pygame.draw.line(self.canvas.screen, (0, 0, 0), (0, self.canvas.height / 2), (self.canvas.width, self.canvas.height / 2), 2)


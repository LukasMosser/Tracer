import pygame

class Character:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):
        pygame.draw.circle(self.canvas.screen, (255, 255, 0), (100, 300), 10, 2)


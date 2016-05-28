import pygame

class Screen:
    width = 800
    height = 600

    dims = (width, height)
    v_center = height / 2
    
    def __init__(self):
	self.screen = pygame.display.set_mode(self.dims)

    def clear(self):
        self.screen.fill((255, 255, 255))


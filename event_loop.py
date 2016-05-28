import pygame
import character

class EventLoop:
    def __init__(self, screen):
        self.character = character.Character(screen)

    def start(self):
        while True:
            self.run()

    def run(self):
	self.character.draw()
        pygame.display.flip()
            

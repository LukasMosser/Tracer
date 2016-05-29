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


class ScoreDisplay(object):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 36)

    def draw_score(self, score, position):
        label = self.font.render("Score: "+str(score), 1, (0, 0, 0))
        self.screen.screen.blit(label, position)


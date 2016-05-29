import pygame
from random import choice

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

    def draw_score(self, text, score, position):
        label = self.font.render(text+" "+str(score), 1, (0, 0, 0))
        self.screen.screen.blit(label, position)


class MessageDisplay(object):
    def __init__(self, text, screen, timeout, color=(0, 0, 0)):
        self.color = color
        self.timeout = timeout
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 36)
        self.label = self.font.render(text, 1, color)
        self.position = None

    def draw_message(self):
        self.screen.screen.blit(self.label, self.position)


class RandomMessageDisplay(object):
    def __init__(self, text, screen, timeout, color=(0, 0, 0)):
        self.color = color
        self.timeout = timeout
        self.screen = screen
        self.font = pygame.font.SysFont("monospace", 36)
        self.text = choice(text)
        self.label = self.font.render(self.text, 1, color)
        print self.text
        if self.text in ["Awesome!", "AMAZING", "WOW", "Much Seismic", "So Geologist"]:
            self.doge = pygame.image.load("doge.bmp")
            self.doge_rect = self.doge.get_rect()
        elif self.text in ["Hype!, WOAHHHH!", "ON FIAAA", "BLAZING", "GODLIKE"]:
            self.doge = pygame.image.load("snoop.jpg")
            self.doge_rect = self.doge.get_rect()
        self.position = None

    def draw_message(self):
        self.screen.screen.blit(self.label, self.position)
        if self.text in ["WOW", "BLAZING", "Much Seismic", "So Geologist"]:
            print "did it"
            self.doge_rect.centerx = self.position[0]+500
            self.doge_rect.centery = self.position[1]-50
            self.screen.screen.blit(self.doge, self.doge_rect)
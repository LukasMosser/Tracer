import pygame
import character, trace

class EventLoop:
    def __init__(self, screen):
	self.screen = screen
        self.character = character.Character(screen)
	self.reference_trace = trace.Trace()
	self.trace_position = 0 # vertical position relative to center

    def start(self):
        while True:
            self.run()

    def run(self):
	self.screen.screen.fill((255, 255, 255))
	trace_position = (self.screen.v_center + self.trace_position) % self.screen.height
	self.reference_trace.draw_line(self.screen.screen, self.screen.width, trace_position)
	self.character.draw()
        pygame.display.flip()
        self.trace_position += 1
            

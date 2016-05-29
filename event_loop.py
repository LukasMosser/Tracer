import pygame
import character, trace

class EventLoop:
    def __init__(self, screen):
        self.step = 0
        peak_num = 1
        self.screen = screen

        self.character = character.Character(screen)

        self.reference_trace = trace.Trace(peak_num, self.screen)
        self.comparison_trace = trace.Trace(peak_num, self.screen)

        self.trace_position = 0 # vertical position relative to center

        self.clock = pygame.time.Clock()

        self.done = False

        self.step = 1 # the number of pixels to move the comparison trace per iteration

    def start(self):
        while not self.done:
            self.run()

        pygame.quit()

    def run(self):
        self.clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.step = -self.step

        self.screen.clear()

        self.reference_trace.draw(0, y_offset=0, x_offset=100, color=(255, 0, 255))
        self.comparison_trace.draw(self.trace_position, y_offset=self.trace_position, x_offset=500-self.trace_position)
        self.character.draw()
        pygame.display.flip()
        self.trace_position += self.step


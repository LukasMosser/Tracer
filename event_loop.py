import pygame
import character, trace
from screen import ScoreDisplay

class EventLoop:
    def __init__(self, screen):
        self.step = 0
        peak_num = 1
        self.screen = screen

        self.character = character.Character(screen)

        self.reference_trace = trace.Trace([400], self.screen)
        self.comparison_trace = trace.Trace([400], self.screen)

        self.score_disp = ScoreDisplay(self.screen)
        self.total_score_disp = ScoreDisplay(self.screen)
        self.normalized_score_disp = ScoreDisplay(self.screen)
        self.total_score = 0
        self.record_score = True
        self.normalized_score = 0.
        self.number_of_traces = 0

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
        score = abs(self.reference_trace.peaks[0]-(self.comparison_trace.peaks[0]-self.trace_position))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.step = -self.step
                if self.record_score:
                    self.number_of_traces += 1
                    self.total_score += score
                    self.normalized_score = self.total_score/float(self.number_of_traces)
                    self.record_score = False
                else:
                    self.record_score = True

        self.screen.clear()
        self.comparison_trace.draw(0, x_offset=100, y_offset=0)
        self.reference_trace.draw(self.trace_position, y_offset=self.trace_position, x_offset=500-self.trace_position)
        self.score_disp.draw_score("Current Score", score, (100, 0))
        self.total_score_disp.draw_score("Total Score", self.total_score, (100, 50))
        self.normalized_score_disp.draw_score("Normed Score", self.normalized_score, (100, 100))
        self.character.draw()
        pygame.display.flip()
        self.trace_position += self.step

